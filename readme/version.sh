#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") module in_file"
}

test -z "${1:-}" && usage
MODULE="${1}"
test -z "${2:-}" && usage
IN_FILE="${2}"

VERSION="$(tr '\n' '\t' <"${MODULE}" |
    grep -o -E 'module\([^\)]+version = "([0-9]|\.)+"[^\)]+\)' |
    tr '\t' '\n' |
    grep 'version' |
    grep -o '".*"' |
    sed 's/"//g')"

sed "s/@@@@@/${VERSION}/g" <"${IN_FILE}"
