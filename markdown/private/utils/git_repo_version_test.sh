#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") git_repo_version_script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${PWD}/${1}"

cd "${TEST_TMPDIR}"

export GIT_AUTHOR_NAME='test'
export GIT_COMMITTER_NAME='test'
export GIT_AUTHOR_EMAIL='test@example.com'
export GIT_COMMITTER_EMAIL='test@example.com'

# Not a git repo
mkdir a
touch a/foo

# Git repo with no commits
mkdir b
touch b/foo
cd b
git init .
cd "${TEST_TMPDIR}"

# Clean git repo
mkdir c
touch c/foo
cd c
git init .
git add foo
git commit -m 'Test'
cd "${TEST_TMPDIR}"

# Dirty git repo
mkdir d
touch d/foo
cd d
git init .
git add foo
git commit -m 'Test'
touch bar
cd "${TEST_TMPDIR}"

# Clean git repo that's ahead of upstream
git clone c e
cd e
touch bar
git add bar
git commit -m 'Test'
cd "${TEST_TMPDIR}"

CLEAN='^[0-9a-f]+, [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\+00:00$'
DIRTY='^[0-9a-f]+-dirty, [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\+00:00$'

# Test output
[ "$("${SCRIPT}" "${TEST_TMPDIR}")" = 'unversioned' ]

[ "$("${SCRIPT}" "${TEST_TMPDIR}/a")" = 'unversioned' ]

[ "$("${SCRIPT}" "${TEST_TMPDIR}/b")" = 'unversioned' ]

"${SCRIPT}" "${TEST_TMPDIR}/c" | grep -E "${CLEAN}"

"${SCRIPT}" "${TEST_TMPDIR}/d" | grep -E "${DIRTY}"

"${SCRIPT}" "${TEST_TMPDIR}/e" | grep -E "${DIRTY}"

exit 0
