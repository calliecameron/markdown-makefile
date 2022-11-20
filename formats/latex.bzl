"""Rules for latex-based outputs."""

load("//core:build_defs.bzl", "MdLibraryInfo")
load(":helpers.bzl", "simple_pandoc_output_impl")

_LATEX_VARS = [
    "--variable=fontsize:12pt",
    "--variable=papersize:a4",
    "--variable=documentclass:article",
    "--variable=geometry:a4paper",
    "--variable=strikeout",
    "--variable=verbatim-in-note",
    "--variable=linkcolor:black",
    "--variable=mainfont:TeX Gyre Termes",
    "--variable=indent",
]

MdTexIntermediateInfo = provider(
    "Info for tex intermediate files",
    fields = {
        "header": "Expanded tex header",
        "before": "Expanded tex before",
    },
)

def _md_tex_intermediate_impl(ctx):
    def gen_intermediate(output, template, name):
        ctx.actions.run(
            outputs = [output],
            inputs = [ctx.attr.lib[MdLibraryInfo].output, template[DefaultInfo].files.to_list()[0]],
            executable = "pandoc",
            arguments = [
                "--from=json",
                "--to=latex",
                "--template=" + template[DefaultInfo].files.to_list()[0].path,
                "--fail-if-warnings",
                "--output=" + output.path,
            ] + _LATEX_VARS + [
                ctx.attr.lib[MdLibraryInfo].output.path,
            ],
            progress_message = "%{label}: generating latex " + name,
        )

    header = ctx.actions.declare_file(ctx.label.name + "_header.tex")
    gen_intermediate(header, ctx.attr._header_template, "header")

    before = ctx.actions.declare_file(ctx.label.name + "_before.tex")
    gen_intermediate(before, ctx.attr._before_template, "before")

    return [
        DefaultInfo(files = depset([header, before])),
        MdTexIntermediateInfo(header = header, before = before),
        ctx.attr.lib[MdLibraryInfo],
    ]

md_tex_intermediate = rule(
    implementation = _md_tex_intermediate_impl,
    doc = "md_tex_intermediate generates intermediate files for latex-based outputs",
    attrs = {
        "lib": attr.label(
            providers = [MdLibraryInfo],
            doc = "An md_library target.",
        ),
        "_header_template": attr.label(
            default = "//formats:tex_header_template",
        ),
        "_before_template": attr.label(
            default = "//formats:tex_before_template",
        ),
    },
)

def _tex_output_impl(ctx, ext, to, extra_args):
    return simple_pandoc_output_impl(
        ctx,
        ext,
        [
            ctx.attr.intermediate[MdTexIntermediateInfo].header,
            ctx.attr.intermediate[MdTexIntermediateInfo].before,
            ctx.attr._template[DefaultInfo].files.to_list()[0],
        ],
        [
            "--to=" + to,
            "--include-in-header=" + ctx.attr.intermediate[MdTexIntermediateInfo].header.path,
            "--include-before-body=" + ctx.attr.intermediate[MdTexIntermediateInfo].before.path,
            "--template=" + ctx.attr._template[DefaultInfo].files.to_list()[0].path,
        ] + extra_args + _LATEX_VARS,
        ctx.attr.intermediate,
        ctx.attr._write_open_script,
    )

def _tex_output_rule(impl, ext):
    return rule(
        implementation = impl,
        executable = True,
        doc = "md_" + ext + " generates " + ext + " output from an md_library.",
        attrs = {
            "intermediate": attr.label(
                providers = [MdLibraryInfo, MdTexIntermediateInfo],
                doc = "An md_tex_intermediate target.",
            ),
            "_write_open_script": attr.label(
                default = "//formats:write_open_script",
            ),
            "_template": attr.label(
                default = "//formats:tex_template",
            ),
        },
    )

def _md_tex_impl(ctx):
    return _tex_output_impl(
        ctx,
        "tex",
        "latex",
        ["--standalone"],
    )

md_tex = _tex_output_rule(_md_tex_impl, "tex")

def _md_pdf_impl(ctx):
    return _tex_output_impl(
        ctx,
        "pdf",
        "pdf",
        ["--pdf-engine=/usr/bin/xelatex"],
    )

md_pdf = _tex_output_rule(_md_pdf_impl, "pdf")
