"""Helpers for output formats."""

load("//core:core.bzl", "MdLibraryInfo")

def expand_locations(ctx, lib, args):
    data = lib[MdLibraryInfo].data.to_list()
    return [ctx.expand_location(arg, targets = data) for arg in args]

def doc_for_ext(ext):
    return "md_" + ext + " generates " + ext + " output from an md_library."

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

def pandoc_script():
    return attr.label(
        default = "@pandoc//:pandoc",
    )

def write_open_script():
    return attr.label(
        default = "//formats:write_open_script",
    )

def zip_cleaner_script():
    return attr.label(
        default = "//formats:zip_cleaner",
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

def pandoc(ctx, ext, to_format, inputs, args, env, lib, output, progress_message = None, include_system_path = False):
    """Run pandoc.

    Args:
        ctx: rule ctx.
        ext: file extension of the output format.
        to_format: pandoc output format.
        inputs: action inputs.
        args: extra action args.
        env: environment variables to pass to pandoc.
        lib: something that provides MdLibraryInfo.
        output: the output file.
        progress_message: message to display when running the action.
        include_system_path: include system dirs on PATH.
    """
    if not progress_message:
        progress_message = "generating " + ext + " output"
    progress_message = "%{label}: " + progress_message
    data_inputs = []
    for target in lib[MdLibraryInfo].data.to_list():
        data_inputs += target.files.to_list()

    if include_system_path:
        env["PATH"] = "/usr/bin"
    ctx.actions.run(
        outputs = [output],
        inputs = [lib[MdLibraryInfo].output] + data_inputs + inputs,
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        arguments = [
            "--from=json",
            "--to=" + to_format,
            "--fail-if-warnings",
            "--output=" + output.path,
        ] + args + [
            lib[MdLibraryInfo].output.path,
        ],
        env = env,
        progress_message = progress_message,
    )

def pandoc_for_output(ctx, ext, to_format, inputs, args, env, lib, include_system_path = False):
    output = ctx.outputs.out
    pandoc(ctx, ext, to_format, inputs, args, env, lib, output, include_system_path = include_system_path)
    return output

def simple_pandoc_output_impl(ctx, ext, to_format, inputs, args, env, lib, write_open_script, include_system_path = False):
    file = pandoc_for_output(ctx, ext, to_format, inputs, args + expand_locations(ctx, lib, ctx.attr.extra_pandoc_flags), env, lib, include_system_path = include_system_path)
    script = open_script(ctx, ext, file, write_open_script)

    return [default_info_for_ext(ctx, file, script)]

def simple_pandoc_output_rule(impl, ext):
    return rule(
        implementation = impl,
        executable = True,
        doc = doc_for_ext(ext),
        attrs = {
            "lib": attr.label(
                providers = [MdLibraryInfo],
                doc = "An md_library target.",
            ),
            "extra_pandoc_flags": attr.string_list(
                doc = "Extra flags to pass to pandoc",
            ),
            "out": attr.output(),
            "_pandoc": pandoc_script(),
            "_write_open_script": write_open_script(),
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
