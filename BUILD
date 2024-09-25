load("@buildifier_prebuilt//:rules.bzl", "buildifier_test")
load("@markdown//:defs.bzl", "md_git_repo", "md_workspace")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = ["requires-network"],
)

md_workspace()

md_git_repo(
    extra_precommit = "//tests:extra_precommit.sh",
)

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
