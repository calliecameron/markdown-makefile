#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_update_script workspace_status workspace_contents_build workspace_contents_bzl workspace_summary workspace_publications workspace_git_update bazelversion bazelrc"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
WORKSPACE_STATUS="${2}"
test -z "${3:-}" && usage
WORKSPACE_CONTENTS_BUILD="${3}"
test -z "${4:-}" && usage
WORKSPACE_CONTENTS_BZL="${4}"
test -z "${5:-}" && usage
WORKSPACE_SUMMARY="${5}"
test -z "${6:-}" && usage
WORKSPACE_PUBLICATIONS="${6}"
test -z "${7:-}" && usage
WORKSPACE_GIT_UPDATE="${7}"
test -z "${8:-}" && usage
BAZELVERSION="${8}"
test -z "${9:-}" && usage
BAZELRC="${9}"

REGISTRY='foo'

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" \
    "${WORKSPACE_STATUS}" \
    "${WORKSPACE_CONTENTS_BUILD}" \
    "${WORKSPACE_CONTENTS_BZL}" \
    "${WORKSPACE_SUMMARY}" \
    "${WORKSPACE_PUBLICATIONS}" \
    "${WORKSPACE_GIT_UPDATE}" \
    "${BAZELVERSION}" \
    "${BAZELRC}" \
    "${REGISTRY}"

TMP_BAZELRC="${TEST_TMPDIR}/tmp_bazelrc"
sed "s|@@@@@|${REGISTRY}|g" <"${BAZELRC}" >"${TMP_BAZELRC}"

diff "${WORKSPACE_STATUS}" "${TEST_TMPDIR}/.bin/workspace_status"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bin/workspace_status")" = '700' ]
diff "${WORKSPACE_CONTENTS_BUILD}" "${TEST_TMPDIR}/.workspace_contents/BUILD"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.workspace_contents/BUILD")" = '600' ]
diff "${WORKSPACE_CONTENTS_BZL}" "${TEST_TMPDIR}/.workspace_contents/workspace_contents.bzl"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.workspace_contents/workspace_contents.bzl")" = '600' ]
diff "${WORKSPACE_SUMMARY}" "${TEST_TMPDIR}/workspace_summary"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_summary")" = '700' ]
diff "${WORKSPACE_PUBLICATIONS}" "${TEST_TMPDIR}/workspace_publications"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_publications")" = '700' ]
diff "${WORKSPACE_GIT_UPDATE}" "${TEST_TMPDIR}/workspace_git_update"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_git_update")" = '700' ]
diff "${BAZELVERSION}" "${TEST_TMPDIR}/.bazelversion"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bazelversion")" = '600' ]
diff "${TMP_BAZELRC}" "${TEST_TMPDIR}/.bazelrc"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bazelversion")" = '600' ]
