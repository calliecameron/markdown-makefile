load("//:build_defs.bzl", "md_collection")
load("//tests:test.bzl", "diff_test")

md_collection(
    name = "test4",
    author = "The Author",
    date = "1 January 2022",
    timestamp_override = "1618243321",
    title = "Test 4",
    version_override = "reproducible",
    deps = [
        "//tests/test1",
        "//tests/test2",
        "//tests/test3",
    ],
)

diff_test(
    skip_doc = True,
    target = "test4",
)
