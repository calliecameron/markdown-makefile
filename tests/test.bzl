"""Test utils."""

load("@bazel_skylib//rules:build_test.bzl", "build_test")
load(
    "//markdown/private/formats:defs.bzl",
    "ext_var_dot",
    "ext_var_underscore",
)

def _build_test(target, extension, variant):
    build_test(
        name = "%s_%s_build_test" % (target, ext_var_underscore(extension, variant)),
        targets = [
            "output/%s.%s" % (target, ext_var_dot(extension, variant)),
        ],
    )

def _diff_test(target, extension, variant, tool, tool_target = None, tool_helper_targets = None, tool_helper_args = None):
    native.sh_test(
        name = "%s_%s_diff_test" % (target, ext_var_underscore(extension, variant)),
        srcs = ["//tests:diff_test.sh"],
        data = [
                   "output/%s.%s" % (target, ext_var_dot(extension, variant)),
                   "saved/%s.%s" % (target, ext_var_dot(extension, variant)),
               ] + ([tool_target] if tool_target else []) +
               (tool_helper_targets if tool_helper_targets else []),
        args = [
            "$(rootpath output/%s.%s)" % (target, ext_var_dot(extension, variant)),
            "$(rootpath saved/%s.%s)" % (target, ext_var_dot(extension, variant)),
            tool,
        ] + (tool_helper_args if tool_helper_args else []),
    )

def _cat_diff_test(target, extension, variant):
    _diff_test(target, extension, variant, "cat")

def _zip_diff_test(target, extension, variant):
    _diff_test(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:zipdump)",
        "//markdown/private/utils:zipdump",
        ["//markdown/private/external:unzip"],
        ["$(rootpath //markdown/private/external:unzip)"],
    )

def _pdf_diff_test(target, extension, variant):
    _diff_test(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:pdfdump)",
        "//markdown/private/utils:pdfdump",
        [
            "//markdown/private/external:pdfinfo",
            "//markdown/private/utils:pdf2txt",
        ],
        [
            "$(rootpath //markdown/private/external:pdfinfo)",
            "$(rootpath //markdown/private/utils:pdf2txt)",
        ],
    )

def diff_test(target, name = None):  # buildifier: disable=unused-variable
    """Diff tests for target's output.

    Args:
        target: name of the output.
        name: unused.
    """
    _cat_diff_test(target, "md", None)
    _cat_diff_test(target, "md", "tumblr")
    _cat_diff_test(target, "txt", None)
    _cat_diff_test(target, "html", None)

    _cat_diff_test(target, "tex", None)
    _pdf_diff_test(target, "pdf", None)

    _zip_diff_test(target, "epub", None)
    _build_test(target, "mobi", None)  # Mobi is nondeterministic, so we only test it builds

    _zip_diff_test(target, "odt", None)
    _zip_diff_test(target, "docx", None)
    _build_test(target, "doc", None)  # Doc is nondeterministic, so we only test it builds

    _zip_diff_test(target, "docx", "shunnmodern")

    _cat_diff_test(target, "json", "metadata")
    _cat_diff_test(target, "json", "deps_metadata")
