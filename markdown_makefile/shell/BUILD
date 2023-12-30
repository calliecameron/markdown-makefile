load("@aspect_rules_lint//lint:shellcheck.bzl", "shellcheck_binary")
load(":shell.bzl", "sh_source")

sh_source(
    name = "shellcheck_test",
    src = "shellcheck_test.sh",
    visibility = ["//visibility:public"],
)

shellcheck_binary(
    name = "shellcheck",
)

alias(
    name = "shfmt",
    actual = "@shfmt_linux_x86_64//file:shfmt",
    visibility = ["//visibility:public"],
)
