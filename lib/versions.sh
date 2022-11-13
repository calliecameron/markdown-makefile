#!/bin/bash
# Generate non-hermetic data for input to bazel.

set -u

function fail() {
    echo "ERROR:" "${@}" >&2
    exit 1
}

function is-git-repo() {
    git rev-parse --git-dir &>/dev/null
}

function get-commit() {
    # This will return nonzero if we're in a new repo with no commits yet
    git describe --no-match --always --long
}

function has-commits() {
    get-commit &>/dev/null
}

function get-commit-suffix {
    local TMPFILE &&
        TMPFILE="$(mktemp)" &&
        git status --porcelain -b >"${TMPFILE}" || return 1
    if grep -q '^##.*\[ahead.*\]$' "${TMPFILE}" || grep -q '^[^##]' "${TMPFILE}"; then
        echo '-dirty'
    fi
    rm "${TMPFILE}" || return 1
}

function get-commit-timestamp() {
    git show --no-patch --no-notes --pretty='%cd' "${1}"
}

function version() {
    local WORKSPACE_DIR="${PWD}" &&
        local PACKAGE &&
        PACKAGE="$(realpath "--relative-to=${WORKSPACE_DIR}" "$(dirname "${1}")")" &&
        local PACKAGE_PATH &&
        PACKAGE_PATH="$(realpath "${PACKAGE}")" &&
        cd "${PACKAGE_PATH}" &&
        local VERSION || return 1

    if type git &>/dev/null && is-git-repo && has-commits; then
        local COMMIT &&
            COMMIT="$(get-commit)" &&
            local SUFFIX &&
            SUFFIX="$(get-commit-suffix)" &&
            local TIMESTAMP &&
            TIMESTAMP="$(get-commit-timestamp "${COMMIT}")" &&
            VERSION="${COMMIT}${SUFFIX}, ${TIMESTAMP}" || return 1
    else
        VERSION='unversioned'
    fi

    cd "${WORKSPACE_DIR}" &&
        local PACKAGE_OUT &&
        PACKAGE_OUT="STABLE_VERSION__$(echo "${PACKAGE}" | sed 's|/|__|g' | sed 's|-|_|g')" &&
        echo "${PACKAGE_OUT}=${VERSION}" || return 1
}

EXPECTED_PANDOC_VERSION='pandoc 2.13'
ACTUAL_PANDOC_VERSION="$(pandoc --version | grep '^pandoc')"

if [ "${ACTUAL_PANDOC_VERSION}" != "${EXPECTED_PANDOC_VERSION}" ]; then
    fail "unsupported pandoc version; expected ${EXPECTED_PANDOC_VERSION}, got ${ACTUAL_PANDOC_VERSION}"
fi

echo "STABLE_PANDOC_VERSION=${ACTUAL_PANDOC_VERSION}"

find . -name BUILD | LC_ALL=C sort | while read -r line; do
    version "${line}" || fail "failed to get version of '${line}'"
done
