"""Workspace macros."""

load("//markdown_makefile/dynamic_group:dynamic_group.bzl", "md_dynamic_group")

def md_workspace(name = None):  # buildifier: disable=unused-variable
    """Workspace setup.

    Args:
        name: unused
    """

    native.sh_binary(
        name = "new",
        srcs = ["@markdown_makefile//markdown_makefile/workspace:new_package.sh"],
        visibility = ["//visibility:private"],
    )

    native.sh_binary(
        name = "workspace_update",
        srcs = ["@markdown_makefile//markdown_makefile/workspace:workspace_update.sh"],
        data = [
            "@markdown_makefile//markdown_makefile/workspace:workspace_status",
            "@markdown_makefile//markdown_makefile/workspace:workspace_git_update",
            "@markdown_makefile//markdown_makefile/workspace:bazelversion",
            "@markdown_makefile//markdown_makefile/workspace:bazelrc",
        ],
        args = [
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:workspace_status)",
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:workspace_git_update)",
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:bazelversion)",
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:bazelrc)",
        ],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "workspace_test",
        srcs = ["@markdown_makefile//markdown_makefile/workspace:workspace_test.sh"],
        data = [
            "@markdown_makefile//markdown_makefile/workspace:workspace_status",
            "@markdown_makefile//markdown_makefile/workspace:workspace_git_update",
            "@markdown_makefile//markdown_makefile/workspace:bazelversion",
            "@markdown_makefile//markdown_makefile/workspace:bazelrc",
            ".bin/workspace_status",
            "workspace_git_update",
            ".bazelversion",
            ".bazelrc",
        ],
        args = [
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:workspace_status)",
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:workspace_git_update)",
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:bazelversion)",
            "$(rootpath @markdown_makefile//markdown_makefile/workspace:bazelrc)",
            "$(rootpath .bin/workspace_status)",
            "$(rootpath workspace_git_update)",
            "$(rootpath .bazelversion)",
            "$(rootpath .bazelrc)",
        ],
        visibility = ["//visibility:private"],
    )

    md_dynamic_group()
