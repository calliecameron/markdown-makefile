load("//markdown/private/support/python:defs.bzl", "py_binary")
load("//markdown/private/support/shell:defs.bzl", "sh_binary")
load("//markdown/private/utils:defs.bzl", "script_py_test")

exports_files(
    [
        "default_markdownlintrc",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "standard_lint",
    srcs = ["standard_lint.sh"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "custom_lint",
    srcs = ["custom_lint.py"],
    visibility = ["//visibility:public"],
)

script_py_test(
    name = "custom_lint_test",
    src = "custom_lint_test.py",
    script = ":custom_lint",
    deps = [":custom_lint"],
)
