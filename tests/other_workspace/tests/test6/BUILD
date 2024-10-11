load("@markdown//:defs.bzl", "md_document")
load("@rules_markdown//markdown/testing:defs.bzl", "output_test", "versioned_test")

md_document(
    name = "test6",
)

output_test(
    reproducible = False,
    target = "test6",
)

versioned_test(
    target = "test6",
)
