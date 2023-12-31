load("@aspect_rules_lint//lint:shellcheck.bzl", "shellcheck_binary")

alias(
    name = "ebook_convert",
    actual = "@calibre//:ebook_convert",
    visibility = ["//:__subpackages__"],
)

alias(
    name = "md2short",
    actual = "@prosegrinder_pandoc_templates//:md2short",
    visibility = ["//:__subpackages__"],
)

alias(
    name = "pandoc",
    actual = "@pandoc//:pandoc",
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
