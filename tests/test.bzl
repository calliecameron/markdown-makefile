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

def _zip_cleaned_test(target, extension, variant):
    native.sh_test(
        name = "%s_%s_zip_cleaned_test" % (target, ext_var_underscore(extension, variant)),
        srcs = ["//tests:zip_cleaned_test.sh"],
        data = [
            "output/%s.%s" % (target, ext_var_dot(extension, variant)),
        ],
        args = [
            "$(rootpath output/%s.%s)" % (target, ext_var_dot(extension, variant)),
        ],
    )

def _dump_and_diff_tests(target, extension, variant, tool, tool_target = None, tool_helper_targets = None, tool_helper_args = None):
    _dump_test(
        target,
        extension,
        variant,
        tool,
        tool_target,
        tool_helper_targets,
        tool_helper_args,
    )
    _diff_test(
        target,
        extension,
        variant,
        tool,
        tool_target,
        tool_helper_targets,
        tool_helper_args,
    )

def _cat_tests(target, extension, variant):
    _dump_and_diff_tests(
        target,
        extension,
        variant,
        "cat",
    )

def _zip_tests(target, extension, variant):
    _dump_and_diff_tests(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:zipdump)",
        "//markdown/private/utils:zipdump",
        ["//markdown/private/external:unzip"],
        ["$(rootpath //markdown/private/external:unzip)"],
    )
    _zip_cleaned_test(
        target,
        extension,
        variant,
    )

def _pdf_tests(target, extension, variant):
    _dump_and_diff_tests(
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

def _bin_tests(target, extension, variant):
    # Nondeterministic output, so we can't diff
    _dump_test(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:bindump)",
        "//markdown/private/utils:bindump",
        ["//markdown/private/external:hexdump"],
        ["$(rootpath //markdown/private/external:hexdump)"],
    )

def _doc_tests(target, extension, variant):
    # Nondeterministic output, so we can't diff
    _dump_test(
        target,
        extension,
        variant,
        "$(rootpath //markdown/private/utils:docdump)",
        "//markdown/private/utils:docdump",
    )

def output_test(target, name = None):  # buildifier: disable=unused-variable
    """Test the target's outputs.

    Args:
        target: name of the output.
        name: unused.
    """
    _cat_tests(target, "md", None)
    _cat_tests(target, "md", "tumblr")
    _cat_tests(target, "txt", None)
    _cat_tests(target, "html", None)

    _cat_tests(target, "tex", None)
    _pdf_tests(target, "pdf", None)

    _zip_tests(target, "epub", None)
    _bin_tests(target, "mobi", None)

    _zip_tests(target, "odt", None)
    _zip_tests(target, "docx", None)
    _doc_tests(target, "doc", None)

    _zip_tests(target, "docx", "shunnmodern")

    _cat_tests(target, "json", "metadata")
    _cat_tests(target, "json", "deps_metadata")
