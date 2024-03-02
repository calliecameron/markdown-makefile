#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"

WORKSPACE="${TEST_TMPDIR}/workspace"
mkdir "${WORKSPACE}"

echo 'a' >"${TEST_TMPDIR}/a"
chmod u=rw,go= "${TEST_TMPDIR}/a"
echo 'b' >"${TEST_TMPDIR}/b"
chmod u=rw,go= "${TEST_TMPDIR}/b"

echo 'a' >"${WORKSPACE}/a"
chmod u=rwx,go= "${WORKSPACE}/a"

mkdir "${WORKSPACE}/package"
echo 'a' >"${WORKSPACE}/package/a"
chmod u=rwx,go= "${WORKSPACE}/package/a"

# Bad args
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' "${TEST_TMPDIR}/a" && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' "${TEST_TMPDIR}/a" 'a' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' "${TEST_TMPDIR}/c" 'a' '600' && exit 1

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' \
    "${TEST_TMPDIR}/a" 'a' '600' \
    "${TEST_TMPDIR}/b" 'b' '700'

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" 'package' \
    "${TEST_TMPDIR}/a" 'a' '600' \
    "${TEST_TMPDIR}/b" 'b' '700'

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/a"
[ "$(stat -c '%a' "${WORKSPACE}/a")" = '600' ]

diff "${TEST_TMPDIR}/b" "${WORKSPACE}/b"
[ "$(stat -c '%a' "${WORKSPACE}/b")" = '700' ]

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/package/a"
[ "$(stat -c '%a' "${WORKSPACE}/package/a")" = '600' ]

diff "${TEST_TMPDIR}/b" "${WORKSPACE}/package/b"
[ "$(stat -c '%a' "${WORKSPACE}/package/b")" = '700' ]
