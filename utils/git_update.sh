#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") docdump pdfdump zipdump gitattributes gitconfig gitignore precommit package"
    exit 1
}

test -z "${1:-}" && usage
DOCDUMP="${1}"
test -z "${2:-}" && usage
PDFDUMP="${2}"
test -z "${3:-}" && usage
ZIPDUMP="${3}"
test -z "${4:-}" && usage
GITATTRIBUTES="${4}"
test -z "${5:-}" && usage
GITCONFIG="${5}"
test -z "${6:-}" && usage
GITIGNORE="${6}"
test -z "${7:-}" && usage
PRECOMMIT="${7}"
PACKAGE="${8:-}" # Package will be empty in the root package.

if [ -n "${PACKAGE}" ]; then
    SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}"
else
    SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}"
fi

GIT_DIR="${SOURCE_DIR}/.git"
BIN_DIR="${SOURCE_DIR}/.bin"

if [ ! -d "${GIT_DIR}" ]; then
    echo "ERROR: package '${PACKAGE}' is not the root of a git repo" >&2
    exit 1
fi

mkdir -p "${BIN_DIR}"
cp "${DOCDUMP}" "${BIN_DIR}/docdump"
cp "${PDFDUMP}" "${BIN_DIR}/pdfdump"
cp "${ZIPDUMP}" "${BIN_DIR}/zipdump"
chmod u=rwx "${BIN_DIR}/docdump" "${BIN_DIR}/pdfdump" "${BIN_DIR}/zipdump"

cp "${GITATTRIBUTES}" "${SOURCE_DIR}/.gitattributes"
cp "${GITCONFIG}" "${SOURCE_DIR}/.gitconfig"
cp "${GITIGNORE}" "${SOURCE_DIR}/.gitignore"
chmod u=rw "${SOURCE_DIR}/.gitattributes" "${SOURCE_DIR}/.gitconfig" "${SOURCE_DIR}/.gitignore"
cp "${PRECOMMIT}" "${SOURCE_DIR}/.git/hooks/pre-commit"
chmod u=rwx "${SOURCE_DIR}/.git/hooks/pre-commit"
cd "${SOURCE_DIR}"
git config --local include.path ../.gitconfig
