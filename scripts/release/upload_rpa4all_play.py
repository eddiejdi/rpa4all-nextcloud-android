#!/usr/bin/env python3
"""
Upload an AAB and/or Play Store listing assets for com.rpa4all.nextcloud.

Prerequisites:
  pip install google-api-python-client google-auth
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import pathlib
import socket
import sys
import time
from typing import Iterable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-account-json", required=True)
    parser.add_argument("--aab")
    parser.add_argument("--metadata-dir")
    parser.add_argument("--package-name", default="com.rpa4all.nextcloud")
    parser.add_argument("--track", default="internal", choices=["internal", "alpha", "beta", "production"])
    parser.add_argument("--release-name", default=None)
    parser.add_argument("--status", default="completed", choices=["completed", "draft", "halted", "inProgress"])
    parser.add_argument("--skip-details", action="store_true")
    parser.add_argument("--skip-listings", action="store_true")
    parser.add_argument("--skip-images", action="store_true")
    return parser.parse_args()


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def load_metadata_config(metadata_dir: pathlib.Path) -> dict:
    config_path = metadata_dir / "config.json"
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def iter_locales(metadata_dir: pathlib.Path) -> Iterable[pathlib.Path]:
    for child in sorted(metadata_dir.iterdir()):
        if child.is_dir():
            yield child


def update_details(edits, package_name: str, edit_id: str, config: dict) -> None:
    details = {}
    for field in ("defaultLanguage", "contactEmail", "contactPhone", "contactWebsite"):
        value = config.get(field)
        if value:
            details[field] = value

    if not details:
        return

    edits.details().update(
        packageName=package_name,
        editId=edit_id,
        body=details,
    ).execute()
    print(f"Updated store details: {sorted(details.keys())}")


def update_listings(edits, package_name: str, edit_id: str, metadata_dir: pathlib.Path) -> None:
    for locale_dir in iter_locales(metadata_dir):
        body = {}
        for filename, field in (
            ("title.txt", "title"),
            ("short_description.txt", "shortDescription"),
            ("full_description.txt", "fullDescription"),
        ):
            file_path = locale_dir / filename
            if file_path.exists():
                body[field] = read_text(file_path)

        if not body:
            continue

        body["language"] = locale_dir.name
        edits.listings().update(
            packageName=package_name,
            editId=edit_id,
            language=locale_dir.name,
            body=body,
        ).execute()
        print(f"Updated listing for {locale_dir.name}")


def iter_image_files(images_root: pathlib.Path, image_type: str) -> list[pathlib.Path]:
    if image_type in {"icon", "featureGraphic", "tvBanner"}:
        file_path = images_root / f"{image_type}.png"
        return [file_path] if file_path.exists() else []

    type_dir = images_root / image_type
    if not type_dir.exists():
        return []

    return sorted(
        path for path in type_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )


def upload_images(edits, media_cls, package_name: str, edit_id: str, metadata_dir: pathlib.Path) -> None:
    image_types = (
        "icon",
        "featureGraphic",
        "phoneScreenshots",
        "sevenInchScreenshots",
        "tenInchScreenshots",
        "tvBanner",
    )

    for locale_dir in iter_locales(metadata_dir):
        images_root = locale_dir / "images"
        if not images_root.exists():
            continue

        for image_type in image_types:
            image_files = iter_image_files(images_root, image_type)
            if not image_files:
                continue

            edits.images().deleteall(
                packageName=package_name,
                editId=edit_id,
                language=locale_dir.name,
                imageType=image_type,
            ).execute()

            for image_file in image_files:
                mime_type = mimetypes.guess_type(image_file.name)[0] or "image/png"
                edits.images().upload(
                    packageName=package_name,
                    editId=edit_id,
                    language=locale_dir.name,
                    imageType=image_type,
                    media_body=media_cls(str(image_file), mimetype=mime_type, resumable=False),
                ).execute()

            print(f"Uploaded {len(image_files)} {image_type} asset(s) for {locale_dir.name}")


def upload_bundle(edits, media_cls, package_name: str, edit_id: str, aab_path: pathlib.Path) -> int:
    media = media_cls(
        str(aab_path),
        mimetype="application/octet-stream",
        resumable=True,
        chunksize=8 * 1024 * 1024,
    )
    upload_request = edits.bundles().upload(
        packageName=package_name,
        editId=edit_id,
        media_body=media,
    )
    bundle_result = None
    max_attempts = 8
    attempt = 0
    while bundle_result is None:
        try:
            status, bundle_result = upload_request.next_chunk(num_retries=5)
            if status is not None:
                progress = int(status.progress() * 100)
                print(f"Upload progress: {progress}%")
        except TimeoutError:
            attempt += 1
            if attempt >= max_attempts:
                raise
            print(f"Upload timeout, retrying ({attempt}/{max_attempts})...")
            time.sleep(2)

    return int(bundle_result["versionCode"])


def main() -> int:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("Missing dependency. Install with: pip install google-api-python-client google-auth", file=sys.stderr)
        return 2

    args = parse_args()

    aab_path = pathlib.Path(args.aab).expanduser() if args.aab else None
    metadata_dir = pathlib.Path(args.metadata_dir).expanduser() if args.metadata_dir else None

    if aab_path is None and metadata_dir is None:
        print("Nothing to do. Provide --aab and/or --metadata-dir.", file=sys.stderr)
        return 2
    if aab_path is not None and not aab_path.exists():
        print(f"AAB not found: {aab_path}", file=sys.stderr)
        return 2
    if metadata_dir is not None and not metadata_dir.exists():
        print(f"Metadata directory not found: {metadata_dir}", file=sys.stderr)
        return 2

    scopes = ["https://www.googleapis.com/auth/androidpublisher"]
    credentials = service_account.Credentials.from_service_account_file(
        args.service_account_json,
        scopes=scopes,
    )
    # Set global socket timeout to avoid hanging on flaky connections.
    socket.setdefaulttimeout(120)
    service = build("androidpublisher", "v3", credentials=credentials, cache_discovery=False)

    edits = service.edits()
    insert_request = edits.insert(body={}, packageName=args.package_name)
    insert_result = insert_request.execute()
    edit_id = insert_result["id"]

    if metadata_dir is not None:
        config = load_metadata_config(metadata_dir)
        if not args.skip_details:
            update_details(edits, args.package_name, edit_id, config)
        if not args.skip_listings:
            update_listings(edits, args.package_name, edit_id, metadata_dir)
        if not args.skip_images:
            upload_images(edits, MediaFileUpload, args.package_name, edit_id, metadata_dir)

    version_code = None
    if aab_path is not None:
        version_code = upload_bundle(edits, MediaFileUpload, args.package_name, edit_id, aab_path)
        release = {
            "name": args.release_name or f"Nextcloud -by RPA4All ({version_code})",
            "status": args.status,
            "versionCodes": [str(version_code)],
        }
        edits.tracks().update(
            packageName=args.package_name,
            editId=edit_id,
            track=args.track,
            body={"releases": [release]},
        ).execute()

    commit_result = edits.commit(packageName=args.package_name, editId=edit_id).execute()
    if version_code is None:
        print(f"Listing update complete. package={args.package_name}")
    else:
        print(f"Upload complete. package={args.package_name} track={args.track} versionCode={version_code}")
    print(commit_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
