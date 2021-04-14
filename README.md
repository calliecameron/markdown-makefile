# markdown-makefile

Pandoc wrapper to convert markdown to other formats with a single `make` command.

    $ ls
    hello.md  Makefile
    $ make pdf
    $ ls
    hello.md  Makefile  output/
    $ ls output
    hello.pdf


## Dependencies

Required:

- Pandoc 2.13
- Python 3

Optional:

- Xelatex for PDF output
- Unoconv for DOC output
- `ebook-convert` from Calibre for MOBI output
- [prosegrinder/pandoc-templates](https://github.com/prosegrinder/pandoc-templates) for DOCX output in [Shunn manuscript format](https://www.shunn.net/format/story/)
- Hunspell for spellchecking
- Git to include commit information in generated files


## Setup

Set `ANTIGEN_THIS_PLUGIN_DIR` to point to this directory, then source `markdown-makefile.env.sh`. Or, install using the antigen-env-2 branch in [my patched version of antigen](https://github.com/calliecameron/antigen).

Run `pip install -r requirements.txt`.

Run `markdown-makefile` to copy a new makefile into the current directory.


## Testing

To ensure it works on your system (i.e. not affected by quirks in the Pandoc or LaTeX installation), run `make all` in each of the tests, and compare the files in `output` to those in `saved`.
