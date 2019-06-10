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

Currently supports Pandoc 1.19.2.4 (the version in Ubuntu 18.04); may not work with other versions, run the tests to check.

Dependencies
------------

- Pandoc
- a LaTeX engine, e.g. xelatex
- LibreOffice
- Unoconv
- Calibre
- Hunspell


Setup
-----

Set `ANTIGEN_THIS_PLUGIN_DIR` to point to this directory, then source `markdown-makefile.env.sh`. Or, install using the antigen-env-2 branch in [my patched version of antigen](https://github.com/callumcameron/antigen).

Run `markdown-makefile` to copy a new makefile into the current directory.
