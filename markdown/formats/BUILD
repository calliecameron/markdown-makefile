load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/python:defs.bzl", "py_test")
load("//markdown/support/shell:defs.bzl", "sh_binary")

bzl_library(
    name = "helpers_bzl",
    srcs = ["helpers.bzl"],
    visibility = ["//markdown/formats:__subpackages__"],
    deps = ["//markdown/core:defs_bzl"],
)

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__pkg__"],
    deps = [
        ":helpers_bzl",
        "//markdown/formats/ebook:defs_bzl",
        "//markdown/formats/latex:defs_bzl",
        "//markdown/formats/word:defs_bzl",
    ],
)

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
    args = ["$(rootpath :write_open_script)"],
    data = [":write_open_script"],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "zip_cleaner",
    srcs = ["zip_cleaner.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "zip_cleaner_test",
    srcs = ["zip_cleaner_test.py"],
    args = ["$(rootpath :zip_cleaner)"],
    data = [":zip_cleaner"],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "write_save_script",
    srcs = ["write_save_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_save_script_test",
    srcs = ["write_save_script_test.py"],
    args = ["$(rootpath :write_save_script)"],
    data = [":write_save_script"],
    deps = ["//markdown/utils:test_utils"],
)

py_test(
    name = "add_title_test",
    srcs = ["add_title_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath add_title.lua)",
    ],
    data = [
        "add_title.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)
