#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") find_git_repos_script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${PWD}/${1}"

cd "${TEST_TMPDIR}"

export GIT_AUTHOR_NAME='test'
export GIT_COMMITTER_NAME='test'
export GIT_AUTHOR_EMAIL='test@example.com'
export GIT_COMMITTER_EMAIL='test@example.com'

# Not a git repo, root package
touch BUILD

# Not a git repo
mkdir a
touch a/BUILD
# Ignored dir
mkdir a/.mypy_cache

# Git repo with no commits
mkdir b
touch b/BUILD
cd b
git init .
cd "${TEST_TMPDIR}"

# Clean git repo
mkdir c
touch c/BUILD
cd c
git init .
git add BUILD
git commit -m 'Test'
cd "${TEST_TMPDIR}"

# Dirty git repo
mkdir -p d/a
touch d/a/BUILD
cd d/a
git init .
git add BUILD
git commit -m 'Test'
mkdir a_b
touch a_b/BUILD
cd "${TEST_TMPDIR}"

# Clean git repo that's ahead of upstream
git clone c e
cd e
touch foo
git add foo
git commit -m 'Test'
cd "${TEST_TMPDIR}"

GOT="${TEST_TMPDIR}/got"
EXPECTED="${TEST_TMPDIR}/expected"

# Root not in a repo
"${SCRIPT}" "${TEST_TMPDIR}" >"${GOT}"
cat <<EOF >"${EXPECTED}"
{
    "dirs": [
        "",
        "a",
        "b",
        "c",
        "d",
        "d/a",
        "d/a/a_b",
        "e"
    ],
    "packages": {
        "b": "git_repo_b",
        "c": "git_repo_c",
        "d/a": "git_repo_d_SOLIDUS_a",
        "d/a/a_b": "git_repo_d_SOLIDUS_a",
        "e": "git_repo_e"
    },
    "repos": {
        "git_repo_b": "b",
        "git_repo_c": "c",
        "git_repo_d_SOLIDUS_a": "d/a",
        "git_repo_e": "e"
    }
}
EOF

diff "${EXPECTED}" "${GOT}"

# Root in a repo
"${SCRIPT}" "${TEST_TMPDIR}/d/a" >"${GOT}"
cat <<EOF >"${EXPECTED}"
{
    "dirs": [
        "",
        "a_b"
    ],
    "packages": {
        "": "git_repo_",
        "a_b": "git_repo_"
    },
    "repos": {
        "git_repo_": ""
    }
}
EOF

diff "${EXPECTED}" "${GOT}"

# Root in subdir of a repo
"${SCRIPT}" "${TEST_TMPDIR}/d/a/a_b" >"${GOT}"
cat <<EOF >"${EXPECTED}"
{
    "dirs": [
        ""
    ],
    "packages": {},
    "repos": {}
}
EOF

diff "${EXPECTED}" "${GOT}"
