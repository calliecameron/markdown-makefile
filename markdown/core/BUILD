load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_binary")
load("//markdown/utils:defs.bzl", "script_py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__subpackages__"],
)

py_binary(
    name = "preprocess",
    srcs = ["preprocess.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:bazel_package"],
)

script_py_test(
    name = "preprocess_test",
    src = "preprocess_test.py",
    script = ":preprocess",
    deps = [":preprocess"],
)

py_binary(
    name = "raw_version",
    srcs = ["raw_version.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//markdown/utils:bazel_package",
        "//markdown/utils:metadata",
    ],
)

script_py_test(
    name = "raw_version_test",
    src = "raw_version_test.py",
    script = ":raw_version",
)

py_binary(
    name = "version",
    srcs = ["version.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:metadata"],
)

script_py_test(
    name = "version_test",
    src = "version_test.py",
    script = ":version",
    deps = [":version"],
)
