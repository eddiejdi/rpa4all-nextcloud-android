#!/usr/bin/env python3
"""
Upload signed AAB to Google Play for com.rpa4all.nextcloud.

Prerequisites:
  pip install google-api-python-client google-auth
"""

from __future__ import annotations

import argparse
import pathlib
import socket
import sys
import time


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--service-account-json", required=True)
    parser.add_argument("--aab", required=True)
    parser.add_argument("--package-name", default="com.rpa4all.nextcloud")
    parser.add_argument("--track", default="internal", choices=["internal", "alpha", "beta", "production"])
    parser.add_argument("--release-name", default=None)
    parser.add_argument("--status", default="completed", choices=["completed", "draft", "halted", "inProgress"])
    return parser.parse_args()


def main() -> int:
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print("Missing dependency. Install with: pip install google-api-python-client google-auth", file=sys.stderr)
        return 2

    args = parse_args()

    aab_path = pathlib.Path(args.aab)
    if not aab_path.exists():
        print(f"AAB not found: {aab_path}", file=sys.stderr)
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

    media = MediaFileUpload(
        str(aab_path),
        mimetype="application/octet-stream",
        resumable=True,
        chunksize=8 * 1024 * 1024,
    )
    upload_request = edits.bundles().upload(
        packageName=args.package_name,
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
    version_code = bundle_result["versionCode"]

    release = {
        "name": args.release_name or f"NextCloud by RPA4All ({version_code})",
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
    print(f"Upload complete. package={args.package_name} track={args.track} versionCode={version_code}")
    print(commit_result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
