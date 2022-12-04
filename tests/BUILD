load("//:build_defs.bzl", "md_group")

exports_files(
    ["diff_test.sh"],
    visibility = ["__subpackages__"],
)

filegroup(
    name = "sh_srcs",
    data = glob(["*.sh"]),
    visibility = ["//:__pkg__"],
)

md_group(
    name = "tests",
    deps = [
        "//tests/test1",
        "//tests/test2",
        "//tests/test3",
        "//tests/test4",
    ],
)
