load("//markdown/support/python:defs.bzl", "py_test")
load("//markdown/support/shell:defs.bzl", "sh_binary")

exports_files(
    [
        "spellcheck_input_template.md",
        "spellcheck_filter.lua",
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "spellcheck_filter_test",
    srcs = ["spellcheck_filter_test.py"],
    args = [
        "$(rootpath //markdown/external:pandoc)",
        "$(rootpath spellcheck_filter.lua)",
    ],
    data = [
        "spellcheck_filter.lua",
        "//markdown/external:pandoc",
    ],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "spellcheck",
    srcs = ["spellcheck.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "spellcheck_test",
    srcs = ["spellcheck_test.py"],
    args = ["$(rootpath :spellcheck)"],
    data = [":spellcheck"],
    deps = ["//markdown/utils:test_utils"],
)

sh_binary(
    name = "gen_dictionary",
    srcs = ["gen_dictionary.sh"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "gen_dictionary_test",
    srcs = ["gen_dictionary_test.py"],
    args = ["$(rootpath :gen_dictionary)"],
    data = [":gen_dictionary"],
    deps = ["//markdown/utils:test_utils"],
)
