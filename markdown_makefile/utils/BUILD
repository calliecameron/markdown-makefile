load("@rules_python//python:defs.bzl", "py_binary", "py_test")
load("@pip//:requirements.bzl", "requirement")
load("//markdown_makefile/validation:validation.bzl", "validation_srcs")

exports_files(
    [
        "collection_header.tex",
        "collection_before.tex",
    ],
    visibility = ["//visibility:public"],
)

validation_srcs()

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "bindump",
    srcs = ["bindump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "docdump",
    srcs = ["docdump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "pdfdump",
    srcs = ["pdfdump.sh"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "zipdump",
    srcs = ["zipdump.sh"],
    visibility = ["//visibility:public"],
)

py_binary(
    name = "collection_src",
    srcs = ["collection_src.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "collection_src_test",
    srcs = ["collection_src_test.py"],
    args = ["$(rootpath collection_src.py)"],
    data = ["collection_src.py"],
    deps = [":test_utils"],
)

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
    deps = [":test_utils"],
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
    deps = [":test_utils"],
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
    deps = [":test_utils"],
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
    deps = [":test_utils"],
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
    deps = [":test_utils"],
)
