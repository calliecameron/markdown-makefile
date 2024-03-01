#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") contents_build contents_bzl contents_update summary publications package"
    exit 1
}

test -z "${1:-}" && usage
CONTENTS_BUILD="${1}"
test -z "${2:-}" && usage
CONTENTS_BZL="${2}"
test -z "${3:-}" && usage
CONTENTS_UPDATE="${3}"
test -z "${4:-}" && usage
SUMMARY="${4}"
test -z "${5:-}" && usage
PUBLICATIONS="${5}"
PACKAGE="${6:-}" # Package will be empty in the root package.

if [ -n "${PACKAGE}" ]; then
    SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}"
else
    SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}"
fi

CONTENTS_DIR="${SOURCE_DIR}/.dynamic_group_contents"

mkdir -p "${CONTENTS_DIR}"

cp "${CONTENTS_BUILD}" "${CONTENTS_DIR}/BUILD"
chmod u=rw,go= "${CONTENTS_DIR}/BUILD"

if [ ! -f "${CONTENTS_DIR}/contents.bzl" ]; then
    cp "${CONTENTS_BZL}" "${CONTENTS_DIR}/contents.bzl"
fi
chmod u=rw,go= "${CONTENTS_DIR}/contents.bzl"

cp "${CONTENTS_UPDATE}" "${CONTENTS_DIR}/update"
chmod u=rwx,go= "${CONTENTS_DIR}/update"

cp "${SUMMARY}" "${SOURCE_DIR}/summary"
chmod u=rwx,go= "${SOURCE_DIR}/summary"

cp "${PUBLICATIONS}" "${SOURCE_DIR}/publications"
chmod u=rwx,go= "${SOURCE_DIR}/publications"
