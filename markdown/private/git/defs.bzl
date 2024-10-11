"""Git repo macros."""

load("//markdown/private/utils:defs.bzl", "extend_file", "required_files")

def md_git_repo(name = None, extra_gitignore_lines = None, extra_precommit = None):  # buildifier: disable=unused-variable
    """Git repo setup.

    Args:
        name: unused
        extra_gitignore_lines: extra lines to add to the generated gitignore
        extra_precommit: an extra script to run at precommit
    """
    native.sh_binary(
        name = "git_test_extra",
        srcs = ["@rules_markdown//markdown/private/git:git_test_extra.sh"],
        data = native.glob([".git/config"]),
        visibility = ["//visibility:private"],
    )

    extend_file(
        name = "gitattributes",
        src = "@rules_markdown//markdown/private/git:default_gitattributes",
        prepend_lines = ["# Auto-generated; do not edit."],
    )

    extend_file(
        name = "gitconfig",
        src = "@rules_markdown//markdown/private/git:default_gitconfig",
        prepend_lines = ["# Auto-generated; do not edit."],
    )

    extend_file(
        name = "gitignore",
        src = "@rules_markdown//markdown/private/git:default_gitignore",
        prepend_lines = ["# Auto-generated; edit extra_gitignore_lines in md_git_repo."],
        append_lines = extra_gitignore_lines,
    )

    copy = [
        (
            ":gitattributes",
            ".gitattributes",
            "600",
        ),
        (
            ":gitconfig",
            ".gitconfig",
            "600",
        ),
        (
            ":gitignore",
            ".gitignore",
            "600",
        ),
        (
            "@rules_markdown//markdown/private/git:run_tests",
            ".git/hooks/markdown_run_tests",
            "700",
        ),
        (
            "@rules_markdown//markdown/private/git:precommit",
            ".git/hooks/pre-commit",
            "700",
        ),
    ]
    if extra_precommit:
        copy.append(
            (
                extra_precommit,
                ".git/hooks/markdown_extra_precommit",
                "700",
            ),
        )
    required_files(
        name = "git",
        copy = copy,
        extra_check = ":git_test_extra",
        extra_update = "@rules_markdown//markdown/private/git:git_update_extra",
    )
