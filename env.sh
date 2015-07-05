# Source this file to set everything up

if [ -z "${MARKDOWN_MAKEFILE_ROOT}" ]; then
    echo 'MARKDOWN_MAKEFILE_ROOT not set'
else
    export PATH="${PATH}:${MARKDOWN_MAKEFILE_ROOT}/bin"
    export MARKDOWN_MAKEFILE="${MARKDOWN_MAKEFILE_ROOT}/makefiles/Makefile.include"
    export MARKDOWN_MAKEFILE_TEMPLATE_LATEX="${MARKDOWN_MAKEFILE_ROOT}/templates/template.tex"
fi
