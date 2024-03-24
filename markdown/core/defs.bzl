"""Markdown rules."""

MdGroupInfo = provider(
    "Info for a group of markdown files.",
    fields = {
        "deps": "The files in the group",
        "metadata": "Metadata of all files in the group, as json",
    },
)

MdFileInfo = provider(
    "Info for a markdown file.",
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
        metadata_args += ["--metadata_file", dep.label.package + ":" + dep.label.name, dep[MdFileInfo].metadata.path]
    ctx.actions.run(
        outputs = [metadata],
        inputs = [dep[MdFileInfo].metadata for dep in ctx.attr.deps],
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
    doc = "md_group is a group of md_file targets.",
    attrs = {
        "deps": attr.label_list(
            allow_empty = True,
            providers = [DefaultInfo, MdFileInfo],
            doc = "md_file targets to include in the group.",
        ),
        "_combine_metadata": attr.label(
            default = "//markdown/core:combine_metadata",
        ),
    },
)

def _lint(ctx):
    lint_input = ctx.actions.declare_file(ctx.label.name + "_lint_input.md")
    ctx.actions.run(
        outputs = [lint_input],
        inputs = [
            ctx.file.src,
        ],
        executable = ctx.attr._gen_lint_input[DefaultInfo].files_to_run,
        arguments = [
            ctx.file.src.path,
            lint_input.path,
        ],
        progress_message = "%{label}: generating input for linting",
    )

    lint_ok = ctx.actions.declare_file(ctx.label.name + "_lint_ok.txt")
    ctx.actions.run(
        outputs = [lint_ok],
        inputs = [
            lint_input,
            ctx.file._pymarkdown_config,
        ],
        executable = ctx.attr._lint[DefaultInfo].files_to_run,
        arguments = [
            lint_ok.path,
            "--strict-config",
            "--config",
            ctx.file._pymarkdown_config.path,
            "scan",
            lint_input.path,
        ],
        progress_message = "%{label}: linting markdown",
    )

    return lint_ok

def _spellcheck(ctx, intermediate):
    dictionary = ctx.actions.declare_file(ctx.label.name + "_dictionary.dic")
    if ctx.attr.dictionaries or ctx.attr.deps[MdGroupInfo].deps:
        dict_inputs = []
        dict_args = []
        for d in ctx.attr.dictionaries:
            dict_inputs += d.files.to_list()
            dict_args += [f.path for f in d.files.to_list()]
        ctx.actions.run(
            outputs = [dictionary],
            inputs = dict_inputs + [dep[MdFileInfo].dictionary for dep in ctx.attr.deps[MdGroupInfo].deps],
            executable = ctx.attr._gen_dictionary[DefaultInfo].files_to_run,
            arguments = [dictionary.path] +
                        dict_args +
                        [dep[MdFileInfo].dictionary.path for dep in ctx.attr.deps[MdGroupInfo].deps],
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

    spellcheck_ok = ctx.actions.declare_file(ctx.label.name + "_spellcheck_ok.txt")
    ctx.actions.run(
        outputs = [spellcheck_ok],
        inputs = [dictionary, spellcheck_input],
        executable = ctx.attr._spellcheck[DefaultInfo].files_to_run,
        arguments = [dictionary.path, spellcheck_input.path, spellcheck_ok.path],
        progress_message = "%{label}: spellchecking",
    )

    return dictionary, spellcheck_ok

def _md_file_impl(ctx):
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
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdFileInfo].output.path]
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

    lint_ok = _lint(ctx)

    intermediate = ctx.actions.declare_file(ctx.label.name + "_intermediate.json")
    intermediate_metadata = ctx.actions.declare_file(ctx.label.name + "_intermediate_metadata.json")
    ctx.actions.run(
        outputs = [intermediate, intermediate_metadata],
        inputs = [
            preprocessed,
            lint_ok,
            base_metadata,
            ctx.file._include,
            ctx.file._starts_with_text,
            ctx.file._wordcount,
            ctx.file._poetry_lines,
            ctx.file._write_metadata,
            ctx.file._cleanup,
        ] + [dep[MdFileInfo].output for dep in ctx.attr.deps[MdGroupInfo].deps],
        executable = ctx.attr._pandoc[DefaultInfo].files_to_run,
        tools = [ctx.attr._validate[DefaultInfo].files_to_run],
        arguments = [
            "--filter=" + ctx.attr._validate[DefaultInfo].files_to_run.executable.path,
            "--lua-filter=" + ctx.file._include.path,
            "--lua-filter=" + ctx.file._starts_with_text.path,
            "--lua-filter=" + ctx.file._wordcount.path,
            "--lua-filter=" + ctx.file._poetry_lines.path,
            "--lua-filter=" + ctx.file._write_metadata.path,
            "--lua-filter=" + ctx.file._cleanup.path,
            "--metadata-file=" + base_metadata.path,
            "--metadata=metadata-out-file:" + intermediate_metadata.path,
            "--from=markdown+smart-pandoc_title_block",
            "--to=json",
            "--strip-comments",
            "--fail-if-warnings",
            "--output=" + intermediate.path,
            preprocessed.path,
        ],
        progress_message = "%{label}: compiling markdown",
    )

    dictionary, spellcheck_ok = _spellcheck(ctx, intermediate)

    output = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.run(
        outputs = [output],
        inputs = [intermediate, spellcheck_ok],
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
        transitive = [dep[MdFileInfo].data for dep in ctx.attr.deps[MdGroupInfo].deps],
    )
    return [
        DefaultInfo(files = depset([output, metadata, dictionary])),
        MdFileInfo(name = ctx.label.name, output = output, metadata = metadata, dictionary = dictionary, data = data),
    ]

