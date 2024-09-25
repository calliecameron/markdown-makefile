"""Shellcheck dependency."""

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def _shellcheck_impl(_ctx):
    http_archive(
        name = "shellcheck",
        build_file = "//markdown/private/external:shellcheck.build",
        url = "https://github.com/koalaman/shellcheck/releases/download/v0.10.0/shellcheck-v0.10.0.linux.x86_64.tar.xz",
        sha256 = "6c881ab0698e4e6ea235245f22832860544f17ba386442fe7e9d629f8cbedf87",
    )

shellcheck = module_extension(
    implementation = _shellcheck_impl,
)
