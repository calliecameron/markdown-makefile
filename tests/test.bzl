"""Test utils."""

load(
    "//markdown/private/formats:defs.bzl",
    "ext_var_dot",
    "ext_var_underscore",
)

def _dump_test(target, extension, variant, tool, tool_target = None, tool_helper_targets = None, tool_helper_args = None):
    native.sh_test(
        name = "%s_%s_dump_test" % (target, ext_var_underscore(extension, variant)),
        srcs = ["//tests:dump_test.sh"],
        data = [
                   "output/%s.%s" % (target, ext_var_dot(extension, variant)),
               ] + ([tool_target] if tool_target else []) +
               (tool_helper_targets if tool_helper_targets else []),
        args = [
            "$(rootpath output/%s.%s)" % (target, ext_var_dot(extension, variant)),
            tool,
        ] + (tool_helper_args if tool_helper_args else []),
    )

def _diff_test(target, extension, variant, tool, tool_target = None, tool_helper_targets = None, tool_helper_args = None):
    _dump_test(
        target,
        extension,
        variant,
        tool,
        tool_target,
        tool_helper_targets,
        tool_helper_args,
    )

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

def _bin_dump_test(target, extension, variant):
    _dump_test(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:bindump)",
        "//markdown/private/utils:bindump",
        ["//markdown/private/external:hexdump"],
        ["$(rootpath //markdown/private/external:hexdump)"],
    )

def _doc_dump_test(target, extension, variant):
    _dump_test(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:docdump)",
        "//markdown/private/utils:docdump",
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
    _bin_dump_test(target, "mobi", None)  # Mobi is nondeterministic, so we can't test the diff

    _zip_diff_test(target, "odt", None)
    _zip_diff_test(target, "docx", None)
    _doc_dump_test(target, "doc", None)  # Doc is nondeterministic, so we can't test the diff

    _zip_diff_test(target, "docx", "shunnmodern")

    _cat_diff_test(target, "json", "metadata")
    _cat_diff_test(target, "json", "deps_metadata")
