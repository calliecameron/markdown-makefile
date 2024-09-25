"""Ruff dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _ruff_impl(_ctx):
    http_archive(
        name = "ruff",
        build_file = "//markdown/private/external:ruff.build",
        url = "https://github.com/astral-sh/ruff/releases/download/0.6.7/ruff-x86_64-unknown-linux-gnu.tar.gz",
        sha256 = "52ed7e34c15809f313e3f8ed4281fe523e7e5f0667e7bf9958885b7e6f2270a8",
    )

ruff = module_extension(
    implementation = _ruff_impl,
)
