#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") out_file package"
    exit 1
}

test -z "${1:-}" && usage
OUT_FILE="${1}"
PACKAGE="${2:-}" # Package will be empty in the root package.

if [ -n "${PACKAGE}" ]; then
    PACKAGE_PATH="${PACKAGE}/"
else
    PACKAGE_PATH=''
fi

cat >"${OUT_FILE}" <<EOF
#!/bin/bash

set -eu

DATA_DIR="\${PWD}/${PACKAGE_PATH}"
SOURCE_DIR="\${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE_PATH}"
GIT_DIR="\${SOURCE_DIR}.git"
BIN_DIR="\${SOURCE_DIR}.bin"

if [ ! -d "\${GIT_DIR}" ]; then
    echo "ERROR: package '${PACKAGE}' is not the root of a git repo" >&2
    exit 1
fi

cd "\${DATA_DIR}"
mkdir -p "\${BIN_DIR}"
cp -t "\${BIN_DIR}" docdump pdfdump zipdump
cd "\${BIN_DIR}"
chmod u=rwx *

cd "\${DATA_DIR}"
cp default_gitattributes "\${SOURCE_DIR}.gitattributes"
cp default_gitconfig "\${SOURCE_DIR}.gitconfig"
cp default_gitignore "\${SOURCE_DIR}.gitignore"
cd "\${SOURCE_DIR}"
chmod u=rw .gitattributes .gitconfig .gitignore
git config --local include.path ../.gitconfig
EOF

chmod u+x "${OUT_FILE}"
