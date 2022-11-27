#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") dict_file in_file out_file"
    exit 1
}

test -z "${1:-}" && usage
DICT_FILE="${1}"
test -z "${2:-}" && usage
IN_FILE="${2}"
test -z "${3:-}" && usage
OUT_FILE="${3}"

if ! command -v hunspell &>/dev/null; then
    echo "ERROR: hunspell is not installed" >&2
    echo >&2
    exit 1
fi

# Hunspell doesn't like single curly quotes
# shellcheck disable=SC1112
OUTPUT="$(
    perl -pe 's/(\W)‘/$1/g;s/’(\W)/$1/g;s/^‘//;s/’$//;' <"${IN_FILE}" |
        HOME="${PWD}" LC_ALL='en_GB.UTF-8' hunspell -d en_GB -p "${DICT_FILE}" -l |
        LC_ALL=C sort |
        uniq
)"

if [ -n "${OUTPUT}" ]; then
    echo "ERROR: found misspelled words; correct them or add them to the dictionary:" >&2
    echo >&2
    echo "${OUTPUT}" >&2
    echo >&2
    exit 1
fi

echo 'OK' >"${OUT_FILE}"
