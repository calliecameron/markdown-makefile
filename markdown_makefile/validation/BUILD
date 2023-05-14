load("validation.bzl", "validation_srcs")

exports_files(
    [
        "mypy_test.py",
        "flake8_test.py",
        "black_test.py",
        "shellcheck_test.sh",
    ],
    visibility = ["//visibility:public"],
)

validation_srcs()
