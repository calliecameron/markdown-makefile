"""Rules for ebook outputs."""

load("//core:build_defs.bzl", "MdLibraryInfo")
load(":helpers.bzl", "default_info_for_ext", "doc_for_ext", "open_script", "output_for_ext", "pandoc", "write_open_script", "zip_cleaner", "zip_cleaner_script")

MdEpubInfo = provider(
    "Info for epub output",
    fields = {
        "output": "Epub file",
    },
)

def _md_epub_impl(ctx):
    intermediate = ctx.actions.declare_file(ctx.label.name + "_intermediate.epub")
    pandoc(
        ctx,
        "epub",
        "epub",
        [ctx.attr._css[DefaultInfo].files.to_list()[0]],
        ["--css=" + ctx.attr._css[DefaultInfo].files.to_list()[0].path] + ctx.attr.extra_pandoc_flags,
        ctx.attr.lib,
        intermediate,
    )

    output = output_for_ext(ctx, "epub", ctx.attr.lib)
    zip_cleaner(ctx, intermediate, output, ctx.attr._zip_cleaner)

    script = open_script(ctx, "epub", output, ctx.attr._write_open_script)

    return [
        default_info_for_ext(ctx, output, script),
        MdEpubInfo(output = output),
        ctx.attr.lib[MdLibraryInfo],
    ]

md_epub = rule(
    implementation = _md_epub_impl,
    executable = True,
    doc = doc_for_ext("epub"),
    attrs = {
        "lib": attr.label(
            providers = [MdLibraryInfo],
            doc = "An md_library target.",
        ),
        "extra_pandoc_flags": attr.string_list(
            doc = "Extra flags to pass to pandoc",
        ),
        "_css": attr.label(
            default = "//formats:epub_css",
        ),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_mobi_impl(ctx):
    output = output_for_ext(ctx, "mobi", ctx.attr.epub)
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.epub[MdEpubInfo].output],
        executable = "ebook-convert",
        arguments = [
            ctx.attr.epub[MdEpubInfo].output.path,
            output.path,
        ],
        progress_message = "%{label}: generating mobi output",
    )

    script = open_script(ctx, "mobi", output, ctx.attr._write_open_script)

    return [default_info_for_ext(ctx, output, script)]

md_mobi = rule(
    implementation = _md_mobi_impl,
    executable = True,
    doc = doc_for_ext("mobi"),
    attrs = {
        "epub": attr.label(
            providers = [MdLibraryInfo, MdEpubInfo],
            doc = "An md_epub target.",
        ),
        "_write_open_script": write_open_script(),
    },
)
