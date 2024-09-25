load("//markdown/private/support/python:defs.bzl", "py_binary")
load("//markdown/private/utils:defs.bzl", "script_py_test")

py_binary(
    name = "combine_deps_metadata",
    srcs = ["combine_deps_metadata.py"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/private/utils:metadata"],
)

script_py_test(
    name = "combine_deps_metadata_test",
    src = "combine_deps_metadata_test.py",
    script = ":combine_deps_metadata",
)
