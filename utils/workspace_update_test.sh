#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_update_script workspace_status workspace_summary"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
WORKSPACE_STATUS="${2}"
test -z "${3:-}" && usage
WORKSPACE_SUMMARY="${3}"

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" "${WORKSPACE_STATUS}" "${WORKSPACE_SUMMARY}"

diff "${WORKSPACE_STATUS}" "${TEST_TMPDIR}/.bin/workspace_status"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bin/workspace_status")" = '700' ]
diff "${WORKSPACE_SUMMARY}" "${TEST_TMPDIR}/workspace_summary"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_summary")" = '700' ]
