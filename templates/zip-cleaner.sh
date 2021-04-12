#!/bin/bash

function usage() {
    echo "Usage: $(basename "${0}") file"
    exit 1
}

test -z "${1}" && usage

if [ -n "${SOURCE_DATE_EPOCH}" ]; then
    strip-nondeterminism -t zip -T "${SOURCE_DATE_EPOCH}" "${1}"
fi
