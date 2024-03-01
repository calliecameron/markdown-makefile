load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary", "py_test")
load("//markdown/support/shell:defs.bzl", "sh_binary")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__pkg__"],
    deps = ["//markdown/core:defs_bzl"],
)

py_binary(
    name = "group_summary",
    srcs = ["group_summary.py"],
    type_stub_deps = [
        requirement("types-tabulate"),
        requirement("types-dateparser"),
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("tabulate"),
        requirement("dateparser"),
        "//markdown/utils:metadata",
        "//markdown/utils:publications",
    ],
)

py_test(
    name = "group_summary_test",
    srcs = ["group_summary_test.py"],
    args = ["$(rootpath group_summary)"],
    data = [":group_summary"],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "write_group_summary_script",
    srcs = ["write_group_summary_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_group_summary_script_test",
    srcs = ["write_group_summary_script_test.py"],
    args = ["$(rootpath :write_group_summary_script)"],
    data = [":write_group_summary_script"],
    deps = ["//markdown/utils:test_utils"],
)

py_binary(
    name = "group_publications",
    srcs = ["group_publications.py"],
    visibility = ["//visibility:public"],
    deps = [
        "//markdown/utils:metadata",
        "//markdown/utils:publications",
    ],
)

py_test(
    name = "group_publications_test",
    srcs = ["group_publications_test.py"],
    args = ["$(rootpath :group_publications)"],
    data = [":group_publications"],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "write_group_publications_script",
    srcs = ["write_group_publications_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_group_publications_script_test",
    srcs = ["write_group_publications_script_test.py"],
    args = ["$(rootpath :write_group_publications_script)"],
    data = [":write_group_publications_script"],
    deps = ["//markdown/utils:test_utils"],
)
