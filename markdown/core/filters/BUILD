load("//markdown/support/python:defs.bzl", "py_test")

exports_files(
    [
        "include.lua",
        "starts_with_text.lua",
        "wordcount.lua",
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
