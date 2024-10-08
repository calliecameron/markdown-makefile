#!/bin/bash
# Runs tests in a container, mainly to detect non-hermetic dependencies.

set -eu

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${THIS_DIR}"

podman build \
    -f Containerfile \
    --build-arg "uid=$(id -u)" \
    --build-arg "gid=$(id -g)" \
    -t rules-markdown-container-test \
    ../
