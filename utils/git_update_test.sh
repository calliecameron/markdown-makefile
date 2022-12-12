#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") git_update_script gitattributes gitconfig gitignore precommit"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"
test -z "${2:-}" && usage
GITATTRIBUTES="${2}"
test -z "${3:-}" && usage
GITCONFIG="${3}"
test -z "${4:-}" && usage
GITIGNORE="${4}"
test -z "${5:-}" && usage
PRECOMMIT="${5}"

(
    cd "${TEST_TMPDIR}"
    mkdir a
    cd a
    git init .
)

BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}" "${SCRIPT}" \
    "${GITATTRIBUTES}" \
    "${GITCONFIG}" \
    "${GITIGNORE}" \
    "${PRECOMMIT}" \
    a

diff "${GITATTRIBUTES}" "${TEST_TMPDIR}/a/.gitattributes"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.gitattributes")" = '600' ]
diff "${GITCONFIG}" "${TEST_TMPDIR}/a/.gitconfig"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.gitconfig")" = '600' ]
diff "${GITIGNORE}" "${TEST_TMPDIR}/a/.gitignore"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.gitignore")" = '600' ]
diff "${PRECOMMIT}" "${TEST_TMPDIR}/a/.git/hooks/pre-commit"
[ "$(stat -c '%a' "${TEST_TMPDIR}/a/.git/hooks/pre-commit")" = '700' ]
grep 'path = ../.gitconfig' "${TEST_TMPDIR}/a/.git/config" >/dev/null
