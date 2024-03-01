"""Calibre dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _calibre_impl(_ctx):
    http_archive(
        name = "calibre",
        build_file = "//markdown/external:calibre.build",
        url = "https://download.calibre-ebook.com/6.15.1/calibre-6.15.1-x86_64.txz",
        sha256 = "1c1b1ae0649395593dadd1b39e2cc6552c99b10f1ca175eb594756bd9284c077",
    )

calibre = module_extension(
    implementation = _calibre_impl,
)
