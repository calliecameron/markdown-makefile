#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_status_script git_repo_version_script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${PWD}/${1}"

test -z "${2:-}" && usage
VERSION_SCRIPT="${PWD}/${2}"

cd "${TEST_TMPDIR}"

export GIT_AUTHOR_NAME='test'
export GIT_COMMITTER_NAME='test'
export GIT_AUTHOR_EMAIL='test@example.com'
export GIT_COMMITTER_EMAIL='test@example.com'

mkdir -p a/b
touch a/b/foo
cd a
git init .
git add b/foo
git commit -m 'Test'
cd "${TEST_TMPDIR}"

# Not versioned
[ -z "$("${SCRIPT}" "${VERSION_SCRIPT}")" ]

# Dir itself is a repo
cd "${TEST_TMPDIR}/a"
[ -z "$("${SCRIPT}" "${VERSION_SCRIPT}")" ]

# Parent is a repo
cd "${TEST_TMPDIR}/a/b"
OUTPUT="$("${SCRIPT}" "${VERSION_SCRIPT}")"
echo "${OUTPUT}" | grep -E "^STABLE_WORKSPACE_PARENT_REPO ${TEST_TMPDIR}/a\$"
echo "${OUTPUT}" | grep -E '^STABLE_WORKSPACE_PARENT_VERSION [0-9a-f]+, [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\+00:00$'
