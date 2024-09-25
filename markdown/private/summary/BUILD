load("@bazel_skylib//:bzl_library.bzl", "bzl_library")
load("//markdown/private/support/shell:defs.bzl", "sh_source")

bzl_library(
    name = "defs_bzl",
    srcs = ["defs.bzl"],
    visibility = [
        "//markdown/private:__pkg__",
        "//markdown/private/workspace:__pkg__",
    ],
    deps = ["//markdown/private/utils:defs_bzl"],
)

bzl_library(
    name = "impl_bzl",
    srcs = ["impl.bzl"],
    visibility = ["//visibility:public"],
    deps = ["//markdown/private/group:defs_bzl"],
)

exports_files(
    [
        "contents.build",
        "contents.bzl",
    ],
    visibility = ["//visibility:public"],
)

sh_source(
    name = "refresh",
    src = "refresh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "summarise_publications",
    src = "summarise_publications",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "summarise_contents",
    src = "summarise_contents",
    visibility = ["//visibility:public"],
)
