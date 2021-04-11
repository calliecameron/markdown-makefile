#!/bin/bash

function usage() {
    echo "Usage: $(basename "${0}") in_file)"
    exit 1
}

test -z "${1}" && usage
IN_FILE="${1}"

if [ -t 1 ]; then
    GREP_COLOUR='--color=always'
fi

OUTPUT="$(grep ${GREP_COLOUR} --context=1 -H -n -E "$(printf '%s|%s\n' '"' "'")" "${IN_FILE}")"
RETVAL="${?}"

if [ "${RETVAL}" = 0 ]; then
    # shellcheck disable=SC1111
    echo "Markdown validation failed: found quotes that weren't converted by smart quotes. Replace them with literal curly quotes (“ ” ‘ ’)."
    echo "${OUTPUT}"
    exit 1
fi

exit 0
