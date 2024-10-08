#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file"
    exit 1
}

test -z "${1:-}" && usage
FILE="${1}"

zipinfo -T "${FILE}" | grep '19800101'
