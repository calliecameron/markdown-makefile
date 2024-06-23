"""Test utils."""

load("@bazel_skylib//rules:build_test.bzl", "build_test")
load(
    "//markdown/formats:defs.bzl",
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

def _diff_test(target, extension, variant, tool, tool_target = None):
    native.sh_test(
        name = "%s_%s_diff_test" % (target, ext_var_underscore(extension, variant)),
        srcs = ["//tests:diff_test.sh"],
        data = [
            "output/%s.%s" % (target, ext_var_dot(extension, variant)),
            "saved/%s.%s" % (target, ext_var_dot(extension, variant)),
        ] + ([tool_target] if tool_target else []),
        args = [
            "$(rootpath output/%s.%s)" % (target, ext_var_dot(extension, variant)),
            "$(rootpath saved/%s.%s)" % (target, ext_var_dot(extension, variant)),
            tool,
        ],
    )

def diff_test(target, name = None):  # buildifier: disable=unused-variable
    """Diff tests for target's output.

    Args:
        target: name of the output.
        name: unused.
    """
    _diff_test(target, "md", None, "cat")
    _diff_test(target, "txt", None, "cat")
    _diff_test(target, "html", None, "cat")

    _diff_test(target, "tex", None, "cat")
    _diff_test(target, "pdf", None, "$(rootpath //markdown/utils:pdfdump)", "//markdown/utils:pdfdump")

    _diff_test(target, "epub", None, "$(rootpath //markdown/utils:zipdump)", "//markdown/utils:zipdump")
    _build_test(target, "mobi", None)  # Mobi is nondeterministic, so we only test it builds

    _diff_test(target, "odt", None, "$(rootpath //markdown/utils:zipdump)", "//markdown/utils:zipdump")
    _diff_test(target, "docx", None, "$(rootpath //markdown/utils:zipdump)", "//markdown/utils:zipdump")
    _build_test(target, "doc", None)  # Doc is nondeterministic, so we only test it builds

    _diff_test(target, "docx", "shunnmodern", "$(rootpath //markdown/utils:zipdump)", "//markdown/utils:zipdump")

    _diff_test(target, "json", "metadata", "cat")
    _diff_test(target, "json", "deps_metadata", "cat")
