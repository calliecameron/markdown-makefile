load("@buildifier_prebuilt//:rules.bzl", "buildifier_test")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("//:build_defs.bzl", "md_git_repo", "md_workspace")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = ["requires-network"],
)

md_workspace()

md_git_repo()

buildifier_test(
    name = "buildifier_test",
    no_sandbox = True,
    workspace = "//:WORKSPACE.bazel",
)

exports_files(
    [
        "pyproject.toml",
    ],
    visibility = ["//:__subpackages__"],
)

exports_files(
    [
        "pymarkdown.json",
    ],
    visibility = ["//visibility:public"],
)
