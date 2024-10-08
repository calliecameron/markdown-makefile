load("@bazel_skylib//rules:native_binary.bzl", "native_binary")

native_binary(
    name = "ebook_convert",
    src = "@calibre//:bin/ebook-convert",
    visibility = ["//markdown/private/formats/ebook:__pkg__"],
)

native_binary(
    name = "hexdump",
    src = "@hexdump//:bin/hexdump",
    visibility = [
        "//markdown/private/utils:__pkg__",
        "//tests:__subpackages__",
    ],
)

native_binary(
    name = "hunspell",
    src = "@hunspell//:bin/hunspell",
    visibility = [
        "//markdown/private/core:__pkg__",
        "//markdown/private/core/spelling:__pkg__",
    ],
)

alias(
    name = "hunspell_dicts",
    actual = "@hunspell_dicts//:dicts",
    visibility = [
        "//markdown/private/core:__pkg__",
        "//markdown/private/core/spelling:__pkg__",
    ],
)

alias(
    name = "md2short",
    actual = "@prosegrinder_pandoc_templates//:md2short",
    visibility = ["//markdown/private/formats/word:__pkg__"],
)

alias(
    name = "pandoc",
    actual = "@pandoc//:pandoc",
    visibility = [
        "//markdown/private/core:__subpackages__",
        "//markdown/private/formats:__subpackages__",
    ],
)

native_binary(
    name = "pdfinfo",
    src = "@poppler_utils//:bin/pdfinfo",
    visibility = [
        "//markdown/private/utils:__pkg__",
        "//tests:__subpackages__",
    ],
)

native_binary(
    name = "ruff",
    src = "@ruff//:bin/ruff",
    visibility = ["//:__subpackages__"],
)

native_binary(
    name = "shellcheck",
    src = "@shellcheck//:bin/shellcheck",
    visibility = ["//:__subpackages__"],
)

native_binary(
    name = "shfmt",
    src = "@shfmt//:bin/shfmt",
    visibility = ["//:__subpackages__"],
)

native_binary(
    name = "strip_nondeterminism",
    src = "@perl538Packages.strip-nondeterminism//:bin/strip-nondeterminism",
    visibility = [
        "//markdown/private/formats:__subpackages__",
    ],
)

native_binary(
    name = "unoconv",
    src = "@unoconv//:bin/unoconv",
    visibility = [
        "//markdown/private/formats/word:__pkg__",
    ],
)

native_binary(
    name = "unzip",
    src = "@unzip//:bin/unzip",
    visibility = [
        "//markdown/private/utils:__pkg__",
        "//tests:__subpackages__",
    ],
)

native_binary(
    name = "zip",
    src = "@zip//:bin/zip",
    visibility = [
        "//markdown/private/formats:__pkg__",
    ],
)

native_binary(
    name = "zipinfo",
    src = "@unzip//:bin/zipinfo",
    visibility = [
        "//markdown/private/formats:__subpackages__",
        "//tests:__subpackages__",
    ],
)
