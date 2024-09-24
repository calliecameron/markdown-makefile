load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_source")
load("//markdown/support/shell:defs.bzl", "sh_test")

bzl_library(
    name = "git_repo_bzl",
    srcs = ["git_repo.bzl"],
    visibility = ["//visibility:private"],
)

bzl_library(
    name = "main_repo_bzl",
    srcs = ["main_repo.bzl"],
    visibility = ["//visibility:private"],
)

bzl_library(
    name = "markdown_bzl",
    srcs = ["markdown.bzl"],
    visibility = ["//visibility:private"],
    deps = [
        ":git_repo_bzl",
        ":main_repo_bzl",
    ],
)

py_source(
    name = "find_git_repos",
    src = "find_git_repos",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "find_git_repos_test",
    srcs = ["find_git_repos_test.sh"],
    args = ["$(rootpath find_git_repos)"],
    data = ["find_git_repos"],
)
