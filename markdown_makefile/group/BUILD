load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("@pip//:requirements.bzl", "requirement")
load("//markdown_makefile/validation:validation.bzl", "validation_srcs")

validation_srcs()

py_binary(
    name = "group_summary",
    srcs = ["group_summary.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "group_summary_test",
    srcs = ["group_summary_test.py"],
    args = ["$(rootpath group_summary.py)"],
    data = ["group_summary.py"],
    deps = ["//markdown_makefile/utils:test_utils"],
)

py_binary(
    name = "group_summary_print",
    srcs = ["group_summary_print.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("tabulate")],
)

py_test(
    name = "group_summary_print_test",
    srcs = ["group_summary_print_test.py"],
    args = ["$(rootpath group_summary_print.py)"],
    data = ["group_summary_print.py"],
    deps = ["//markdown_makefile/utils:test_utils"],
)

sh_binary(
    name = "write_group_summary_script",
    srcs = ["write_group_summary_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_group_summary_script_test",
    srcs = ["write_group_summary_script_test.py"],
    args = ["$(rootpath write_group_summary_script.sh)"],
    data = ["write_group_summary_script.sh"],
    deps = ["//markdown_makefile/utils:test_utils"],
)

py_binary(
    name = "group_publications",
    srcs = ["group_publications.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "group_publications_test",
    srcs = ["group_publications_test.py"],
    args = ["$(rootpath group_publications.py)"],
    data = ["group_publications.py"],
    deps = ["//markdown_makefile/utils:test_utils"],
)

sh_binary(
    name = "write_group_publications_script",
    srcs = ["write_group_publications_script.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_group_publications_script_test",
    srcs = ["write_group_publications_script_test.py"],
    args = ["$(rootpath write_group_publications_script.sh)"],
    data = ["write_group_publications_script.sh"],
    deps = ["//markdown_makefile/utils:test_utils"],
)
