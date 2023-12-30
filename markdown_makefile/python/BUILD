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

alias(
    name = "ruff",
    actual = "@ruff_x86_64-unknown-linux-gnu//:ruff",
    visibility = ["//visibility:public"],
)
