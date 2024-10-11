#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file zipinfo"
    exit 1
}

test -z "${1:-}" && usage
FILE="${1}"
test -z "${2:-}" && usage
ZIPINFO="${2}"

"${ZIPINFO}" -T "${FILE}" | grep '19800101'
