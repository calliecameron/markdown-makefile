load("@pip_310//:requirements.bzl", "entry_point")
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
    name = "black",
    actual = entry_point("black"),
    visibility = ["//visibility:public"],
)

alias(
    name = "isort",
    actual = entry_point("isort"),
    visibility = ["//visibility:public"],
)

alias(
    name = "flake8",
    actual = entry_point("flake8"),
    visibility = ["//visibility:public"],
)

# Temporarily broken
# alias(
#     name = "pylint",
#     actual = entry_point("pylint"),
#     visibility = ["//visibility:public"],
# )
