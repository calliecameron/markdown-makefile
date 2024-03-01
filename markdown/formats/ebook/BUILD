load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/shell:defs.bzl", "sh_binary")

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
        "epub.css",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "ebook_convert",
    srcs = ["ebook_convert.sh"],
    visibility = ["//visibility:public"],
)
