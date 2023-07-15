load("//markdown_makefile/shell:shell.bzl", "sh_source")
load("@pip//:requirements.bzl", "entry_point")

sh_source(
    name = "stub",
    src = "stub.sh",
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

alias(
    name = "mypy",
    actual = entry_point("mypy"),
    visibility = ["//visibility:public"],
)

alias(
    name = "pylint",
    actual = entry_point("pylint"),
    visibility = ["//visibility:public"],
)
