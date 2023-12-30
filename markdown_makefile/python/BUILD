load("@python_versions//3.10:defs.bzl", "py_console_script_binary")
load("//markdown_makefile/python:python.bzl", "py_source")
load("//markdown_makefile/shell:shell.bzl", "sh_source")

sh_source(
    name = "stub",
    src = "stub.sh",
    visibility = ["//visibility:public"],
)

py_source(
    name = "mypy_stub",
    src = "mypy_stub.py",
    visibility = ["//visibility:public"],
)

py_console_script_binary(
    name = "black",
    pkg = "@pip//black:pkg",
    visibility = ["//visibility:public"],
)

py_console_script_binary(
    name = "isort",
    pkg = "@pip//isort:pkg",
    visibility = ["//visibility:public"],
)

py_console_script_binary(
    name = "flake8",
    pkg = "@pip//flake8:pkg",
    visibility = ["//visibility:public"],
)

# Temporarily broken
# alias(
#     name = "pylint",
#     actual = entry_point("pylint"),
#     visibility = ["//visibility:public"],
# )
