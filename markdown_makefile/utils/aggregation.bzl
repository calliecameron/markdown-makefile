"""Aggregation rules."""

load("//markdown_makefile/core:core.bzl", "MdLibraryInfo")

MdGroupInfo = provider(
    "Info for a group of markdown libraries.",
    fields = {
        "deps": "The libraries in the group",
    },
)

def _md_group_impl(ctx):
    output = []
    for dep in ctx.attr.deps:
        output += dep[DefaultInfo].files.to_list()

    return [
        DefaultInfo(files = depset(output)),
        MdGroupInfo(deps = ctx.attr.deps),
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
    },
)

def _md_group_summary_impl(ctx):
    dep_args = []
    for dep in ctx.attr.deps[MdGroupInfo].deps:
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].metadata.path]
    summary = ctx.actions.declare_file(ctx.label.name + ".csv")
    ctx.actions.run(
        outputs = [summary],
        inputs = [dep[MdLibraryInfo].metadata for dep in ctx.attr.deps[MdGroupInfo].deps],
        executable = ctx.attr._group_summary[DefaultInfo].files_to_run,
        arguments = [summary.path] + dep_args,
        progress_message = "%{label}: generating summary",
    )

    script = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.run(
        outputs = [script],
        inputs = [summary],
        executable = ctx.attr._write_group_summary_script[DefaultInfo].files_to_run,
        arguments = [
            ctx.workspace_name,
            summary.short_path,
            ctx.attr._group_summary_print.files_to_run.executable.short_path,
            script.path,
        ],
        progress_message = "%{label}: generating summary script",
    )

    return [
        DefaultInfo(
            files = depset([summary, script]),
            runfiles = ctx.runfiles(
                files = [summary],
                transitive_files = ctx.attr._group_summary_print[DefaultInfo].default_runfiles.files,
            ),
            executable = script,
        ),
    ]

md_group_summary = rule(
    implementation = _md_group_summary_impl,
    executable = True,
    doc = "md_group_summary summarises the contents of an md_group.",
    attrs = {
        "deps": attr.label(
            providers = [MdGroupInfo],
            doc = "md_group to summarise.",
        ),
        "_group_summary": attr.label(
            default = "//markdown_makefile/utils:group_summary",
        ),
        "_write_group_summary_script": attr.label(
            default = "//markdown_makefile/utils:write_group_summary_script",
        ),
        "_group_summary_print": attr.label(
            default = "//markdown_makefile/utils:group_summary_print",
        ),
    },
)

def _md_group_publications_impl(ctx):
    dep_args = []
    for dep in ctx.attr.deps[MdGroupInfo].deps:
        dep_args += ["--dep", dep.label.package + ":" + dep.label.name, dep[MdLibraryInfo].metadata.path]
    publications = ctx.actions.declare_file(ctx.label.name + ".html")
    ctx.actions.run(
        outputs = [publications],
        inputs = [dep[MdLibraryInfo].metadata for dep in ctx.attr.deps[MdGroupInfo].deps],
        executable = ctx.attr._group_publications[DefaultInfo].files_to_run,
        arguments = [publications.path] + dep_args,
        progress_message = "%{label}: generating publications",
    )

    script = ctx.actions.declare_file(ctx.label.name + ".sh")
    ctx.actions.run(
        outputs = [script],
        inputs = [publications],
        executable = ctx.attr._write_group_publications_script[DefaultInfo].files_to_run,
        arguments = [ctx.workspace_name, publications.short_path, script.path],
        progress_message = "%{label}: generating publications script",
    )

    return [
        DefaultInfo(
            files = depset([publications, script]),
            runfiles = ctx.runfiles(files = [publications]),
            executable = script,
        ),
    ]

md_group_publications = rule(
    implementation = _md_group_publications_impl,
    executable = True,
    doc = "md_group_publications displays the publications of an md_group.",
    attrs = {
        "deps": attr.label(
            providers = [MdGroupInfo],
            doc = "md_group to process.",
        ),
        "_group_publications": attr.label(
            default = "//markdown_makefile/utils:group_publications",
        ),
        "_write_group_publications_script": attr.label(
            default = "//markdown_makefile/utils:write_group_publications_script",
        ),
    },
)
