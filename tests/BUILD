load("//:build_defs.bzl", "md_document")

md_document(
    name = "foo",
    main_document = False,
    version_override = "blah",
)

md_document(
    name = "bar",
    extra_latex_flags = ["--number-sections"],
    extra_pandoc_flags = ["--table-of-contents"],
    increment_included_headers = True,
    deps = [":foo"],
)
