#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") update_script contents_build contents_bzl contents_update summary publications"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
CONTENTS_BUILD="${2}"
test -z "${3:-}" && usage
CONTENTS_BZL="${3}"
test -z "${4:-}" && usage
CONTENTS_UPDATE="${4}"
test -z "${5:-}" && usage
SUMMARY="${5}"
test -z "${6:-}" && usage
PUBLICATIONS="${6}"

mkdir "${TEST_TMPDIR}/a"

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" \
    "${CONTENTS_BUILD}" \
    "${CONTENTS_BZL}" \
    "${CONTENTS_UPDATE}" \
    "${SUMMARY}" \
    "${PUBLICATIONS}" \
    a

diff "${CONTENTS_BUILD}" "${TEST_TMPDIR}/a/.dynamic_group_contents/BUILD"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.dynamic_group_contents/BUILD")" = '600' ]
diff "${CONTENTS_BZL}" "${TEST_TMPDIR}/a/.dynamic_group_contents/contents.bzl"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.dynamic_group_contents/contents.bzl")" = '600' ]
diff "${CONTENTS_UPDATE}" "${TEST_TMPDIR}/a/.dynamic_group_contents/update"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.dynamic_group_contents/update")" = '700' ]
diff "${SUMMARY}" "${TEST_TMPDIR}/a/summary"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/summary")" = '700' ]
diff "${PUBLICATIONS}" "${TEST_TMPDIR}/a/publications"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/publications")" = '700' ]
