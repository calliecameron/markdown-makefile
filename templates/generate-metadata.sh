#!/bin/bash

THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function usage() {
    echo "Usage: $(basename "${0}") out_file in_file"
    exit 1
}

function get-commit() {
    # This will return nonzero if we're in a new repo with no commits yet
    git describe --no-match --always --long
}

function describe-commit() {
    git describe --no-match --always --long --dirty
}

function commit-timestamp() {
    git show --no-patch --no-notes --pretty='%cd' "${1}"
}


test -z "${1}" && usage
OUTFILE="${1}"
test -z "${2}" && usage
INFILE="${2}"


if [ -n "${DOC_VERSION}" ]; then
    # Use explicit version if set (for reproducible builds)
    VERSION="${DOC_VERSION}"
elif type git &>/dev/null && git rev-parse --git-dir &>/dev/null && get-commit &>/dev/null; then
    # Use git commit if we can
    COMMIT="$(get-commit)"
    DESCRIPTION="$(describe-commit)"
    TIMESTAMP="$(commit-timestamp "${COMMIT}")"
    VERSION="${DESCRIPTION}, ${TIMESTAMP}"
else
    # Else fall back to the current date and time
    VERSION="unversioned, $(date)"
fi

STARTS_WITH_TEXT="$(pandoc -t json "${INFILE}" | "${THIS_DIR}/starts-with-text.py")"
SOURCE_MD5="$(md5sum < "${INFILE}" | cut -d ' ' -f 1)"

TMPFILE="$(mktemp)"
cat > "${TMPFILE}" <<EOF
---
docversion: "${VERSION}"
subject: "Version: ${VERSION}"
lang: "en-GB"
starts-with-text: "${STARTS_WITH_TEXT}"
pandoc-options:
source-md5: "${SOURCE_MD5}"
---
EOF

# Since make uses timestamps, not contents, to determine whether to rebuild, we
# only update the output file if it would differ.
if ! cmp "${TMPFILE}" "${OUTFILE}" &>/dev/null; then
    cp "${TMPFILE}" "${OUTFILE}"
fi

rm "${TMPFILE}"
