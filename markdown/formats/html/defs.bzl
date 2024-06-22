"""Rules for html outputs."""

load(
    "//markdown/formats:helpers.bzl",
    "add_title_arg",
    "remove_collection_separators_arg",
    "simple_pandoc_output_impl",
    "simple_pandoc_output_rule",
)

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
        ctx.attr.file,
        ctx.executable._write_open_script,
    )

md_html = simple_pandoc_output_rule(_md_html_impl, "html")
