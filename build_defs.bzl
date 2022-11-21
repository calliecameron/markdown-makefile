"""Public API of the module."""

load("//core:build_defs.bzl", _md_library = "md_library")
load("//formats:misc.bzl", _md_md = "md_md", _md_txt = "md_txt")
load("//formats:latex.bzl", _md_pdf = "md_pdf", _md_tex = "md_tex", _md_tex_intermediate = "md_tex_intermediate")
load("//formats:ebook.bzl", _md_epub = "md_epub", _md_mobi = "md_mobi")
load("//formats:word.bzl", _md_doc = "md_doc", _md_docx = "md_docx", _md_ms_docx = "md_ms_docx", _md_odt = "md_odt")

_FORMATS = [
    "md",
    "txt",
    "tex",
    "pdf",
    "epub",
    "mobi",
    "odt",
    "docx",
    "doc",
    "ms_docx",
]

def md_library(
        name,
        src = None,
        deps = None,
        extra_dictionaries = None,
        increment_included_headers = False,
        version_override = ""):
    """md_library represents a markdown source file.

    Args:
        name: the name of the library.
        src: the source file, if different from <name>.md.
        deps: other md_library targets used in !include statements in src.
        extra_dictionaries: extra dictionaries for spellchecking.
        increment_included_headers: if true, header level in included files is
            incremented, e.g. level 1 headers become level 2 headers. If false,
            headers are unchanged.
        version_override: set the document version to this value, rather than
           the computed value. Should only be used for testing.
    """
    if not src:
        src = name + ".md"
    deps = deps or []
    extra_dictionaries = extra_dictionaries or []

    _md_library(
        name = name,
        src = src,
        deps = deps,
        dictionaries = native.glob([name + ".dic"]) + extra_dictionaries,
        increment_included_headers = increment_included_headers,
        version_override = version_override,
        visibility = ["//visibility:public"],
    )

def md_document(
        name,
        deps = None,
        extra_dictionaries = None,
        increment_included_headers = False,
        version_override = None,
        existing_lib = None,
        main_document = True):
    """md_document compiles a markdown source file into many formats.

    Args:
        name: the name of the document.
        deps: other md_library targets used in !include statements in src.
        extra_dictionaries: extra dictionaries for spellchecking.
        increment_included_headers: if true, header level in included files is
            incremented, e.g. level 1 headers become level 2 headers. If false,
            headers are unchanged.
        version_override: set the document version to this value, rather than
            the computed value. Should only be used for testing.
        existing_lib: use an existing md_library rather than creating one; if
            set, most other args must not be set.
        main_document: whether this is the main document in the package; creates
            some convenience aliases.
    """
    if existing_lib:
        if deps or extra_dictionaries or increment_included_headers or version_override:
            native.fail("Other args must not be set when existing_lib is set")
        lib = existing_lib
    else:
        md_library(
            name = name,
            deps = deps,
            extra_dictionaries = extra_dictionaries,
            increment_included_headers = increment_included_headers,
            version_override = version_override,
        )
        lib = name

    _md_md(
        name = name + "_md",
        lib = lib,
        visibility = ["//visibility:private"],
    )
    _md_txt(
        name = name + "_txt",
        lib = lib,
        visibility = ["//visibility:private"],
    )
    _md_tex_intermediate(
        name = name + "_tex_intermediate",
        lib = lib,
        visibility = ["//visibility:private"],
    )
    _md_tex(
        name = name + "_tex",
        intermediate = name + "_tex_intermediate",
        visibility = ["//visibility:private"],
    )
    _md_pdf(
        name = name + "_pdf",
        intermediate = name + "_tex_intermediate",
        visibility = ["//visibility:private"],
    )
    _md_epub(
        name = name + "_epub",
        lib = lib,
        visibility = ["//visibility:private"],
    )
    _md_mobi(
        name = name + "_mobi",
        epub = name + "_epub",
        visibility = ["//visibility:private"],
    )
    _md_odt(
        name = name + "_odt",
        lib = lib,
        visibility = ["//visibility:private"],
    )
    _md_docx(
        name = name + "_docx",
        lib = lib,
        visibility = ["//visibility:private"],
    )
    _md_doc(
        name = name + "_doc",
        docx = name + "_docx",
        visibility = ["//visibility:private"],
    )
    _md_ms_docx(
        name = name + "_ms_docx",
        lib = lib,
        visibility = ["//visibility:private"],
    )

    native.filegroup(
        name = name + "_all",
        srcs = [name + "_" + f for f in _FORMATS],
        visibility = ["//visibility:private"],
    )

    if main_document:
        for f in _FORMATS:
            native.alias(
                name = f,
                actual = name + "_" + f,
                visibility = ["//visibility:private"],
            )
