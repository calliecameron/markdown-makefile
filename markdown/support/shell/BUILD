load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load(":defs.bzl", "sh_source")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//:__subpackages__"],
)

sh_source(
    name = "shellcheck_test",
    src = "shellcheck_test.sh",
    visibility = ["//:__subpackages__"],
)
