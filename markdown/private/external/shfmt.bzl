"""Shfmt dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_file")

def _shfmt_impl(_ctx):
    http_file(
        name = "shfmt",
        url = "https://github.com/mvdan/sh/releases/download/v3.8.0/shfmt_v3.8.0_linux_amd64",
        sha256 = "27b3c6f9d9592fc5b4856c341d1ff2c88856709b9e76469313642a1d7b558fe0",
        executable = True,
    )

shfmt = module_extension(
    implementation = _shfmt_impl,
)
