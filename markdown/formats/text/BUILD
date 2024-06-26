load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/utils:defs.bzl", "pandoc_filter_py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown/formats:__pkg__"],
    deps = [
        "//markdown/formats:lib_bzl",
        "//markdown/formats:types_bzl",
    ],
)

exports_files(
    [
        "markdown_tumblr_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

pandoc_filter_py_test(
    name = "markdown_tumblr_filter_test",
    src = "markdown_tumblr_filter_test.py",
    filter = "markdown_tumblr_filter.lua",
)
