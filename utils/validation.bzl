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

    py_test(
        name = "flake8_test",
        srcs = ["//utils:flake8_test.py"],
        args = [
            "--config=$(rootpath //:.flake8)",
            "core",
            "formats",
            "utils",
        ],
        data = [
            "//:.flake8",
            "//core:py_srcs",
            "//formats:py_srcs",
            "//utils:py_srcs",
        ],
        deps = [requirement("flake8")],
    )

    py_test(
        name = "autopep8_test",
        srcs = ["//utils:autopep8_test.py"],
        args = [
            "--global-config=$(rootpath //:.flake8)",
            "--recursive",
            "--diff",
            "--exit-code",
            "--aggressive",
            "--aggressive",
            "--aggressive",
            "core",
            "formats",
            "utils",
        ],
        data = [
            "//:.flake8",
            "//core:py_srcs",
            "//formats:py_srcs",
            "//utils:py_srcs",
        ],
        deps = [requirement("autopep8")],
    )

def sh_validation(name = None):  # buildifier: disable=unused-variable
    native.sh_test(
        name = "shellcheck_test",
        srcs = ["//utils:shellcheck_test.sh"],
        args = [
            "$(rootpath @shellcheck//:shellcheck)",
            "core",
            "formats",
            "tests",
            "utils",
        ],
        data = [
            "@shellcheck//:shellcheck",
            "//core:sh_srcs",
            "//formats:sh_srcs",
            "//tests:sh_srcs",
            "//utils:sh_srcs",
        ],
    )
