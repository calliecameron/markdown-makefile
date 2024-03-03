"""Summary implementation macros."""

load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("@markdown_makefile//markdown:defs.bzl", "md_group")
load("@markdown_makefile//markdown/utils:defs.bzl", "required_files")

def md_summary_impl(contents):
    bzl_library(
        name = "contents_bzl",
        srcs = ["contents.bzl"],
        visibility = ["//visibility:private"],
    )

    required_files(
        name = "contents",
        copy = [
            (
                "@markdown_makefile//markdown/summary:contents.build",
                "BUILD",
                "600",
            ),
            (
                "@markdown_makefile//markdown/summary:refresh",
                "refresh",
                "700",
            ),
        ],
        create = [
            (
                "@markdown_makefile//markdown/summary:contents.bzl",
                "contents.bzl",
                "600",
            ),
        ],
    )

    md_group(
        name = "contents",
        deps = contents,
    )
