load("@rules_python//python:defs.bzl", "py_binary", "py_test")

exports_files(
    [
        "bindump",
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
        "collection_header.tex",
    ],
    visibility = ["//visibility:public"],
)

sh_test(
    name = "git_update_test",
    srcs = ["git_update_test.sh"],
    args = [
        "$(rootpath git_update.sh)",
        "$(rootpath bindump)",
        "$(rootpath docdump)",
        "$(rootpath pdfdump)",
        "$(rootpath zipdump)",
        "$(rootpath default_gitattributes)",
        "$(rootpath default_gitconfig)",
        "$(rootpath default_gitignore)",
        "$(rootpath precommit)",
    ],
    data = [
        "bindump",
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

py_binary(
    name = "collection_src",
    srcs = ["collection_src.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "collection_src_test",
    srcs = ["collection_src_test.py"],
    args = ["$(rootpath collection_src.py)"],
    data = ["collection_src.py"],
)
