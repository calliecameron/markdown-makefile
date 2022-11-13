MdLibraryInfo = provider(
    "Info for a markdown library.",
    fields = {
        "output": "Compiled library, as json",
        "version": "Version of the library",
    },
)

def _md_library_impl(ctx):
    if ctx.file.src:
        src = ctx.file.src
    else:
        src = ctx.actions.declare_file(ctx.label.name + ".md")

    raw_version = ctx.actions.declare_file(ctx.label.name + "_raw_version.json")
    ctx.actions.run(
        outputs = [raw_version],
        inputs = [ctx.info_file],
        executable = ctx.attr._raw_version[DefaultInfo].files_to_run,
        arguments = [ctx.info_file.path, raw_version.path, ctx.label.package],
    )

    version = ctx.actions.declare_file(ctx.label.name + "_version.json")
    dep_versions = ctx.actions.declare_file(ctx.label.name + "_dep_versions.json")
    base_metadata = ctx.actions.declare_file(ctx.label.name + "_base_metadata.json")
    dep_version_args = []
    for dep in ctx.attr.deps:
        dep_version_args += ["--dep_version_file", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].version.path]
    ctx.actions.run(
        outputs = [version, dep_versions, base_metadata],
        inputs = [raw_version] + [dep[MdLibraryInfo].version for dep in ctx.attr.deps],
        executable = ctx.attr._base_metadata[DefaultInfo].files_to_run,
        arguments = dep_version_args + [raw_version.path, version.path, dep_versions.path, base_metadata.path],
    )

    preprocessed = ctx.actions.declare_file(ctx.label.name + "_preprocessed.md")
    dep_args = []
    for dep in ctx.attr.deps:
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].output.path]
    ctx.actions.run(
        outputs = [preprocessed],
        inputs = [src] + [dep[MdLibraryInfo].output for dep in ctx.attr.deps],
        executable = ctx.attr._preprocess[DefaultInfo].files_to_run,
        arguments = dep_args + [src.path, preprocessed.path],
    )

    output = ctx.actions.declare_file(ctx.label.name + ".json")
    ctx.actions.write(output, "foo")

    return [
        DefaultInfo(files = depset([preprocessed, base_metadata])),
        MdLibraryInfo(output = output, version = version),
    ]

md_library = rule(
    implementation = _md_library_impl,
    attrs = {
        "src": attr.label(
            allow_single_file = [".md"],
            default = None,
        ),
        "deps": attr.label_list(
            allow_empty = True,
            providers = [MdLibraryInfo],
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
    },
)
