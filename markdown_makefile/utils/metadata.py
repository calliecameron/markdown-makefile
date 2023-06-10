from typing import Any, Dict, cast

TITLE = "title"
AUTHOR = "author"
DATE = "date"
NOTES = "notes"
FINISHED = "finished"
PUBLICATIONS = "publications"

DOCVERSION = "docversion"
IDENTIFIER = "identifier"
INCREMENT_INCLUDED_HEADERS = "increment-included-headers"
LANG = "lang"
METADATA_OUT_FILE = "metadata-out-file"
POETRY_LINES = "poetry-lines"
REPO = "repo"
SOURCE_MD5 = "source-md5"
SUBJECT = "subject"
WORDCOUNT = "wordcount"


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
