load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown:defs.bzl", "md_group", "md_summary")
load("//markdown/support/shell:defs.bzl", "sh_source")

bzl_library(
    name = "test_bzl",
    srcs = ["test.bzl"],
    visibility = ["//visibility:private"],
    deps = [
        "//markdown/formats:defs_bzl",
    ],
)

sh_source(
    name = "diff_test",
    src = "diff_test.sh",
    visibility = ["__subpackages__"],
)

sh_source(
    name = "extra_precommit",
    src = "extra_precommit.sh",
    visibility = ["//:__pkg__"],
)

md_group(
    name = "tests",
    deps = [
        "//tests/test1",
        "//tests/test2",
        "//tests/test3",
        "//tests/test4",
        "//tests/test5",
    ],
)

md_summary()
