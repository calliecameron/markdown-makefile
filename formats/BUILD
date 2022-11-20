load("@rules_python//python:defs.bzl", "py_test")

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
)

filegroup(
    name = "tex_header_template",
    srcs = ["header_template.tex"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "tex_before_template",
    srcs = ["before_template.tex"],
    visibility = ["//visibility:public"],
)

filegroup(
    name = "tex_template",
    srcs = ["template.tex"],
    visibility = ["//visibility:public"],
)
