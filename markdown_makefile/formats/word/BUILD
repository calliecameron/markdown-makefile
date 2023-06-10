load("//markdown_makefile/python:python.bzl", "py_binary", "py_test")
load("//markdown_makefile/shell:shell.bzl", "sh_binary", "sh_test")

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
    deps = ["//markdown_makefile/utils:metadata"],
)

py_test(
    name = "ms_metadata_test",
    srcs = ["ms_metadata_test.py"],
    args = ["$(rootpath :ms_metadata)"],
    data = [":ms_metadata"],
    deps = ["//markdown_makefile/utils:test_utils"],
)

sh_test(
    name = "ms_docx_filter_test",
    srcs = ["ms_docx_filter_test.sh"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath ms_docx_filter.lua)",
        "$(rootpath reference.docx)",
    ],
    data = [
        "ms_docx_filter.lua",
        "reference.docx",
        "@pandoc",
    ],
)
