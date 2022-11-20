load("//core:build_defs.bzl", "md_library")
load("//formats:misc.bzl", "md_md", "md_txt")
load("//formats:latex.bzl", "md_pdf", "md_tex", "md_tex_intermediate")
load("//formats:ebook.bzl", "md_epub", "md_mobi")
load("//formats:word.bzl", "md_doc", "md_docx", "md_odt")

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

md_epub(
    name = "foo_epub",
    lib = ":foo",
)

md_mobi(
    name = "foo_mobi",
    epub = ":foo_epub",
)

md_odt(
    name = "foo_odt",
    lib = ":foo",
)

md_docx(
    name = "foo_docx",
    lib = ":foo",
)

md_doc(
    name = "foo_doc",
    docx = ":foo_docx",
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
