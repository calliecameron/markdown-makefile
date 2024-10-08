load("@markdown//:defs.bzl", "md_collection", "md_file")
load("//tests:test.bzl", "output_test")

md_collection(
    name = "test4",
    author = "The Author",
    date = "1 January 2022",
    extra_metadata = "test4.yaml",
    repo_override = "reproducible",
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

output_test(
    target = "test4",
)

md_file(
    name = "test4a",
    repo_override = "reproducible",
    version_override = "reproducible",
)
