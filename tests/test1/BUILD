load("@markdown//:defs.bzl", "md_document")
load("//markdown/testing:defs.bzl", "output_test")

md_document(
    name = "test1",
    repo_override = "reproducible",
    timestamp_override = "1618243321",
    version_override = "reproducible",
)

output_test(
    reproducible = True,
    target = "test1",
)
