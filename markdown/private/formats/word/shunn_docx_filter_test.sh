#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") pandoc strip_nondeterminism zipinfo filter reference_docx"
    exit 1
}

test -z "${1:-}" && usage
PANDOC="${1}"
test -z "${2:-}" && usage
STRIP_NONDETERMINISM="${2}"
test -z "${3:-}" && usage
ZIPINFO="${3}"
test -z "${4:-}" && usage
FILTER="${4}"
test -z "${5:-}" && usage
REFERENCE_DOCX="${5}"

cp "${REFERENCE_DOCX}" "${TEST_TMPDIR}/reference.docx"

"${ZIPINFO}" -T "${TEST_TMPDIR}/reference.docx" | grep '19800101' >/dev/null && exit 1

echo 'hello' | PANDOC_DATA_DIR="${TEST_TMPDIR}" "${PANDOC}" \
    --from=markdown \
    --to=docx \
    "--data-dir=${TEST_TMPDIR}" \
    "--metadata=strip-nondeterminism:${STRIP_NONDETERMINISM}" \
    "--lua-filter=${FILTER}" >/dev/null

"${ZIPINFO}" -T "${TEST_TMPDIR}/reference.docx" | grep '19800101' >/dev/null
