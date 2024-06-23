"""Rules for text outputs."""

load(
    "//markdown/formats:lib.bzl",
    "filters",
    "simple_pandoc_output_impl",
    "simple_pandoc_output_rule",
)

def _md_md_impl(ctx):
    return simple_pandoc_output_impl(
        ctx = ctx,
        extension = "md",
        variant = None,
        to_format = "markdown-smart",
        inputs = [
            filters.cleanup_metadata.file(ctx),
            filters.remove_paragraph_annotations.file(ctx),
            filters.remove_collection_separators.file(ctx),
        ],
        args = [
            "--standalone",
            "--wrap=none",
            filters.cleanup_metadata.arg(ctx),
            filters.remove_paragraph_annotations.arg(ctx),
            filters.remove_collection_separators.arg(ctx),
        ],
        env = {},
        file = ctx.attr.file,
    )

md_md = simple_pandoc_output_rule(
    impl = _md_md_impl,
    extension = "md",
    variant = None,
    filters = [
        filters.cleanup_metadata,
        filters.remove_paragraph_annotations,
        filters.remove_collection_separators,
    ],
)

def _md_txt_impl(ctx):
    return simple_pandoc_output_impl(
        ctx = ctx,
        extension = "txt",
        variant = None,
        to_format = "plain",
        inputs = [
            filters.cleanup_metadata.file(ctx),
            filters.remove_collection_separators.file(ctx),
        ],
        args = [
            "--standalone",
            "--wrap=none",
            filters.cleanup_metadata.arg(ctx),
            filters.remove_collection_separators.arg(ctx),
        ],
        env = {},
        file = ctx.attr.file,
    )

md_txt = simple_pandoc_output_rule(
    impl = _md_txt_impl,
    extension = "txt",
    variant = None,
    filters = [
        filters.cleanup_metadata,
        filters.remove_collection_separators,
    ],
)
