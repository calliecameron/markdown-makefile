load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/private/support/shell:defs.bzl", "sh_source")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = ["//visibility:public"],
    deps = [
        "//markdown/private/formats:defs_bzl",
    ],
)

sh_source(
    name = "diff_test",
    src = "diff_test.sh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "dump_test",
    src = "dump_test.sh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "zip_cleaned_test",
    src = "zip_cleaned_test.sh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "version_test",
    src = "version_test.sh",
    visibility = ["//visibility:public"],
)
