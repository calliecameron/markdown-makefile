# rules_markdown

Bazel rules for markdown.

```starlark
# If you just want to validate a markdown file (spellchecking, lint, etc.), use
# md_file. Also creates a validation test target.
md_file(
    name = "foo",  # Uses foo.md by default
)

# For all of the above, plus conversion to output formats (pdf, docx, epub,
# etc.), use md_document.
md_document(
    name = "bar",  # Uses bar.md by default
)
```

```shell
# Validate foo.md
$ bazel test :foo_test
# Validate bar.md and generate a pdf
$ bazel build :bar_pdf
```

The rules connect many existing tools: pandoc, calibre, unoconv, hunspell...

See below for detailed usage.

## Limitations

Current limitations, to be addressed later:

* Customisation options are limited. Language, lint config, templates etc. can't
  be customised. The current settings are aimed at my own usecase as a British-
  English-speaking creative writer.
* Not all dependencies are hermetic. Developed on Ubuntu 22.04; output may
  differ on other systems.
* Some dependencies that are hermetic, are specific to linux amd64, and won't
  work on other systems. Ideally we'd use something like rules_nixpkgs to make
  all dependencies hermetic and platform-independent, but it doesn't support
  bzlmod yet.
* Linting currently uses pymarkdownlint instead of the more standard
  markdownlint-cli, because markdownlint-cli doesn't work under bzlmod.

## Installation

## Usage

`md_file` represents a markdown file and its dependencies. The target will only build if the file is valid -- no [spelling mistakes], no [linter warnings], [inclusion] used correctly, etc. `md_file` also creates a test that checks the file is valid:

By default, `src` is based on `name`, and can be omitted:

Each markdown file has its own `md_file`:

Files can have the standard pandoc metadata: title, author, date, as well as [custom metadata]. Metadata must be in a yaml front matter block, not pandoc style metadata.

If validation is all you need, and never want to render the file in an output format (e.g. a readme in a git repo), then using `md_file` directly is enough. To convert to output formats, use `md_document`:

`md_document` by default creates an `md_file` behind the scenes. You can pass `md_file` arguments to `md_document`:

Or pass it an existing `md_file` instead:

`md_document` creates targets for each output format:

You can also run these targets, to open the generated file in the default program for its filetype:

If your package is at the root of a git repo:

If your package is at the root of the workspace:

## Validation

By design, a file with spelling mistakes or lint warnings won't build. Just like
a program with detectable errors shouldn't compile, neither should a document.

### Spellchecking

Spellchecking uses the hunspell dictionary for the configured language. You can
also add custom dictionaries. All words in the custom dictionary are considered
correct.

### Lint

### Inclusion

### Collections

### Custom metadata

## Output formats

## Why

I'm a writer as well as a programmer, and I want to use the same tools
(markdown, git) when writing as when coding. This project started off as a
simple makefile wrapping pandoc, and gradually grew as my needs changed. The
makefile version was messy, slow and hard to maintain, and, since I use bazel at work,
rewriting in bazel was the obvious solution.
