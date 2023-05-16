load("//:build_defs.bzl", "md_document")
load("//tests:test.bzl", "diff_test")

md_document(
    name = "test5",
    timestamp_override = "1618243321",
    version_override = "reproducible",
)

diff_test(
    target = "test5",
)
