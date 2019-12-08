# To use, set BASE to the name of the source markdown file, without
# the extension.
BASE := test1

# Normally these come from environment variables but for testing
# purposes we set them explicitly
MARKDOWN_MAKEFILE=../../makefiles/Makefile.include
MARKDOWN_MAKEFILE_TEMPLATE_LATEX=../../templates/template.tex
MARKDOWN_MAKEFILE_EPUB_CSS=../../templates/epub.css
MARKDOWN_MAKEFILE_METADATA_GENERATOR=../../templates/generate-metadata.sh

# Optional variables you can set:
#
#    STARTS_WITH_TEXT - set this (to anything) if the document begins
#        with text rather than a section header; it will fix a LaTeX
#        formatting problem.
#    ADDITIONAL_DICTIONARIES - by default, spell-checking uses the
#        Hunspell default personal dictionary ~/.hunspell_en_GB, plus
#        $(BASE).dic. Use this variable to specify additional
#        dictionaries.
#    EXTRA_PANDOC_FLAGS - additional flags to pass to pandoc.
#

STARTS_WITH_TEXT := t
ADDITIONAL_DICTIONARIES :=
EXTRA_PANDOC_FLAGS :=


######################################################################
# DO NOT MODIFY THIS SECTION

ifndef MARKDOWN_MAKEFILE
$(error Cannot find the main makefile; is markdown-makefile installed?)
else
include $(MARKDOWN_MAKEFILE)
endif


# These targets are here so tools which don't follow includes
# (e.g. helm-make in Emacs) can still offer sensible options to the
# user. They have no effect on actual functionality.

main:
all:
tex:
pdf:
odt:
doc:
docx:
rtf:
epub:
mobi:
save:
spell:
gitignore:
clean:
