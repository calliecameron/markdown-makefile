"""Python rules."""

load("@rules_python//python:defs.bzl", _py_binary = "py_binary", _py_library = "py_library", _py_test = "py_test")
load("@pip//:requirements.bzl", "requirement")

def py_library(name, **kwargs):
    _py_lint(
        name = name,
        **kwargs
    )
    _py_library(
        name = name,
        **kwargs
    )

def py_binary(name, **kwargs):
    _py_lint(
        name = name,
        **kwargs
    )
    _py_binary(
        name = name,
        **kwargs
    )

def py_test(name, **kwargs):
    _py_lint(
        name = name,
        **kwargs
    )
    _py_test(
        name = name,
        **kwargs
    )

def py_source(name, src, visibility = None):
    if visibility:
        native.exports_files(
            [src],
            visibility = visibility,
        )
    _py_lint(
        name = name,
        srcs = [src],
    )

def _py_lint(name, **kwargs):
    srcs = kwargs.get("srcs", [])
    deps = kwargs.get("deps", [])

    if not srcs:
        return

    _py_test(
        name = name + "_mypy_test",
        srcs = ["//markdown_makefile/python:mypy_test.py"],
        main = "//markdown_makefile/python:mypy_test.py",
        args = [
            "--config-file=$(rootpath //:mypy.ini)",
            "--strict",
            "--explicit-package-bases",
            "--scripts-are-modules",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:mypy.ini",
        ] + srcs + deps,
        deps = [requirement("mypy")] + deps,
    )

    _py_test(
        name = name + "_flake8_test",
        srcs = ["//markdown_makefile/python:flake8_test.py"],
        main = "//markdown_makefile/python:flake8_test.py",
        args = [
            "--config=$(rootpath //:.flake8)",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:.flake8",
        ] + srcs + deps,
        deps = [requirement("flake8")],
    )

    _py_test(
        name = name + "_black_test",
        srcs = ["//markdown_makefile/python:black_test.py"],
        main = "//markdown_makefile/python:black_test.py",
        args = [
            "--config",
            "$(rootpath //:pyproject.toml)",
            "--check",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:pyproject.toml",
        ] + srcs + deps,
        deps = [requirement("black")],
    )
