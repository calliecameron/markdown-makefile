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
        "workspace_status",
        "workspace_summary",
        "workspace_update.sh",
        "workspace_test.sh",
        "collection_header.tex",
        "collection_before.tex",
        "mypy_test.py",
        "flake8_test.py",
        "autopep8_test.py",
        "summary.py",
    ],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "py_srcs",
    data = glob(["*.py"]) + ["workspace_status"],
    visibility = ["//:__pkg__"],
)

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
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

sh_test(
    name = "workspace_status_test",
    srcs = ["workspace_status_test.sh"],
    args = ["$(rootpath workspace_status)"],
    data = ["workspace_status"],
)

sh_test(
    name = "workspace_update_test",
    srcs = ["workspace_update_test.sh"],
    args = [
        "$(rootpath workspace_update.sh)",
        "$(rootpath workspace_status)",
        "$(rootpath workspace_summary)",
    ],
    data = [
        "workspace_status",
        "workspace_summary",
        "workspace_update.sh",
    ],
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
    deps = [":test_utils"],
)

py_test(
    name = "summary_test",
    srcs = ["summary_test.py"],
    args = ["$(rootpath summary.py)"],
    data = ["summary.py"],
    deps = [":test_utils"],
)
