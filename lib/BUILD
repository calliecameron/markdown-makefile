load(":build_defs.bzl", "md_library")

sh_binary(
    name = "gen_metadata",
    srcs = ["gen_metadata.sh"],
)

md_library(
    name = "foo",
    src = "foo.md",
)

sh_test(
    name = "workspace_status_test",
    srcs = ["workspace_status_test.sh"],
    args = ["$(rootpath workspace_status.py)"],
    data = ["workspace_status.py"],
)
