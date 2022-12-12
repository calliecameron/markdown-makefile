#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") gitattributes gitconfig gitignore precommit package"
    exit 1
}

test -z "${1:-}" && usage
GITATTRIBUTES="${1}"
test -z "${2:-}" && usage
GITCONFIG="${2}"
test -z "${3:-}" && usage
GITIGNORE="${3}"
test -z "${4:-}" && usage
PRECOMMIT="${4}"
PACKAGE="${5:-}" # Package will be empty in the root package.

if [ -n "${PACKAGE}" ]; then
    SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}"
else
    SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}"
fi

GIT_DIR="${SOURCE_DIR}/.git"

if [ ! -d "${GIT_DIR}" ]; then
    echo "ERROR: package '${PACKAGE}' is not the root of a git repo" >&2
    exit 1
fi

cp "${GITATTRIBUTES}" "${SOURCE_DIR}/.gitattributes"
cp "${GITCONFIG}" "${SOURCE_DIR}/.gitconfig"
cp "${GITIGNORE}" "${SOURCE_DIR}/.gitignore"
chmod u=rw,go= "${SOURCE_DIR}/.gitattributes" "${SOURCE_DIR}/.gitconfig" "${SOURCE_DIR}/.gitignore"
cp "${PRECOMMIT}" "${SOURCE_DIR}/.git/hooks/pre-commit"
chmod u=rwx,go= "${SOURCE_DIR}/.git/hooks/pre-commit"
cd "${SOURCE_DIR}"
git config --local include.path ../.gitconfig
