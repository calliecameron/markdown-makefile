load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/shell:defs.bzl", "sh_binary")
load("//markdown/utils:defs.bzl", "pandoc_filter_py_test", "script_py_test")

bzl_library(
    name = "lib_bzl",
    srcs = ["lib.bzl"],
    visibility = ["//markdown/formats:__subpackages__"],
    deps = ["//markdown/core:defs_bzl"],
)

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__pkg__"],
    deps = [
        "//markdown/formats/ebook:defs_bzl",
        "//markdown/formats/html:defs_bzl",
        "//markdown/formats/latex:defs_bzl",
        "//markdown/formats/markdown:defs_bzl",
        "//markdown/formats/metadata:defs_bzl",
        "//markdown/formats/text:defs_bzl",
        "//markdown/formats/word:defs_bzl",
    ],
)

exports_files(
    [
        "add_title.lua",
        "remove_paragraph_annotations.lua",
        "remove_collection_separators.lua",
        "remove_collection_separators_before_headers.lua",
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

script_py_test(
    name = "write_open_script_test",
    src = "write_open_script_test.py",
    script = ":write_open_script",
)

sh_binary(
    name = "zip_cleaner",
    srcs = ["zip_cleaner.sh"],
    visibility = ["//visibility:public"],
)

script_py_test(
    name = "zip_cleaner_test",
    src = "zip_cleaner_test.py",
    script = ":zip_cleaner",
)

sh_binary(
    name = "write_save_script",
    srcs = ["write_save_script.sh"],
    visibility = ["//visibility:public"],
)

script_py_test(
    name = "write_save_script_test",
    src = "write_save_script_test.py",
    script = ":write_save_script",
)

pandoc_filter_py_test(
    name = "add_title_test",
    src = "add_title_test.py",
    filter = "add_title.lua",
)

pandoc_filter_py_test(
    name = "remove_paragraph_annotations_test",
    src = "remove_paragraph_annotations_test.py",
    filter = "remove_paragraph_annotations.lua",
)

pandoc_filter_py_test(
    name = "remove_collection_separators_test",
    src = "remove_collection_separators_test.py",
    filter = "remove_collection_separators.lua",
)

pandoc_filter_py_test(
    name = "remove_collection_separators_before_headers_test",
    src = "remove_collection_separators_before_headers_test.py",
    filter = "remove_collection_separators_before_headers.lua",
)
