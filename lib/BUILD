load("@rules_python//python:defs.bzl", "py_binary", "py_library", "py_test")
load(":build_defs.bzl", "md_library", "md_md", "md_txt")

md_library(
    name = "foo",
    src = "foo.md",
    dictionaries = ["foo.dic"],
    version_override = "blah",
)

md_md(
    name = "foo_md",
    lib = ":foo",
)

md_txt(
    name = "foo_txt",
    lib = ":foo",
)

md_library(
    name = "bar",
    src = "bar.md",
    dictionaries = ["bar.dic"],
    increment_included_headers = True,
    deps = [":foo"],
)

md_md(
    name = "bar_md",
    lib = ":bar",
)

py_library(
    name = "bazel_package",
    srcs = ["bazel_package.py"],
)

py_test(
    name = "bazel_package_test",
    srcs = ["bazel_package_test.py"],
    deps = [":bazel_package"],
)

sh_test(
    name = "workspace_status_test",
    srcs = ["workspace_status_test.sh"],
    args = ["$(rootpath workspace_status.py)"],
    data = [
        "bazel_package.py",
        "workspace_status.py",
    ],
)

py_binary(
    name = "raw_version",
    srcs = ["raw_version.py"],
    visibility = ["//visibility:public"],
    deps = [":bazel_package"],
)

py_test(
    name = "raw_version_test",
    srcs = ["raw_version_test.py"],
    args = ["$(rootpath raw_version.py)"],
    data = ["raw_version.py"],
)

py_binary(
    name = "base_metadata",
    srcs = ["base_metadata.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "base_metadata_test",
    srcs = ["base_metadata_test.py"],
    args = ["$(rootpath base_metadata.py)"],
    data = ["base_metadata.py"],
    deps = [":base_metadata"],
)

py_binary(
    name = "preprocess",
    srcs = ["preprocess.py"],
    visibility = ["//visibility:public"],
    deps = [":bazel_package"],
)

py_test(
    name = "preprocess_test",
    srcs = ["preprocess_test.py"],
    args = ["$(rootpath preprocess.py)"],
    data = ["preprocess.py"],
    deps = [":preprocess"],
)

py_library(
    name = "test_utils",
    testonly = True,
    srcs = ["test_utils.py"],
)

filegroup(
    name = "validate",
    srcs = ["validate.py"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "validate_test",
    srcs = ["validate_test.py"],
    args = ["$(rootpath validate.py)"],
    data = ["validate.py"],
    deps = [":test_utils"],
)

filegroup(
    name = "include",
    srcs = ["include.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "include_test",
    srcs = ["include_test.py"],
    args = ["$(rootpath include.lua)"],
    data = ["include.lua"],
    deps = [":test_utils"],
)

filegroup(
    name = "wordcount",
    srcs = ["wordcount.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "wordcount_test",
    srcs = ["wordcount_test.py"],
    args = ["$(rootpath wordcount.lua)"],
    data = ["wordcount.lua"],
    deps = [":test_utils"],
)

filegroup(
    name = "starts_with_text",
    srcs = ["starts_with_text.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "starts_with_text_test",
    srcs = ["starts_with_text_test.py"],
    args = ["$(rootpath starts_with_text.lua)"],
    data = ["starts_with_text.lua"],
    deps = [":test_utils"],
)

filegroup(
    name = "write_metadata",
    srcs = ["write_metadata.lua"],
    visibility = ["//visibility:public"],
)

py_test(
    name = "write_metadata_test",
    srcs = ["write_metadata_test.py"],
    args = ["$(rootpath write_metadata.lua)"],
    data = ["write_metadata.lua"],
    deps = [":test_utils"],
)

sh_binary(
    name = "write_dictionary",
    srcs = ["write_dictionary.sh"],
)

py_test(
    name = "write_dictionary_test",
    srcs = ["write_dictionary_test.py"],
    args = ["$(rootpath write_dictionary.sh)"],
    data = ["write_dictionary.sh"],
)

filegroup(
    name = "spellcheck_input_template",
    srcs = ["spellcheck_input_template.md"],
    visibility = ["//visibility:public"],
)

sh_binary(
    name = "spellcheck",
    srcs = ["spellcheck.sh"],
)

py_test(
    name = "spellcheck_test",
    srcs = ["spellcheck_test.py"],
    args = ["$(rootpath spellcheck.sh)"],
    data = ["spellcheck.sh"],
)

sh_binary(
    name = "write_open_script",
    srcs = ["write_open_script.sh"],
)

py_test(
    name = "write_open_script_test",
    srcs = ["write_open_script_test.py"],
    args = ["$(rootpath write_open_script.sh)"],
    data = ["write_open_script.sh"],
)
