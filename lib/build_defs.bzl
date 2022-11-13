# MdLibraryInfo = provider(
#     "Info from a markdown library.",
#     fields = {
#         "text": "Text of the library, in json format",
#         # "metadata": "",
#         # "dictionary": "",
#         # "versions": "",
#     },
# )

def _md_library_impl(ctx):
    # if ctx.file.src:
    #     src = ctx.file.src
    # else:
    #     src = ctx.actions.declare_file(ctx.label.name + ".md")

    # metadata = ctx.actions.declare_file(ctx.label.name + "_metadata.yml")
    # ctx.actions.run(
    #     outputs = [metadata],
    #     inputs = [ctx.info_file],
    #     executable = ctx.attr._gen_metadata[DefaultInfo].files_to_run,
    #     arguments = [ctx.info_file.path, ctx.label.package, metadata.path],
    # )

    raw_version = ctx.actions.declare_file(ctx.label.name + "_raw_version.json")
    ctx.actions.run(
        outputs = [raw_version],
        inputs = [ctx.info_file],
        executable = ctx.attr._raw_version[DefaultInfo].files_to_run,
        arguments = [ctx.info_file.path, raw_version.path, ctx.label.package],
    )

    # out = ctx.actions.declare_file(ctx.label.name + ".md")
    # ctx.actions.run(
    #     outputs = [out],
    #     inputs = [ctx.file.src],
    #     executable = "pandoc",
    #     arguments = ["-f", "markdown", "-t", "markdown", "-o", out.path, ctx.file.src.path],
    # )
    return [
        DefaultInfo(files = depset([raw_version])),
    ]

md_library = rule(
    implementation = _md_library_impl,
    attrs = {
        "src": attr.label(
            allow_single_file = [".md"],
            default = None,
        ),
        # "deps": attr.label_list(
        #     allow_empty = True,
        #     providers = [MdLibraryInfo],
        # ),
        "_raw_version": attr.label(
            default = "//lib:raw_version",
        ),
    },
)
