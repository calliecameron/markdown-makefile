#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") workspace_status"
    exit 1
}

test -z "${1:-}" && usage
WORKSPACE_STATUS="${1}"

SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}"
BIN_DIR="${SOURCE_DIR}/.bin"

mkdir -p "${BIN_DIR}"
cp "${WORKSPACE_STATUS}" "${BIN_DIR}/workspace_status"
chmod u=rwx,go= "${BIN_DIR}/workspace_status"
