load("@aspect_rules_lint//lint:shellcheck.bzl", "shellcheck_binary")

alias(
    name = "ebook_convert",
    actual = "@calibre//:ebook_convert",
    visibility = ["//markdown/formats/ebook:__pkg__"],
)

alias(
    name = "md2short",
    actual = "@prosegrinder_pandoc_templates//:md2short",
    visibility = ["//markdown/formats/word:__pkg__"],
)

alias(
    name = "pandoc",
    actual = "@pandoc//:pandoc",
    visibility = [
        "//markdown/core:__subpackages__",
        "//markdown/formats:__subpackages__",
    ],
)

alias(
    name = "ruff",
    actual = "@ruff_x86_64-unknown-linux-gnu//:ruff",
    visibility = ["//:__subpackages__"],
)

shellcheck_binary(
    name = "_shellcheck",
)

alias(
    name = "shellcheck",
    actual = ":_shellcheck",
    visibility = ["//:__subpackages__"],
)

alias(
    name = "shfmt",
    actual = "@shfmt_linux_x86_64//file:shfmt",
    visibility = ["//:__subpackages__"],
)
