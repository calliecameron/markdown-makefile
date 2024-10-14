#!/bin/bash
# Interactive shell in the container.

set -eu

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"${THIS_DIR}/container_build.sh"

podman run \
    --rm \
    -it \
    --user "$(id -u):$(id -g)" \
    -e "TERM=${TERM}" \
    rules-markdown-container-test
