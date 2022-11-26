"""Python utils."""

load("@rules_python//python:defs.bzl", "py_test")
load("@pip//:requirements.bzl", "requirement")

def py_validation():
    py_test(
        name = "mypy_test",
        srcs = ["//utils:mypy_test.py"],
        args = [
            "--config-file=$(rootpath //:mypy.ini)",
            "--strict",
            "--explicit-package-bases",
            "--scripts-are-modules",
            "core",
            "formats",
            "utils",
        ],
        data = [
            "//:mypy.ini",
            "//core:py_srcs",
            "//formats:py_srcs",
            "//utils:py_srcs",
        ],
        deps = [requirement("mypy")],
    )
