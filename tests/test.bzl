"""Test utils."""

def _diff_test(target, ext, tool, tool_target = None):
    native.sh_test(
        name = "%s_%s_diff_test" % (target, ext.replace(".", "_")),
        srcs = ["//tests:diff_test.sh"],
        data = [
            "output/%s.%s" % (target, ext),
            "saved/%s.%s" % (target, ext),
        ] + ([tool_target] if tool_target else []),
        args = [
            "$(rootpath output/%s.%s)" % (target, ext),
            "$(rootpath saved/%s.%s)" % (target, ext),
            tool,
        ],
    )

def diff_test(target, name = None):  # buildifier: disable=unused-variable
    """Diff tests for target's output.

    Args:
        target: name of the output.
        name: unused.
    """
    _diff_test(target, "md", "cat")
    _diff_test(target, "txt", "cat")

    _diff_test(target, "tex", "cat")
    _diff_test(target, "pdf", "$(rootpath //utils:pdfdump)", "//utils:pdfdump")

    _diff_test(target, "epub", "$(rootpath //utils:zipdump)", "//utils:zipdump")
    # Mobi is nondeterministic, so we don't test it

    _diff_test(target, "odt", "$(rootpath //utils:zipdump)", "//utils:zipdump")
    _diff_test(target, "docx", "$(rootpath //utils:zipdump)", "//utils:zipdump")
    _diff_test(target, "doc", "$(rootpath //utils:docdump)", "//utils:docdump")
    _diff_test(target, "ms.docx", "$(rootpath //utils:zipdump)", "//utils:zipdump")
