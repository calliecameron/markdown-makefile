#!/bin/bash

function usage() {
    echo "Usage: $(basename "${0}") out_file in_file"
    exit 1
}

test -z "${1}" && usage
OUT_FILE="${1}"
test -z "${2}" && usage
IN_FILE="${2}"

function get-var() {
    local VAR="${1}"
    local FILE="${2}"
    local TMPFILE
    TMPFILE="$(mktemp).md"
    echo "\$${VAR}\$" > "${TMPFILE}"
    pandoc "--template=${TMPFILE}" --to=markdown "${FILE}"
    rm "${TMPFILE}"
}

TITLE="$(get-var 'title' "${IN_FILE}")"

echo "${TITLE}" > "${OUT_FILE}"
