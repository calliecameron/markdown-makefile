load("@bazel_skylib//:bzl_library.bzl", "bzl_library")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown/formats:__pkg__"],
    deps = [
        "//markdown/core:defs_bzl",
        "//markdown/formats:helpers_bzl",
    ],
)
