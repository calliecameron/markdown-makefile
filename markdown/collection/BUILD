load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__pkg__"],
    deps = ["//markdown/core:defs_bzl"],
)

exports_files(
    [
        "collection_header.tex",
        "collection_before.tex",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "collection_src",
    srcs = ["collection_src.py"],
    type_stub_deps = [requirement("types-PyYAML")],
    visibility = ["//visibility:public"],
    deps = [
        requirement("PyYAML"),
        "//markdown/utils:metadata",
    ],
)

py_test(
    name = "collection_src_test",
    srcs = ["collection_src_test.py"],
    args = ["$(rootpath :collection_src)"],
    data = [":collection_src"],
    deps = ["//markdown/utils:test_utils"],
)
