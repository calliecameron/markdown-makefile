load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("//:build_defs.bzl", "md_git_repo", "md_workspace")
load("//utils:validation.bzl", "py_validation", "sh_validation")

compile_pip_requirements(
    name = "requirements",
    requirements_in = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = ["requires-network"],
)

md_workspace(
    registry_override = "file:///%workspace%/registry",
)

md_git_repo()

py_validation()

sh_validation()
