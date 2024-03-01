#!/bin/bash
# Unoconv can't run multiple instances in parallel, so we need a global lock.

LOCK="/tmp/markdown-makefile-unoconv.lock"

function unlock() {
    # shellcheck disable=SC2317
    rm -rf "${LOCK}"
}

while ! mkdir "${LOCK}" &>/dev/null; do
    sleep 1
done

trap unlock EXIT

unoconv "${@}"
EXIT_CODE="$?"

exit "${EXIT_CODE}"
