load("@bazel_skylib//:bzl_library.bzl", "bzl_library")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown/formats:__subpackages__"],
    deps = [
        "//markdown/core:defs_bzl",
        "//markdown/formats:helpers_bzl",
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
