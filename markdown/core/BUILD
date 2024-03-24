load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__subpackages__"],
)

py_binary(
    name = "combine_metadata",
    srcs = ["combine_metadata.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "combine_metadata_test",
    srcs = ["combine_metadata_test.py"],
    args = ["$(rootpath :combine_metadata)"],
    data = [":combine_metadata"],
    deps = ["//markdown/utils:test_utils"],
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
    name = "base_metadata",
    srcs = ["base_metadata.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/utils:metadata"],
)

py_test(
    name = "base_metadata_test",
    srcs = ["base_metadata_test.py"],
    args = ["$(rootpath :base_metadata)"],
    deps = [
        ":base_metadata",
        "//markdown/utils:test_utils",
    ],
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
    name = "validate",
    srcs = ["validate.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//markdown/utils:metadata",
        "//markdown/utils:publications",
    ],
)

py_test(
    name = "validate_test",
    srcs = ["validate_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath :validate)",
    ],
    data = [
        ":validate",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)
