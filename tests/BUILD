load("@markdown//:defs.bzl", "md_group", "md_summary")
load("//markdown/private/support/shell:defs.bzl", "sh_source")

sh_source(
    name = "container_test",
    src = "container_test.sh",
    visibility = ["//visibility:private"],
)

sh_source(
    name = "extra_precommit",
    src = "extra_precommit.sh",
    visibility = ["//:__pkg__"],
)

md_group(
    name = "tests",
    deps = [
        "//tests/test1",
        "//tests/test2",
        "//tests/test3",
        "//tests/test4",
        "//tests/test5",
        "//tests/test6",
    ],
)

md_summary()
