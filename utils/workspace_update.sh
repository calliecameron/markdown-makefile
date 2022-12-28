#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") workspace_status workspace_contents_build workspace_contents_bzl workspace_summary workspace_publications bazelversion bazelrc registry"
    exit 1
}

test -z "${1:-}" && usage
WORKSPACE_STATUS="${1}"
test -z "${2:-}" && usage
WORKSPACE_CONTENTS_BUILD="${2}"
test -z "${3:-}" && usage
WORKSPACE_CONTENTS_BZL="${3}"
test -z "${4:-}" && usage
WORKSPACE_SUMMARY="${4}"
test -z "${5:-}" && usage
WORKSPACE_PUBLICATIONS="${5}"
test -z "${6:-}" && usage
BAZELVERSION="${6}"
test -z "${7:-}" && usage
BAZELRC="${7}"
test -z "${8:-}" && usage
REGISTRY="${8}"

SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}"
BIN_DIR="${SOURCE_DIR}/.bin"
CONTENTS_DIR="${SOURCE_DIR}/.workspace_contents"

mkdir -p "${BIN_DIR}"
mkdir -p "${CONTENTS_DIR}"

cp "${WORKSPACE_STATUS}" "${BIN_DIR}/workspace_status"
chmod u=rwx,go= "${BIN_DIR}/workspace_status"

cp "${WORKSPACE_CONTENTS_BUILD}" "${CONTENTS_DIR}/BUILD"
chmod u=rw,go= "${CONTENTS_DIR}/BUILD"

if [ ! -f "${CONTENTS_DIR}/workspace_contents.bzl" ]; then
    cp "${WORKSPACE_CONTENTS_BZL}" "${CONTENTS_DIR}/workspace_contents.bzl"
fi
chmod u=rw,go= "${CONTENTS_DIR}/workspace_contents.bzl"

cp "${WORKSPACE_SUMMARY}" "${SOURCE_DIR}/workspace_summary"
chmod u=rwx,go= "${SOURCE_DIR}/workspace_summary"

cp "${WORKSPACE_PUBLICATIONS}" "${SOURCE_DIR}/workspace_publications"
chmod u=rwx,go= "${SOURCE_DIR}/workspace_publications"

cp "${BAZELVERSION}" "${SOURCE_DIR}/.bazelversion"
chmod u=rw,go= "${SOURCE_DIR}/.bazelversion"

sed "s|@@@@@|${REGISTRY}|g" <"${BAZELRC}" >"${SOURCE_DIR}/.bazelrc"
chmod u=rw,go= "${SOURCE_DIR}/.bazelrc"
