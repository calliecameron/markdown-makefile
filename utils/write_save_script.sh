#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") package out_file"
    exit 1
}

test -z "${1:-}" && usage
PACKAGE="${1}"
test -z "${2:-}" && usage
OUT_FILE="${2}"

cat >"${OUT_FILE}" <<EOF
#!/bin/bash

set -eu

OUTPUT_DIR="${PACKAGE}/output"
SAVE_DIR="\${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}/saved"

mkdir -p "\${SAVE_DIR}"
cd "\${OUTPUT_DIR}"
cp -t "\${SAVE_DIR}" *
cd "\${SAVE_DIR}"
chmod u=rw *
EOF

chmod u+x "${OUT_FILE}"
