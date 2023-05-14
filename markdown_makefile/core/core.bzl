"""Markdown rules."""

MdGroupInfo = provider(
    "Info for a group of markdown libraries.",
    fields = {
        "deps": "The libraries in the group",
        "metadata": "Metadata of all libraries in the group, as json",
    },
)

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

def _md_group_impl(ctx):
    output = []
    for dep in ctx.attr.deps:
        output += dep[DefaultInfo].files.to_list()

    metadata = ctx.actions.declare_file(ctx.label.name + "_metadata.json")
    metadata_args = []
    for dep in ctx.attr.deps:
        metadata_args += ["--metadata_file", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].metadata.path]
    ctx.actions.run(
        outputs = [metadata],
        inputs = [dep[MdLibraryInfo].metadata for dep in ctx.attr.deps],
        executable = ctx.attr._combine_metadata[DefaultInfo].files_to_run,
        arguments = metadata_args + [metadata.path],
        progress_message = "%{label}: combining deps metadata",
    )

    return [
        DefaultInfo(files = depset([metadata] + output)),
        MdGroupInfo(deps = ctx.attr.deps, metadata = metadata),
    ]

md_group = rule(
    implementation = _md_group_impl,
    doc = "md_group is a group of md_library targets.",
    attrs = {
        "deps": attr.label_list(
            allow_empty = True,
            providers = [DefaultInfo, MdLibraryInfo],
            doc = "md_library targets to include in the group.",
        ),
        "_combine_metadata": attr.label(
            default = "//markdown_makefile/core:combine_metadata",
        ),
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

    base_metadata = ctx.actions.declare_file(ctx.label.name + "_base_metadata.json")
    extra_args = []
    if ctx.attr.increment_included_headers:
        extra_args.append("--increment_included_headers")
    if ctx.attr.version_override:
        extra_args += ["--version_override", ctx.attr.version_override]
    ctx.actions.run(
        outputs = [base_metadata],
        inputs = [raw_version, ctx.attr.deps[MdGroupInfo].metadata],
        executable = ctx.attr._base_metadata[DefaultInfo].files_to_run,
        arguments = extra_args + [raw_version.path, ctx.attr.deps[MdGroupInfo].metadata.path, base_metadata.path],
        progress_message = "%{label}: generating base metadata",
    )

    preprocessed = ctx.actions.declare_file(ctx.label.name + "_preprocessed.md")
    dep_args = []
    for dep in ctx.attr.deps[MdGroupInfo].deps:
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
    intermediate_metadata = ctx.actions.declare_file(ctx.label.name + "_intermediate_metadata.json")
    ctx.actions.run(
        outputs = [intermediate, intermediate_metadata],
        inputs = [
            preprocessed,
            base_metadata,
            ctx.file._validate,
            ctx.file._include,
            ctx.file._starts_with_text,
            ctx.file._wordcount,
            ctx.file._write_metadata,
            ctx.file._cleanup,
        ] + [dep[MdLibraryInfo].output for dep in ctx.attr.deps[MdGroupInfo].deps],
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        arguments = [
            "--filter=" + ctx.file._validate.path,
            "--lua-filter=" + ctx.file._include.path,
            "--lua-filter=" + ctx.file._starts_with_text.path,
            "--lua-filter=" + ctx.file._wordcount.path,
            "--lua-filter=" + ctx.file._write_metadata.path,
            "--lua-filter=" + ctx.file._cleanup.path,
            "--metadata-file=" + base_metadata.path,
            "--metadata=metadata-out-file:" + intermediate_metadata.path,
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
    if ctx.attr.dictionaries or ctx.attr.deps[MdGroupInfo].deps:
        dict_inputs = []
        dict_args = []
        for d in ctx.attr.dictionaries:
            dict_inputs += d.files.to_list()
            dict_args += [f.path for f in d.files.to_list()]
        ctx.actions.run(
            outputs = [dictionary],
            inputs = dict_inputs + [dep[MdLibraryInfo].dictionary for dep in ctx.attr.deps[MdGroupInfo].deps],
            executable = ctx.attr._write_dictionary[DefaultInfo].files_to_run,
            arguments = [dictionary.path] +
                        dict_args +
                        [dep[MdLibraryInfo].dictionary.path for dep in ctx.attr.deps[MdGroupInfo].deps],
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
        inputs = [
            intermediate,
            ctx.file._spellcheck_input_template,
            ctx.file._spellcheck_filter,
        ],
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        arguments = [
            "--lua-filter=" + ctx.file._spellcheck_filter.path,
            "--from=json",
            "--to=markdown-smart",
            "--template=" + ctx.file._spellcheck_input_template.path,
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

    metadata = ctx.outputs.metadata_out
    ctx.actions.run(
        outputs = [metadata],
        inputs = [output, intermediate_metadata],
        executable = "cp",
        arguments = [intermediate_metadata.path, metadata.path],
        progress_message = "%{label}: generating metadata",
    )

    data = depset(
        ctx.attr.data + ctx.attr.images,
        transitive = [dep[MdLibraryInfo].data for dep in ctx.attr.deps[MdGroupInfo].deps],
    )
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
        "deps": attr.label(
            providers = [MdGroupInfo],
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
            default = "//markdown_makefile/core:raw_version",
        ),
        "_base_metadata": attr.label(
            default = "//markdown_makefile/core:base_metadata",
        ),
        "_preprocess": attr.label(
            default = "//markdown_makefile/core:preprocess",
        ),
        "_validate": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:validate.py",
        ),
        "_include": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:include.lua",
        ),
        "_starts_with_text": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:starts_with_text.lua",
        ),
        "_wordcount": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:wordcount.lua",
        ),
        "_write_metadata": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:write_metadata.lua",
        ),
        "_cleanup": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:cleanup.lua",
        ),
        "_write_dictionary": attr.label(
            default = "//markdown_makefile/core:write_dictionary",
        ),
        "_spellcheck_input_template": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:spellcheck_input_template.md",
        ),
        "_spellcheck_filter": attr.label(
            allow_single_file = True,
            default = "//markdown_makefile/core:spellcheck_filter.lua",
        ),
        "_spellcheck": attr.label(
            default = "//markdown_makefile/core:spellcheck",
        ),
    },
)
