load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load(":defs.bzl", "py_source")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//:__subpackages__"],
)

py_source(
    name = "mypy_stub",
    src = "mypy_stub.py",
    visibility = ["//:__subpackages__"],
)
