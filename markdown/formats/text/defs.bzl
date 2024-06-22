"""Rules for text outputs."""

load(
    "//markdown/formats:lib.bzl",
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
        ctx.attr.file,
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
        ctx.attr.file,
        ctx.executable._write_open_script,
    )

md_txt = simple_pandoc_output_rule(_md_txt_impl, "txt")
