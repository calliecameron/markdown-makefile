"""Rules for latex-based outputs."""

load("//markdown/private/core:defs.bzl", "MdFileInfo")
load(
    "//markdown/private/formats:lib.bzl",
    "docstring",
    "expand_locations",
    "filters",
    "pandoc",
    "simple_pandoc_output_impl",
    "timestamp_override",
    "tools",
)

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
            ctx = ctx,
            extension = "",
            variant = None,
            to_format = "latex",
            inputs = [template],
            args = ["--template=" + template.path] +
                   _LATEX_VARS + expand_locations(ctx, ctx.attr.file, ctx.attr.extra_pandoc_flags),
            env = {},
            file = ctx.attr.file,
            output = output,
            progress_message = "generating latex " + name,
        )

    header = ctx.actions.declare_file(ctx.label.name + "_header.tex")
    gen_intermediate(header, ctx.file._header_template, "header")

    before = ctx.actions.declare_file(ctx.label.name + "_before.tex")
    gen_intermediate(before, ctx.file._before_template, "before")

    return [
        DefaultInfo(files = depset([header, before])),
        MdTexIntermediateInfo(header = header, before = before),
        ctx.attr.file[MdFileInfo],
    ]

md_tex_intermediate = rule(
    implementation = _md_tex_intermediate_impl,
    doc = "md_tex_intermediate generates intermediate files for latex-based outputs",
    attrs = {
                "file": attr.label(
                    providers = [MdFileInfo],
                    doc = "An md_file target.",
                ),
                "extra_pandoc_flags": attr.string_list(
                    doc = "Extra flags to pass to pandoc",
                ),
                "_header_template": attr.label(
                    allow_single_file = True,
                    default = "//markdown/private/formats/latex:header_template.tex",
                ),
                "_before_template": attr.label(
                    allow_single_file = True,
                    default = "//markdown/private/formats/latex:before_template.tex",
                ),
            } |
            tools.pandoc.attr,
)

def _tex_output_impl(ctx, extension, to, extra_args):
    return simple_pandoc_output_impl(
        ctx = ctx,
        extension = extension,
        variant = None,
        to_format = to,
        inputs = [
            ctx.attr.intermediate[MdTexIntermediateInfo].header,
            ctx.attr.intermediate[MdTexIntermediateInfo].before,
            ctx.file._template,
            filters.add_subject.file(ctx),
            filters.cleanup_metadata.file(ctx),
            filters.remove_collection_separators_before_headers.file(ctx),
            ctx.file._latex_filter,
        ],
        args = [
            "--include-in-header=" + ctx.attr.intermediate[MdTexIntermediateInfo].header.path,
            "--include-before-body=" + ctx.attr.intermediate[MdTexIntermediateInfo].before.path,
            "--template=" + ctx.file._template.path,
            filters.add_subject.arg(ctx),
            filters.cleanup_metadata.arg(ctx),
            filters.remove_collection_separators_before_headers.arg(ctx),
            "--lua-filter=" + ctx.file._latex_filter.path,
        ] + extra_args + _LATEX_VARS + expand_locations(ctx, ctx.attr.intermediate, ctx.attr.extra_pandoc_flags),
        env = timestamp_override.env(ctx),
        file = ctx.attr.intermediate,
    )

def _tex_output_rule(impl, extension):
    return rule(
        implementation = impl,
        executable = True,
        doc = docstring(extension, None),
        attrs = {
                    "intermediate": attr.label(
                        providers = [MdFileInfo, MdTexIntermediateInfo],
                        doc = "An md_tex_intermediate target.",
                    ),
                    "extra_pandoc_flags": attr.string_list(
                        doc = "Extra flags to pass to pandoc",
                    ),
                    "out": attr.output(),
                    "_template": attr.label(
                        allow_single_file = True,
                        default = "//markdown/private/formats/latex:template.tex",
                    ),
                    "_latex_filter": attr.label(
                        allow_single_file = True,
                        default = "//markdown/private/formats/latex:latex_filter.lua",
                    ),
                } |
                tools.pandoc.attr |
                tools.write_open_script.attr |
                filters.add_subject.attr |
                filters.cleanup_metadata.attr |
                filters.remove_collection_separators_before_headers.attr |
                timestamp_override.attr,
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
