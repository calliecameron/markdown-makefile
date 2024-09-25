import argparse
import csv
import functools
import re
import sys
from collections.abc import Mapping
from typing import Any

import tabulate

from markdown.private.utils.metadata import MetadataMap

TARGET = "target"
TITLE = "title"
AUTHOR = "author"
RAW_DATE = "raw date"
DATE = "date"
WORDCOUNT = "wordcount"
POETRY_LINES = "poetry lines"
FINISHED = "finished"
PUBLICATION = "publication"
VERSION = "version"
STATUS = "status"

COLUMNS = (
    TARGET,
    TITLE,
    AUTHOR,
    RAW_DATE,
    DATE,
    WORDCOUNT,
    POETRY_LINES,
    FINISHED,
    PUBLICATION,
    VERSION,
    STATUS,
)


class Filter:
    def __init__(self, field: str, regex: str) -> None:
        super().__init__()
        self._field = field
        self._regex = regex

    def match(self, data: Mapping[str, Any]) -> bool:
        return re.search(self._regex, str(data[self._field])) is not None


class Sorter:
    def __init__(self, field: str, reverse: bool) -> None:
        super().__init__()
        self._field = field
        self._reverse = reverse

    def key(self, elem: Mapping[str, Any]) -> Any:  # noqa: ANN401
        if self._field == DATE:
            return ", ".join(
                sorted([d.strip() for d in elem[self._field].split(",")], reverse=self._reverse),
            )
        if isinstance(elem[self._field], str):
            return elem[self._field].lower()
        return elem[self._field]

    def sort(self, data: list[Mapping[str, Any]]) -> None:
        data.sort(key=self.key, reverse=self._reverse)


def sanitise(s: str) -> str:
    return s.replace("\n", "\\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarise the contents of the group")
    parser.add_argument("in_file")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="output CSV instead of a human-readable table",
    )
    parser.add_argument("--reverse", action="store_true", help="reverse sorting direction")

    filter_msg = (
        "To be displayed, a row must match any include and no excludes; by default all "
        "rows are displayed"
    )
    includes = parser.add_argument_group("includes", filter_msg)
    excludes = parser.add_argument_group("excludes", filter_msg)
    sorters = parser.add_mutually_exclusive_group()

    for field in COLUMNS:
        name = field.replace(" ", "-")
        includes.add_argument(
            "--include-" + name,
            action="append",
            type=functools.partial(Filter, field),
            dest="includes",
            metavar="regex",
            help="include rows matching regex on " + field,
        )
        excludes.add_argument(
            "--exclude-" + name,
            action="append",
            type=functools.partial(Filter, field),
            dest="excludes",
            metavar="regex",
            help="exclude rows matching regex on " + field,
        )
        sorters.add_argument(
            "--sort-" + name,
            action="store_const",
            const=functools.partial(Sorter, field),
            dest="sorter",
            default=functools.partial(Sorter, field) if field == TARGET else None,
            help="sort by " + field,
        )
    return parser.parse_args()


def should_include(row: Mapping[str, Any], args: argparse.Namespace) -> bool:
    if any(f.match(row) for f in args.excludes or []):
        return False
    if not args.includes:
        return True
    return any(f.match(row) for f in args.includes)


def main() -> None:
    args = parse_args()

    data: list[dict[str, Any]] = []
    with open(args.in_file, encoding="utf-8") as f:
        for target, m in MetadataMap.model_validate_json(f.read()).items():
            publication = ""
            if m.publications:
                publication = (
                    m.publications.highest_active_state.name.lower().replace("_", "-")
                    if m.publications.highest_active_state
                    else "attempted"
                )

            row = {
                TARGET: target,
                TITLE: sanitise(m.title),
                AUTHOR: sanitise(", ".join(m.author)),
                RAW_DATE: sanitise(m.date),
                DATE: sanitise(", ".join(m.parsed_dates)) if m.parsed_dates else "",
                WORDCOUNT: m.wordcount,
                POETRY_LINES: m.poetry_lines,
                FINISHED: "yes" if m.finished else "no",
                PUBLICATION: publication,
                VERSION: m.version,
                STATUS: "DIRTY" if "dirty" in m.version else "ok",
            }

            if should_include(row, args):
                data.append(row)

    args.sorter(args.reverse).sort(data)

    if args.raw:
        out = csv.DictWriter(
            sys.stdout,
            COLUMNS,
        )
        out.writeheader()
        out.writerows(data)
    else:
        print(tabulate.tabulate(data, headers="keys", tablefmt="github"))


if __name__ == "__main__":
    main()
