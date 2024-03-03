#!/bin/bash

set -eu

function usage() {
    cat <<EOF
Usage: $(basename "${0}") package file_specs...

Valid file_specs:
    --copy src dst_package_rel_path dst_mode
        make dst have the same contents as src and the specified mode
    --create src dst_package_rel_path dst_mode
        if dst doesn't exist, same as copy; otherwise only set dst's mode
    --extra_script script_abs_path
        run script and check it succeeded
EOF
    exit 1
}

PACKAGE="${1:-}" # Package will be empty in the root package.
shift

if [ -n "${PACKAGE}" ]; then
    DST_DIR="${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}"
else
    DST_DIR="${BUILD_WORKSPACE_DIRECTORY}"
fi

if [ -z "${1:-}" ]; then
    echo 'No files specified'
    exit 1
fi

while [[ "${#}" -gt 0 ]]; do
    case "${1}" in
    --copy)
        test -z "${2:-}" && usage
        test -e "${2}" || usage
        SRC="${2}"
        test -z "${3:-}" && usage
        DST="${DST_DIR}/${3}"
        test -z "${4:-}" && usage
        DST_MODE="${4}"

        mkdir -p "$(dirname "${DST}")"
        cp "${SRC}" "${DST}"
        chmod "${DST_MODE}" "${DST}"
        shift 4
        ;;
    --create)
        test -z "${2:-}" && usage
        test -e "${2}" || usage
        SRC="${2}"
        test -z "${3:-}" && usage
        DST="${DST_DIR}/${3}"
        test -z "${4:-}" && usage
        DST_MODE="${4}"

        if [ ! -e "${DST}" ]; then
            mkdir -p "$(dirname "${DST}")"
            cp "${SRC}" "${DST}"
        fi
        chmod "${DST_MODE}" "${DST}"
        shift 4
        ;;
    --extra_script)
        test -z "${2:-}" && usage
        test -x "${2}" || usage
        SCRIPT="${2}"

        DST_DIR="${DST_DIR}" "${SCRIPT}"
        shift 2
        ;;
    *)
        echo "Unknown arg: ${1}"
        usage
        ;;
    esac
done
