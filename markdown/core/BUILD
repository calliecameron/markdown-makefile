load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")
load("//markdown/support/shell:defs.bzl", "sh_binary")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__subpackages__"],
)

exports_files(
    [
        "include.lua",
        "starts_with_text.lua",
        "wordcount.lua",
        "poetry_lines.lua",
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
    name = "lint_input",
    srcs = ["lint_input.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "lint_input_test",
    srcs = ["lint_input_test.py"],
    args = ["$(rootpath :lint_input)"],
    data = [":lint_input"],
    deps = ["//markdown/utils:test_utils"],
)

py_binary(
    name = "lint",
    srcs = ["lint.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("pymarkdownlnt")],
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

py_test(
    name = "include_test",
    srcs = ["include_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath include.lua)",
    ],
    data = [
        "include.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "starts_with_text_test",
    srcs = ["starts_with_text_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath starts_with_text.lua)",
    ],
    data = [
        "starts_with_text.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "wordcount_test",
    srcs = ["wordcount_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath wordcount.lua)",
    ],
    data = [
        "wordcount.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "poetry_lines_test",
    srcs = ["poetry_lines_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath poetry_lines.lua)",
    ],
    data = [
        "poetry_lines.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "write_metadata_test",
    srcs = ["write_metadata_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath write_metadata.lua)",
    ],
    data = [
        "write_metadata.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "cleanup_test",
    srcs = ["cleanup_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath cleanup.lua)",
    ],
    data = [
        "cleanup.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "write_dictionary",
    srcs = ["write_dictionary.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_dictionary_test",
    srcs = ["write_dictionary_test.py"],
    args = ["$(rootpath :write_dictionary)"],
    data = [":write_dictionary"],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "spellcheck_filter_test",
    srcs = ["spellcheck_filter_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath spellcheck_filter.lua)",
    ],
    data = [
        "spellcheck_filter.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "spellcheck",
    srcs = ["spellcheck.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "spellcheck_test",
    srcs = ["spellcheck_test.py"],
    args = ["$(rootpath :spellcheck)"],
    data = [":spellcheck"],
    deps = ["//markdown/utils:test_utils"],
)
