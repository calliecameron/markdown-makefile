#!/bin/bash
# Concatenate Hunspell dictionaries. A dictionary is a list of words, one per
# line.

function usage() {
    echo "Usage: $(basename "${0}") out_file dicts..."
    exit 1
}

test -z "${1}" && usage
OUT_FILE="${1}"

shift

(
    while (($#)); do
        if [ -f "${1}" ]; then
            cat "${1}"
        fi
        shift
    done
) > "${OUT_FILE}"
