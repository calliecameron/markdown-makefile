#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") xelatex"
    exit 1
}

test -z "${1:-}" && usage
XELATEX="$(dirname "$(readlink -f "${1}")")/xelatex"

cat <<EOF
#!/bin/bash

set -eu

XELATEX='${XELATEX}'

function cleanup() {
    rm -rf "\${TMPDIR}"
}

if [ -z "\${XDG_CACHE_HOME:-}" ]; then
    TMPDIR="\$(mktemp -d)"
    export XDG_CACHE_HOME="\${TMPDIR}"
    trap cleanup EXIT
fi

"\${XELATEX}" "\${@}"
EOF
