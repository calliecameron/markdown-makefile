load("//markdown_makefile/python:python.bzl", "py_binary", "py_library", "py_test")
load("//markdown_makefile/shell:shell.bzl", "sh_binary")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
    visibility = ["//visibility:public"],
)

py_library(
    name = "bazel_package",
    srcs = ["bazel_package.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "bazel_package_test",
    srcs = ["bazel_package_test.py"],
    deps = [":bazel_package"],
)

sh_binary(
    name = "bindump",
    srcs = ["bindump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "docdump",
    srcs = ["docdump.sh"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "pdf2txt",
    srcs = ["pdf2txt.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("pdfminer.six")],
)

sh_binary(
    name = "pdfdump",
    srcs = ["pdfdump.sh"],
    args = ["$(rootpath pdf2txt)"],
    data = [":pdf2txt"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "zipdump",
    srcs = ["zipdump.sh"],
    visibility = ["//visibility:public"],
)
