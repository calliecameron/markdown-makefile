load("//markdown_makefile/shell:shell.bzl", "sh_source", "sh_test")

exports_files(
    [
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
    ],
    visibility = ["//visibility:public"],
)

sh_source(
    name = "precommit",
    src = "precommit",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "git_update",
    src = "git_update.sh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "git_test",
    src = "git_test.sh",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "git_update_test",
    srcs = ["git_update_test.sh"],
    args = [
        "$(rootpath git_update.sh)",
        "$(rootpath default_gitattributes)",
        "$(rootpath default_gitconfig)",
        "$(rootpath default_gitignore)",
        "$(rootpath precommit)",
    ],
    data = [
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
        "git_update.sh",
        "precommit",
    ],
)
