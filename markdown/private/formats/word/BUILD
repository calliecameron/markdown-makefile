load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/private/support/python:defs.bzl", "py_binary")
load("//markdown/private/support/shell:defs.bzl", "sh_binary", "sh_test")
load("//markdown/private/utils:defs.bzl", "pandoc_filter_py_test", "script_py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown/private/formats:__pkg__"],
    deps = [
        "//markdown/private/core:defs_bzl",
        "//markdown/private/formats:lib_bzl",
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
    args = ["$(rootpath //markdown/private/external:unoconv)"],
    data = ["//markdown/private/external:unoconv"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "shunn_metadata",
    srcs = ["shunn_metadata.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/private/utils:metadata"],
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
        "$(rootpath //markdown/private/external:pandoc)",
        "$(rootpath //markdown/private/external:strip_nondeterminism)",
        "$(rootpath //markdown/private/external:zipinfo)",
        "$(rootpath shunn_docx_filter.lua)",
        "$(rootpath reference.docx)",
    ],
    data = [
        "reference.docx",
        "shunn_docx_filter.lua",
        "//markdown/private/external:pandoc",
        "//markdown/private/external:strip_nondeterminism",
        "//markdown/private/external:zipinfo",
    ],
)
