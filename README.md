markdown-makefile
=================

A wrapper for Pandoc and other tools so you can convert markdown files to other formats with a single `make` command.

    $ ls
    hello.md  Makefile
    $ make pdf
    $ ls
    hello.md  Makefile  output/
    $ ls output
    hello.pdf


Dependencies
------------

- Pandoc
- a LaTeX engine, e.g. pdflatex
- LibreOffice
- unoconv
- Calibre


Setup
-----

Set `MARKDOWN_MAKEFILE_ROOT` to point to this directory, then source `env.sh`.

Run `markdown-makefile` to copy a new makefile into the current directory.
