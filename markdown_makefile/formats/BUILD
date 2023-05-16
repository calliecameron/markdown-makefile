load("//markdown_makefile/python:python.bzl", "py_test")
load("//markdown_makefile/shell:shell.bzl", "sh_binary")

exports_files(
    [
        "add_title.lua",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "pandoc",
    srcs = ["pandoc.sh"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
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
    deps = ["//markdown_makefile/utils:test_utils"],
)

py_test(
    name = "add_title_test",
    srcs = ["add_title_test.py"],
    args = [
        "$(rootpath @pandoc//:pandoc)",
        "$(rootpath add_title.lua)",
    ],
    data = [
        "add_title.lua",
        "@pandoc",
    ],
    deps = ["//markdown_makefile/utils:test_utils"],
)
