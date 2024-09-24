"""Repository rule for the main markdown repo."""

def _main_repo_impl(repository_ctx):
    bzl_entries = []
    for package, repo in sorted(repository_ctx.attr.package_repos.items()):
        bzl_entries.append("    \"%s\": \"@markdown//:%s_version.json\"," % (package, repo))

    repository_ctx.file(
        "versions.bzl",
        content = """_VERSION_FILES = {
%s
}

def version_file(package):
    return _VERSION_FILES.get(package, None)
""" % "\n".join(bzl_entries),
        executable = False,
    )

    build_entries = []

    for repo in sorted(repository_ctx.attr.repos):
        build_entries.append("""alias(
    name = "%s_version.json",
    actual = "@%s//:version.json",
    visibility = ["//visibility:public"],
)""" % (repo, repo))

    repository_ctx.file(
        "BUILD",
        content = """exports_files(
    ["versions.bzl"],
    visibility = ["//visibility:public"],
)

""" + "\n\n".join(build_entries) + "\n",
        executable = False,
    )

main_repo = repository_rule(
    implementation = _main_repo_impl,
    local = True,
    attrs = {
        "package_repos": attr.string_dict(mandatory = True),
        "repos": attr.string_list(mandatory = True),
    },
)
