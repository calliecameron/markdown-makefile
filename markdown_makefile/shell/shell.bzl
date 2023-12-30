"""Shell rules."""

def sh_library(name, **kwargs):
    _sh_lint(
        name = name,
        **kwargs
    )
    native.sh_library(
        name = name,
        **kwargs
    )

def sh_binary(name, **kwargs):
    _sh_lint(
        name = name,
        **kwargs
    )
    native.sh_binary(
        name = name,
        **kwargs
    )

def sh_test(name, **kwargs):
    _sh_lint(
        name = name,
        **kwargs
    )
    native.sh_test(
        name = name,
        **kwargs
    )

def sh_source(name, src, visibility = None):
    if visibility:
        native.exports_files(
            [src],
            visibility = visibility,
        )
    _sh_lint(
        name = name,
        srcs = [src],
    )

def _sh_lint(name, **kwargs):
    srcs = kwargs.get("srcs", [])

    if not srcs:
        return

    native.sh_test(
        name = name + "_shellcheck_test",
        srcs = ["//markdown_makefile/shell:shellcheck_test.sh"],
        args = [
            "$(rootpath //markdown_makefile/shell:shellcheck)",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//markdown_makefile/shell:shellcheck",
        ] + srcs,
    )

    native.sh_test(
        name = name + "_shfmt_test",
        srcs = ["//markdown_makefile/utils:stub.sh"],
        args = [
            "$(rootpath //markdown_makefile/shell:shfmt)",
            "-l",
            "-d",
            "-i",
            "4",
        ] + ["$(location %s)" % src for src in srcs],
        data = [
            "//markdown_makefile/shell:shfmt",
        ] + srcs,
    )
