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
        "tumblr_markdown_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

pandoc_filter_py_test(
    name = "tumblr_markdown_filter_test",
    src = "tumblr_markdown_filter_test.py",
    filter = "tumblr_markdown_filter.lua",
)
