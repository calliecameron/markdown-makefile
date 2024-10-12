#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") md2short pandoc zip unzip args..."
    exit 1
}

test -z "${1:-}" && usage
MD2SHORT="${1}"
test -z "${2:-}" && usage
PANDOC="${2}"
test -z "${3:-}" && usage
ZIP="$(readlink -f "${3}")"
test -z "${4:-}" && usage
UNZIP="$(readlink -f "${4}")"

PANDOC="${PANDOC}" PATH="$(dirname "${ZIP}"):$(dirname "${UNZIP}"):${PATH}" "${MD2SHORT}" "${@:5}"
