load("@buildifier_prebuilt//:rules.bzl", "buildifier_test")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("//markdown/private:defs.bzl", "md_git_repo", "md_workspace")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = ["requires-network"],
)

md_workspace()

md_git_repo(
    extra_gitignore_lines = [
        "/.env",
        "/.mypy_cache/",
        "/.vscode/",
    ],
    extra_precommit = "//tests:extra_precommit.sh",
)

buildifier_test(
    name = "buildifier_test",
    no_sandbox = True,
    workspace = "//:WORKSPACE",
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
