load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@pip//:requirements.bzl", "requirement")
load("//markdown/support/python:defs.bzl", "py_binary", "py_library", "py_test")
load("//markdown/support/shell:defs.bzl", "sh_binary", "sh_source", "sh_test")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//markdown:__subpackages__"],
)

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
    visibility = ["//markdown:__subpackages__"],
    deps = [requirement("panflute")],
)

py_library(
    name = "bazel_package",
    srcs = ["bazel_package.py"],
    visibility = ["//markdown:__subpackages__"],
)

py_test(
    name = "bazel_package_test",
    srcs = ["bazel_package_test.py"],
    deps = [":bazel_package"],
)

py_library(
    name = "metadata",
    srcs = ["metadata.py"],
    visibility = ["//markdown:__subpackages__"],
    deps = [requirement("pydantic")],
)

py_test(
    name = "metadata_test",
    srcs = ["metadata_test.py"],
    deps = [":metadata"],
)

py_library(
    name = "publications",
    srcs = ["publications.py"],
    visibility = ["//markdown:__subpackages__"],
    deps = [requirement("pydantic")],
)

py_test(
    name = "publications_test",
    srcs = ["publications_test.py"],
    deps = [":publications"],
)

sh_binary(
    name = "bindump",
    srcs = ["bindump.sh"],
    visibility = ["//:__subpackages__"],
)

sh_binary(
    name = "docdump",
    srcs = ["docdump.sh"],
    visibility = ["//:__subpackages__"],
)

py_binary(
    name = "pdf2txt",
    srcs = ["pdf2txt.py"],
    visibility = ["//visibility:private"],
    deps = [requirement("pdfminer.six")],
)

sh_binary(
    name = "pdfdump",
    srcs = ["pdfdump.sh"],
    args = ["$(rootpath pdf2txt)"],
    data = [":pdf2txt"],
    visibility = ["//:__subpackages__"],
)

sh_binary(
    name = "zipdump",
    srcs = ["zipdump.sh"],
    visibility = ["//:__subpackages__"],
)

sh_source(
    name = "required_files_test",
    src = "required_files_test.sh",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "required_files_test_test",
    srcs = ["required_files_test_test.sh"],
    args = ["$(rootpath required_files_test.sh)"],
    data = ["required_files_test.sh"],
)

sh_source(
    name = "required_files_update",
    src = "required_files_update.sh",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "required_files_update_test",
    srcs = ["required_files_update_test.sh"],
    args = ["$(rootpath required_files_update.sh)"],
    data = ["required_files_update.sh"],
)
