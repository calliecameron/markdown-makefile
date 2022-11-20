load("//core:build_defs.bzl", "md_library")
load("//formats:misc.bzl", "md_md", "md_txt")

md_library(
    name = "foo",
    src = "foo.md",
    dictionaries = ["foo.dic"],
    version_override = "blah",
)

md_md(
    name = "foo_md",
    lib = ":foo",
)

md_txt(
    name = "foo_txt",
    lib = ":foo",
)

md_library(
    name = "bar",
    src = "bar.md",
    dictionaries = ["bar.dic"],
    increment_included_headers = True,
    deps = [":foo"],
)

md_md(
    name = "bar_md",
    lib = ":bar",
)
