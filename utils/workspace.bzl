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
        data = [
            "@markdown_makefile//utils:workspace_status",
            "@markdown_makefile//utils:workspace_summary",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
        ],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "workspace_test",
        srcs = ["@markdown_makefile//utils:workspace_test.sh"],
        data = [
            "@markdown_makefile//utils:workspace_status",
            "@markdown_makefile//utils:workspace_summary",
            ".bin/workspace_status",
            "workspace_summary",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath .bin/workspace_status)",
            "$(rootpath workspace_summary)",
        ],
        visibility = ["//visibility:private"],
    )
