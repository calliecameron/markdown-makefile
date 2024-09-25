load("@pip//:requirements.bzl", "requirement")
load("//markdown/private/support/python:defs.bzl", "py_binary")
load("//markdown/private/utils:defs.bzl", "script_py_test")

py_binary(
    name = "gen_standard_lint_input",
    srcs = ["gen_standard_lint_input.py"],
    visibility = ["//visibility:public"],
)

script_py_test(
    name = "gen_standard_lint_input_test",
    src = "gen_standard_lint_input_test.py",
    script = ":gen_standard_lint_input",
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

script_py_test(
    name = "custom_lint_test",
    src = "custom_lint_test.py",
    script = ":custom_lint",
    deps = [":custom_lint"],
)
