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
        srcs = ["@markdown_makefile//markdown/workspace:new_package.sh"],
        visibility = ["//visibility:private"],
    )

    required_files(
        name = "workspace",
        copy = [
            (
                "@markdown_makefile//markdown/workspace:workspace_status",
                ".markdown_workspace/workspace_status",
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

    md_summary()
