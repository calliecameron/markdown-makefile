"""Pandoc dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _pandoc_impl(_ctx):
    http_archive(
        name = "pandoc",
        build_file = "//markdown/external:pandoc.build",
        url = "https://github.com/jgm/pandoc/releases/download/3.1.2/pandoc-3.1.2-linux-amd64.tar.gz",
        sha256 = "4e1c607f7e4e9243fa1e1f5b208cd4f1d3f6fd055d5d8c39ba0cdc38644e1c35",
        strip_prefix = "pandoc-3.1.2",
    )

pandoc = module_extension(
    implementation = _pandoc_impl,
)
