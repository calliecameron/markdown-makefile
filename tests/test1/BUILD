load("@markdown//:defs.bzl", "md_document")
load("//tests:test.bzl", "output_test")

md_document(
    name = "test1",
    repo_override = "reproducible",
    timestamp_override = "1618243321",
    version_override = "reproducible",
)

output_test(
    target = "test1",
)
