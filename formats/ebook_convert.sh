#!/bin/bash
# ebook-convert is chatty, so we wrap it and capture the output.

OUTPUT="$("${1}" "${@:2}" 2>&1)"
EXIT_CODE="$?"

if [ "${EXIT_CODE}" != '0' ]; then
    echo "${OUTPUT}" >&2
fi

exit "${EXIT_CODE}"