md_file = rule(
    implementation = _md_file_impl,
    doc = "md_file compiles and validates a single markdown file.",
    attrs = {
        "src": attr.label(
            allow_single_file = [".md"],
            doc = "A markdown source file.",
        ),
        "deps": attr.label(
            providers = [MdGroupInfo],
            doc = "Other md_file targets used in !include statements in src.",
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
            default = "//markdown/external:pandoc",
        ),
        "_raw_version": attr.label(
            default = "//markdown/core:raw_version",
        ),
        "_base_metadata": attr.label(
            default = "//markdown/core:base_metadata",
        ),
        "_gen_lint_input": attr.label(
            default = "//markdown/core/lint:gen_lint_input",
        ),
        "_lint": attr.label(
            default = "//markdown/core/lint:lint",
        ),
        "_preprocess": attr.label(
            default = "//markdown/core:preprocess",
        ),
        "_validate": attr.label(
            default = "//markdown/core:validate",
        ),
        "_pymarkdown_config": attr.label(
            allow_single_file = True,
            default = "//:pymarkdown.json",
        ),
        "_include": attr.label(
            allow_single_file = True,
            default = "//markdown/core/filters:include.lua",
        ),
        "_starts_with_text": attr.label(
            allow_single_file = True,
            default = "//markdown/core/filters:starts_with_text.lua",
        ),
        "_wordcount": attr.label(
            allow_single_file = True,
            default = "//markdown/core/filters:wordcount.lua",
        ),
        "_poetry_lines": attr.label(
            allow_single_file = True,
            default = "//markdown/core/filters:poetry_lines.lua",
        ),
        "_write_metadata": attr.label(
            allow_single_file = True,
            default = "//markdown/core/filters:write_metadata.lua",
        ),
        "_cleanup": attr.label(
            allow_single_file = True,
            default = "//markdown/core/filters:cleanup.lua",
        ),
        "_gen_dictionary": attr.label(
            default = "//markdown/core/spelling:gen_dictionary",
        ),
        "_spellcheck_input_template": attr.label(
            allow_single_file = True,
            default = "//markdown/core/spelling:spellcheck_input_template.md",
        ),
        "_spellcheck_filter": attr.label(
            allow_single_file = True,
            default = "//markdown/core/spelling:spellcheck_filter.lua",
        ),
        "_spellcheck": attr.label(
            default = "//markdown/core/spelling:spellcheck",
        ),
    },
)
