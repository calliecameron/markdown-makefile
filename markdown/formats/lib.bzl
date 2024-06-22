"""Helpers for output formats."""

load("//markdown/core:defs.bzl", "MdFileInfo")

tools = struct(
    pandoc = struct(
        attr = {
            "_pandoc_wrapped": attr.label(
                default = "//markdown/external:pandoc",
                executable = True,
                cfg = "exec",
            ),
            "_pandoc": attr.label(
                default = "//markdown/formats:pandoc",
                executable = True,
                cfg = "exec",
            ),
        },
        executable = lambda ctx: ctx.executable._pandoc,
        wrapped_executable = lambda ctx: ctx.executable._pandoc_wrapped,
    ),
    write_open_script = struct(
        attr = {
            "_write_open_script": attr.label(
                default = "//markdown/formats:write_open_script",
                executable = True,
                cfg = "exec",
            ),
        },
        executable = lambda ctx: ctx.executable._write_open_script,
    ),
    zip_cleaner = struct(
        attr = {
            "_zip_cleaner": attr.label(
                default = "//markdown/formats:zip_cleaner",
                executable = True,
                cfg = "exec",
            ),
        },
        executable = lambda ctx: ctx.executable._zip_cleaner,
    ),
)

filters = struct(
    add_title = struct(
        attr = {
            "_add_title": attr.label(
                allow_single_file = True,
                default = "//markdown/formats:add_title.lua",
            ),
        },
        file = lambda ctx: ctx.file._add_title,
        arg = lambda ctx: "--lua-filter=" + ctx.file._add_title.path,
    ),
    remove_paragraph_annotations = struct(
        attr = {
            "_remove_paragraph_annotations": attr.label(
                allow_single_file = True,
                default = "//markdown/formats:remove_paragraph_annotations.lua",
            ),
        },
        file = lambda ctx: ctx.file._remove_paragraph_annotations,
        arg = lambda ctx: "--lua-filter=" + ctx.file._remove_paragraph_annotations.path,
    ),
    remove_collection_separators = struct(
        attr = {
            "_remove_collection_separators": attr.label(
                allow_single_file = True,
                default = "//markdown/formats:remove_collection_separators.lua",
            ),
        },
        file = lambda ctx: ctx.file._remove_collection_separators,
        arg = lambda ctx: "--lua-filter=" + ctx.file._remove_collection_separators.path,
    ),
    remove_collection_separators_before_headers = struct(
        attr = {
            "_remove_collection_separators_before_headers": attr.label(
                allow_single_file = True,
                default = "//markdown/formats:remove_collection_separators_before_headers.lua",
            ),
        },
        file = lambda ctx: ctx.file._remove_collection_separators_before_headers,
        arg = lambda ctx: "--lua-filter=" + ctx.file._remove_collection_separators_before_headers.path,
    ),
)

def _timestamp_override(ctx):
    env = {}
    if ctx.attr.timestamp_override:
        env["SOURCE_DATE_EPOCH"] = ctx.attr.timestamp_override
    return env

timestamp_override = struct(
    attr = {
        "timestamp_override": attr.string(),
    },
    env = _timestamp_override,
)

def expand_locations(ctx, file, args):
    data = file[MdFileInfo].data.to_list()
    return [ctx.expand_location(arg, targets = data) for arg in args]

def docstring(ext):
    return "md_" + ext + " generates " + ext + " output from an md_file."

def _progress_message_without_label(ext):
    return "generating " + ext + " output"

def progress_message(ext):
    return "%{label}: " + _progress_message_without_label(ext)

def default_info(ctx, output, script):
    return DefaultInfo(
        files = depset([output, script]),
        runfiles = ctx.runfiles(files = [output]),
        executable = script,
    )

def write_open_script(ctx, ext, file_to_open):
    script = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.run(
        outputs = [script],
        inputs = [file_to_open],
        executable = tools.write_open_script.executable(ctx),
        arguments = [ctx.workspace_name, file_to_open.short_path, script.path],
        progress_message = "%{label}: generating " + ext + " open script",
    )
    return script

def clean_zip(ctx, in_file, out_file):
    ctx.actions.run(
        outputs = [out_file],
        inputs = [in_file],
        executable = tools.zip_cleaner.executable(ctx),
        arguments = [
            in_file.path,
            out_file.path,
        ],
        progress_message = "%{label}: cleaining zip file",
    )

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
        progress_message = _progress_message_without_label(ext)
    progress_message = "%{label}: " + progress_message
    data_inputs = []
    for target in file[MdFileInfo].data.to_list():
        data_inputs += target.files.to_list()

    ctx.actions.run(
        outputs = [output],
        inputs = [
            file[MdFileInfo].output,
            tools.pandoc.wrapped_executable(ctx),
        ] + data_inputs + inputs,
        executable = tools.pandoc.executable(ctx),
        arguments = [
            tools.pandoc.wrapped_executable(ctx).path,
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

def simple_pandoc_output_impl(ctx, ext, to_format, inputs, args, env, file):
    output = ctx.outputs.out
    pandoc(
        ctx = ctx,
        ext = ext,
        to_format = to_format,
        inputs = inputs,
        args = args + expand_locations(ctx, file, ctx.attr.extra_pandoc_flags),
        env = env,
        file = file,
        output = output,
    )
    script = write_open_script(
        ctx = ctx,
        ext = ext,
        file_to_open = output,
    )

    return [default_info(ctx, output, script)]

def simple_pandoc_output_rule(impl, ext, filters = None):
    attrs = {
        "file": attr.label(
            providers = [MdFileInfo],
            doc = "An md_file target.",
        ),
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "out": attr.output(),
    } | tools.pandoc.attr | tools.write_open_script.attr

    for filter in filters or []:
        attrs |= filter.attr

    return rule(
        implementation = impl,
        executable = True,
        doc = docstring(ext),
        attrs = attrs,
    )
