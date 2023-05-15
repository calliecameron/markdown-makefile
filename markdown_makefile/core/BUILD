load("//markdown_makefile/python:python.bzl", "py_binary", "py_test")
load("//markdown_makefile/shell:shell.bzl", "sh_binary")

exports_files(
    [
        "include.lua",
        "starts_with_text.lua",
        "wordcount.lua",
        "write_metadata.lua",
        "cleanup.lua",
        "spellcheck_input_template.md",
        "spellcheck_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "combine_metadata",
    srcs = ["combine_metadata.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "combine_metadata_test",
    srcs = ["combine_metadata_test.py"],
    args = ["$(rootpath combine_metadata.py)"],
    data = ["combine_metadata.py"],
    deps = [
        "//markdown_makefile/utils:test_utils",
    ],
)

py_binary(
    name = "raw_version",
    srcs = ["raw_version.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown_makefile/utils:bazel_package"],
)

py_test(
    name = "raw_version_test",
    srcs = ["raw_version_test.py"],
    args = ["$(rootpath raw_version.py)"],
    data = [
        "raw_version.py",
        "//markdown_makefile/utils:bazel_package",
    ],
    deps = ["//markdown_makefile/utils:test_utils"],
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
        "//markdown_makefile/utils:test_utils",
    ],
)

py_binary(
    name = "preprocess",
    srcs = ["preprocess.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown_makefile/utils:bazel_package"],
)

py_test(
    name = "preprocess_test",
    srcs = ["preprocess_test.py"],
    args = ["$(rootpath preprocess.py)"],
    data = ["preprocess.py"],
    deps = [
        ":preprocess",
        "//markdown_makefile/utils:test_utils",
    ],
)

py_binary(
    name = "validate",
    srcs = ["validate.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "validate_test",
    srcs = ["validate_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath validate)",
    ],
    data = [
        ":validate",
        "@pandoc",
    ],
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
)
