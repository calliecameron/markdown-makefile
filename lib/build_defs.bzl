"""Markdown rules."""

MdLibraryInfo = provider(
    "Info for a markdown library.",
    fields = {
        "output": "Compiled document, as json",
        "metadata": "Document metadata, as json",
    },
)

def _md_library_impl(ctx):
    raw_version = ctx.actions.declare_file(ctx.label.name + "_raw_version.json")
    ctx.actions.run(
        outputs = [raw_version],
        inputs = [ctx.info_file],
        executable = ctx.attr._raw_version[DefaultInfo].files_to_run,
        arguments = [ctx.info_file.path, raw_version.path, ctx.label.package],
    )

    dep_versions = ctx.actions.declare_file(ctx.label.name + "_dep_versions.json")
    base_metadata = ctx.actions.declare_file(ctx.label.name + "_base_metadata.json")
    dep_version_args = []
    for dep in ctx.attr.deps:
        dep_version_args += ["--dep_version_file", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].metadata.path]
    extra_args = []
    if ctx.attr.increment_included_headers:
        extra_args.append("--increment_included_headers")
    if ctx.attr.version_override:
        extra_args += ["--version_override", ctx.attr.version_override]
    ctx.actions.run(
        outputs = [dep_versions, base_metadata],
        inputs = [raw_version] + [dep[MdLibraryInfo].metadata for dep in ctx.attr.deps],
        executable = ctx.attr._base_metadata[DefaultInfo].files_to_run,
        arguments = dep_version_args + extra_args + [raw_version.path, dep_versions.path, base_metadata.path],
    )

    preprocessed = ctx.actions.declare_file(ctx.label.name + "_preprocessed.md")
    dep_args = []
    for dep in ctx.attr.deps:
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].output.path]
    ctx.actions.run(
        outputs = [preprocessed],
        inputs = [ctx.file.src],
        executable = ctx.attr._preprocess[DefaultInfo].files_to_run,
        arguments = dep_args + [ctx.file.src.path, preprocessed.path, ctx.label.package],
    )

    intermediate = ctx.actions.declare_file(ctx.label.name + "_intermediate.json")
    metadata = ctx.actions.declare_file(ctx.label.name + "_metadata.json")
    ctx.actions.run(
        outputs = [intermediate, metadata],
        inputs = [preprocessed, base_metadata] +
                 ctx.attr._validate[DefaultInfo].files.to_list() +
                 ctx.attr._include[DefaultInfo].files.to_list() +
                 ctx.attr._starts_with_text[DefaultInfo].files.to_list() +
                 ctx.attr._wordcount[DefaultInfo].files.to_list() +
                 ctx.attr._write_metadata[DefaultInfo].files.to_list() +
                 [dep[MdLibraryInfo].output for dep in ctx.attr.deps],
        executable = "pandoc",
        arguments = [
            "--filter=" + ctx.attr._validate[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._include[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._starts_with_text[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._wordcount[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._write_metadata[DefaultInfo].files.to_list()[0].path,
            "--metadata-file=" + base_metadata.path,
            "--metadata=metadata-out-file:" + metadata.path,
            "--from=markdown+smart",
            "--to=json",
            "--strip-comments",
            "--fail-if-warnings",
            "--output",
            intermediate.path,
            preprocessed.path,
        ],
    )

    # TODO
    output = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.run(
        outputs = [output],
        inputs = [intermediate],
        executable = "cp",
        arguments = [intermediate.path, output.path],
    )

    return [
        DefaultInfo(files = depset([output, metadata])),
        MdLibraryInfo(output = output, metadata = metadata),
    ]

md_library = rule(
    implementation = _md_library_impl,
    attrs = {
        "src": attr.label(
            allow_single_file = [".md"],
        ),
        "deps": attr.label_list(
            allow_empty = True,
            providers = [MdLibraryInfo],
        ),
        "increment_included_headers": attr.bool(
            default = False,
        ),
        "version_override": attr.string(
            default = "",
        ),
        "_raw_version": attr.label(
            default = "//lib:raw_version",
        ),
        "_base_metadata": attr.label(
            default = "//lib:base_metadata",
        ),
        "_preprocess": attr.label(
            default = "//lib:preprocess",
        ),
        "_validate": attr.label(
            default = "//lib:validate",
        ),
        "_include": attr.label(
            default = "//lib:include",
        ),
        "_starts_with_text": attr.label(
            default = "//lib:starts_with_text",
        ),
        "_wordcount": attr.label(
            default = "//lib:wordcount",
        ),
        "_write_metadata": attr.label(
            default = "//lib:write_metadata",
        ),
    },
)
