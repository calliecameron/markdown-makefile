"""Git repo macros."""

load("//markdown/utils:defs.bzl", "required_files")

def md_git_repo(name = None, extra_precommit = None):  # buildifier: disable=unused-variable
    """Git repo setup.

    Args:
        name: unused
        extra_precommit: an extra script to run at precommit
    """
    native.sh_binary(
        name = "git_test_extra",
        srcs = ["@markdown_makefile//markdown/git:git_test_extra.sh"],
        data = native.glob([".git/config"]),
        visibility = ["//visibility:private"],
    )

    copy = [
        (
            "@markdown_makefile//markdown/git:default_gitattributes",
            ".gitattributes",
            "600",
        ),
        (
            "@markdown_makefile//markdown/git:default_gitconfig",
            ".gitconfig",
            "600",
        ),
        (
            "@markdown_makefile//markdown/git:default_gitignore",
            ".gitignore",
            "600",
        ),
        (
            "@markdown_makefile//markdown/git:precommit",
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
        extra_update = "@markdown_makefile//markdown/git:git_update_extra",
    )
