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
echo 'c' >"${WORKSPACE}/c"
chmod u=rw,go= "${WORKSPACE}/c"

mkdir "${WORKSPACE}/package"
echo 'a' >"${WORKSPACE}/package/a"
chmod u=rwx,go= "${WORKSPACE}/package/a"

cat >"${TEST_TMPDIR}/success" <<EOF
#!/bin/bash
exit 0
EOF
chmod u=rwx,go= "${TEST_TMPDIR}/success"

cat >"${TEST_TMPDIR}/failure" <<EOF
#!/bin/bash
exit 1
EOF
chmod u=rwx,go= "${TEST_TMPDIR}/failure"

# Bad args
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' 'foo' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--foo' && exit 1

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--copy' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--copy' "${TEST_TMPDIR}/a" && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--copy' "${TEST_TMPDIR}/a" 'a' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--copy' "${TEST_TMPDIR}/z" 'a' '600' && exit 1

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--create' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--create' "${TEST_TMPDIR}/a" && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--create' "${TEST_TMPDIR}/a" 'a' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--create' "${TEST_TMPDIR}/z" 'a' '600' && exit 1

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--extra_script' && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--extra_script' "${TEST_TMPDIR}/z" && exit 1
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--extra_script' "${TEST_TMPDIR}/a" && exit 1

# extra_script
# Success
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--extra_script' "${TEST_TMPDIR}/success"
# Failure
BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' '--extra_script' "${TEST_TMPDIR}/failure" && exit 1

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" '' \
    '--copy' "${TEST_TMPDIR}/a" 'a' '600' \
    '--copy' "${TEST_TMPDIR}/b" 'b' '700' \
    '--copy' "${TEST_TMPDIR}/a" 'subdir/a' '600' \
    '--create' "${TEST_TMPDIR}/a" 'c' '700' \
    '--extra_script' "${TEST_TMPDIR}/success"

BUILD_WORKSPACE_DIRECTORY="${WORKSPACE}" "${SCRIPT}" 'package' \
    '--copy' "${TEST_TMPDIR}/a" 'a' '600' \
    '--copy' "${TEST_TMPDIR}/b" 'b' '700' \
    '--copy' "${TEST_TMPDIR}/a" 'subdir/a' '600' \
    '--create' "${TEST_TMPDIR}/a" 'c' '700' \
    '--extra_script' "${TEST_TMPDIR}/success"

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/a"
[ "$(stat -c '%a' "${WORKSPACE}/a")" = '600' ]

diff "${TEST_TMPDIR}/b" "${WORKSPACE}/b"
[ "$(stat -c '%a' "${WORKSPACE}/b")" = '700' ]

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/subdir/a"
[ "$(stat -c '%a' "${WORKSPACE}/subdir/a")" = '600' ]

[ "$(cat "${WORKSPACE}/c")" = 'c' ]
[ "$(stat -c '%a' "${WORKSPACE}/c")" = '700' ]

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/package/a"
[ "$(stat -c '%a' "${WORKSPACE}/package/a")" = '600' ]

diff "${TEST_TMPDIR}/b" "${WORKSPACE}/package/b"
[ "$(stat -c '%a' "${WORKSPACE}/package/b")" = '700' ]

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/package/subdir/a"
[ "$(stat -c '%a' "${WORKSPACE}/package/subdir/a")" = '600' ]

diff "${TEST_TMPDIR}/a" "${WORKSPACE}/package/c"
[ "$(stat -c '%a' "${WORKSPACE}/c")" = '700' ]
