#!/bin/bash
# Concatenate Hunspell dictionaries. A dictionary is a list of words, one per
# line.

set -eu

function usage() {
    echo "Usage: $(basename "${0}") out_file dicts..."
    exit 1
}

test -z "${1:-}" && usage
OUT_FILE="${1}"

shift

cat "${@}" | LC_ALL=C sort | uniq >"${OUT_FILE}"
