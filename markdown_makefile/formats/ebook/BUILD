load("//markdown_makefile/shell:shell.bzl", "sh_binary")

exports_files(
    [
        "epub.css",
    ],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "ebook_convert",
    srcs = ["ebook_convert.sh"],
    visibility = ["//visibility:public"],
)
