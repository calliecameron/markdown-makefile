load("//:build_defs.bzl", "md_document", "md_library")
load("//tests:test.bzl", "diff_test")

md_library(
    name = "include1",
    deps = [":include2"],
)

md_library(
    name = "include2",
)

md_document(
    name = "test3",
    data = ["custom-toc.tex"],
    extra_dictionaries = ["extra.dic"],
    extra_latex_flags = ["--include-in-header=$(rootpath custom-toc.tex)"],
    extra_pandoc_flags = [
        "--table-of-contents",
        "--toc-depth=1",
    ],
    timestamp_override = "1618243321",
    version_override = "reproducible",
    deps = [":include1"],
)

diff_test(
    skip_doc = True,
    target = "test3",
)

md_document(
    name = "test3a",
    existing_lib = ":test3",
    extra_latex_flags = ["--include-in-header=$(rootpath custom-toc.tex)"],
    extra_pandoc_flags = [
        "--table-of-contents",
        "--toc-depth=1",
    ],
    main_document = False,
    timestamp_override = "1618243321",
)

diff_test(
    skip_doc = True,
    target = "test3a",
)
