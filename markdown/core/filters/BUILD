load("//markdown/support/python:defs.bzl", "py_binary")
load("//markdown/utils:defs.bzl", "pandoc_filter_test")

exports_files(
    [
        "validate_ids.lua",
        "include.lua",
        "starts_with_text.lua",
        "wordcount.lua",
        "header_auto_ids.lua",
        "poetry_lines.lua",
        "write_metadata.lua",
        "cleanup.lua",
    ],
    visibility = ["//visibility:public"],
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

pandoc_filter_test(
    name = "validate_test",
    src = "validate_test.py",
    filter = ":validate",
)

pandoc_filter_test(
    name = "validate_ids_test",
    src = "validate_ids_test.py",
    filter = "validate_ids.lua",
)

pandoc_filter_test(
    name = "include_test",
    src = "include_test.py",
    filter = "include.lua",
)

pandoc_filter_test(
    name = "starts_with_text_test",
    src = "starts_with_text_test.py",
    filter = "starts_with_text.lua",
)

pandoc_filter_test(
    name = "header_auto_ids_test",
    src = "header_auto_ids_test.py",
    filter = "header_auto_ids.lua",
)

pandoc_filter_test(
    name = "wordcount_test",
    src = "wordcount_test.py",
    filter = "wordcount.lua",
)

pandoc_filter_test(
    name = "poetry_lines_test",
    src = "poetry_lines_test.py",
    filter = "poetry_lines.lua",
)

pandoc_filter_test(
    name = "write_metadata_test",
    src = "write_metadata_test.py",
    filter = "write_metadata.lua",
)

pandoc_filter_test(
    name = "cleanup_test",
    src = "cleanup_test.py",
    filter = "cleanup.lua",
)
