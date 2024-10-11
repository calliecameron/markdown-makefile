#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file regex"
    exit 1
}

test -z "${1:-}" && usage
FILE="${1}"
test -z "${2:-}" && usage
REGEX="${2}"

VERSION="$(grep '"version"' <"${FILE}" | sed 's/^ *"version": *"//g' | sed 's/",\?$//g')"

if ! echo "${VERSION}" | grep -E "^${REGEX}\$" >/dev/null; then
    echo "Version '${VERSION}' doesn't match regex '^${REGEX}\$'"
    exit 1
fi

exit 0
