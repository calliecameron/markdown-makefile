load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")

py_binary(
    name = "gen_lint_input",
    srcs = ["gen_lint_input.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "gen_lint_input_test",
    srcs = ["gen_lint_input_test.py"],
    args = ["$(rootpath :gen_lint_input)"],
    data = [":gen_lint_input"],
    deps = ["//markdown/utils:test_utils"],
)

py_binary(
    name = "lint",
    srcs = ["lint.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("pymarkdownlnt")],
)
