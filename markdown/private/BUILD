load("@bazel_skylib//:bzl_library.bzl", "bzl_library")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//visibility:public"],
    deps = [
        "//markdown/private/collection:defs_bzl",
        "//markdown/private/core:defs_bzl",
        "//markdown/private/formats:defs_bzl",
        "//markdown/private/git:defs_bzl",
        "//markdown/private/group:defs_bzl",
        "//markdown/private/summary:defs_bzl",
        "//markdown/private/workspace:defs_bzl",
    ],
)
