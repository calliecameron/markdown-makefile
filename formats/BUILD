load("@rules_python//python:defs.bzl", "py_binary", "py_test")

sh_binary(
    name = "write_open_script",
    srcs = ["write_open_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_open_script_test",
    srcs = ["write_open_script_test.py"],
    args = ["$(rootpath write_open_script.sh)"],
    data = ["write_open_script.sh"],
)

filegroup(
    name = "tex_header_template",
    srcs = ["header_template.tex"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "tex_before_template",
    srcs = ["before_template.tex"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "tex_template",
    srcs = ["template.tex"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "epub_css",
    srcs = ["epub.css"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "reference_docx",
    srcs = ["reference.docx"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "docx_filter",
    srcs = ["docx_filter.lua"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "ms_metadata",
    srcs = ["ms_metadata.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "ms_metadata_test",
    srcs = ["ms_metadata_test.py"],
    args = ["$(rootpath ms_metadata.py)"],
    data = ["ms_metadata.py"],
)

filegroup(
    name = "ms_docx_filter",
    srcs = ["ms_docx_filter.lua"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "zip_cleaner",
    srcs = ["zip_cleaner.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "zip_cleaner_test",
    srcs = ["zip_cleaner_test.py"],
    args = ["$(rootpath zip_cleaner.sh)"],
    data = ["zip_cleaner.sh"],
)
