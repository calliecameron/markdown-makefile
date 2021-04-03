#!/bin/bash

function usage() {
    echo "Usage: $(basename "${0}") out_file in_file"
    exit 1
}

function get-var() {
    local VAR="${1}"
    local FILE="${2}"
    local TMPFILE
    TMPFILE="$(mktemp).md"
    echo "\$${VAR}\$" > "${TMPFILE}"
    pandoc "--template=${TMPFILE}" --to=markdown "${FILE}"
    rm "${TMPFILE}"
}

test -z "${1}" && usage
test -z "${2}" && usage
OUTFILE="${1}"
INFILE="${2}"

TITLE="$(get-var title "${INFILE}")"
AUTHOR="$(get-var author "${INFILE}")"
AUTHOR_LASTNAME="$(python3 -c "print('${AUTHOR}'.split()[-1])")"

TMPFILE="$(mktemp)"
cat > "${TMPFILE}" <<EOF
---
short_title: "${TITLE}"
author_lastname: "${AUTHOR_LASTNAME}"
contact_name: "${AUTHOR}"
contact_address: \n
contact_city_state_zip: \n
contact_phone: \n
contact_email: \n
---
EOF

# Since make uses timestamps, not contents, to determine whether to rebuild, we
# only update the output file if it would differ.
if ! cmp "${TMPFILE}" "${OUTFILE}" &>/dev/null; then
    cp "${TMPFILE}" "${OUTFILE}"
fi

rm "${TMPFILE}"
