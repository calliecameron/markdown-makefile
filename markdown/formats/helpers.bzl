"""Helpers for output formats."""

load("//markdown/core:defs.bzl", "MdFileInfo")

def expand_locations(ctx, lib, args):
    data = lib[MdFileInfo].data.to_list()
    return [ctx.expand_location(arg, targets = data) for arg in args]

def doc_for_ext(ext):
    return "md_" + ext + " generates " + ext + " output from an md_file."

def default_info_for_ext(ctx, output, script):
    return DefaultInfo(
        files = depset([output, script]),
        runfiles = ctx.runfiles(files = [output]),
        executable = script,
    )

def timestamp_override(ctx):
    env = {}
    if ctx.attr.timestamp_override:
        env["SOURCE_DATE_EPOCH"] = ctx.attr.timestamp_override
    return env

def pandoc_bin():
    return attr.label(
        default = "//markdown/external:pandoc",
    )

def pandoc_script():
    return attr.label(
        default = "//markdown/formats:pandoc",
    )

def write_open_script():
    return attr.label(
        default = "//markdown/formats:write_open_script",
    )

def zip_cleaner_script():
    return attr.label(
        default = "//markdown/formats:zip_cleaner",
    )

def open_script(ctx, ext, file, write_open_script):
    script = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.run(
        outputs = [script],
        inputs = [file],
        executable = write_open_script[DefaultInfo].files_to_run,
        arguments = [ctx.workspace_name, file.short_path, script.path],
        progress_message = "%{label}: generating " + ext + " open script",
    )
    return script

def add_title_filter():
    return attr.label(
        allow_single_file = True,
        default = "//markdown/formats:add_title.lua",
    )

def add_title_arg(ctx):
    return "--lua-filter=" + ctx.file._add_title.path

def pandoc(ctx, ext, to_format, inputs, args, env, lib, output, progress_message = None):
    """Run pandoc.

    Args:
        ctx: rule ctx.
        ext: file extension of the output format.
        to_format: pandoc output format.
        inputs: action inputs.
        args: extra action args.
        env: environment variables to pass to pandoc.
        lib: something that provides MdFileInfo.
        output: the output file.
        progress_message: message to display when running the action.
    """
    if not progress_message:
        progress_message = "generating " + ext + " output"
    progress_message = "%{label}: " + progress_message
    data_inputs = []
    for target in lib[MdFileInfo].data.to_list():
        data_inputs += target.files.to_list()

    ctx.actions.run(
        outputs = [output],
        inputs = [
            lib[MdFileInfo].output,
            ctx.attr._pandoc_bin.files_to_run.executable,
        ] + data_inputs + inputs,
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        arguments = [
            ctx.attr._pandoc_bin.files_to_run.executable.path,
            "--from=json",
            "--to=" + to_format,
            "--fail-if-warnings",
            "--output=" + output.path,
        ] + args + [
            lib[MdFileInfo].output.path,
        ],
        env = env,
        progress_message = progress_message,
    )

def pandoc_for_output(ctx, ext, to_format, inputs, args, env, lib):
    output = ctx.outputs.out
    pandoc(ctx, ext, to_format, inputs, args, env, lib, output)
    return output

def simple_pandoc_output_impl(ctx, ext, to_format, inputs, args, env, lib, write_open_script):
    file = pandoc_for_output(ctx, ext, to_format, inputs, args + expand_locations(ctx, lib, ctx.attr.extra_pandoc_flags), env, lib)
    script = open_script(ctx, ext, file, write_open_script)

    return [default_info_for_ext(ctx, file, script)]

def simple_pandoc_output_rule(impl, ext):
    return rule(
        implementation = impl,
        executable = True,
        doc = doc_for_ext(ext),
        attrs = {
            "lib": attr.label(
                providers = [MdFileInfo],
                doc = "An md_file target.",
            ),
            "extra_pandoc_flags": attr.string_list(
                doc = "Extra flags to pass to pandoc",
            ),
            "out": attr.output(),
            "_pandoc": pandoc_script(),
            "_pandoc_bin": pandoc_bin(),
            "_write_open_script": write_open_script(),
            "_add_title": add_title_filter(),
        },
    )

def zip_cleaner(ctx, in_file, out_file, script):
    ctx.actions.run(
        outputs = [out_file],
        inputs = [in_file],
        executable = script[DefaultInfo].files_to_run,
        arguments = [
            in_file.path,
            out_file.path,
        ],
        progress_message = "%{label}: cleaining zip file",
    )
