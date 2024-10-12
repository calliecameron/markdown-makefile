load("@markdown//:defs.bzl", "md_document", "md_file")
load("//markdown/private/utils:defs.bzl", "extend_file")
load("//markdown/testing:defs.bzl", "output_test")

extend_file(
    name = "bazeliskrc_md",
    src = "//markdown/private/workspace:default_bazeliskrc",
    out = "bazeliskrc.md",
    append_lines = ["```"],
    prepend_lines = ["```text"],
)

md_file(
    name = "bazeliskrc",
    src = ":bazeliskrc_md",
    repo_override = "reproducible",
    version_override = "reproducible",
)

extend_file(
    name = "bazelrc_md",
    src = "//markdown/private/workspace:default_bazelrc",
    out = "bazelrc.md",
    append_lines = ["```"],
    prepend_lines = ["```text"],
)

md_file(
    name = "bazelrc",
    src = ":bazelrc_md",
    repo_override = "reproducible",
    version_override = "reproducible",
)

md_document(
    name = "readme",
    repo_override = "reproducible",
    timestamp_override = "1618243321",
    version_override = "reproducible",
    deps = [
        ":bazeliskrc",
        ":bazelrc",
    ],
)

genrule(
    name = "readme_generated",
    srcs = ["output/readme.plain.md"],
    outs = ["readme_generated.md"],
    cmd = "sed 's/\\\\!/!/g' <$< | sed 's/\\\\\\$$/\\$$/g' | sed 's/ / /g' >$@",
    visibility = ["//:__pkg__"],
)

output_test(
    # It is reproducible, but we don't need diff tests since we use
    # requried_files elsewhere.
    reproducible = False,
    target = "readme",
)
