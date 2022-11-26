"""Rules for ebook outputs."""

load("//core:build_defs.bzl", "MdLibraryInfo")
load(":helpers.bzl", "default_info_for_ext", "doc_for_ext", "expand_locations", "open_script", "pandoc", "pandoc_script", "timestamp_override", "write_open_script", "zip_cleaner", "zip_cleaner_script")

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
        ["--css=" + ctx.attr._css[DefaultInfo].files.to_list()[0].path] + expand_locations(ctx, ctx.attr.lib, ctx.attr.extra_pandoc_flags),
        timestamp_override(ctx),
        ctx.attr.lib,
        intermediate,
    )

    output = ctx.outputs.out
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
        "out": attr.output(),
        "timestamp_override": attr.string(),
        "_css": attr.label(
            default = "//formats:epub_css",
        ),
        "_pandoc": pandoc_script(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_mobi_impl(ctx):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [ctx.attr.epub[MdEpubInfo].output],
        executable = ctx.attr._ebook_convert[DefaultInfo].files_to_run,
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
        "out": attr.output(),
        "_ebook_convert": attr.label(
            default = "//formats:ebook_convert",
        ),
        "_write_open_script": write_open_script(),
    },
)
