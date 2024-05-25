from collections.abc import Mapping, Sequence
from typing import Any, cast

from pydantic import BaseModel, ConfigDict, field_validator

from markdown.utils.publications import Publications

TITLE = "title"
AUTHOR = "author"
DATE = "date"
NOTES = "notes"
FINISHED = "finished"
PUBLICATIONS = "publications"

DOCVERSION = "docversion"
IDENTIFIER = "identifier"
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


class _BaseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
        extra="forbid",
        alias_generator=lambda s: s.replace("_", "-"),
    )


class Version(_BaseModel):
    docversion: str
    repo: str


class VersionMetadata(_BaseModel):
    docversion: str
    repo: str
    subject: str


class Identifier(_BaseModel):
    scheme: str
    text: str


class _BaseMetadata(_BaseModel):
    title: str = ""
    author: Sequence[str] = []
    date: str = ""
    notes: str = ""
    finished: bool = False
    publications: Publications = Publications.model_construct([])
    identifier: Sequence[Identifier] = []

    @field_validator("author", mode="before")
    @classmethod
    def _convert_author(cls, v: Any) -> Any:  # noqa: ANN401
        if isinstance(v, str):
            return [v]
        if isinstance(v, list) and not v:
            raise ValueError(
                f"metadata item 'author' must be a non-empty list of string or a string; got "
                f"{v}",
            )
        return v


class InputMetadata(_BaseMetadata):
    pass


class OutputMetadata(_BaseMetadata):
    pass
