"""Auto-generated build file."""

load("@markdown_makefile//markdown:defs.bzl", "md_group")
load("contents.bzl", "contents")

exports_files(
    [
        "BUILD",
        "contents.bzl",
        "update",
    ],
    visibility = ["//" + "/".join(package_name().split("/")[:-1]) + ":__pkg__"],
)

md_group(
    name = "contents",
    deps = contents(),
)
