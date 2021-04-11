#!/bin/bash

if [ -t 1 ]; then
    GREP_COLOUR='--color=always'
fi

OUTPUT="$(grep ${GREP_COLOUR} --context=1 -n -E "$(printf '%s|%s\n' '"' "'")")"
RETVAL="${?}"

if [ "${RETVAL}" = 0 ]; then
    echo "Markdown validation failed: found quotes that weren't converted by smart quotes. Replace them with literal curly quotes."
    echo "${OUTPUT}"
    exit 1
fi

exit 0
