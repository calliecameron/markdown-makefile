"""Collection rules."""

load("//markdown_makefile/core:core.bzl", "MdLibraryInfo")

def _md_collection_src_impl(ctx):
    output = ctx.actions.declare_file(ctx.label.name + ".md")
    dep_metadata_args = []
    for dep in ctx.attr.deps:
        dep_metadata_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].metadata.path]
    ctx.actions.run(
        outputs = [output],
        inputs = [dep[MdLibraryInfo].metadata for dep in ctx.attr.deps],
        executable = ctx.attr._collection_src[DefaultInfo].files_to_run,
        arguments = dep_metadata_args + [ctx.attr.title, ctx.attr.author, ctx.attr.date, output.path],
        progress_message = "%{label}: generating collection markdown",
    )

    return [
        DefaultInfo(files = depset([output])),
    ]

md_collection_src = rule(
    implementation = _md_collection_src_impl,
    doc = "md_collection_src collects md_library targets into a single doc.",
    attrs = {
        "title": attr.string(
            mandatory = True,
        ),
        "author": attr.string(
            mandatory = True,
        ),
        "date": attr.string(),
        "deps": attr.label_list(
            allow_empty = False,
            providers = [MdLibraryInfo],
            doc = "md_library targets to include in the collection.",
        ),
        "_collection_src": attr.label(
            default = "//markdown_makefile/collection:collection_src",
        ),
    },
)
