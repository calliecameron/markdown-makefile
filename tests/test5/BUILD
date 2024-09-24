load("//markdown:defs.bzl", "md_document")
load("//tests:test.bzl", "diff_test")

md_document(
    name = "test5",
    repo_override = "reproducible",
    timestamp_override = "1618243321",
    version_override = "reproducible",
)

diff_test(
    target = "test5",
)
