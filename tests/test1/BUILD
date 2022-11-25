load("//:build_defs.bzl", "md_document")
load("//tests:test.bzl", "diff_test")

md_document(
    name = "test1",
    version_override = "reproducible",
)

diff_test(
    target = "test1",
)

# SOURCE_DATE_EPOCH := 1618243321
