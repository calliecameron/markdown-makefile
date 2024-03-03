#!/bin/bash

set -eu

function usage() {
    cat <<EOF
Usage: $(basename "${0}") updater file_specs...

Valid file_specs:
    --check src dst_abs_path dst_mode
        check that the contents of dst match src and dst's mode is correct
    --check_mode_only dst_abs_path dst_mode
        check that dst's mode is correct
    --missing_file dst_package_rel_path
        report dst as missing
    --extra_check script_abs_path
        run script and check it succeeded
EOF
    exit 1
}

test -z "${1:-}" && usage
UPDATER="${1}"
shift

if [ -z "${1:-}" ]; then
    echo 'No files specified'
    exit 1
fi

DIFF=''

function check() {
    local MODE
    MODE="$(stat -L -c '%a' "${2}")"
    echo "Diffing $(basename "${2}")"
    if ! diff "${1}" "${2}"; then
        DIFF='t'
    elif [ "${MODE}" != "${3}" ]; then
        echo "Modes differ: want ${3}, got ${MODE}"
        DIFF='t'
    else
        echo 'OK'
    fi
    echo
}

function check_mode_only() {
    local MODE
    MODE="$(stat -L -c '%a' "${1}")"
    echo "Diffing $(basename "${1}")"
    if [ "${MODE}" != "${2}" ]; then
        echo "Modes differ: want ${2}, got ${MODE}"
        DIFF='t'
    else
        echo 'OK'
    fi
    echo
}

function missing_file() {
    echo "File ${1} is missing"
    DIFF='t'
    echo
}

function extra_check() {
    echo "Running ${1}"
    if ! "${SCRIPT}"; then
        echo 'Failed'
        DIFF='t'
    else
        echo 'OK'
    fi
    echo
}

while [[ "${#}" -gt 0 ]]; do
    case "${1}" in
    --check)
        test -z "${2:-}" && usage
        test -e "${2}" || usage
        SRC="${2}"
        test -z "${3:-}" && usage
        test -e "${3}" || usage
        DST="${3}"
        test -z "${4:-}" && usage
        DST_MODE="${4}"

        check "${SRC}" "${DST}" "${DST_MODE}"
        shift 4
        ;;
    --check_mode_only)
        test -z "${2:-}" && usage
        test -e "${2}" || usage
        DST="${2}"
        test -z "${3:-}" && usage
        DST_MODE="${3}"

        check_mode_only "${DST}" "${DST_MODE}"
        shift 3
        ;;
    --missing_file)
        test -z "${2:-}" && usage
        DST="${2}"

        missing_file "${DST}"
        shift 2
        ;;
    --extra_check)
        test -z "${2:-}" && usage
        test -x "${2}" || usage
        SCRIPT="${2}"

        extra_check "${SCRIPT}"
        shift 2
        ;;
    *)
        echo "Unknown arg: ${1}"
        usage
        ;;
    esac
done

if [ -n "${DIFF}" ]; then
    echo "Found diff; 'bazel run ${UPDATER}' to fix"
    exit 1
fi

echo 'All OK'
exit 0
