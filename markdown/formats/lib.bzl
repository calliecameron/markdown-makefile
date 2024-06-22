"""Helpers for output formats."""

load("//markdown/core:defs.bzl", "MdFileInfo")

def expand_locations(ctx, file, args):
    data = file[MdFileInfo].data.to_list()
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
        executable = True,
        cfg = "exec",
    )

def pandoc_script():
    return attr.label(
        default = "//markdown/formats:pandoc",
        executable = True,
        cfg = "exec",
    )

def write_open_script():
    return attr.label(
        default = "//markdown/formats:write_open_script",
        executable = True,
        cfg = "exec",
    )

def zip_cleaner_script():
    return attr.label(
        default = "//markdown/formats:zip_cleaner",
        executable = True,
        cfg = "exec",
    )

def open_script(ctx, ext, file, write_open_script):
    script = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.run(
        outputs = [script],
        inputs = [file],
        executable = write_open_script,
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

def remove_paragraph_annotations_filter():
    return attr.label(
        allow_single_file = True,
        default = "//markdown/formats:remove_paragraph_annotations.lua",
    )

def remove_paragraph_annotations_arg(ctx):
    return "--lua-filter=" + ctx.file._remove_paragraph_annotations.path

def remove_collection_separators_filter():
    return attr.label(
        allow_single_file = True,
        default = "//markdown/formats:remove_collection_separators.lua",
    )

def remove_collection_separators_arg(ctx):
    return "--lua-filter=" + ctx.file._remove_collection_separators.path

def remove_collection_separators_before_headers_filter():
    return attr.label(
        allow_single_file = True,
        default = "//markdown/formats:remove_collection_separators_before_headers.lua",
    )

def remove_collection_separators_before_headers_arg(ctx):
    return "--lua-filter=" + ctx.file._remove_collection_separators_before_headers.path

def pandoc(ctx, ext, to_format, inputs, args, env, file, output, progress_message = None):
    """Run pandoc.

    Args:
        ctx: rule ctx.
        ext: file extension of the output format.
        to_format: pandoc output format.
        inputs: action inputs.
        args: extra action args.
        env: environment variables to pass to pandoc.
        file: something that provides MdFileInfo.
        output: the output file.
        progress_message: message to display when running the action.
    """
    if not progress_message:
        progress_message = "generating " + ext + " output"
    progress_message = "%{label}: " + progress_message
    data_inputs = []
    for target in file[MdFileInfo].data.to_list():
        data_inputs += target.files.to_list()

    ctx.actions.run(
        outputs = [output],
        inputs = [
            file[MdFileInfo].output,
            ctx.executable._pandoc_bin,
        ] + data_inputs + inputs,
        executable = ctx.executable._pandoc,
        arguments = [
            ctx.executable._pandoc_bin.path,
            "--from=json",
            "--to=" + to_format,
            "--fail-if-warnings",
            "--output=" + output.path,
        ] + args + [
            file[MdFileInfo].output.path,
        ],
        env = env,
        progress_message = progress_message,
    )

def pandoc_for_output(ctx, ext, to_format, inputs, args, env, file):
    output = ctx.outputs.out
    pandoc(ctx, ext, to_format, inputs, args, env, file, output)
    return output

def simple_pandoc_output_impl(ctx, ext, to_format, inputs, args, env, file, write_open_script):
    file = pandoc_for_output(ctx, ext, to_format, inputs, args + expand_locations(ctx, file, ctx.attr.extra_pandoc_flags), env, file)
    script = open_script(ctx, ext, file, write_open_script)

    return [default_info_for_ext(ctx, file, script)]

def simple_pandoc_output_rule(impl, ext):
    return rule(
        implementation = impl,
        executable = True,
        doc = doc_for_ext(ext),
        attrs = {
            "file": attr.label(
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
            "_remove_paragraph_annotations": remove_paragraph_annotations_filter(),
            "_remove_collection_separators": remove_collection_separators_filter(),
        },
    )

def zip_cleaner(ctx, in_file, out_file, script):
    ctx.actions.run(
        outputs = [out_file],
        inputs = [in_file],
        executable = script,
        arguments = [
            in_file.path,
            out_file.path,
        ],
        progress_message = "%{label}: cleaining zip file",
    )
