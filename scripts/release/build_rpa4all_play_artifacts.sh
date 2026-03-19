#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_DIR="${ROOT_DIR}/release-play"
UNSIGNED_AAB="${ROOT_DIR}/app/build/outputs/bundle/rpa4allRelease/app-rpa4all-release.aab"
SIGNED_AAB="${OUT_DIR}/app-rpa4all-release-signed.aab"

mkdir -p "${OUT_DIR}"

echo "[1/4] Building rpa4all release AAB"
(
  cd "${ROOT_DIR}"
  ./gradlew :app:bundleRpa4allRelease --no-daemon --console=plain -x lintVitalRpa4allRelease
)

if [[ ! -f "${UNSIGNED_AAB}" ]]; then
  echo "Build did not produce AAB: ${UNSIGNED_AAB}" >&2
  exit 1
fi

echo "[2/4] Copying unsigned AAB to release-play/"
cp -f "${UNSIGNED_AAB}" "${OUT_DIR}/app-rpa4all-release-unsigned.aab"

echo "[3/4] Optional signing with jarsigner (requires env vars)"
if [[ -n "${RPA4ALL_KEYSTORE_FILE:-}" && -n "${RPA4ALL_KEYSTORE_PASSWORD:-}" && -n "${RPA4ALL_KEY_ALIAS:-}" && -n "${RPA4ALL_KEY_PASSWORD:-}" ]]; then
  cp -f "${UNSIGNED_AAB}" "${SIGNED_AAB}"
  jarsigner \
    -keystore "${RPA4ALL_KEYSTORE_FILE}" \
    -storepass "${RPA4ALL_KEYSTORE_PASSWORD}" \
    -keypass "${RPA4ALL_KEY_PASSWORD}" \
    "${SIGNED_AAB}" \
    "${RPA4ALL_KEY_ALIAS}"
  jarsigner -verify "${SIGNED_AAB}"
  echo "Signed AAB: ${SIGNED_AAB}"
else
  echo "Signing skipped. Set env vars to sign:"
  echo "  RPA4ALL_KEYSTORE_FILE"
  echo "  RPA4ALL_KEYSTORE_PASSWORD"
  echo "  RPA4ALL_KEY_ALIAS"
  echo "  RPA4ALL_KEY_PASSWORD"
fi

echo "[4/4] SHA256"
sha256sum "${OUT_DIR}"/*.aab
echo "Done. Artifacts in: ${OUT_DIR}"
