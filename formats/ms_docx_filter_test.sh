#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") pandoc filter reference_docx"
    exit 1
}

test -z "${1:-}" && usage
PANDOC="${1}"
test -z "${2:-}" && usage
FILTER="${2}"
test -z "${3:-}" && usage
REFERENCE_DOCX="${3}"

cp "${REFERENCE_DOCX}" "${TEST_TMPDIR}/reference.docx"

zipinfo -T "${TEST_TMPDIR}/reference.docx" | grep '19800101' >/dev/null && exit 1

echo 'hello' | PANDOC_DATA_DIR="${TEST_TMPDIR}" "${PANDOC}" \
    --from=markdown \
    --to=docx "--data-dir=${TEST_TMPDIR}" \
    "--lua-filter=${FILTER}" >/dev/null

zipinfo -T "${TEST_TMPDIR}/reference.docx" | grep '19800101' >/dev/null
