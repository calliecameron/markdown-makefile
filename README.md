# rules_markdown

Opinionated bazel rules for markdown. Uses pandoc and other tools to convert
markdown to many output formats. Formatting is intended for short stories and
poems.

Supported output formats: markdown, plain text, html, latex, pdf, epub, mobi,
odt, docx, doc, and docx in [Shunn manuscript
format](https://github.com/prosegrinder/pandoc-templates).

## Setup

Install system dependencies (assuming Ubuntu 20.04):

``` shell
sudo apt-get install -y catdoc git gcc hunspell hunspell-en-gb libegl1 \
    libopengl0 libxkbcommon0 python3-pip \
    strip-nondeterminism texlive-xetex unoconv
```

Set up the files in your workspace:

`.bazelrc`:

``` text
common --experimental_isolated_extension_usages
build "--workspace_status_command=/bin/bash -c 'if [ -x ./.markdown_workspace/workspace_status ] && [ -x ./.markdown_workspace/git_repo_version ]; then ./.markdown_workspace/workspace_status ./.markdown_workspace/git_repo_version; fi'"
build --nobuild_runfile_links --sandbox_default_allow_network=false
test --nobuild_runfile_links --build_tests_only
```

`.bazeliskrc`:

``` text
USE_BAZEL_VERSION=7.3.1
```

`WORKSPACE`:

``` text
# Empty file
```

`MODULE.bazel`:

``` text
module(
    name = "my_module",
    version = "0.0.0",
)

bazel_dep(
    name = "rules_markdown",
    # Set this to the latest tag on github
    version = ...,
)

archive_override(
    module_name = "rules_markdown",
    # Set these from the latest tag on github
    urls = ...
    integrity = ...
    strip_prefix = ...
)
```

`BUILD`:

``` text
load("@rules_markdown//markdown:defs.bzl", "md_workspace")

md_workspace()
```

If your workspace is also the root of a git repo, add `md_git_repo()` to the
BUILD file.

Initialise:

``` shell
bazel run :workspace_update
bazel test :workspace_test
```

If you added `md_git_repo` to the BUILD file in the previous step, also run:

``` shell
bazel run :git_update
bazel test :git_test
```

## Usage

Example BUILD file:

``` text
load("@rules_markdown//markdown:defs.bzl", "md_document")

md_document(
    name = "foo",
)
```

By default this looks for source file `foo.md`, and dictionary `foo.dic` for
spellchecking, if it exists. See the loaded bzl file for docs.

Compile to different formats by running e.g. `bazel build :pdf` or
`bazel build :epub`. View the results with e.g. `bazel run :pdf`.

To initialise a subdirectory with a default BUILD file, run `bazel run //:new`
in that directory.

## Includes

Include a file with:

``` markdown
!include $LABEL
```

in markdown, where ‘$LABEL’ is the label of an md_file or md_document target in
this target’s ‘deps’.
