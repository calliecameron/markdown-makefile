load("//:build_defs.bzl", "md_document")

md_document(
    name = "foo",
    main_document = False,
    version_override = "blah",
)

md_document(
    name = "bar",
    data = ["custom-toc.tex"],
    extra_latex_flags = [
        "--number-sections",
        "--include-in-header=$(rootpath custom-toc.tex)",
    ],
    extra_pandoc_flags = [
        "--table-of-contents",
        "--toc-depth=1",
    ],
    increment_included_headers = True,
    deps = [":foo"],
)

exports_files(
    ["diff_test.sh"],
    visibility = ["__subpackages__"],
)
