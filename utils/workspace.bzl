"""Workspace macros."""

_DEFAULT_REGISTRY = "https://raw.githubusercontent.com/calliecameron/markdown-makefile/master/registry"

def md_workspace(registry_override = None, name = None):  # buildifier: disable=unused-variable
    registry = registry_override or _DEFAULT_REGISTRY

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
            "@markdown_makefile//utils:workspace_git_update",
            "@markdown_makefile//utils:bazelversion",
            "@markdown_makefile//utils:bazelrc",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_build)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_bzl)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath @markdown_makefile//utils:workspace_publications)",
            "$(rootpath @markdown_makefile//utils:workspace_git_update)",
            "$(rootpath @markdown_makefile//utils:bazelversion)",
            "$(rootpath @markdown_makefile//utils:bazelrc)",
            registry,
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
            "@markdown_makefile//utils:workspace_git_update",
            "@markdown_makefile//utils:bazelversion",
            "@markdown_makefile//utils:bazelrc",
            ".bin/workspace_status",
            "//.workspace_contents:BUILD",
            "//.workspace_contents:workspace_contents.bzl",
            "workspace_summary",
            "workspace_publications",
            "workspace_git_update",
            ".bazelversion",
            ".bazelrc",
        ],
        args = [
            "$(rootpath @markdown_makefile//utils:workspace_status)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_build)",
            "$(rootpath @markdown_makefile//utils:workspace_contents_bzl)",
            "$(rootpath @markdown_makefile//utils:workspace_summary)",
            "$(rootpath @markdown_makefile//utils:workspace_publications)",
            "$(rootpath @markdown_makefile//utils:workspace_git_update)",
            "$(rootpath @markdown_makefile//utils:bazelversion)",
            "$(rootpath @markdown_makefile//utils:bazelrc)",
            "$(rootpath .bin/workspace_status)",
            "$(rootpath //.workspace_contents:BUILD)",
            "$(rootpath //.workspace_contents:workspace_contents.bzl)",
            "$(rootpath workspace_summary)",
            "$(rootpath workspace_publications)",
            "$(rootpath workspace_git_update)",
            "$(rootpath .bazelversion)",
            "$(rootpath .bazelrc)",
            registry,
        ],
        visibility = ["//visibility:private"],
    )
