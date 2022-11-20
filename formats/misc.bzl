"""Misc output formats."""

load(":helpers.bzl", "simple_pandoc_output_impl", "simple_pandoc_output_rule")

def _md_md_impl(ctx):
    return simple_pandoc_output_impl(ctx, "md", [], ["--to=markdown-smart", "--standalone"])

md_md = simple_pandoc_output_rule(_md_md_impl, "md")

def _md_txt_impl(ctx):
    return simple_pandoc_output_impl(ctx, "txt", [], ["--to=plain", "--standalone"])

md_txt = simple_pandoc_output_rule(_md_txt_impl, "txt")
