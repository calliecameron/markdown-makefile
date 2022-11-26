load("//:build_defs.bzl", "md_collection", "md_library")
load("//tests:test.bzl", "diff_test")

md_collection(
    name = "test4",
    author = "The Author",
    date = "1 January 2022",
    extra_metadata = "test4.yaml",
    timestamp_override = "1618243321",
    title = "Test 4",
    version_override = "reproducible",
    deps = [
        # do not sort
        "//tests/test1",
        "//tests/test2",
        "//tests/test3",
        ":test4a",
    ],
)

diff_test(
    skip_doc = True,
    target = "test4",
)

md_library(
    name = "test4a",
    version_override = "reproducible",
)
