"""Rules for ebook outputs."""

load("//markdown/core:defs.bzl", "MdLibraryInfo")
load(
    "//markdown/formats:helpers.bzl",
    "add_title_arg",
    "add_title_filter",
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
        [ctx.file._css, ctx.file._add_title],
        [
            "--css=" + ctx.file._css.path,
            add_title_arg(ctx),
        ] + expand_locations(ctx, ctx.attr.lib, ctx.attr.extra_pandoc_flags),
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
            allow_single_file = True,
            default = "//markdown/formats/ebook:epub.css",
        ),
        "_add_title": add_title_filter(),
        "_pandoc": pandoc_script(),
        "_pandoc_bin": pandoc_bin(),
        "_zip_cleaner": zip_cleaner_script(),
        "_write_open_script": write_open_script(),
    },
)

def _md_mobi_impl(ctx):
    output = ctx.outputs.out
    ctx.actions.run(
        outputs = [output],
        inputs = [
            ctx.attr.epub[MdEpubInfo].output,
            ctx.attr._ebook_convert_bin.files_to_run.executable,
        ],
        executable = ctx.attr._ebook_convert[DefaultInfo].files_to_run,
        arguments = [
            ctx.attr._ebook_convert_bin.files_to_run.executable.path,
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
            default = "//markdown/formats/ebook:ebook_convert",
        ),
        "_ebook_convert_bin": attr.label(
            default = "//markdown/external:ebook_convert",
        ),
        "_write_open_script": write_open_script(),
    },
)
