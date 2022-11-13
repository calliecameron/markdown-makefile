#!/bin/bash
# Generate initial metadata.

set -eu

function usage() {
    echo "Usage: $(basename "${0}") version_file package out_file"
    exit 1
}

test -z "${1:-}" && usage
VERSION_FILE="${1}"
test -z "${2:-}" && usage
PACKAGE="${2}"
test -z "${3:-}" && usage
OUT_FILE="${3}"

VERSION_KEY="STABLE_VERSION__$(echo "${PACKAGE}" | sed 's|/|__|g' | sed 's|-|_|g')" &&
    VERSION="$(grep "${VERSION_KEY}" "${VERSION_FILE}" | sed "s|^${VERSION_KEY}=||g")" || exit 1

if [ -z "${VERSION}" ]; then
    echo "Can't find version info for package '${PACKAGE}'"
    exit 1
fi

cat >"${OUT_FILE}" <<EOF
---
docversion: "${VERSION}"
subject: "Version: ${VERSION}"
lang: "en-GB"
pandoc-options:
---
EOF
