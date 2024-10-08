#!/bin/bash
# Unoconv can't run multiple instances in parallel, so we need a global lock.

set -u

function usage() {
    echo "Usage: $(basename "${0}") unoconv args..."
    exit 1
}

test -z "${1:-}" && usage
UNOCONV="${1}"

LOCK="/tmp/markdown-makefile-unoconv.lock"

function unlock() {
    # shellcheck disable=SC2317
    rm -rf "${LOCK}"
}

while ! mkdir "${LOCK}" &>/dev/null; do
    sleep 1
done

trap unlock EXIT

"${UNOCONV}" "${@:2}"
EXIT_CODE="$?"

exit "${EXIT_CODE}"
