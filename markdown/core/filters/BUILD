load("//markdown/support/python:defs.bzl", "py_binary")
load("//markdown/utils:defs.bzl", "pandoc_filter_py_test")

exports_files(
    [
        "validate_ids.lua",
        "validate_quotes.lua",
        "include.lua",
        "paragraph_annotations.lua",
        "starts_with_text.lua",
        "wordcount.lua",
        "header_auto_ids.lua",
        "poetry_lines.lua",
        "write_metadata.lua",
        "cleanup.lua",
    ],
    visibility = ["//visibility:public"],
)

pandoc_filter_py_test(
    name = "validate_ids_test",
    src = "validate_ids_test.py",
    filter = "validate_ids.lua",
)

pandoc_filter_py_test(
    name = "validate_quotes_test",
    src = "validate_quotes_test.py",
    filter = "validate_quotes.lua",
)

py_binary(
    name = "validate_metadata",
    srcs = ["validate_metadata.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//markdown/utils:metadata",
        "//markdown/utils:publications",
    ],
)

pandoc_filter_py_test(
    name = "validate_metadata_test",
    src = "validate_metadata_test.py",
    filter = ":validate_metadata",
)

pandoc_filter_py_test(
    name = "include_test",
    src = "include_test.py",
    filter = "include.lua",
)

pandoc_filter_py_test(
    name = "paragraph_annotations_test",
    src = "paragraph_annotations_test.py",
    filter = "paragraph_annotations.lua",
)

pandoc_filter_py_test(
    name = "starts_with_text_test",
    src = "starts_with_text_test.py",
    filter = "starts_with_text.lua",
)

pandoc_filter_py_test(
    name = "header_auto_ids_test",
    src = "header_auto_ids_test.py",
    filter = "header_auto_ids.lua",
)

pandoc_filter_py_test(
    name = "wordcount_test",
    src = "wordcount_test.py",
    filter = "wordcount.lua",
)

pandoc_filter_py_test(
    name = "poetry_lines_test",
    src = "poetry_lines_test.py",
    filter = "poetry_lines.lua",
)

pandoc_filter_py_test(
    name = "write_metadata_test",
    src = "write_metadata_test.py",
    filter = "write_metadata.lua",
)

pandoc_filter_py_test(
    name = "cleanup_test",
    src = "cleanup_test.py",
    filter = "cleanup.lua",
)
