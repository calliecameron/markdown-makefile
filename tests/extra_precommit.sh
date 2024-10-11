#!/bin/bash

set -eu

if ! grep "$(date '+%Y')" 'LICENSE' &>/dev/null; then
    echo 'Error: update LICENSE to contain the current year'
    exit 1
fi

exit 0
