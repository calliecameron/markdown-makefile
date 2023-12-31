load(":shell.bzl", "sh_source")

sh_source(
    name = "shellcheck_test",
    src = "shellcheck_test.sh",
    visibility = ["//visibility:public"],
)

alias(
    name = "shfmt",
    actual = "@shfmt_linux_x86_64//file:shfmt",
    visibility = ["//visibility:public"],
)
