load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__subpackages__"],
)

py_binary(
    name = "combine_deps_metadata",
    srcs = ["combine_deps_metadata.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "combine_deps_metadata_test",
    srcs = ["combine_deps_metadata_test.py"],
    args = ["$(rootpath :combine_deps_metadata)"],
    data = [":combine_deps_metadata"],
    deps = ["//markdown/utils:test_utils"],
)

py_binary(
    name = "preprocess",
    srcs = ["preprocess.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:bazel_package"],
)

py_test(
    name = "preprocess_test",
    srcs = ["preprocess_test.py"],
    args = ["$(rootpath :preprocess)"],
    deps = [
        ":preprocess",
        "//markdown/utils:test_utils",
    ],
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

py_test(
    name = "raw_version_test",
    srcs = ["raw_version_test.py"],
    args = ["$(rootpath :raw_version)"],
    data = [":raw_version"],
    deps = ["//markdown/utils:test_utils"],
)

py_binary(
    name = "version",
    srcs = ["version.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:metadata"],
)

py_test(
    name = "version_test",
    srcs = ["version_test.py"],
    args = ["$(rootpath :version)"],
    deps = [
        ":version",
        "//markdown/utils:test_utils",
    ],
)
