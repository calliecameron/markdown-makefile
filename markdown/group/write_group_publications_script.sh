#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") workspace_name file_to_open out_file"
    exit 1
}

test -z "${1:-}" && usage
WORKSPACE_NAME="${1}"
test -z "${2:-}" && usage
FILE_TO_OPEN="${2}"
test -z "${3:-}" && usage
OUT_FILE="${3}"

cat >"${OUT_FILE}" <<EOF
#!/bin/bash

set -eu

FILE_TO_OPEN="\${0}.runfiles/${WORKSPACE_NAME}/${FILE_TO_OPEN}"

xdg-open "\${FILE_TO_OPEN}"
EOF

chmod u+x "${OUT_FILE}"
