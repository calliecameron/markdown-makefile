load("@rules_python//python:defs.bzl", "py_test")

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
)
