#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") new_script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"

(
    cd "${TEST_TMPDIR}"

    # Not a git repo
    mkdir a
    mkdir a/a

    # Already a git repo
    mkdir b
    mkdir b/a
    mkdir b/b
    echo '% Foo' >b/b/b.md
    (
        cd b
        git init .
    )

    # Git repo in subpackage
    mkdir c
    mkdir c/a
    (
        cd c/a
        git init .
    )

)

# Root package; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/a" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/a" "${SCRIPT}" && exit 1
# Normal package; success, git init
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/a" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/a/a" "${SCRIPT}"
test -d "${TEST_TMPDIR}/a/a/.git"
grep 'md_git_repo' "${TEST_TMPDIR}/a/a/BUILD" >/dev/null
grep 'md_document' "${TEST_TMPDIR}/a/a/BUILD" >/dev/null
grep '% a' "${TEST_TMPDIR}/a/a/a.md" >/dev/null
# Same package again; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/a" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/a/a" "${SCRIPT}" && exit 1

# Root package; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/b" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/b" "${SCRIPT}" && exit 1
# Normal package; success, already in git
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/b" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/b/a" "${SCRIPT}"
test -d "${TEST_TMPDIR}/b/.git"
test ! -d "${TEST_TMPDIR}/b/a/.git"
grep 'md_git_repo' "${TEST_TMPDIR}/b/a/BUILD" >/dev/null && exit 1
grep 'md_document' "${TEST_TMPDIR}/b/a/BUILD" >/dev/null
grep '% a' "${TEST_TMPDIR}/b/a/a.md" >/dev/null
# Same package again; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/b" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/b/a" "${SCRIPT}" && exit 1
# Package that already has an md file; success, already in git, don't overwrite md
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/b" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/b/b" "${SCRIPT}"
test -d "${TEST_TMPDIR}/b/.git"
test ! -d "${TEST_TMPDIR}/b/b/.git"
grep 'md_git_repo' "${TEST_TMPDIR}/b/b/BUILD" >/dev/null && exit 1
grep 'md_document' "${TEST_TMPDIR}/b/b/BUILD" >/dev/null
grep '% Foo' "${TEST_TMPDIR}/b/b/b.md" >/dev/null
# Same package again; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/b" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/b/b" "${SCRIPT}" && exit 1

# Root package; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/c" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/c" "${SCRIPT}" && exit 1
# Package at git root; success
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/c" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/c/a" "${SCRIPT}"
test -d "${TEST_TMPDIR}/c/a/.git"
grep 'md_git_repo' "${TEST_TMPDIR}/c/a/BUILD" >/dev/null
grep 'md_document' "${TEST_TMPDIR}/c/a/BUILD" >/dev/null
grep '% a' "${TEST_TMPDIR}/c/a/a.md" >/dev/null
# Same package again; fail
BUILD_WORKSPACE_DIRECTORY="${TEST_TMPDIR}/c" BUILD_WORKING_DIRECTORY="${TEST_TMPDIR}/c/a" "${SCRIPT}" && exit 1

exit 0
