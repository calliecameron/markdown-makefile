load("//markdown_makefile/utils:validation.bzl", "validation_srcs")

exports_files(
    [
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
        "precommit",
        "git_update.sh",
        "git_test.sh",
    ],
    visibility = ["//visibility:public"],
)

validation_srcs(
    extra_sh_files = [
        "precommit",
    ],
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
