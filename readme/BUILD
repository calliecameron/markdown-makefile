load("@markdown//:defs.bzl", "md_document")
load("//markdown/testing:defs.bzl", "output_test", "versioned_test")

md_document(
    name = "readme",
)

genrule(
    name = "readme_generated",
    srcs = ["output/readme.plain.md"],
    outs = ["readme_generated.md"],
    cmd = "sed 's/\\\\!/!/g' <$< | sed 's/\\\\\\$$/\\$$/g' | sed 's/ / /g' >$@",
    visibility = ["//:__pkg__"],
)

output_test(
    reproducible = False,
    target = "readme",
)

versioned_test(
    target = "readme",
)
