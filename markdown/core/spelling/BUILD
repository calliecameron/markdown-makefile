load("//markdown/support/shell:defs.bzl", "sh_binary")
load("//markdown/utils:defs.bzl", "pandoc_filter_test", "script_test")

exports_files(
    [
        "spellcheck_input_template.md",
        "spellcheck_filter.lua",
        "spellcheck_cleanup.lua",
    ],
    visibility = ["//visibility:public"],
)

pandoc_filter_test(
    name = "spellcheck_filter_test",
    src = "spellcheck_filter_test.py",
    filter = "spellcheck_filter.lua",
)

pandoc_filter_test(
    name = "spellcheck_cleanup_test",
    src = "spellcheck_cleanup_test.py",
    filter = "spellcheck_cleanup.lua",
)

sh_binary(
    name = "spellcheck",
    srcs = ["spellcheck.sh"],
    visibility = ["//visibility:public"],
)

script_test(
    name = "spellcheck_test",
    src = "spellcheck_test.py",
    script = ":spellcheck",
)

sh_binary(
    name = "gen_dictionary",
    srcs = ["gen_dictionary.sh"],
    visibility = ["//visibility:public"],
)

script_test(
    name = "gen_dictionary_test",
    src = "gen_dictionary_test.py",
    script = ":gen_dictionary",
)
