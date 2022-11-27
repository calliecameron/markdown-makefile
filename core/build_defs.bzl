"""Markdown rules."""

MdLibraryInfo = provider(
    "Info for a markdown library.",
    fields = {
        "name": "The name of the document",
        "output": "Compiled document, as json",
        "metadata": "Document metadata, as json",
        "dictionary": "Dictionary used for spellchecking",
        "data": "Data deps of the document",
    },
)

def _md_library_impl(ctx):
    raw_version = ctx.actions.declare_file(ctx.label.name + "_raw_version.json")
    ctx.actions.run(
        outputs = [raw_version],
        inputs = [ctx.info_file],
        executable = ctx.attr._raw_version[DefaultInfo].files_to_run,
        arguments = [ctx.info_file.path, raw_version.path, ctx.label.package],
        progress_message = "%{label}: computing version",
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
        progress_message = "%{label}: generating base metadata",
    )

    preprocessed = ctx.actions.declare_file(ctx.label.name + "_preprocessed.md")
    dep_args = []
    for dep in ctx.attr.deps:
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].output.path]
    image_args = []
    for image in ctx.attr.images:
        image_args += ["--image", image.label.package + ":" + image.label.name, image[DefaultInfo].files.to_list()[0].path]
    ctx.actions.run(
        outputs = [preprocessed],
        inputs = [ctx.file.src],
        executable = ctx.attr._preprocess[DefaultInfo].files_to_run,
        arguments = dep_args + image_args + [ctx.file.src.path, preprocessed.path, ctx.label.package],
        progress_message = "%{label}: preprocessing markdown",
    )

    intermediate = ctx.actions.declare_file(ctx.label.name + "_intermediate.json")
    metadata = ctx.outputs.metadata_out
    ctx.actions.run(
        outputs = [intermediate, metadata],
        inputs = [preprocessed, base_metadata] +
                 ctx.attr._validate[DefaultInfo].files.to_list() +
                 ctx.attr._include[DefaultInfo].files.to_list() +
                 ctx.attr._starts_with_text[DefaultInfo].files.to_list() +
                 ctx.attr._wordcount[DefaultInfo].files.to_list() +
                 ctx.attr._write_metadata[DefaultInfo].files.to_list() +
                 ctx.attr._cleanup[DefaultInfo].files.to_list() +
                 [dep[MdLibraryInfo].output for dep in ctx.attr.deps],
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        arguments = [
            "--filter=" + ctx.attr._validate[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._include[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._starts_with_text[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._wordcount[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._write_metadata[DefaultInfo].files.to_list()[0].path,
            "--lua-filter=" + ctx.attr._cleanup[DefaultInfo].files.to_list()[0].path,
            "--metadata-file=" + base_metadata.path,
            "--metadata=metadata-out-file:" + metadata.path,
            "--from=markdown+smart",
            "--to=json",
            "--strip-comments",
            "--fail-if-warnings",
            "--output=" + intermediate.path,
            preprocessed.path,
        ],
        progress_message = "%{label}: compiling markdown",
    )

    dictionary = ctx.actions.declare_file(ctx.label.name + "_dictionary.dic")
    if ctx.attr.dictionaries or ctx.attr.deps:
        dict_inputs = []
        dict_args = []
        for d in ctx.attr.dictionaries:
            dict_inputs += d.files.to_list()
            dict_args += [f.path for f in d.files.to_list()]
        ctx.actions.run(
            outputs = [dictionary],
            inputs = dict_inputs + [dep[MdLibraryInfo].dictionary for dep in ctx.attr.deps],
            executable = ctx.attr._write_dictionary[DefaultInfo].files_to_run,
            arguments = [dictionary.path] +
                        dict_args +
                        [dep[MdLibraryInfo].dictionary.path for dep in ctx.attr.deps],
            progress_message = "%{label}: generating dictionary",
        )
    else:
        ctx.actions.write(
            output = dictionary,
            content = "",
        )

    spellcheck_input = ctx.actions.declare_file(ctx.label.name + "_spellcheck_input.md")
    ctx.actions.run(
        outputs = [spellcheck_input],
        inputs = [intermediate] +
                 ctx.attr._spellcheck_input_template.files.to_list() +
                 ctx.attr._spellcheck_filter.files.to_list(),
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        arguments = [
            "--lua-filter=" + ctx.attr._spellcheck_filter[DefaultInfo].files.to_list()[0].path,
            "--from=json",
            "--to=markdown-smart",
            "--template=" + ctx.attr._spellcheck_input_template[DefaultInfo].files.to_list()[0].path,
            "--fail-if-warnings",
            "--output=" + spellcheck_input.path,
            intermediate.path,
        ],
        progress_message = "%{label}: generating input for spellchecking",
    )

    spellchecked = ctx.actions.declare_file(ctx.label.name + "_spellchecked.txt")
    ctx.actions.run(
        outputs = [spellchecked],
        inputs = [dictionary, spellcheck_input],
        executable = ctx.attr._spellcheck[DefaultInfo].files_to_run,
        arguments = [dictionary.path, spellcheck_input.path, spellchecked.path],
        progress_message = "%{label}: spellchecking",
    )

    output = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.run(
        outputs = [output],
        inputs = [intermediate, spellchecked],
        executable = "cp",
        arguments = [intermediate.path, output.path],
        progress_message = "%{label}: generating output",
    )

    data = depset(ctx.attr.data + ctx.attr.images, transitive = [dep[MdLibraryInfo].data for dep in ctx.attr.deps])
    return [
        DefaultInfo(files = depset([output, metadata, dictionary])),
        MdLibraryInfo(name = ctx.label.name, output = output, metadata = metadata, dictionary = dictionary, data = data),
    ]

md_library = rule(
    implementation = _md_library_impl,
    doc = "md_library compiles and validates a single markdown file.",
    attrs = {
        "src": attr.label(
            allow_single_file = [".md"],
            doc = "A markdown source file.",
        ),
        "deps": attr.label_list(
            allow_empty = True,
            providers = [MdLibraryInfo],
            doc = "Other md_library targets used in !include statements in src.",
        ),
        "dictionaries": attr.label_list(
            allow_empty = True,
            allow_files = [".dic"],
            doc = "Dictionary files for spellchecking.",
        ),
        "data": attr.label_list(
            allow_empty = True,
            allow_files = True,
            doc = "Data dependencies.",
        ),
        "images": attr.label_list(
            allow_empty = True,
            allow_files = True,
            doc = "Image dependencies.",
        ),
        "increment_included_headers": attr.bool(
            default = False,
            doc = "If true, header level in included files is incremented, e.g. level 1 headers become level 2 headers. If false, headers are unchanged.",
        ),
        "version_override": attr.string(
            default = "",
            doc = "Set the document version to this value, rather than the computed value. Should only be used for testing.",
        ),
        "metadata_out": attr.output(
            doc = "Label of the output metadata file.",
        ),
        "_pandoc": attr.label(
            default = "@pandoc//:pandoc",
        ),
        "_raw_version": attr.label(
            default = "//core:raw_version",
        ),
        "_base_metadata": attr.label(
            default = "//core:base_metadata",
        ),
        "_preprocess": attr.label(
            default = "//core:preprocess",
        ),
        "_validate": attr.label(
            default = "//core:validate",
        ),
        "_include": attr.label(
            default = "//core:include",
        ),
        "_starts_with_text": attr.label(
            default = "//core:starts_with_text",
        ),
        "_wordcount": attr.label(
            default = "//core:wordcount",
        ),
        "_write_metadata": attr.label(
            default = "//core:write_metadata",
        ),
        "_cleanup": attr.label(
            default = "//core:cleanup",
        ),
        "_write_dictionary": attr.label(
            default = "//core:write_dictionary",
        ),
        "_spellcheck_input_template": attr.label(
            default = "//core:spellcheck_input_template",
        ),
        "_spellcheck_filter": attr.label(
            default = "//core:spellcheck_filter",
        ),
        "_spellcheck": attr.label(
            default = "//core:spellcheck",
        ),
    },
)
