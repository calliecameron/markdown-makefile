load("@buildifier_prebuilt//:rules.bzl", "buildifier_test")
load("@markdown//:defs.bzl", "md_git_repo", "md_workspace")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = ["requires-network"],
)

md_workspace(
    extra_bazelrc_lines = [
        "build --deleted_packages=tests/other_workspace,tests/other_workspace/.markdown_summary,tests/other_workspace/test2,tests/other_workspace/test3,tests/other_workspace/test3/.markdown_summary,tests/other_workspace/test4",
        "query --deleted_packages=tests/other_workspace,tests/other_workspace/.markdown_summary,tests/other_workspace/test2,tests/other_workspace/test3,tests/other_workspace/test3/.markdown_summary,tests/other_workspace/test4",
    ],
)

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
