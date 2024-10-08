#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") hunspell dict_dir locale_archive custom_dict_file in_file out_file language"
    exit 1
}

test -z "${1:-}" && usage
HUNSPELL="${1}"
test -z "${2:-}" && usage
DICT_DIR="${2}"
test -z "${3:-}" && usage
LOCALE_ARCHIVE="${3}"
test -z "${4:-}" && usage
CUSTOM_DICT_FILE="${4}"
test -z "${5:-}" && usage
IN_FILE="${5}"
test -z "${6:-}" && usage
OUT_FILE="${6}"
test -z "${7:-}" && usage
LANGUAGE="${7}"

# Hunspell doesn't like single curly quotes
# shellcheck disable=SC1112
OUTPUT="$(
    perl -pe 's/(\W)‘/$1/g;s/’(\W)/$1/g;s/^‘//;s/’$//;' <"${IN_FILE}" |
        HOME="${PWD}" LC_ALL="${LANGUAGE}.UTF-8" LOCALE_ARCHIVE="${LOCALE_ARCHIVE}" DICPATH="${DICT_DIR}" "${HUNSPELL}" -d "${LANGUAGE}" -p "${CUSTOM_DICT_FILE}" -l |
        LC_ALL=C sort --ignore-case |
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
