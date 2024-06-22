"""Misc output formats."""

load(
    "//markdown/formats/ebook:defs.bzl",
    _md_epub = "md_epub",
    _md_mobi = "md_mobi",
)
load(
    "//markdown/formats/html:defs.bzl",
    _md_html = "md_html",
)
load(
    "//markdown/formats/latex:defs.bzl",
    _md_pdf = "md_pdf",
    _md_tex = "md_tex",
    _md_tex_intermediate = "md_tex_intermediate",
)
load(
    "//markdown/formats/metadata:defs.bzl",
    _md_deps_metadata_json = "md_deps_metadata_json",
    _md_metadata_json = "md_metadata_json",
)
load(
    "//markdown/formats/text:defs.bzl",
    _md_md = "md_md",
    _md_txt = "md_txt",
)
load(
    "//markdown/formats/word:defs.bzl",
    _md_doc = "md_doc",
    _md_docx = "md_docx",
    _md_ms_docx = "md_ms_docx",
    _md_odt = "md_odt",
)

md_md = _md_md
md_txt = _md_txt
md_html = _md_html
md_epub = _md_epub
md_mobi = _md_mobi
md_pdf = _md_pdf
md_tex = _md_tex
md_tex_intermediate = _md_tex_intermediate
md_doc = _md_doc
md_docx = _md_docx
md_ms_docx = _md_ms_docx
md_odt = _md_odt
md_metadata_json = _md_metadata_json
md_deps_metadata_json = _md_deps_metadata_json
