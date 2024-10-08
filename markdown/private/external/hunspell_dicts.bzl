"""Hunspell dicts dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _hunspell_dicts_impl(module_ctx):
    http_archive(
        name = "hunspell_dicts",
        build_file = "//markdown/private/external:hunspell_dicts.build",
        url = "https://github.com/LibreOffice/dictionaries/archive/refs/tags/libreoffice-24.8.2.1.tar.gz",
        sha256 = "9beee5de1c87d130fdeedee201772dbd2846a7f3065c5eb52d5dbcdce559ce9b",
        strip_prefix = "dictionaries-libreoffice-24.8.2.1",
    )

    return module_ctx.extension_metadata(reproducible = True)

hunspell_dicts = module_extension(
    implementation = _hunspell_dicts_impl,
)
