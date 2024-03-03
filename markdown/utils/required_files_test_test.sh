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
"${SCRIPT}" && exit 1
"${SCRIPT}" "${UPDATER}" && exit 1
"${SCRIPT}" "${UPDATER}" 'foo' && exit 1
"${SCRIPT}" "${UPDATER}" '--foo' && exit 1

"${SCRIPT}" "${UPDATER}" '--check' && exit 1
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/a" && exit 1
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" && exit 1
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/c" "${TEST_TMPDIR}/a2" '600' && exit 1
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/c" '600' && exit 1

"${SCRIPT}" "${UPDATER}" '--check_mode_only' && exit 1
"${SCRIPT}" "${UPDATER}" '--check_mode_only' "${TEST_TMPDIR}/a" && exit 1
"${SCRIPT}" "${UPDATER}" '--check_mode_only' "${TEST_TMPDIR}/c" '600' && exit 1

"${SCRIPT}" "${UPDATER}" '--missing_file' && exit 1

"${SCRIPT}" "${UPDATER}" '--extra_check' && exit 1
"${SCRIPT}" "${UPDATER}" '--extra_check' "${TEST_TMPDIR}/c" && exit 1
"${SCRIPT}" "${UPDATER}" '--extra_check' "${TEST_TMPDIR}/a" && exit 1

# check
# Same
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600'
# Contents differ
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/b" '600' && exit 1
# Mode differs
"${SCRIPT}" "${UPDATER}" '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a_wrong_mode" '600' && exit 1

# check_mode_only
# OK
"${SCRIPT}" "${UPDATER}" '--check_mode_only' "${TEST_TMPDIR}/a" '600'
# Mode differs
"${SCRIPT}" "${UPDATER}" '--check_mode_only' "${TEST_TMPDIR}/a_wrong_mode" '600' && exit 1

# missing_file
"${SCRIPT}" "${UPDATER}" '--missing_file' 'a' && exit 1

# extra_check
# Success
"${SCRIPT}" "${UPDATER}" '--extra_check' "${TEST_TMPDIR}/success"
# Failure
"${SCRIPT}" "${UPDATER}" '--extra_check' "${TEST_TMPDIR}/failure" && exit 1

# Everything
# Success
"${SCRIPT}" "${UPDATER}" \
    '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' \
    '--check' "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b2" '600' \
    '--check_mode_only' "${TEST_TMPDIR}/a" '600' \
    '--check_mode_only' "${TEST_TMPDIR}/a_wrong_mode" '700' \
    '--extra_check' "${TEST_TMPDIR}/success"
# Failure
"${SCRIPT}" "${UPDATER}" \
    '--check' "${TEST_TMPDIR}/a" "${TEST_TMPDIR}/a2" '600' \
    '--check' "${TEST_TMPDIR}/b" "${TEST_TMPDIR}/b2" '600' \
    '--check_mode_only' "${TEST_TMPDIR}/a" '600' \
    '--check_mode_only' "${TEST_TMPDIR}/a_wrong_mode" '600' \
    '--extra_check' "${TEST_TMPDIR}/success" && exit 1

exit 0
