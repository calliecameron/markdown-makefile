"""Rules for latex-based outputs."""

load("//core:build_defs.bzl", "MdLibraryInfo")
load(":helpers.bzl", "doc_for_ext", "expand_locations", "pandoc", "pandoc_script", "simple_pandoc_output_impl", "timestamp_override", "write_open_script")

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
        pandoc(
            ctx,
            "",
            "latex",
            [template],
            ["--template=" + template.path] +
            _LATEX_VARS + expand_locations(ctx, ctx.attr.lib, ctx.attr.extra_pandoc_flags),
            {},
            ctx.attr.lib,
            output,
            "generating latex " + name,
        )

    header = ctx.actions.declare_file(ctx.label.name + "_header.tex")
    gen_intermediate(header, ctx.file._header_template, "header")

    before = ctx.actions.declare_file(ctx.label.name + "_before.tex")
    gen_intermediate(before, ctx.file._before_template, "before")

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
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "_pandoc": pandoc_script(),
        "_header_template": attr.label(
            allow_single_file = True,
            default = "//formats:header_template.tex",
        ),
        "_before_template": attr.label(
            allow_single_file = True,
            default = "//formats:before_template.tex",
        ),
    },
)

def _tex_output_impl(ctx, ext, to, extra_args):
    return simple_pandoc_output_impl(
        ctx,
        ext,
        to,
        [
            ctx.attr.intermediate[MdTexIntermediateInfo].header,
            ctx.attr.intermediate[MdTexIntermediateInfo].before,
            ctx.file._template,
            ctx.file._filter,
        ],
        [
            "--include-in-header=" + ctx.attr.intermediate[MdTexIntermediateInfo].header.path,
            "--include-before-body=" + ctx.attr.intermediate[MdTexIntermediateInfo].before.path,
            "--template=" + ctx.file._template.path,
            "--lua-filter=" + ctx.file._filter.path,
        ] + extra_args + _LATEX_VARS + expand_locations(ctx, ctx.attr.intermediate, ctx.attr.extra_pandoc_flags),
        timestamp_override(ctx),
        ctx.attr.intermediate,
        ctx.attr._write_open_script,
    )

def _tex_output_rule(impl, ext):
    return rule(
        implementation = impl,
        executable = True,
        doc = doc_for_ext(ext),
        attrs = {
            "intermediate": attr.label(
                providers = [MdLibraryInfo, MdTexIntermediateInfo],
                doc = "An md_tex_intermediate target.",
            ),
            "extra_pandoc_flags": attr.string_list(
                doc = "Extra flags to pass to pandoc",
            ),
            "timestamp_override": attr.string(),
            "out": attr.output(),
            "_pandoc": pandoc_script(),
            "_write_open_script": write_open_script(),
            "_template": attr.label(
                allow_single_file = True,
                default = "//formats:template.tex",
            ),
            "_filter": attr.label(
                allow_single_file = True,
                default = "//formats:latex_filter.lua",
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
