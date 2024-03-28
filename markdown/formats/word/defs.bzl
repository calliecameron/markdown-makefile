"""Rules for word-processor outputs."""

load("//markdown/core:defs.bzl", "MdFileInfo")
load(
    "//markdown/formats:helpers.bzl",
    "default_info_for_ext",
    "doc_for_ext",
    "expand_locations",
    "open_script",
    "pandoc",
    "pandoc_bin",
    "pandoc_script",
    "timestamp_override",
    "write_open_script",
    "zip_cleaner",
    "zip_cleaner_script",
)

MdDocxInfo = provider(
    "Info for docx output",
    fields = {
        "output": "Docx file",
    },
)

def _md_odt_impl(ctx):
    intermediate = ctx.actions.declare_file(ctx.label.name + "_intermediate.odt")
    pandoc(
        ctx,
        "odt",
        "odt",
        [],
        expand_locations(ctx, ctx.attr.lib, ctx.attr.extra_pandoc_flags),
        timestamp_override(ctx),
        ctx.attr.lib,
        intermediate,
    )

    output = ctx.outputs.out
    zip_cleaner(ctx, intermediate, output, ctx.executable._zip_cleaner)

    script = open_script(ctx, "odt", output, ctx.executable._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_odt = rule(
    implementation = _md_odt_impl,
    executable = True,
    doc = doc_for_ext("odt"),
    attrs = {
        "lib": attr.label(
            providers = [MdFileInfo],
            doc = "An md_file target.",
        ),
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_pandoc": pandoc_script(),
        "_pandoc_bin": pandoc_bin(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_docx_impl(ctx):
    intermediate = ctx.actions.declare_file(ctx.label.name + "_intermediate.docx")
    pandoc(
        ctx,
        "docx",
        "docx",
        [
            ctx.file._template,
            ctx.file._filter,
        ],
        [
            "--reference-doc=" + ctx.file._template.path,
            "--lua-filter=" + ctx.file._filter.path,
        ] + expand_locations(ctx, ctx.attr.lib, ctx.attr.extra_pandoc_flags),
        timestamp_override(ctx),
        ctx.attr.lib,
        intermediate,
    )

    output = ctx.outputs.out
    zip_cleaner(ctx, intermediate, output, ctx.executable._zip_cleaner)

    script = open_script(ctx, "docx", output, ctx.executable._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
        MdDocxInfo(output = output),
        ctx.attr.lib[MdFileInfo],
    ]

md_docx = rule(
    implementation = _md_docx_impl,
    executable = True,
    doc = doc_for_ext("docx"),
    attrs = {
        "lib": attr.label(
            providers = [MdFileInfo],
            doc = "An md_file target.",
        ),
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_template": attr.label(
            allow_single_file = True,
            default = "//markdown/formats/word:reference.docx",
        ),
        "_filter": attr.label(
            allow_single_file = True,
            default = "//markdown/formats/word:docx_filter.lua",
        ),
        "_pandoc": pandoc_script(),
        "_pandoc_bin": pandoc_bin(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_doc_impl(ctx):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.docx[MdDocxInfo].output],
        executable = ctx.executable._unoconv,
        arguments = [
            "--format",
            "doc",
            "--output",
            output.path,
            ctx.attr.docx[MdDocxInfo].output.path,
        ],
        env = {"HOME": "/tmp"},
        progress_message = "%{label}: generating doc output",
    )

    script = open_script(ctx, "doc", output, ctx.executable._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_doc = rule(
    implementation = _md_doc_impl,
    executable = True,
    doc = doc_for_ext("doc"),
    attrs = {
        "docx": attr.label(
            providers = [MdFileInfo, MdDocxInfo],
            doc = "An md_docx target.",
        ),
        "out": attr.output(),
        "_unoconv": attr.label(
            default = "//markdown/formats/word:unoconv",
            executable = True,
            cfg = "exec",
        ),
        "_write_open_script": write_open_script(),
    },
)

def _md_ms_docx_impl(ctx):
    metadata = ctx.actions.declare_file(ctx.label.name + "_ms_metadata.json")
    ctx.actions.run(
        outputs = [metadata],
        inputs = [ctx.attr.lib[MdFileInfo].metadata],
        executable = ctx.executable._ms_metadata,
        arguments = [
            ctx.attr.lib[MdFileInfo].metadata.path,
            metadata.path,
        ],
        progress_message = "%{label}: generating ms metadata",
    )

    intermediate_docx = ctx.actions.declare_file(ctx.label.name + "_ms_intermediate.docx")
    env = timestamp_override(ctx)
    env["PANDOC"] = ctx.executable._pandoc_bin.path
    data_inputs = []
    for target in ctx.attr.lib[MdFileInfo].data.to_list():
        data_inputs += target.files.to_list()
    ctx.actions.run(
        outputs = [intermediate_docx],
        inputs = data_inputs + [
            ctx.attr.lib[MdFileInfo].output,
            metadata,
            ctx.file._filter,
            ctx.executable._pandoc_bin,
        ],
        executable = ctx.executable._md2short,
        arguments = [
            "--overwrite",
            "--modern",
            "--from",
            "json",
            "--output",
            intermediate_docx.path,
            "--metadata-file=" + metadata.path,
            "--lua-filter=" + ctx.file._filter.path,
            ctx.attr.lib[MdFileInfo].output.path,
        ],
        env = env,
        progress_message = "%{label}: generating ms.docx output",
    )

    output = ctx.outputs.out
    zip_cleaner(ctx, intermediate_docx, output, ctx.executable._zip_cleaner)

    script = open_script(ctx, "ms.docx", output, ctx.executable._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_ms_docx = rule(
    implementation = _md_ms_docx_impl,
    executable = True,
    doc = doc_for_ext("ms.docx"),
    attrs = {
        "lib": attr.label(
            providers = [MdFileInfo],
            doc = "An md_file target.",
        ),
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_ms_metadata": attr.label(
            default = "//markdown/formats/word:ms_metadata",
            executable = True,
            cfg = "exec",
        ),
        "_md2short": attr.label(
            default = "//markdown/external:md2short",
            executable = True,
            cfg = "exec",
        ),
        "_filter": attr.label(
            allow_single_file = True,
            default = "//markdown/formats/word:ms_docx_filter.lua",
        ),
        "_pandoc_bin": pandoc_bin(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)
