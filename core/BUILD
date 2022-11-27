load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")

filegroup(
    name = "py_srcs",
    data = glob(["*.py"]),
    visibility = ["//:__pkg__"],
)

py_library(
    name = "bazel_package",
    srcs = ["bazel_package.py"],
)

py_test(
    name = "bazel_package_test",
    srcs = ["bazel_package_test.py"],
    deps = [":bazel_package"],
)

py_binary(
    name = "raw_version",
    srcs = ["raw_version.py"],
    visibility = ["//visibility:public"],
    deps = [":bazel_package"],
)

py_test(
    name = "raw_version_test",
    srcs = ["raw_version_test.py"],
    args = ["$(rootpath raw_version.py)"],
    data = [
        "bazel_package.py",
        "raw_version.py",
    ],
    deps = ["//utils:test_utils"],
)

py_binary(
    name = "base_metadata",
    srcs = ["base_metadata.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "base_metadata_test",
    srcs = ["base_metadata_test.py"],
    args = ["$(rootpath base_metadata.py)"],
    data = ["base_metadata.py"],
    deps = [
        ":base_metadata",
        "//utils:test_utils",
    ],
)

py_binary(
    name = "preprocess",
    srcs = ["preprocess.py"],
    visibility = ["//visibility:public"],
    deps = [":bazel_package"],
)

py_test(
    name = "preprocess_test",
    srcs = ["preprocess_test.py"],
    args = ["$(rootpath preprocess.py)"],
    data = ["preprocess.py"],
    deps = [
        ":preprocess",
        "//utils:test_utils",
    ],
)

filegroup(
    name = "validate",
    srcs = ["validate.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "validate_test",
    srcs = ["validate_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath validate.py)",
    ],
    data = [
        "validate.py",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

filegroup(
    name = "include",
    srcs = ["include.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "include_test",
    srcs = ["include_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath include.lua)",
    ],
    data = [
        "include.lua",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

filegroup(
    name = "wordcount",
    srcs = ["wordcount.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "wordcount_test",
    srcs = ["wordcount_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath wordcount.lua)",
    ],
    data = [
        "wordcount.lua",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

filegroup(
    name = "starts_with_text",
    srcs = ["starts_with_text.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "starts_with_text_test",
    srcs = ["starts_with_text_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath starts_with_text.lua)",
    ],
    data = [
        "starts_with_text.lua",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

filegroup(
    name = "write_metadata",
    srcs = ["write_metadata.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_metadata_test",
    srcs = ["write_metadata_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath write_metadata.lua)",
    ],
    data = [
        "write_metadata.lua",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

filegroup(
    name = "cleanup",
    srcs = ["cleanup.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "cleanup_test",
    srcs = ["cleanup_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath cleanup.lua)",
    ],
    data = [
        "cleanup.lua",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

sh_binary(
    name = "write_dictionary",
    srcs = ["write_dictionary.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_dictionary_test",
    srcs = ["write_dictionary_test.py"],
    args = ["$(rootpath write_dictionary.sh)"],
    data = ["write_dictionary.sh"],
    deps = ["//utils:test_utils"],
)

filegroup(
    name = "spellcheck_input_template",
    srcs = ["spellcheck_input_template.md"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "spellcheck_filter",
    srcs = ["spellcheck_filter.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "spellcheck_filter_test",
    srcs = ["spellcheck_filter_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath spellcheck_filter.lua)",
    ],
    data = [
        "spellcheck_filter.lua",
        "@pandoc",
    ],
    deps = ["//utils:test_utils"],
)

sh_binary(
    name = "spellcheck",
    srcs = ["spellcheck.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "spellcheck_test",
    srcs = ["spellcheck_test.py"],
    args = ["$(rootpath spellcheck.sh)"],
    data = ["spellcheck.sh"],
    deps = ["//utils:test_utils"],
)
