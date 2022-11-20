"""Rules for word-processor outputs."""

load("//core:build_defs.bzl", "MdLibraryInfo")
load(":helpers.bzl", "default_info_for_ext", "doc_for_ext", "open_script", "output_for_ext", "pandoc", "write_open_script", "zip_cleaner", "zip_cleaner_script")

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
        [],
        ctx.attr.lib,
        intermediate,
    )

    output = output_for_ext(ctx, "odt", ctx.attr.lib)
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
        ],
        ctx.attr.lib,
        intermediate,
    )

    output = output_for_ext(ctx, "docx", ctx.attr.lib)
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
        "_template": attr.label(
            default = "//formats:reference_docx",
        ),
        "_filter": attr.label(
            default = "//formats:docx_filter",
        ),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_doc_impl(ctx):
    output = output_for_ext(ctx, "doc", ctx.attr.docx)
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.docx[MdDocxInfo].output],
        executable = "unoconv",
        arguments = [
            "-f",
            "doc",
            "-o",
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
        "_write_open_script": write_open_script(),
    },
)
