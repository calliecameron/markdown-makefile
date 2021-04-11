# To use, set BASE to the name of the source markdown file, without
# the extension.
BASE := test3

# Normally these come from environment variables but for testing
# purposes we set them explicitly
MARKDOWN_MAKEFILE_DIR=../..
MARKDOWN_MAKEFILE=../../makefiles/Makefile.include

# There are several variables you can set here to customise behaviour.
# See the included makefile for details.

EXTRA_PANDOC_FLAGS := --table-of-contents --toc-depth=1
EXTRA_LATEX_FLAGS := --include-in-header=custom-toc.tex
EXTRA_DEPS := custom-toc.tex include1.md include2.md


######################################################################
# DO NOT MODIFY THIS SECTION

ifndef MARKDOWN_MAKEFILE
$(error Cannot find the main makefile; is markdown-makefile installed?)
else
include $(MARKDOWN_MAKEFILE)
endif
