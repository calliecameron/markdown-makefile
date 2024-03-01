"""Dynamic group macros."""

def md_dynamic_group(name = None):  # buildifier: disable=unused-variable
    native.sh_binary(
        name = "dynamic_group_update",
        srcs = ["@markdown_makefile//markdown/dynamic_group:dynamic_group_update.sh"],
        data = [
            "@markdown_makefile//markdown/dynamic_group:contents_build",
            "@markdown_makefile//markdown/dynamic_group:contents_bzl",
            "@markdown_makefile//markdown/dynamic_group:contents_update",
            "@markdown_makefile//markdown/dynamic_group:summary",
            "@markdown_makefile//markdown/dynamic_group:publications",
        ],
        args = [
            "$(rootpath @markdown_makefile//markdown/dynamic_group:contents_build)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:contents_bzl)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:contents_update)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:summary)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:publications)",
            native.package_name(),
        ],
        visibility = ["//visibility:private"],
    )

    contents_package = "//" + (native.package_name() + "/" if native.package_name() else "") + ".dynamic_group_contents"

    native.sh_test(
        name = "dynamic_group_test",
        srcs = ["@markdown_makefile//markdown/dynamic_group:dynamic_group_test.sh"],
        data = [
            "@markdown_makefile//markdown/dynamic_group:contents_build",
            "@markdown_makefile//markdown/dynamic_group:contents_bzl",
            "@markdown_makefile//markdown/dynamic_group:contents_update",
            "@markdown_makefile//markdown/dynamic_group:summary",
            "@markdown_makefile//markdown/dynamic_group:publications",
            contents_package + ":BUILD",
            contents_package + ":contents.bzl",
            contents_package + ":update",
            "summary",
            "publications",
        ],
        args = [
            "$(rootpath @markdown_makefile//markdown/dynamic_group:contents_build)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:contents_bzl)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:contents_update)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:summary)",
            "$(rootpath @markdown_makefile//markdown/dynamic_group:publications)",
            "$(rootpath %s:BUILD)" % contents_package,
            "$(rootpath %s:contents.bzl)" % contents_package,
            "$(rootpath %s:update)" % contents_package,
            "$(rootpath summary)",
            "$(rootpath publications)",
        ],
        visibility = ["//visibility:private"],
    )
