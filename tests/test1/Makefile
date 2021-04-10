# To use, set BASE to the name of the source markdown file, without
# the extension.
BASE := test1

# Normally these come from environment variables but for testing
# purposes we set them explicitly
MARKDOWN_MAKEFILE_DIR=../..
MARKDOWN_MAKEFILE=../../makefiles/Makefile.include

# There are several variables you can set here to customise behaviour.
# See the included makefile for details.

STARTS_WITH_TEXT := t


######################################################################
# DO NOT MODIFY THIS SECTION

ifndef MARKDOWN_MAKEFILE
$(error Cannot find the main makefile; is markdown-makefile installed?)
else
include $(MARKDOWN_MAKEFILE)
endif
