load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("//markdown_makefile/validation:validation.bzl", "validation_srcs")

exports_files(
    [
        "collection_header.tex",
        "collection_before.tex",
    ],
    visibility = ["//visibility:public"],
)

validation_srcs()

py_binary(
    name = "collection_src",
    srcs = ["collection_src.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "collection_src_test",
    srcs = ["collection_src_test.py"],
    args = ["$(rootpath collection_src.py)"],
    data = ["collection_src.py"],
    deps = ["//markdown_makefile/utils:test_utils"],
)
