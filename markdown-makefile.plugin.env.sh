# Set ANTIGEN_THIS_PLUGIN_DIR to this directory, then source this file to set everything up

if [ -z "${ANTIGEN_THIS_PLUGIN_DIR}" ]; then
    echo 'ANTIGEN_THIS_PLUGIN_DIR not set'
else
    export PATH="${ANTIGEN_THIS_PLUGIN_DIR}/bin:${PATH}"
    export MARKDOWN_MAKEFILE="${ANTIGEN_THIS_PLUGIN_DIR}/makefiles/Makefile.include"
    export MARKDOWN_MAKEFILE_TEMPLATE_LATEX="${ANTIGEN_THIS_PLUGIN_DIR}/templates/template.tex"
    export MARKDOWN_MAKEFILE_EPUB_CSS="${ANTIGEN_THIS_PLUGIN_DIR}/templates/epub.css"
    export MARKDOWN_MAKEFILE_METADATA_GENERATOR="${ANTIGEN_THIS_PLUGIN_DIR}/templates/generate-metadata.sh"
fi
