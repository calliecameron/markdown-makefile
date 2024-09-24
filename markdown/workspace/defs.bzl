"""Workspace macros."""

load("//markdown/summary:defs.bzl", "md_summary")
load("//markdown/utils:defs.bzl", "required_files")

def md_workspace(name = None):  # buildifier: disable=unused-variable
    """Workspace setup.

    Args:
        name: unused
    """

    if native.package_name():
        fail("md_workspace may only be used in the workspace root")

    native.sh_binary(
        name = "new",
        srcs = ["@rules_markdown//markdown/workspace:new_package.sh"],
        visibility = ["//visibility:private"],
    )

    required_files(
        name = "workspace",
        copy = [
            (
                "@rules_markdown//markdown/workspace:workspace_status",
                ".markdown_workspace/workspace_status",
                "700",
            ),
            (
                "@rules_markdown//markdown/utils:git_repo_version",
                ".markdown_workspace/git_repo_version",
                "700",
            ),
            (
                "@rules_markdown//markdown/workspace:bazelversion",
                ".bazelversion",
                "600",
            ),
            (
                "@rules_markdown//markdown/workspace:bazelrc",
                ".bazelrc",
                "600",
            ),
        ],
    )

    md_summary()
