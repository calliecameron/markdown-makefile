"""Rules for word-processor outputs."""

load("//core:build_defs.bzl", "MdLibraryInfo")
load(":helpers.bzl", "default_info_for_ext", "doc_for_ext", "expand_locations", "open_script", "pandoc", "pandoc_script", "timestamp_override", "write_open_script", "zip_cleaner", "zip_cleaner_script")

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
    zip_cleaner(ctx, intermediate, output, ctx.attr._zip_cleaner)

    script = open_script(ctx, "odt", output, ctx.attr._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_odt = rule(
    implementation = _md_odt_impl,
    executable = True,
    doc = doc_for_ext("odt"),
    attrs = {
        "lib": attr.label(
            providers = [MdLibraryInfo],
            doc = "An md_library target.",
        ),
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_pandoc": pandoc_script(),
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
            ctx.attr._template[DefaultInfo].files.to_list()[0],
            ctx.attr._filter[DefaultInfo].files.to_list()[0],
        ],
        [
            "--reference-doc=" + ctx.attr._template[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._filter[DefaultInfo].files.to_list()[0].path,
        ] + expand_locations(ctx, ctx.attr.lib, ctx.attr.extra_pandoc_flags),
        timestamp_override(ctx),
        ctx.attr.lib,
        intermediate,
    )

    output = ctx.outputs.out
    zip_cleaner(ctx, intermediate, output, ctx.attr._zip_cleaner)

    script = open_script(ctx, "docx", output, ctx.attr._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
        MdDocxInfo(output = output),
        ctx.attr.lib[MdLibraryInfo],
    ]

md_docx = rule(
    implementation = _md_docx_impl,
    executable = True,
    doc = doc_for_ext("docx"),
    attrs = {
        "lib": attr.label(
            providers = [MdLibraryInfo],
            doc = "An md_library target.",
        ),
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_template": attr.label(
            default = "//formats:reference_docx",
        ),
        "_filter": attr.label(
            default = "//formats:docx_filter",
        ),
        "_pandoc": pandoc_script(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_doc_impl(ctx):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.docx[MdDocxInfo].output],
        executable = ctx.attr._unoconv[DefaultInfo].files_to_run,
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

    script = open_script(ctx, "doc", output, ctx.attr._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_doc = rule(
    implementation = _md_doc_impl,
    executable = True,
    doc = doc_for_ext("doc"),
    attrs = {
        "docx": attr.label(
            providers = [MdLibraryInfo, MdDocxInfo],
            doc = "An md_docx target.",
        ),
        "out": attr.output(),
        "_unoconv": attr.label(
            default = "//formats:unoconv",
        ),
        "_write_open_script": write_open_script(),
    },
)

def _md_ms_docx_impl(ctx):
    metadata = ctx.actions.declare_file(ctx.label.name + "_ms_metadata.json")
    ctx.actions.run(
        outputs = [metadata],
        inputs = [ctx.attr.lib[MdLibraryInfo].metadata],
        executable = ctx.attr._ms_metadata[DefaultInfo].files_to_run,
        arguments = [
            ctx.attr.lib[MdLibraryInfo].metadata.path,
            metadata.path,
        ],
        progress_message = "%{label}: generating ms metadata",
    )

    intermediate_md = ctx.actions.declare_file(ctx.label.name + "_ms_intermediate.md")
    pandoc(
        ctx,
        "",
        "markdown-smart",
        [ctx.attr.lib[MdLibraryInfo].output, metadata],
        [
            "--metadata-file=" + metadata.path,
            "--standalone",
        ],
        {},
        ctx.attr.lib,
        intermediate_md,
        "generating ms intermediate markdown",
    )

    intermediate_docx = ctx.actions.declare_file(ctx.label.name + "_ms_intermediate.docx")
    env = timestamp_override(ctx)
    env["PANDOC"] = ctx.attr._pandoc[DefaultInfo].files_to_run.executable.path
    ctx.actions.run(
        outputs = [intermediate_docx],
        inputs = [
            ctx.attr._md2short[DefaultInfo].files.to_list()[0],
            intermediate_md,
            ctx.attr._filter[DefaultInfo].files.to_list()[0],
            ctx.attr._pandoc[DefaultInfo].files_to_run.executable,
        ],
        executable = ctx.attr._ms_docx[DefaultInfo].files_to_run,
        arguments = [
            ctx.attr._md2short[DefaultInfo].files.to_list()[0].path,
            "--overwrite",
            "--modern",
            "--output",
            intermediate_docx.path,
            "--lua-filter=" + ctx.attr._filter[DefaultInfo].files.to_list()[0].path,
            intermediate_md.path,
        ],
        env = env,
        progress_message = "%{label}: generating ms.docx output",
    )

    output = ctx.outputs.out
    zip_cleaner(ctx, intermediate_docx, output, ctx.attr._zip_cleaner)

    script = open_script(ctx, "ms.docx", output, ctx.attr._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
    ]

md_ms_docx = rule(
    implementation = _md_ms_docx_impl,
    executable = True,
    doc = doc_for_ext("ms.docx"),
    attrs = {
        "lib": attr.label(
            providers = [MdLibraryInfo],
            doc = "An md_library target.",
        ),
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_ms_metadata": attr.label(
            default = "//formats:ms_metadata",
        ),
        "_ms_docx": attr.label(
            default = "//formats:ms_docx",
        ),
        "_md2short": attr.label(
            default = "@prosegrinder_pandoc_templates//:md2short",
        ),
        "_filter": attr.label(
            default = "//formats:ms_docx_filter",
        ),
        "_pandoc": pandoc_script(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)
