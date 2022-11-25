"""Workspace macros."""

def md_workspace(name = None):  # buildifier: disable=unused-variable
    native.sh_binary(
        name = "new",
        srcs = ["@markdown_makefile//utils:new_package.sh"],
        visibility = ["//visibility:private"],
    )
