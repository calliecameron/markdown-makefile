#!/bin/bash
# Unoconv can't run multiple instances in parallel, so we need a global lock.

LOCK="/tmp/markdown-makefile-unoconv.lock"

while ! mkdir "${LOCK}" &>/dev/null; do
    sleep 1
done

unoconv "${@}"
EXIT_CODE="$?"

rmdir "${LOCK}"

exit "${EXIT_CODE}"
