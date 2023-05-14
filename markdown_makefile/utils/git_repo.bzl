"""Git repo macros."""

def md_git_repo(name = None):  # buildifier: disable=unused-variable
    common_args = [
        "$(rootpath @markdown_makefile//markdown_makefile/utils:default_gitattributes)",
        "$(rootpath @markdown_makefile//markdown_makefile/utils:default_gitconfig)",
        "$(rootpath @markdown_makefile//markdown_makefile/utils:default_gitignore)",
        "$(rootpath @markdown_makefile//markdown_makefile/utils:precommit)",
    ]
    common_data = [
        "@markdown_makefile//markdown_makefile/utils:default_gitattributes",
        "@markdown_makefile//markdown_makefile/utils:default_gitconfig",
        "@markdown_makefile//markdown_makefile/utils:default_gitignore",
        "@markdown_makefile//markdown_makefile/utils:precommit",
    ]

    native.sh_binary(
        name = "git_update",
        srcs = ["@markdown_makefile//markdown_makefile/utils:git_update.sh"],
        data = common_data,
        args = common_args + [native.package_name()],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "git_test",
        srcs = ["@markdown_makefile//markdown_makefile/utils:git_test.sh"],
        data = common_data + [
            ".gitattributes",
            ".gitconfig",
            ".gitignore",
            ".git/config",
            ".git/hooks/pre-commit",
        ],
        args = common_args + [
            "$(rootpath .gitattributes)",
            "$(rootpath .gitconfig)",
            "$(rootpath .gitignore)",
            "$(rootpath .git/config)",
            "$(rootpath .git/hooks/pre-commit)",
        ],
        visibility = ["//visibility:private"],
    )
