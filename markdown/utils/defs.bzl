"""Utils macros."""

def _required_files_update(name, files):
    # without the inner quotes, sh_binary will discard this instead of passing
    # an empty arg
    args = [native.package_name() or "''"]
    data = []
    for src, dst, dst_mode in files:
        args += ["$(rootpath %s)" % src, dst, dst_mode]
        data.append(src)

    native.sh_binary(
        name = name + "_update",
        srcs = ["@markdown_makefile//markdown/utils:required_files_update.sh"],
        args = args,
        data = data,
        visibility = ["//visibility:private"],
    )

def _required_files_test(name, files):
    args = ["//%s:%s_update" % (native.package_name(), name)]
    data = []
    for src, dst, dst_mode in files:
        args.append("$(rootpath %s)" % src)
        data.append(src)

        dsts = native.glob([dst])
        if not dsts:
            # without the inner quotes, sh_test will discard this instead of
            # passing an empty arg
            args.append("''")
        elif len(dsts) == 1:
            args.append("$(rootpath %s)" % dst)
            data.append(dst)
        else:
            fail("found multiple files matching", dst)

        args.append(dst_mode)

    native.sh_test(
        name = name + "_test",
        srcs = ["@markdown_makefile//markdown/utils:required_files_test.sh"],
        args = args,
        data = data,
        visibility = ["//visibility:private"],
    )

def required_files(name, files):
    """A set of files that must exist in the source tree with specific contents.

    Creates a test to check that the files are correct, and a binary to update
    them.

    Args:
        name: name of the set of files.
        files: list of (src, dst, dst_mode) tuples of the files; dst is relative
            to the package.
    """

    if not files:
        fail("no files specified")

    for f in files:
        if len(f) != 3:
            fail("each entry in files must be a tuple (src, dst, dst_mode); got", f)

    _required_files_update(name, files)
    _required_files_test(name, files)
