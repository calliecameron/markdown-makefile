#!/bin/bash
# Runs tests in a container, mainly to detect non-hermetic dependencies.

set -eu

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${THIS_DIR}"

NIXPKGS_COMMIT="$(tr '\n' '\t' <../MODULE.bazel |
    grep -o -P 'nix_repo\.github\(.*?\)' |
    tr '\t' '\n' |
    grep commit |
    grep -o '".*"' |
    sed 's/"//g')"

podman build \
    -f Containerfile \
    --build-arg "uid=$(id -u)" \
    --build-arg "gid=$(id -g)" \
    --build-arg "nixpkgs_commit=${NIXPKGS_COMMIT}" \
    -t rules-markdown-container-test \
    ../
