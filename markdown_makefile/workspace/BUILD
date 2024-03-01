load("//markdown_makefile/python:python.bzl", "py_source")
load("//markdown_makefile/shell:shell.bzl", "sh_source", "sh_test")

exports_files(
    [
        "bazelversion",
        "bazelrc",
    ],
    visibility = ["//visibility:public"],
)

sh_source(
    name = "new_package",
    src = "new_package.sh",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "new_package_test",
    srcs = ["new_package_test.sh"],
    args = ["$(rootpath new_package.sh)"],
    data = ["new_package.sh"],
)

py_source(
    name = "workspace_status",
    src = "workspace_status",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "workspace_status_test",
    srcs = ["workspace_status_test.sh"],
    args = ["$(rootpath workspace_status)"],
    data = ["workspace_status"],
)

sh_source(
    name = "workspace_update",
    src = "workspace_update.sh",
    visibility = ["//visibility:public"],
)

sh_test(
    name = "workspace_update_test",
    srcs = ["workspace_update_test.sh"],
    args = [
        "$(rootpath workspace_update.sh)",
        "$(rootpath workspace_status)",
        "$(rootpath workspace_git_update)",
        "$(rootpath bazelversion)",
        "$(rootpath bazelrc)",
    ],
    data = [
        "bazelrc",
        "bazelversion",
        "workspace_git_update",
        "workspace_status",
        "workspace_update.sh",
    ],
)

sh_source(
    name = "workspace_test",
    src = "workspace_test.sh",
    visibility = ["//visibility:public"],
)

sh_source(
    name = "workspace_git_update",
    src = "workspace_git_update",
    visibility = ["//visibility:public"],
)
