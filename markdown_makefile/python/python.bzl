"""Python rules."""

load("@pip//:requirements.bzl", "requirement")
load("@python_versions//3.10:defs.bzl", _py_binary = "py_binary", _py_test = "py_test")
load("@rules_python//python:defs.bzl", _py_library = "py_library")

def py_library(name, type_stub_deps = None, **kwargs):
    _py_lint(
        name = name,
        type_stub_deps = type_stub_deps,
        **kwargs
    )
    _py_library(
        name = name,
        **kwargs
    )

def py_binary(name, type_stub_deps = None, **kwargs):
    _py_lint(
        name = name,
        type_stub_deps = type_stub_deps,
        **kwargs
    )
    _py_binary(
        name = name,
        **kwargs
    )

def py_test(name, type_stub_deps = None, **kwargs):
    _py_lint(
        name = name,
        type_stub_deps = type_stub_deps,
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

def _py_lint(name, type_stub_deps = None, **kwargs):
    srcs = kwargs.get("srcs", [])
    deps = kwargs.get("deps", [])
    type_stub_deps = type_stub_deps or []

    if not srcs:
        return

    _py_test(
        name = name + "_mypy_test",
        srcs = ["//markdown_makefile/python:mypy_stub.py"],
        main = "//markdown_makefile/python:mypy_stub.py",
        deps = deps + type_stub_deps + [requirement("mypy")],
        args = [
            "--config-file=$(rootpath //:pyproject.toml)",
            "--strict",
            "--explicit-package-bases",
            "--scripts-are-modules",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:pyproject.toml",
        ] + srcs,
    )

    native.sh_test(
        name = name + "_ruff_lint_test",
        srcs = ["//markdown_makefile/utils:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/python:ruff)",
            "check",
            "--config=$(rootpath //:pyproject.toml)",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:pyproject.toml",
            "//markdown_makefile/python:ruff",
        ] + srcs + deps,
    )

    native.sh_test(
        name = name + "_ruff_format_test",
        srcs = ["//markdown_makefile/utils:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/python:ruff)",
            "format",
            "--config=$(rootpath //:pyproject.toml)",
            "--diff",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//:pyproject.toml",
            "//markdown_makefile/python:ruff",
        ] + srcs + deps,
    )
