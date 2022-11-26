#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") bindump docdump pdfdump zipdump gitattributes gitconfig gitignore precommit package"
    exit 1
}

test -z "${1:-}" && usage
BINDUMP="${1}"
test -z "${2:-}" && usage
DOCDUMP="${2}"
test -z "${3:-}" && usage
PDFDUMP="${3}"
test -z "${4:-}" && usage
ZIPDUMP="${4}"
test -z "${5:-}" && usage
GITATTRIBUTES="${5}"
test -z "${6:-}" && usage
GITCONFIG="${6}"
test -z "${7:-}" && usage
GITIGNORE="${7}"
test -z "${8:-}" && usage
PRECOMMIT="${8}"
PACKAGE="${9:-}" # Package will be empty in the root package.

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
cp "${BINDUMP}" "${BIN_DIR}/bindump"
cp "${DOCDUMP}" "${BIN_DIR}/docdump"
cp "${PDFDUMP}" "${BIN_DIR}/pdfdump"
cp "${ZIPDUMP}" "${BIN_DIR}/zipdump"
chmod u=rwx,go= "${BIN_DIR}/bindump" "${BIN_DIR}/docdump" "${BIN_DIR}/pdfdump" "${BIN_DIR}/zipdump"

cp "${GITATTRIBUTES}" "${SOURCE_DIR}/.gitattributes"
cp "${GITCONFIG}" "${SOURCE_DIR}/.gitconfig"
cp "${GITIGNORE}" "${SOURCE_DIR}/.gitignore"
chmod u=rw,go= "${SOURCE_DIR}/.gitattributes" "${SOURCE_DIR}/.gitconfig" "${SOURCE_DIR}/.gitignore"
cp "${PRECOMMIT}" "${SOURCE_DIR}/.git/hooks/pre-commit"
chmod u=rwx,go= "${SOURCE_DIR}/.git/hooks/pre-commit"
cd "${SOURCE_DIR}"
git config --local include.path ../.gitconfig
