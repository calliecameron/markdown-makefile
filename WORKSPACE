load("//:bazel_deps.bzl", "install_bazel_deps")

install_bazel_deps()

load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "pip",
    requirements_lock = "//:requirements_lock.txt",
)

load("@pip//:requirements.bzl", "install_deps")

install_deps()
