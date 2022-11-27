load("@rules_python//python:defs.bzl", "py_binary", "py_test")

filegroup(
    name = "py_srcs",
    data = glob(["*.py"]),
    visibility = ["//:__pkg__"],
)

exports_files(
    [
        "header_template.tex",
        "before_template.tex",
        "template.tex",
        "latex_filter.lua",
        "epub.css",
        "reference.docx",
        "docx_filter.lua",
        "ms_docx_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

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
    deps = ["//utils:test_utils"],
)

sh_binary(
    name = "ebook_convert",
    srcs = ["ebook_convert.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "unoconv",
    srcs = ["unoconv.sh"],
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
    deps = ["//utils:test_utils"],
)

sh_test(
    name = "ms_docx_filter_test",
    srcs = ["ms_docx_filter_test.sh"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath ms_docx_filter.lua)",
        "$(rootpath reference.docx)",
    ],
    data = [
        "ms_docx_filter.lua",
        "reference.docx",
        "@pandoc",
    ],
)

sh_binary(
    name = "ms_docx",
    srcs = ["ms_docx.sh"],
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
    deps = ["//utils:test_utils"],
)

sh_binary(
    name = "write_save_script",
    srcs = ["write_save_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_save_script_test",
    srcs = ["write_save_script_test.py"],
    args = ["$(rootpath write_save_script.sh)"],
    data = ["write_save_script.sh"],
    deps = ["//utils:test_utils"],
)
