"""Workspace macros."""

def md_workspace(name = None):  # buildifier: disable=unused-variable
    native.sh_binary(
        name = "new",
        srcs = ["@markdown_makefile//utils:new_package.sh"],
        visibility = ["//visibility:private"],
    )

    native.sh_binary(
        name = "workspace_update",
        srcs = ["@markdown_makefile//utils:workspace_update.sh"],
        data = ["@markdown_makefile//utils:workspace_status"],
        args = ["$(rootpath @markdown_makefile//utils:workspace_status)"],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "workspace_test",
        srcs = ["@markdown_makefile//utils:workspace_test.sh"],
        data = [
            "@markdown_makefile//utils:workspace_status",
            ".bin/workspace_status",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath .bin/workspace_status)",
        ],
        visibility = ["//visibility:private"],
    )
