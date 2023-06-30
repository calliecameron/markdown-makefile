"""Python rules."""

load("@rules_python//python:defs.bzl", _py_binary = "py_binary", _py_library = "py_library", _py_test = "py_test")

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

    native.sh_test(
        name = name + "_mypy_test",
        srcs = ["//markdown_makefile/python:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/python:mypy)",
            "--config-file=$(rootpath //:mypy.ini)",
            "--strict",
            "--explicit-package-bases",
            "--scripts-are-modules",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:mypy.ini",
            "//markdown_makefile/python:mypy",
        ] + srcs + deps,
    )

    native.sh_test(
        name = name + "_pylint_test",
        srcs = ["//markdown_makefile/python:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/python:pylint)",
            "--rcfile=$(rootpath //:pylintrc)",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:pylintrc",
            "//markdown_makefile/python:pylint",
        ] + srcs + deps,
    )

    native.sh_test(
        name = name + "_flake8_test",
        srcs = ["//markdown_makefile/python:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/python:flake8)",
            "--config=$(rootpath //:.flake8)",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:.flake8",
            "//markdown_makefile/python:flake8",
        ] + srcs + deps,
    )

    native.sh_test(
        name = name + "_black_test",
        srcs = ["//markdown_makefile/python:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/python:black)",
            "--config",
            "$(rootpath //:pyproject.toml)",
            "--check",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:pyproject.toml",
            "//markdown_makefile/python:black",
        ] + srcs + deps,
    )
