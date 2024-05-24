from collections.abc import Mapping
from typing import Any, cast

from pydantic import BaseModel, ConfigDict

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
SOURCE_HASH = "source-hash"
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
    ],
)


def parse_author(metadata: Mapping[str, Any]) -> str:
    if AUTHOR not in metadata:
        return ""
    author = metadata[AUTHOR]
    if isinstance(author, str):
        return author
    if isinstance(author, list) and author and all(isinstance(a, str) for a in author):
        return cast(str, author[0])
    raise ValueError(
        f"metadata item '{AUTHOR}' must be a non-empty list of string or a string; got {author}",
    )


class Version(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    docversion: str
    repo: str


class VersionMetadata(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
    )

    docversion: str
    repo: str
    subject: str
