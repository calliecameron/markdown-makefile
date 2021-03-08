# Set ANTIGEN_THIS_PLUGIN_DIR to this directory, then source this file to set everything up

if [ -z "${ANTIGEN_THIS_PLUGIN_DIR}" ]; then
    echo 'ANTIGEN_THIS_PLUGIN_DIR not set'
else
    export MARKDOWN_MAKEFILE_DIR="${ANTIGEN_THIS_PLUGIN_DIR}"
    export PATH="${MARKDOWN_MAKEFILE_DIR}/bin:${PATH}"
    export MARKDOWN_MAKEFILE="${MARKDOWN_MAKEFILE_DIR}/makefiles/Makefile.include"
fi
