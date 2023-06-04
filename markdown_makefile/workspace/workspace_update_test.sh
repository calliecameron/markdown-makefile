#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_update_script workspace_status workspace_git_update bazelversion bazelrc"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
WORKSPACE_STATUS="${2}"
test -z "${3:-}" && usage
WORKSPACE_GIT_UPDATE="${3}"
test -z "${4:-}" && usage
BAZELVERSION="${4}"
test -z "${5:-}" && usage
BAZELRC="${5}"

REGISTRY='foo'

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" \
    "${WORKSPACE_STATUS}" \
    "${WORKSPACE_GIT_UPDATE}" \
    "${BAZELVERSION}" \
    "${BAZELRC}" \
    "${REGISTRY}"

TMP_BAZELRC="${TEST_TMPDIR}/tmp_bazelrc"
sed "s|@@@@@|${REGISTRY}|g" <"${BAZELRC}" >"${TMP_BAZELRC}"

diff "${WORKSPACE_STATUS}" "${TEST_TMPDIR}/.bin/workspace_status"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bin/workspace_status")" = '700' ]
diff "${WORKSPACE_GIT_UPDATE}" "${TEST_TMPDIR}/workspace_git_update"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_git_update")" = '700' ]
diff "${BAZELVERSION}" "${TEST_TMPDIR}/.bazelversion"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bazelversion")" = '600' ]
diff "${TMP_BAZELRC}" "${TEST_TMPDIR}/.bazelrc"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bazelversion")" = '600' ]
