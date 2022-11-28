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
            "@markdown_makefile//utils:bazelversion",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath @markdown_makefile//utils:bazelversion)",
        ],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "workspace_test",
        srcs = ["@markdown_makefile//utils:workspace_test.sh"],
        data = [
            "@markdown_makefile//utils:workspace_status",
            "@markdown_makefile//utils:workspace_summary",
            "@markdown_makefile//utils:bazelversion",
            ".bin/workspace_status",
            "workspace_summary",
            ".bazelversion",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath @markdown_makefile//utils:bazelversion)",
            "$(rootpath .bin/workspace_status)",
            "$(rootpath workspace_summary)",
            "$(rootpath .bazelversion)",
        ],
        visibility = ["//visibility:private"],
    )
