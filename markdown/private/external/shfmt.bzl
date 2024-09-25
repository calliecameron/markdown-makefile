"""Shfmt dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_file")

def _shfmt_impl(_ctx):
    http_file(
        name = "shfmt",
        url = "https://github.com/mvdan/sh/releases/download/v3.9.0/shfmt_v3.9.0_linux_amd64",
        sha256 = "d99b06506aee2ac9113daec3049922e70dc8cffb84658e3ae512c6a6cbe101b6",
        executable = True,
    )

shfmt = module_extension(
    implementation = _shfmt_impl,
)
