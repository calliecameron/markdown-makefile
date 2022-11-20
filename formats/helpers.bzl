"""Helpers for output formats."""

load("//core:build_defs.bzl", "MdLibraryInfo")

def open_script(ctx, file, ext):
    script = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.run(
        outputs = [script],
        inputs = [file],
        executable = ctx.attr._write_open_script[DefaultInfo].files_to_run,
        arguments = [ctx.workspace_name, file.short_path, script.path],
        progress_message = "%{label}: generating " + ext + " open script",
    )
    return script

def pandoc(ctx, inputs, args, ext):
    output = ctx.actions.declare_file("output/" + ctx.attr.lib[MdLibraryInfo].name + "." + ext)
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.lib[MdLibraryInfo].output] + inputs,
        executable = "pandoc",
        arguments = [
            "--from=json",
            "--fail-if-warnings",
            "--output=" + output.path,
        ] + args + [
            ctx.attr.lib[MdLibraryInfo].output.path,
        ],
        progress_message = "%{label}: generating " + ext + " output",
    )
    return output

def simple_pandoc_output_impl(ctx, ext, inputs, args):
    file = pandoc(ctx, inputs, args, ext)
    script = open_script(ctx, file, ext)

    return [
        DefaultInfo(
            files = depset([script]),
            runfiles = ctx.runfiles(files = [file]),
            executable = script,
        ),
    ]

def simple_pandoc_output_rule(impl, ext):
    return rule(
        implementation = impl,
        executable = True,
        doc = "md_" + ext + " generates " + ext + " output from an md_library.",
        attrs = {
            "lib": attr.label(
                providers = [MdLibraryInfo],
                doc = "An md_library target.",
            ),
            "_write_open_script": attr.label(
                default = "//formats:write_open_script",
            ),
        },
    )
