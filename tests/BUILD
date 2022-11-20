load("//core:build_defs.bzl", "md_library")
load("//formats:misc.bzl", "md_md", "md_txt")
load("//formats:latex.bzl", "md_pdf", "md_tex", "md_tex_intermediate")

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

md_tex_intermediate(
    name = "foo_tex_intermediate",
    lib = ":foo",
)

md_tex(
    name = "foo_tex",
    intermediate = ":foo_tex_intermediate",
)

md_pdf(
    name = "foo_pdf",
    intermediate = ":foo_tex_intermediate",
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
