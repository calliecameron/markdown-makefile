load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_binary")
load("//markdown/support/shell:defs.bzl", "sh_binary", "sh_test")
load("//markdown/utils:defs.bzl", "pandoc_filter_py_test", "script_py_test")

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
        "reference.docx",
        "docx_filter.lua",
        "shunn_docx_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "unoconv",
    srcs = ["unoconv.sh"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "shunn_metadata",
    srcs = ["shunn_metadata.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:metadata"],
)

script_py_test(
    name = "shunn_metadata_test",
    src = "shunn_metadata_test.py",
    script = ":shunn_metadata",
)

pandoc_filter_py_test(
    name = "docx_filter_test",
    src = "docx_filter_test.py",
    filter = "docx_filter.lua",
)

sh_test(
    name = "shunn_docx_filter_test",
    srcs = ["shunn_docx_filter_test.sh"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath shunn_docx_filter.lua)",
        "$(rootpath reference.docx)",
    ],
    data = [
        "reference.docx",
        "shunn_docx_filter.lua",
        "//markdown/external:pandoc",
    ],
)
