"""Rules for metadata outputs."""

load("//markdown/core:defs.bzl", "MdFileInfo", "MdGroupInfo")
load(
    "//markdown/formats:lib.bzl",
    "default_info_for_ext",
    "doc_for_ext",
    "open_script",
    "write_open_script",
)

def _md_metadata_json_impl(ctx):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.file[MdFileInfo].metadata],
        executable = "cp",
        arguments = [ctx.attr.file[MdFileInfo].metadata.path, output.path],
        progress_message = "%{label}: generating metadata.json output",
    )

    script = open_script(ctx, "metadata.json", output, ctx.executable._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_metadata_json = rule(
    implementation = _md_metadata_json_impl,
    executable = True,
    doc = doc_for_ext("metadata.json"),
    attrs = {
        "file": attr.label(
            providers = [MdFileInfo],
            doc = "An md_file target.",
        ),
        "out": attr.output(),
        "_write_open_script": write_open_script(),
    },
)

def _md_deps_metadata_json_impl(ctx):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.group[MdGroupInfo].metadata],
        executable = "cp",
        arguments = [ctx.attr.group[MdGroupInfo].metadata.path, output.path],
        progress_message = "%{label}: generating deps_metadata.json output",
    )

    script = open_script(ctx, "deps_metadata.json", output, ctx.executable._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_deps_metadata_json = rule(
    implementation = _md_deps_metadata_json_impl,
    executable = True,
    doc = doc_for_ext("deps_metadata.json"),
    attrs = {
        "group": attr.label(
            providers = [MdGroupInfo],
            doc = "An md_group target.",
        ),
        "out": attr.output(),
        "_write_open_script": write_open_script(),
    },
)
