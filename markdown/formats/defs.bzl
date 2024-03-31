"""Misc output formats."""

load(
    "//markdown/formats/ebook:defs.bzl",
    _md_epub = "md_epub",
    _md_mobi = "md_mobi",
)
load(
    "//markdown/formats/latex:defs.bzl",
    _md_pdf = "md_pdf",
    _md_tex = "md_tex",
    _md_tex_intermediate = "md_tex_intermediate",
)
load(
    "//markdown/formats/word:defs.bzl",
    _md_doc = "md_doc",
    _md_docx = "md_docx",
    _md_ms_docx = "md_ms_docx",
    _md_odt = "md_odt",
)
load(
    ":helpers.bzl",
    "add_title_arg",
    "remove_collection_separators_arg",
    "remove_paragraph_annotations_arg",
    "simple_pandoc_output_impl",
    "simple_pandoc_output_rule",
)

def _md_md_impl(ctx):
    return simple_pandoc_output_impl(
        ctx,
        "md",
        "markdown-smart",
        [
            ctx.file._remove_paragraph_annotations,
            ctx.file._remove_collection_separators,
        ],
        [
            "--standalone",
            "--wrap=none",
            remove_paragraph_annotations_arg(ctx),
            remove_collection_separators_arg(ctx),
        ],
        {},
        ctx.attr.lib,
        ctx.executable._write_open_script,
    )

md_md = simple_pandoc_output_rule(_md_md_impl, "md")

def _md_txt_impl(ctx):
    return simple_pandoc_output_impl(
        ctx,
        "txt",
        "plain",
        [ctx.file._remove_collection_separators],
        [
            "--standalone",
            "--wrap=none",
            remove_collection_separators_arg(ctx),
        ],
        {},
        ctx.attr.lib,
        ctx.executable._write_open_script,
    )

md_txt = simple_pandoc_output_rule(_md_txt_impl, "txt")

def _md_html_impl(ctx):
    return simple_pandoc_output_impl(
        ctx,
        "html",
        "html",
        [
            ctx.file._add_title,
            ctx.file._remove_collection_separators,
        ],
        [
            "--standalone",
            add_title_arg(ctx),
            remove_collection_separators_arg(ctx),
        ],
        {},
        ctx.attr.lib,
        ctx.executable._write_open_script,
    )

md_html = simple_pandoc_output_rule(_md_html_impl, "html")

md_epub = _md_epub
md_mobi = _md_mobi
md_pdf = _md_pdf
md_tex = _md_tex
md_tex_intermediate = _md_tex_intermediate
md_doc = _md_doc
md_docx = _md_docx
md_ms_docx = _md_ms_docx
md_odt = _md_odt
