# Set MARKDOWN_MAKEFILE_DIR to this directory, then source this file to set everything up

if [ -z "${MARKDOWN_MAKEFILE_DIR}" ]; then
    echo 'MARKDOWN_MAKEFILE_DIR not set'
else
    export MARKDOWN_MAKEFILE_DIR
    export PATH="${MARKDOWN_MAKEFILE_DIR}/bin:${PATH}"
    export MARKDOWN_MAKEFILE="${MARKDOWN_MAKEFILE_DIR}/makefiles/Makefile.include"
fi
