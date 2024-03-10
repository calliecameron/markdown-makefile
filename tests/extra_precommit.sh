#!/bin/bash

set -eu

if ! grep "$(date '+%Y')" 'LICENSE' &>/dev/null; then
    echo 'Error: update LICENSE to contain the current year'
    exit 1
fi

cd tests/other_workspace
bazel build ...:all
bazel test --build_tests_only ...:all

exit 0
