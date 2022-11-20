"""Markdown rules."""

MdLibraryInfo = provider(
    "Info for a markdown library.",
    fields = {
        "output": "Compiled document, as json",
        "metadata": "Document metadata, as json",
        "dictionary": "Dictionary used for spellchecking",
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
            "--output=" + intermediate.path,
            preprocessed.path,
        ],
    )

    dictionary = ctx.actions.declare_file(ctx.label.name + "_dictionary.dic")
    if ctx.attr.dictionaries:
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
        )
    else:
        ctx.actions.write(
            output = dictionary,
            content = "",
        )

    spellcheck_input = ctx.actions.declare_file(ctx.label.name + "_spellcheck_input.md")
    ctx.actions.run(
        outputs = [spellcheck_input],
        inputs = [intermediate] + ctx.attr._spellcheck_input_template.files.to_list(),
        executable = "pandoc",
        arguments = [
            "--from=json",
            "--to=markdown-smart",
            "--template=" + ctx.attr._spellcheck_input_template[DefaultInfo].files.to_list()[0].path,
            "--fail-if-warnings",
            "--output=" + spellcheck_input.path,
            intermediate.path,
        ],
    )

    spellchecked = ctx.actions.declare_file(ctx.label.name + "_spellchecked.txt")
    ctx.actions.run(
        outputs = [spellchecked],
        inputs = [dictionary, spellcheck_input],
        executable = ctx.attr._spellcheck[DefaultInfo].files_to_run,
        arguments = [dictionary.path, spellcheck_input.path, spellchecked.path],
    )

    output = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.run(
        outputs = [output],
        inputs = [intermediate, spellchecked],
        executable = "cp",
        arguments = [intermediate.path, output.path],
    )

    return [
        DefaultInfo(files = depset([output, metadata, dictionary])),
        MdLibraryInfo(output = output, metadata = metadata, dictionary = dictionary),
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
        "dictionaries": attr.label_list(
            allow_empty = True,
            allow_files = [".dic"],
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
        "_write_dictionary": attr.label(
            default = "//lib:write_dictionary",
        ),
        "_spellcheck_input_template": attr.label(
            default = "//lib:spellcheck_input_template",
        ),
        "_spellcheck": attr.label(
            default = "//lib:spellcheck",
        ),
    },
)
