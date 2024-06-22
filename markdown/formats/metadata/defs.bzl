"""Rules for metadata outputs."""

load("//markdown/core:defs.bzl", "MdFileInfo", "MdGroupInfo")
load(
    "//markdown/formats:lib.bzl",
    "default_info",
    "docstring",
    "progress_message",
    "tools",
    "write_open_script",
)

def _copy_impl(ctx, ext, input):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [input],
        executable = "cp",
        arguments = [input.path, output.path],
        progress_message = progress_message(ext),
    )

    script = write_open_script(
        ctx = ctx,
        ext = ext,
        file_to_open = output,
    )

    return [
        default_info(ctx, output, script),
    ]

def _md_metadata_json_impl(ctx):
    return _copy_impl(
        ctx = ctx,
        ext = "metadata.json",
        input = ctx.attr.file[MdFileInfo].metadata,
    )

md_metadata_json = rule(
    implementation = _md_metadata_json_impl,
    executable = True,
    doc = docstring("metadata.json"),
    attrs = {
                "file": attr.label(
                    providers = [MdFileInfo],
                    doc = "An md_file target.",
                ),
                "out": attr.output(),
            } |
            tools.write_open_script.attr,
)

def _md_deps_metadata_json_impl(ctx):
    return _copy_impl(
        ctx = ctx,
        ext = "deps_metadata.json",
        input = ctx.attr.group[MdGroupInfo].metadata,
    )

md_deps_metadata_json = rule(
    implementation = _md_deps_metadata_json_impl,
    executable = True,
    doc = docstring("deps_metadata.json"),
    attrs = {
                "group": attr.label(
                    providers = [MdGroupInfo],
                    doc = "An md_group target.",
                ),
                "out": attr.output(),
            } |
            tools.write_open_script.attr,
)
