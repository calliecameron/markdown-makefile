load("//:build_defs.bzl", "md_dynamic_group", "md_group")
load("//markdown_makefile/shell:shell.bzl", "sh_source")

sh_source(
    name = "diff_test",
    src = "diff_test.sh",
    visibility = ["__subpackages__"],
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

md_dynamic_group()
