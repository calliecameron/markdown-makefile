load("//markdown_makefile/python:python.bzl", "py_binary", "py_test")
load("//markdown_makefile/shell:shell.bzl", "sh_binary")
load("@pip//:requirements.bzl", "requirement")

py_binary(
    name = "group_summary",
    srcs = ["group_summary.py"],
    visibility = ["//visibility:public"],
    deps = [
        requirement("tabulate"),
        requirement("dateparser"),
        "//markdown_makefile/utils:metadata",
        "//markdown_makefile/utils:publications",
    ],
)

py_test(
    name = "group_summary_test",
    srcs = ["group_summary_test.py"],
    args = ["$(rootpath group_summary)"],
    data = ["group_summary"],
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
    deps = [
        "//markdown_makefile/utils:metadata",
        "//markdown_makefile/utils:publications",
    ],
)

py_test(
    name = "group_publications_test",
    srcs = ["group_publications_test.py"],
    args = ["$(rootpath group_publications)"],
    data = ["group_publications"],
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
