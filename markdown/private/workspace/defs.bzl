"""Workspace macros."""

load("//markdown/private/summary:defs.bzl", "md_summary")
load("//markdown/private/utils:defs.bzl", "required_files")

def md_workspace(name = None):  # buildifier: disable=unused-variable
    """Workspace setup.

    Args:
        name: unused
    """

    if native.package_name():
        fail("md_workspace may only be used in the workspace root")

    native.sh_binary(
        name = "new",
        srcs = ["@rules_markdown//markdown/private/workspace:new_package.sh"],
        visibility = ["//visibility:private"],
    )

    required_files(
        name = "workspace",
        copy = [
            (
                "@rules_markdown//markdown/private/workspace:workspace_status",
                ".markdown_workspace/workspace_status",
                "700",
            ),
            (
                "@rules_markdown//markdown/private/utils:git_repo_version",
                ".markdown_workspace/git_repo_version",
                "700",
            ),
            (
                "@rules_markdown//markdown/private/workspace:bazelversion",
                ".bazelversion",
                "600",
            ),
            (
                "@rules_markdown//markdown/private/workspace:bazelrc",
                ".bazelrc",
                "600",
            ),
        ],
    )

    md_summary()
