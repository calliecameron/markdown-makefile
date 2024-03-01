load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")
load("//markdown/support/shell:defs.bzl", "sh_binary", "sh_test")

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
        "reference.docx",
        "docx_filter.lua",
        "ms_docx_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "unoconv",
    srcs = ["unoconv.sh"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "ms_metadata",
    srcs = ["ms_metadata.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:metadata"],
)

py_test(
    name = "ms_metadata_test",
    srcs = ["ms_metadata_test.py"],
    args = ["$(rootpath :ms_metadata)"],
    data = [":ms_metadata"],
    deps = ["//markdown/utils:test_utils"],
)

sh_test(
    name = "ms_docx_filter_test",
    srcs = ["ms_docx_filter_test.sh"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath ms_docx_filter.lua)",
        "$(rootpath reference.docx)",
    ],
    data = [
        "ms_docx_filter.lua",
        "reference.docx",
        "//markdown/external:pandoc",
    ],
)
