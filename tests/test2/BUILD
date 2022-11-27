load("//:build_defs.bzl", "md_document")
load("//tests:test.bzl", "diff_test")

md_document(
    name = "test2",
    extra_latex_flags = ["--variable=section-page-break"],
    images = ["image.png"],
    timestamp_override = "1618243321",
    version_override = "reproducible",
)

diff_test(
    target = "test2",
)
