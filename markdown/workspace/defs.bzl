"""Workspace macros."""

load("//markdown/dynamic_group:defs.bzl", "md_dynamic_group")
load("//markdown/utils:defs.bzl", "required_files")

def md_workspace(name = None):  # buildifier: disable=unused-variable
    """Workspace setup.

    Args:
        name: unused
    """

    native.sh_binary(
        name = "new",
        srcs = ["@markdown_makefile//markdown/workspace:new_package.sh"],
        visibility = ["//visibility:private"],
    )

    required_files(
        name = "workspace",
        copy = [
            (
                "@markdown_makefile//markdown/workspace:workspace_status",
                ".bin/workspace_status",
                "700",
            ),
            (
                "@markdown_makefile//markdown/workspace:workspace_git_update",
                "workspace_git_update",
                "700",
            ),
            (
                "@markdown_makefile//markdown/workspace:bazelversion",
                ".bazelversion",
                "600",
            ),
            (
                "@markdown_makefile//markdown/workspace:bazelrc",
                ".bazelrc",
                "600",
            ),
        ],
    )

    md_dynamic_group()
