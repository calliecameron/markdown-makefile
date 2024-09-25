load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary")
load("//markdown/support/shell:defs.bzl", "sh_binary")
load("//markdown/utils:defs.bzl", "script_py_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = [
        "//markdown/private:__pkg__",
        "//markdown/summary:__pkg__",
    ],
    deps = ["//markdown/core:defs_bzl"],
)

py_binary(
    name = "group_summary",
    srcs = ["group_summary.py"],
    type_stub_deps = [
        requirement("types-tabulate"),
    ],
    visibility = ["//visibility:public"],
    deps = [
        requirement("tabulate"),
        "//markdown/utils:metadata",
        "//markdown/utils:publications",
    ],
)

script_py_test(
    name = "group_summary_test",
    src = "group_summary_test.py",
    script = ":group_summary",
)

sh_binary(
    name = "write_group_summary_script",
    srcs = ["write_group_summary_script.sh"],
    visibility = ["//visibility:public"],
)

script_py_test(
    name = "write_group_summary_script_test",
    src = "write_group_summary_script_test.py",
    script = ":write_group_summary_script",
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

script_py_test(
    name = "group_publications_test",
    src = "group_publications_test.py",
    script = ":group_publications",
)

sh_binary(
    name = "write_group_publications_script",
    srcs = ["write_group_publications_script.sh"],
    visibility = ["//visibility:public"],
)

script_py_test(
    name = "write_group_publications_script_test",
    src = "write_group_publications_script_test.py",
    script = ":write_group_publications_script",
)
