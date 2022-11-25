exports_files(
    [
        "docdump",
        "pdfdump",
        "zipdump",
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
        "precommit",
        "git_update.sh",
        "git_test.sh",
        "new_package.sh",
    ],
    visibility = ["//visibility:public"],
)

sh_test(
    name = "git_update_test",
    srcs = ["git_update_test.sh"],
    args = [
        "$(rootpath git_update.sh)",
        "$(rootpath docdump)",
        "$(rootpath pdfdump)",
        "$(rootpath zipdump)",
        "$(rootpath default_gitattributes)",
        "$(rootpath default_gitconfig)",
        "$(rootpath default_gitignore)",
        "$(rootpath precommit)",
    ],
    data = [
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
        "docdump",
        "git_update.sh",
        "pdfdump",
        "precommit",
        "zipdump",
    ],
)

sh_test(
    name = "new_package_test",
    srcs = ["new_package_test.sh"],
    args = ["$(rootpath new_package.sh)"],
    data = ["new_package.sh"],
)
