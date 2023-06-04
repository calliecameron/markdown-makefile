load("//markdown_makefile/shell:shell.bzl", "sh_source", "sh_test")

exports_files(
    [
        "contents_build",
        "contents_bzl",
    ],
    visibility = ["//visibility:public"],
)

sh_source(
    name = "dynamic_group_update",
    src = "dynamic_group_update.sh",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "dynamic_group_update_test",
    srcs = ["dynamic_group_update_test.sh"],
    args = [
        "$(rootpath dynamic_group_update.sh)",
        "$(rootpath contents_build)",
        "$(rootpath contents_bzl)",
        "$(rootpath contents_update)",
        "$(rootpath summary)",
        "$(rootpath publications)",
    ],
    data = [
        "contents_build",
        "contents_bzl",
        "contents_update",
        "dynamic_group_update.sh",
        "publications",
        "summary",
    ],
)

sh_source(
    name = "dynamic_group_test",
    src = "dynamic_group_test.sh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "contents_update",
    src = "contents_update",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "publications",
    src = "publications",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "summary",
    src = "summary",
    visibility = ["//visibility:public"],
)
