load("//markdown_makefile/validation:validation.bzl", "validation_srcs")

exports_files(
    [
        "new_package.sh",
        "workspace_status",
        "workspace_contents_build",
        "workspace_contents_bzl",
        "workspace_summary",
        "workspace_publications",
        "workspace_git_update",
        "bazelversion",
        "bazelrc",
        "workspace_update.sh",
        "workspace_test.sh",
    ],
    visibility = ["//visibility:public"],
)

validation_srcs(
    extra_py_files = ["workspace_status"],
    extra_sh_files = [
        "workspace_git_update",
        "workspace_publications",
        "workspace_summary",
    ],
)

sh_test(
    name = "new_package_test",
    srcs = ["new_package_test.sh"],
    args = ["$(rootpath new_package.sh)"],
    data = ["new_package.sh"],
)

sh_test(
    name = "workspace_status_test",
    srcs = ["workspace_status_test.sh"],
    args = ["$(rootpath workspace_status)"],
    data = ["workspace_status"],
)

sh_test(
    name = "workspace_update_test",
    srcs = ["workspace_update_test.sh"],
    args = [
        "$(rootpath workspace_update.sh)",
        "$(rootpath workspace_status)",
        "$(rootpath workspace_contents_build)",
        "$(rootpath workspace_contents_bzl)",
        "$(rootpath workspace_summary)",
        "$(rootpath workspace_publications)",
        "$(rootpath workspace_git_update)",
        "$(rootpath bazelversion)",
        "$(rootpath bazelrc)",
    ],
    data = [
        "bazelrc",
        "bazelversion",
        "workspace_contents_build",
        "workspace_contents_bzl",
        "workspace_git_update",
        "workspace_publications",
        "workspace_status",
        "workspace_summary",
        "workspace_update.sh",
    ],
)
