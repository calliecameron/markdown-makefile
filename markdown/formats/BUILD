load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/support/shell:defs.bzl", "sh_binary")
load("//markdown/utils:defs.bzl", "script_py_test")

bzl_library(
    name = "types_bzl",
    srcs = ["types.bzl"],
    visibility = ["//markdown/formats:__subpackages__"],
)

bzl_library(
    name = "lib_bzl",
    srcs = ["lib.bzl"],
    visibility = ["//markdown/formats:__subpackages__"],
    deps = [
        ":types_bzl",
        "//markdown/core:defs_bzl",
    ],
)

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = [
        "//markdown:__pkg__",
        "//tests:__pkg__",
    ],
    deps = [
        ":lib_bzl",
        "//markdown/formats/ebook:defs_bzl",
        "//markdown/formats/html:defs_bzl",
        "//markdown/formats/latex:defs_bzl",
        "//markdown/formats/metadata:defs_bzl",
        "//markdown/formats/text:defs_bzl",
        "//markdown/formats/word:defs_bzl",
    ],
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
