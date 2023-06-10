from typing import Any, Dict, cast

TITLE = "title"
AUTHOR = "author"
DATE = "date"
NOTES = "notes"
FINISHED = "finished"
PUBLICATIONS = "publications"

USER_KEYS = frozenset(
    [
        TITLE,
        AUTHOR,
        DATE,
        NOTES,
        FINISHED,
        PUBLICATIONS,
    ]
)

KNOWN_KEYS = USER_KEYS | frozenset(
    [
        # Keys added by the author
        # Keys added during processing
        "docversion",
        "identifier",
        "increment-included-headers",
        "lang",
        "metadata-out-file",
        "repo",
        "source-md5",
        "subject",
    ]
)


def parse_author(metadata: Dict[str, Any]) -> str:
    if AUTHOR not in metadata:
        return ""
    author = metadata[AUTHOR]
    if isinstance(author, str):
        return author
    if isinstance(author, list) and author and all([isinstance(a, str) for a in author]):
        return cast(str, author[0])
    raise ValueError(
        "metadata item '%s' must be a non-empty list of string or a string; got %s"
        % (AUTHOR, str(author))
    )
