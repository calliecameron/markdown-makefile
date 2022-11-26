#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_update_script workspace_status"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
WORKSPACE_STATUS="${2}"

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" "${WORKSPACE_STATUS}"

diff "${WORKSPACE_STATUS}" "${TEST_TMPDIR}/.bin/workspace_status"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bin/workspace_status")" = '700' ]
