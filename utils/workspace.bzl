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
            "@markdown_makefile//utils:workspace_contents_build",
            "@markdown_makefile//utils:workspace_contents_bzl",
            "@markdown_makefile//utils:workspace_summary",
            "@markdown_makefile//utils:workspace_publications",
            "@markdown_makefile//utils:bazelversion",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_build)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_bzl)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath @markdown_makefile//utils:workspace_publications)",
            "$(rootpath @markdown_makefile//utils:bazelversion)",
        ],
        visibility = ["//visibility:private"],
    )

    native.sh_test(
        name = "workspace_test",
        srcs = ["@markdown_makefile//utils:workspace_test.sh"],
        data = [
            "@markdown_makefile//utils:workspace_status",
            "@markdown_makefile//utils:workspace_contents_build",
            "@markdown_makefile//utils:workspace_contents_bzl",
            "@markdown_makefile//utils:workspace_summary",
            "@markdown_makefile//utils:workspace_publications",
            "@markdown_makefile//utils:bazelversion",
            ".bin/workspace_status",
            "//.workspace_contents:BUILD",
            "//.workspace_contents:workspace_contents.bzl",
            "workspace_summary",
            "workspace_publications",
            ".bazelversion",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_build)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_bzl)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath @markdown_makefile//utils:workspace_publications)",
            "$(rootpath @markdown_makefile//utils:bazelversion)",
            "$(rootpath .bin/workspace_status)",
            "$(rootpath //.workspace_contents:BUILD)",
            "$(rootpath //.workspace_contents:workspace_contents.bzl)",
            "$(rootpath workspace_summary)",
            "$(rootpath workspace_publications)",
            "$(rootpath .bazelversion)",
        ],
        visibility = ["//visibility:private"],
    )
