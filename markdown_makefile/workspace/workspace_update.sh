#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") workspace_status workspace_git_update bazelversion bazelrc"
    exit 1
}

test -z "${1:-}" && usage
WORKSPACE_STATUS="${1}"
test -z "${2:-}" && usage
WORKSPACE_GIT_UPDATE="${2}"
test -z "${3:-}" && usage
BAZELVERSION="${3}"
test -z "${4:-}" && usage
BAZELRC="${4}"

SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}"
BIN_DIR="${SOURCE_DIR}/.bin"

mkdir -p "${BIN_DIR}"

cp "${WORKSPACE_STATUS}" "${BIN_DIR}/workspace_status"
chmod u=rwx,go= "${BIN_DIR}/workspace_status"

cp "${WORKSPACE_GIT_UPDATE}" "${SOURCE_DIR}/workspace_git_update"
chmod u=rwx,go= "${SOURCE_DIR}/workspace_git_update"

cp "${BAZELVERSION}" "${SOURCE_DIR}/.bazelversion"
chmod u=rw,go= "${SOURCE_DIR}/.bazelversion"

cp "${BAZELRC}" "${SOURCE_DIR}/.bazelrc"
chmod u=rw,go= "${SOURCE_DIR}/.bazelrc"
