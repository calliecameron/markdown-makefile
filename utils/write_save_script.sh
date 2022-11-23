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
    PACKAGE="${PACKAGE}/"
fi

cat >"${OUT_FILE}" <<EOF
#!/bin/bash

set -eu

OUTPUT_DIR="${PACKAGE}output"
SAVE_DIR="\${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}saved"

mkdir -p "\${SAVE_DIR}"
cd "\${OUTPUT_DIR}"
cp -t "\${SAVE_DIR}" *
cd "\${SAVE_DIR}"
chmod u=rw *
EOF

chmod u+x "${OUT_FILE}"
