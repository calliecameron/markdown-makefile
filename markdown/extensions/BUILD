load("@bazel_skylib//:bzl_library.bzl", "bzl_library")

bzl_library(
    name = "markdown_bzl",
    srcs = ["markdown.bzl"],
    visibility = ["//visibility:private"],
    deps = [
        "//markdown/extensions/private:git_repo_bzl",
        "//markdown/extensions/private:main_repo_bzl",
    ],
)
