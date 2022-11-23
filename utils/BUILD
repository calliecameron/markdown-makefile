load("@rules_python//python:defs.bzl", "py_test")

filegroup(
    name = "git_utils",
    data = [
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
        "docdump",
        "pdfdump",
        "zipdump",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "write_git_update_script",
    srcs = ["write_git_update_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_git_update_script_test",
    srcs = ["write_git_update_script_test.py"],
    args = ["$(rootpath write_git_update_script.sh)"],
    data = ["write_git_update_script.sh"],
)
