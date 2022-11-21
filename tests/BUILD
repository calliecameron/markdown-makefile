load("//:build_defs.bzl", "md_document")

md_document(
    name = "foo",
    main_document = False,
    version_override = "blah",
)

md_document(
    name = "bar",
    increment_included_headers = True,
    deps = [":foo"],
)
