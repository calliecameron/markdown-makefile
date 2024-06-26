load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/utils:defs.bzl", "pandoc_filter_py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown/formats:__pkg__"],
    deps = [
        "//markdown/core:defs_bzl",
        "//markdown/formats:lib_bzl",
    ],
)

exports_files(
    [
        "header_template.tex",
        "before_template.tex",
        "template.tex",
        "latex_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

pandoc_filter_py_test(
    name = "latex_filter_test",
    src = "latex_filter_test.py",
    filter = "latex_filter.lua",
)
