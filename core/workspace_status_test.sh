#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") workspace_status_script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${PWD}/${1}"

cd "${TEST_TMPDIR}"

# Not a git repo
mkdir a
touch a/BUILD

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
mkdir d
touch d/BUILD
cd d
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

# Fake pandoc
mkdir bin
printf '#!/bin/bash\necho pandoc foo' >bin/pandoc
chmod u+x bin/pandoc
PATH="${TEST_TMPDIR}/bin:${PATH}" "${SCRIPT}" && exit 1

# Test output
OUTPUT="$("${SCRIPT}")"

echo "${OUTPUT}" | grep 'STABLE_PANDOC_VERSION '

echo "${OUTPUT}" | grep 'STABLE_VERSION_A unversioned'
echo "${OUTPUT}" | grep 'STABLE_REPO_A unversioned'

echo "${OUTPUT}" | grep 'STABLE_VERSION_B unversioned'
echo "${OUTPUT}" | grep 'STABLE_REPO_B unversioned'

echo "${OUTPUT}" | grep 'STABLE_VERSION_C '
echo "${OUTPUT}" | grep 'STABLE_VERSION_C ' | grep 'unversioned' && exit 1
echo "${OUTPUT}" | grep 'STABLE_VERSION_C ' | grep 'dirty' && exit 1
echo "${OUTPUT}" | grep "STABLE_REPO_C ${TEST_TMPDIR}/c/.git"

echo "${OUTPUT}" | grep 'STABLE_VERSION_D '
echo "${OUTPUT}" | grep 'STABLE_VERSION_D ' | grep 'unversioned' && exit 1
echo "${OUTPUT}" | grep 'STABLE_VERSION_D ' | grep 'dirty'
echo "${OUTPUT}" | grep "STABLE_REPO_D ${TEST_TMPDIR}/d/.git"
echo "${OUTPUT}" | grep 'STABLE_VERSION_D_SOLIDUS_A__B '
echo "${OUTPUT}" | grep 'STABLE_VERSION_D_SOLIDUS_A__B ' | grep 'unversioned' && exit 1
echo "${OUTPUT}" | grep 'STABLE_VERSION_D_SOLIDUS_A__B ' | grep 'dirty'
echo "${OUTPUT}" | grep "STABLE_REPO_D_SOLIDUS_A__B ${TEST_TMPDIR}/d/.git"

echo "${OUTPUT}" | grep 'STABLE_VERSION_E '
echo "${OUTPUT}" | grep 'STABLE_VERSION_E ' | grep 'unversioned' && exit 1
echo "${OUTPUT}" | grep 'STABLE_VERSION_E ' | grep 'dirty'
echo "${OUTPUT}" | grep "STABLE_REPO_E ${TEST_TMPDIR}/e/.git"
