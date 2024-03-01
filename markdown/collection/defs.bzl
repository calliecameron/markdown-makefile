"""Collection rules."""

load("//markdown/core:defs.bzl", "MdGroupInfo")

def _md_collection_src_impl(ctx):
    output = ctx.actions.declare_file(ctx.label.name + ".md")
    dep_args = []
    for dep in ctx.attr.deps[MdGroupInfo].deps:
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name]
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.deps[MdGroupInfo].metadata],
        executable = ctx.attr._collection_src[DefaultInfo].files_to_run,
        arguments = dep_args + [
            ctx.attr.title,
            ctx.attr.author,
            ctx.attr.date,
            ctx.attr.deps[MdGroupInfo].metadata.path,
            output.path,
        ],
        progress_message = "%{label}: generating collection markdown",
    )

    return [
        DefaultInfo(files = depset([output])),
    ]

md_collection_src = rule(
    implementation = _md_collection_src_impl,
    doc = "md_collection_src collects md_file targets into a single doc.",
    attrs = {
        "title": attr.string(
            mandatory = True,
        ),
        "author": attr.string(
            mandatory = True,
        ),
        "date": attr.string(),
        "deps": attr.label(
            providers = [MdGroupInfo],
            doc = "md_file targets to include in the collection.",
        ),
        "_collection_src": attr.label(
            default = "//markdown/collection:collection_src",
        ),
    },
)
