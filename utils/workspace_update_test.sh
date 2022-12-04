#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_update_script workspace_status workspace_contents_build workspace_contents_bzl workspace_summary bazelversion"
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
BAZELVERSION="${6}"

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" \
    "${WORKSPACE_STATUS}" \
    "${WORKSPACE_CONTENTS_BUILD}" \
    "${WORKSPACE_CONTENTS_BZL}" \
    "${WORKSPACE_SUMMARY}" \
    "${BAZELVERSION}"

diff "${WORKSPACE_STATUS}" "${TEST_TMPDIR}/.bin/workspace_status"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bin/workspace_status")" = '700' ]
diff "${WORKSPACE_CONTENTS_BUILD}" "${TEST_TMPDIR}/.workspace_contents/BUILD"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.workspace_contents/BUILD")" = '600' ]
diff "${WORKSPACE_CONTENTS_BZL}" "${TEST_TMPDIR}/.workspace_contents/workspace_contents.bzl"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.workspace_contents/workspace_contents.bzl")" = '600' ]
diff "${WORKSPACE_SUMMARY}" "${TEST_TMPDIR}/workspace_summary"
[ "$(stat -c '%a' "${TEST_TMPDIR}/workspace_summary")" = '700' ]
diff "${BAZELVERSION}" "${TEST_TMPDIR}/.bazelversion"
[ "$(stat -c '%a' "${TEST_TMPDIR}/.bazelversion")" = '600' ]
