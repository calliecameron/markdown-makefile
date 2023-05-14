load("@rules_python//python:defs.bzl", "py_test")
load("//markdown_makefile/validation:validation.bzl", "validation_srcs")

validation_srcs()

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

sh_binary(
    name = "pdfdump",
    srcs = ["pdfdump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "zipdump",
    srcs = ["zipdump.sh"],
    visibility = ["//visibility:public"],
)
