load("//markdown_makefile/python:python.bzl", "py_binary", "py_test")
load("@pip//:requirements.bzl", "requirement")

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
    visibility = ["//visibility:public"],
    deps = [
        requirement("PyYAML"),
        "//markdown_makefile/utils:metadata",
    ],
)

py_test(
    name = "collection_src_test",
    srcs = ["collection_src_test.py"],
    args = ["$(rootpath :collection_src)"],
    data = [":collection_src"],
    deps = ["//markdown_makefile/utils:test_utils"],
)
