#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_update_script workspace_status workspace_summary bazelversion"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
WORKSPACE_STATUS="${2}"
test -z "${3:-}" && usage
WORKSPACE_SUMMARY="${3}"
test -z "${4:-}" && usage
BAZELVERSION="${4}"

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" \
    "${WORKSPACE_STATUS}" \
    "${WORKSPACE_SUMMARY}" \
    "${BAZELVERSION}"

diff "${WORKSPACE_STATUS}" "${TEST_TMPDIR}/.bin/workspace_status"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bin/workspace_status")" = '700' ]
diff "${WORKSPACE_SUMMARY}" "${TEST_TMPDIR}/workspace_summary"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_summary")" = '700' ]
diff "${BAZELVERSION}" "${TEST_TMPDIR}/.bazelversion"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bazelversion")" = '600' ]
