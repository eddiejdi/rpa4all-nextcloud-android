#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
METADATA_DIR="${ROOT_DIR}/src/rpa4all/fastlane/metadata"
SOURCE_IMAGES_DIR="${ROOT_DIR}/src/generic/fastlane/metadata/en-US/images"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

write_svg() {
  local path="$1"
  local locale="$2"
  local kind="$3"

  if [[ "${kind}" == "icon" ]]; then
    cat >"${path}" <<'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bg" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0A1830"/>
      <stop offset="100%" stop-color="#0B6EA8"/>
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="20%" r="70%">
      <stop offset="0%" stop-color="#14B8A6" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#14B8A6" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="512" height="512" rx="108" fill="url(#bg)"/>
  <rect width="512" height="512" rx="108" fill="url(#glow)"/>
  <circle cx="256" cy="196" r="108" fill="#EAF6FF"/>
  <path fill="#0B6EA8" d="M188 240h136c24 0 44 20 44 44s-20 44-44 44h-22c-10 30-37 52-70 56-41 5-79-18-95-56h-5c-24 0-44-20-44-44s20-44 44-44z"/>
  <circle cx="144" cy="416" r="56" fill="#14B8A6" fill-opacity="0.22"/>
  <circle cx="410" cy="112" r="42" fill="#EAF6FF" fill-opacity="0.12"/>
</svg>
EOF
    return
  fi

  if [[ "${locale}" == "pt-BR" ]]; then
    local title_line1="Nextcloud"
    local title_line2="-by RPA4All"
    local subtitle="Arquivos corporativos seguros no Android"
    local pill1="Sync seguro"
    local pill2="Offline"
    local pill3="Auto upload"
  else
    local title_line1="Nextcloud"
    local title_line2="-by RPA4All"
    local subtitle="Secure corporate files on Android"
    local pill1="Secure sync"
    local pill2="Offline"
    local pill3="Auto upload"
  fi

  cat >"${path}" <<EOF
<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="500" viewBox="0 0 1024 500">
  <defs>
    <linearGradient id="bg" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0A1830"/>
      <stop offset="100%" stop-color="#0B6EA8"/>
    </linearGradient>
    <linearGradient id="card" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F8FCFF"/>
      <stop offset="100%" stop-color="#DDEFFC"/>
    </linearGradient>
  </defs>
  <rect width="1024" height="500" rx="36" fill="url(#bg)"/>
  <circle cx="140" cy="88" r="120" fill="#14B8A6" fill-opacity="0.16"/>
  <circle cx="910" cy="430" r="160" fill="#EAF6FF" fill-opacity="0.08"/>
  <circle cx="800" cy="112" r="84" fill="#14B8A6" fill-opacity="0.18"/>
  <text x="88" y="148" fill="#FFFFFF" font-size="64" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700">${title_line1}</text>
  <text x="88" y="206" fill="#FFFFFF" font-size="56" font-family="DejaVu Sans, Arial, sans-serif" font-weight="700">${title_line2}</text>
  <text x="88" y="252" fill="#D9EEFF" font-size="28" font-family="DejaVu Sans, Arial, sans-serif">${subtitle}</text>

  <rect x="88" y="290" rx="18" ry="18" width="170" height="52" fill="#FFFFFF" fill-opacity="0.14"/>
  <rect x="276" y="290" rx="18" ry="18" width="128" height="52" fill="#FFFFFF" fill-opacity="0.14"/>
  <rect x="422" y="290" rx="18" ry="18" width="166" height="52" fill="#FFFFFF" fill-opacity="0.14"/>
  <text x="112" y="324" fill="#FFFFFF" font-size="24" font-family="DejaVu Sans, Arial, sans-serif">${pill1}</text>
  <text x="310" y="324" fill="#FFFFFF" font-size="24" font-family="DejaVu Sans, Arial, sans-serif">${pill2}</text>
  <text x="454" y="324" fill="#FFFFFF" font-size="24" font-family="DejaVu Sans, Arial, sans-serif">${pill3}</text>

  <g transform="translate(730 72)">
    <rect width="214" height="356" rx="34" fill="#061423" fill-opacity="0.58"/>
    <rect x="12" y="12" width="190" height="332" rx="28" fill="url(#card)"/>
    <rect x="28" y="38" width="156" height="18" rx="9" fill="#C4E0F7"/>
    <rect x="28" y="76" width="156" height="54" rx="16" fill="#FFFFFF"/>
    <rect x="28" y="146" width="72" height="72" rx="16" fill="#0B6EA8" fill-opacity="0.14"/>
    <rect x="112" y="146" width="72" height="72" rx="16" fill="#14B8A6" fill-opacity="0.14"/>
    <rect x="28" y="230" width="156" height="24" rx="12" fill="#C4E0F7"/>
    <rect x="28" y="268" width="128" height="24" rx="12" fill="#C4E0F7"/>
    <circle cx="104" cy="320" r="34" fill="#0B6EA8"/>
    <circle cx="104" cy="320" r="18" fill="#EAF6FF"/>
  </g>

  <g transform="translate(634 146)">
    <circle cx="90" cy="82" r="82" fill="#EAF6FF"/>
    <path fill="#0B6EA8" d="M38 90h104c18 0 34 16 34 34s-16 34-34 34h-18c-8 22-28 38-52 40-31 4-60-13-72-40H4c-18 0-32-14-32-34s14-34 32-34z"/>
  </g>
</svg>
EOF
}

render_png() {
  local input_svg="$1"
  local output_png="$2"
  convert "${input_svg}" "${output_png}"
}

copy_screenshots() {
  local locale_dir="$1"
  mkdir -p "${locale_dir}/images/phoneScreenshots"

  local index
  for index in {1..8}; do
    cp -f "${SOURCE_IMAGES_DIR}/${index}.png" \
      "${locale_dir}/images/phoneScreenshots/$(printf '%02d' "${index}").png"
  done
}

main() {
  require_command convert

  if [[ ! -d "${SOURCE_IMAGES_DIR}" ]]; then
    echo "Source screenshots not found: ${SOURCE_IMAGES_DIR}" >&2
    exit 1
  fi

  local locale
  for locale in pt-BR en-US; do
    local locale_dir="${METADATA_DIR}/${locale}"
    mkdir -p "${locale_dir}/images"

    copy_screenshots "${locale_dir}"

    write_svg "${TMP_DIR}/${locale}-icon.svg" "${locale}" "icon"
    render_png "${TMP_DIR}/${locale}-icon.svg" "${locale_dir}/images/icon.png"

    write_svg "${TMP_DIR}/${locale}-feature.svg" "${locale}" "feature"
    render_png "${TMP_DIR}/${locale}-feature.svg" "${locale_dir}/images/featureGraphic.png"
  done

  echo "Assets generated under ${METADATA_DIR}"
}

main "$@"
