load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary")
load("//markdown/utils:defs.bzl", "script_test")

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
    name = "gen_collection_src",
    srcs = ["gen_collection_src.py"],
    type_stub_deps = [requirement("types-PyYAML")],
    visibility = ["//visibility:public"],
    deps = [
        requirement("PyYAML"),
        "//markdown/utils:metadata",
    ],
)

script_test(
    name = "gen_collection_src_test",
    src = "gen_collection_src_test.py",
    script = ":gen_collection_src",
)
