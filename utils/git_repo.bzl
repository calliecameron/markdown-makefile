"""Git repo macros."""

def md_git_repo(name = None):  # buildifier: disable=unused-variable
    common_args = [
        "$(rootpath @markdown_makefile//utils:docdump)",
        "$(rootpath @markdown_makefile//utils:pdfdump)",
        "$(rootpath @markdown_makefile//utils:zipdump)",
        "$(rootpath @markdown_makefile//utils:default_gitattributes)",
        "$(rootpath @markdown_makefile//utils:default_gitconfig)",
        "$(rootpath @markdown_makefile//utils:default_gitignore)",
    ]
    common_data = [
        "@markdown_makefile//utils:docdump",
        "@markdown_makefile//utils:pdfdump",
        "@markdown_makefile//utils:zipdump",
        "@markdown_makefile//utils:default_gitattributes",
        "@markdown_makefile//utils:default_gitconfig",
        "@markdown_makefile//utils:default_gitignore",
    ]

    native.sh_binary(
        name = "git_update",
        srcs = ["@markdown_makefile//utils:git_update.sh"],
        data = common_data,
        args = common_args + [native.package_name()],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "git_test",
        srcs = ["@markdown_makefile//utils:git_test.sh"],
        data = common_data + [
            ".bin/docdump",
            ".bin/pdfdump",
            ".bin/zipdump",
            ".gitattributes",
            ".gitconfig",
            ".gitignore",
            ".git/config",
        ],
        args = common_args + [
            "$(rootpath .bin/docdump)",
            "$(rootpath .bin/pdfdump)",
            "$(rootpath .bin/zipdump)",
            "$(rootpath .gitattributes)",
            "$(rootpath .gitconfig)",
            "$(rootpath .gitignore)",
            "$(rootpath .git/config)",
        ],
        visibility = ["//visibility:private"],
    )
