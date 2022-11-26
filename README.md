# markdown-makefile

Opinionated bazel rules for markdown, using pandoc. Converts markdown to many
output formats.

## Installation

Install dependencies:

```shell
sudo apt-get install FOO
```

Set up your workspace:

```shell
cat > .bazelrc <<EOF
build "--workspace_status_command=/bin/bash -c 'if [ -x ./.bin/workspace_status ]; then ./.bin/workspace_status; fi'"
common --experimental_enable_bzlmod --registry=https://raw.githubusercontent.com/calliecameron/markdown-makefile/master/registry --registry=https://raw.githubusercontent.com/bazelbuild/bazel-central-registry/main
EOF
cat > .bazelversion <<EOF
6.0.0rc2
EOF
touch WORKSPACE
cat > MODULE.bazel <<EOF
module(
    name = "my_module",
    version = "0.0.0",
)

bazel_dep(
    name = "markdown_makefile",
    version = "<VERSION>",
)
EOF
cat > BUILD <<EOF
load("@markdown_makefile//:build_defs.bzl", "md_workspace")

md_workspace()
EOF
bazel run :workspace_update
bazel test :workspace_test
```

If your workspace is also the root of a git repo, add `md_git_repo()` to the
BUILD file, and run `bazel run :git_update`.

## Usage

Example BUILD file:

```build
load("@markdown_makefile//:build_defs.bzl", "md_document")

md_document(
    name = "foo",
)
```

By default this looks for source file `foo.md`. See the loaded bzl file for
docs.

Compile to different formats by running e.g. `bazel build :pdf` or
`bazel build :epub`. View the results with e.g. `bazel run :pdf`.

To initialise a subdirectory with a default BUILD file, run `bazel run //:new`
in that directory.
