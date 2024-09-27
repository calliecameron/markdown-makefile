#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file tool [tool_helpers...]"
    exit 1
}

test -z "${1:-}" && usage
FILE="${1}"
test -z "${2:-}" && usage
TOOL="${2}"

"${TOOL}" "${@:3}" "$(readlink -f "${FILE}")"
