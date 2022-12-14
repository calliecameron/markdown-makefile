# markdown-makefile

Opinionated bazel rules for markdown. Uses pandoc and other tools to convert
markdown to many output formats. Formatting is intended for short stories and
poems.

Supported output formats: markdown, plain text, html, latex, pdf, epub, mobi,
odt, docx, doc, and docx in
[Shunn manuscript format](https://github.com/prosegrinder/pandoc-templates).

## Setup

1. Install system dependencies (assuming Ubuntu 20.04):

    ```shell
    sudo apt-get install -y catdoc csvkit git gcc hunspell hunspell-en-gb \
        libegl1 libopengl0 libxkbcommon0 poppler-utils python3-pip \
        strip-nondeterminism texlive-xetex unoconv
    ```

2. Install python dependencies:

    ```shell
    pip install pdfminer
    ```

    and make sure the folder containing pdf2txt.py is on the PATH (usually
    ~/.local/bin).

3. Set up the files in your workspace:

    `.bazelrc`:

    ```text
    build "--workspace_status_command=/bin/bash -c 'if [ -x ./.bin/workspace_status ]; then ./.bin/workspace_status; fi'"
    common --experimental_enable_bzlmod --registry=https://raw.githubusercontent.com/calliecameron/markdown-makefile/master/registry --registry=https://raw.githubusercontent.com/bazelbuild/bazel-central-registry/main
    ```

    `.bazelversion`:

    ```text
    6.0.0rc5
    ```

    `WORKSPACE`:

    ```text
    # Empty file
    ```

    `MODULE.bazel`:

    ```text
    module(
        name = "my_module",
        version = "0.0.0",
    )

    bazel_dep(
        name = "markdown_makefile",
        version = "<VERSION>",
    )
    ```

    `BUILD`:

    ```text
    load("@markdown_makefile//:build_defs.bzl", "md_workspace")

    md_workspace()
    ```

    If your workspace is also the root of a git repo, add `md_git_repo()` to the
    BUILD file.

4. Initialise:

    ```shell
    bazel run :workspace_update
    bazel test :workspace_test
    ```

    If you added `md_git_repo` to the BUILD file in the previous step, also run:

    ```shell
    bazel run :git_update
    bazel run :git_test
    ```

## Usage

Example BUILD file:

```build
load("@markdown_makefile//:build_defs.bzl", "md_document")

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

```markdown
!include $LABEL
```

in markdown, where '$LABEL' is the label of an md_library or md_document target
in this target's 'deps'.
