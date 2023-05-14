"""Python utils."""

load("@rules_python//python:defs.bzl", "py_test")
load("@pip//:requirements.bzl", "requirement")
load("@buildifier_prebuilt//:rules.bzl", "buildifier_test")

def validation_srcs(name = None, extra_sh_files = None, extra_py_files = None):  # buildifier: disable=unused-variable
    extra_sh_files = extra_sh_files or []
    extra_py_files = extra_py_files or []

    native.filegroup(
        name = "sh_srcs",
        srcs = native.glob(["*.sh"]) + extra_sh_files,
        data = native.glob(["*.sh"]) + extra_sh_files,
        visibility = ["//:__pkg__"],
    )

    native.filegroup(
        name = "py_srcs",
        srcs = native.glob(["*.py"]) + extra_py_files,
        data = native.glob(["*.py"]) + extra_py_files,
        visibility = ["//:__pkg__"],
    )

def validation(name = None):  # buildifier: disable=unused-variable
    _py_validation()
    _sh_validation()
    _bzl_validation()

def _py_validation():
    py_test(
        name = "mypy_test",
        srcs = ["//markdown_makefile/utils:mypy_test.py"],
        args = [
            "--config-file=$(rootpath //:mypy.ini)",
            "--strict",
            "--explicit-package-bases",
            "--scripts-are-modules",
            "$(locations //markdown_makefile/core:py_srcs)",
            "$(locations //markdown_makefile/formats:py_srcs)",
            "$(locations //markdown_makefile/utils:py_srcs)",
            "$(locations //markdown_makefile/workspace:py_srcs)",
        ],
        data = [
            "//:mypy.ini",
            "//markdown_makefile/core:py_srcs",
            "//markdown_makefile/formats:py_srcs",
            "//markdown_makefile/utils:py_srcs",
            "//markdown_makefile/workspace:py_srcs",
        ],
        deps = [requirement("mypy")],
    )

    py_test(
        name = "flake8_test",
        srcs = ["//markdown_makefile/utils:flake8_test.py"],
        args = [
            "--config=$(rootpath //:.flake8)",
            "$(locations //markdown_makefile/core:py_srcs)",
            "$(locations //markdown_makefile/formats:py_srcs)",
            "$(locations //markdown_makefile/utils:py_srcs)",
            "$(locations //markdown_makefile/workspace:py_srcs)",
        ],
        data = [
            "//:.flake8",
            "//markdown_makefile/core:py_srcs",
            "//markdown_makefile/formats:py_srcs",
            "//markdown_makefile/utils:py_srcs",
            "//markdown_makefile/workspace:py_srcs",
        ],
        deps = [requirement("flake8")],
    )

    py_test(
        name = "black_test",
        srcs = ["//markdown_makefile/utils:black_test.py"],
        args = [
            "--config",
            "$(rootpath //:pyproject.toml)",
            "--check",
            "$(locations //markdown_makefile/core:py_srcs)",
            "$(locations //markdown_makefile/formats:py_srcs)",
            "$(locations //markdown_makefile/utils:py_srcs)",
            "$(locations //markdown_makefile/workspace:py_srcs)",
        ],
        data = [
            "//:pyproject.toml",
            "//markdown_makefile/core:py_srcs",
            "//markdown_makefile/formats:py_srcs",
            "//markdown_makefile/utils:py_srcs",
            "//markdown_makefile/workspace:py_srcs",
        ],
        deps = [requirement("black")],
    )

def _sh_validation(name = None):  # buildifier: disable=unused-variable
    native.sh_test(
        name = "shellcheck_test",
        srcs = ["//markdown_makefile/utils:shellcheck_test.sh"],
        args = [
            "$(rootpath @shellcheck//:shellcheck)",
            "markdown_makefile/core",
            "markdown_makefile/formats",
            "markdown_makefile/git",
            "markdown_makefile/utils",
            "markdown_makefile/workspace",
            "tests",
        ],
        data = [
            "@shellcheck//:shellcheck",
            "//markdown_makefile/core:sh_srcs",
            "//markdown_makefile/formats:sh_srcs",
            "//markdown_makefile/git:sh_srcs",
            "//markdown_makefile/utils:sh_srcs",
            "//markdown_makefile/workspace:sh_srcs",
            "//tests:sh_srcs",
        ],
    )

def _bzl_validation():
    buildifier_test(
        name = "buildifier_test",
        no_sandbox = True,
        workspace = "//:WORKSPACE",
    )
