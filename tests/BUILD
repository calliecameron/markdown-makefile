load("//:build_defs.bzl", "md_group")
load("//markdown_makefile/utils:validation.bzl", "validation_srcs")

exports_files(
    ["diff_test.sh"],
    visibility = ["__subpackages__"],
)

validation_srcs()

md_group(
    name = "tests",
    deps = [
        "//tests/test1",
        "//tests/test2",
        "//tests/test3",
        "//tests/test4",
    ],
)
