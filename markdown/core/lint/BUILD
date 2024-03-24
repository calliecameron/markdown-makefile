load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")

py_binary(
    name = "gen_standard_lint_input",
    srcs = ["gen_standard_lint_input.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "gen_standard_lint_input_test",
    srcs = ["gen_standard_lint_input_test.py"],
    args = ["$(rootpath :gen_standard_lint_input)"],
    data = [":gen_standard_lint_input"],
    deps = ["//markdown/utils:test_utils"],
)

py_binary(
    name = "standard_lint",
    srcs = ["standard_lint.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("pymarkdownlnt")],
)

py_binary(
    name = "custom_lint",
    srcs = ["custom_lint.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "custom_lint_test",
    srcs = ["custom_lint_test.py"],
    args = ["$(rootpath :custom_lint)"],
    deps = [
        ":custom_lint",
        "//markdown/utils:test_utils",
    ],
)
