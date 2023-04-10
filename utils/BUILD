load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("validation.bzl", "validation_srcs")

exports_files(
    [
        "default_gitattributes",
        "default_gitconfig",
        "default_gitignore",
        "precommit",
        "git_update.sh",
        "git_test.sh",
        "new_package.sh",
        "workspace_status",
        "workspace_contents_build",
        "workspace_contents_bzl",
        "workspace_summary",
        "workspace_publications",
        "workspace_git_update",
        "bazelversion",
        "bazelrc",
        "workspace_update.sh",
        "workspace_test.sh",
        "collection_header.tex",
        "collection_before.tex",
        "mypy_test.py",
        "flake8_test.py",
        "black_test.py",
        "shellcheck_test.sh",
        "summary.py",
    ],
    visibility = ["//visibility:public"],
)

validation_srcs(
    extra_py_files = ["workspace_status"],
    extra_sh_files = [
        "precommit",
        "workspace_git_update",
        "workspace_publications",
        "workspace_summary",
    ],
)

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "bindump",
    srcs = ["bindump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "docdump",
    srcs = ["docdump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "pdfdump",
    srcs = ["pdfdump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "zipdump",
    srcs = ["zipdump.sh"],
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
        "$(rootpath workspace_contents_build)",
        "$(rootpath workspace_contents_bzl)",
        "$(rootpath workspace_summary)",
        "$(rootpath workspace_publications)",
        "$(rootpath workspace_git_update)",
        "$(rootpath bazelversion)",
        "$(rootpath bazelrc)",
    ],
    data = [
        "bazelrc",
        "bazelversion",
        "workspace_contents_build",
        "workspace_contents_bzl",
        "workspace_git_update",
        "workspace_publications",
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

py_binary(
    name = "group_summary",
    srcs = ["group_summary.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "group_summary_test",
    srcs = ["group_summary_test.py"],
    args = ["$(rootpath group_summary.py)"],
    data = ["group_summary.py"],
    deps = [":test_utils"],
)

sh_binary(
    name = "write_group_summary_script",
    srcs = ["write_group_summary_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_group_summary_script_test",
    srcs = ["write_group_summary_script_test.py"],
    args = ["$(rootpath write_group_summary_script.sh)"],
    data = ["write_group_summary_script.sh"],
    deps = ["//utils:test_utils"],
)

py_binary(
    name = "group_publications",
    srcs = ["group_publications.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "group_publications_test",
    srcs = ["group_publications_test.py"],
    args = ["$(rootpath group_publications.py)"],
    data = ["group_publications.py"],
    deps = [":test_utils"],
)

sh_binary(
    name = "write_group_publications_script",
    srcs = ["write_group_publications_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_group_publications_script_test",
    srcs = ["write_group_publications_script_test.py"],
    args = ["$(rootpath write_group_publications_script.sh)"],
    data = ["write_group_publications_script.sh"],
    deps = ["//utils:test_utils"],
)
