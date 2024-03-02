#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
UPDATER='foo'

echo 'a' >"${TEST_TMPDIR}/a"
chmod u=rw,go= "${TEST_TMPDIR}/a"
echo 'a' >"${TEST_TMPDIR}/a2"
chmod u=rw,go= "${TEST_TMPDIR}/a2"
echo 'a' >"${TEST_TMPDIR}/a_wrong_mode"
chmod u=rwx,go= "${TEST_TMPDIR}/a_wrong_mode"

echo 'b' >"${TEST_TMPDIR}/b"
chmod u=rw,go= "${TEST_TMPDIR}/b"
echo 'b' >"${TEST_TMPDIR}/b2"
chmod u=rw,go= "${TEST_TMPDIR}/b2"
echo 'b' >"${TEST_TMPDIR}/b_wrong_mode"
chmod u=rwx,go= "${TEST_TMPDIR}/b_wrong_mode"

# Bad args
"${SCRIPT}" && exit 1
"${SCRIPT}" "${UPDATER}" && exit 1
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" && exit 1
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" && exit 1
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/c" '600' && exit 1
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' "${TEST_TMPDIR}/b" && exit 1

# One file, ok
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600'
# Missing file
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" '' '600' && exit 1
# Contents differ
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/b" '600' && exit 1
# Mode differs
"${SCRIPT}" "${UPDATER}" "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a_wrong_mode" '600' && exit 1

# Two files, ok
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' \
    "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b2" '600'
# First file missing
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" '' '600' \
    "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b2" '600' && exit 1
# First file's contents differ
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/b" '600' \
    "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b2" '600' && exit 1
# First file's mode differs
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a_wrong_mode" '600' \
    "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b2" '600' && exit 1
# Second file missing
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' \
    "${TEST_TMPDIR}/b" '' '600' && exit 1
# Second file's contents differ
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' \
    "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/a" '600' && exit 1
# Second file's mode differs
"${SCRIPT}" "${UPDATER}" \
    "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' \
    "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b_wrong_mode" '600' && exit 1

exit 0
