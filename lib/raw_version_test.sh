#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") raw_version_script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${PWD}/${1}"

INFILE="${TEST_TMPDIR}/infile"
OUTFILE="${TEST_TMPDIR}/outfile"
EXPECTED="${TEST_TMPDIR}/expected"
PACKAGE='a/b'

# Everything as expected
cat >"${INFILE}" <<EOF
STABLE_PANDOC_VERSION 1.2.3
STABLE_VERSION_A_SOLIDUS_B 10
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
EOF

"${SCRIPT}" "${INFILE}" "${OUTFILE}" "${PACKAGE}"

cat <<EOF | head -c -1 >"${EXPECTED}"
{
    "pandoc_version": "1.2.3",
    "repo": "/foo/.git",
    "version": "10"
}
EOF

diff "${OUTFILE}" "${EXPECTED}"

# Missing pandoc version
cat >"${INFILE}" <<EOF
STABLE_VERSION_A_SOLIDUS_B 10
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
EOF

"${SCRIPT}" "${INFILE}" "${OUTFILE}" "${PACKAGE}" && exit 1

# Missing version
cat >"${INFILE}" <<EOF
STABLE_PANDOC_VERSION 1.2.3
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
EOF

"${SCRIPT}" "${INFILE}" "${OUTFILE}" "${PACKAGE}" && exit 1

# Missing repo
cat >"${INFILE}" <<EOF
STABLE_PANDOC_VERSION 1.2.3
STABLE_VERSION_A_SOLIDUS_B 10
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
EOF

"${SCRIPT}" "${INFILE}" "${OUTFILE}" "${PACKAGE}" && exit 1

true
