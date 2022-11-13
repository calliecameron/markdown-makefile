load(":build_defs.bzl", "md_library")

# sh_binary(
#     name = "gen_metadata",
#     srcs = ["gen_metadata.sh"],
# )

md_library(
    name = "foo",
    src = "foo.md",
)

py_library(
    name = "bazel_package",
    srcs = ["bazel_package.py"],
)

py_test(
    name = "bazel_package_test",
    srcs = ["bazel_package_test.py"],
    deps = [":bazel_package"],
)

sh_test(
    name = "workspace_status_test",
    srcs = ["workspace_status_test.sh"],
    args = ["$(rootpath workspace_status.py)"],
    data = [
        "bazel_package.py",
        "workspace_status.py",
    ],
)

py_binary(
    name = "raw_version",
    srcs = ["raw_version.py"],
    deps = [":bazel_package"],
)

sh_test(
    name = "raw_version_test",
    srcs = ["raw_version_test.sh"],
    args = ["$(rootpath raw_version.py)"],
    data = ["raw_version.py"],
)
