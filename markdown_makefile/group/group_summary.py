import argparse
import csv
import functools
import json
import re
import sys
from collections.abc import Mapping
from typing import Any

import tabulate
from dateparser.date import DateDataParser
from dateparser.search import search_dates

from markdown_makefile.utils import metadata
from markdown_makefile.utils.publications import Publications

TARGET = "target"
TITLE = "title"
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


def parse_date(date: str) -> str:
    settings = {"DATE_ORDER": "DMY", "PARSERS": ["custom-formats", "absolute-time"]}
    parser = DateDataParser(["en"], ["en-GB"], settings=settings)  # type: ignore[arg-type]

    out = set()
    for text, _ in search_dates(date, languages=["en"], settings=settings) or []:
        data = parser.get_date_data(text)
        if data.date_obj:
            if data.period == "year":
                out.add(data.date_obj.strftime("%Y"))
            elif data.period == "month":
                out.add(data.date_obj.strftime("%Y/%m"))
            elif data.period == "day":
                out.add(data.date_obj.strftime("%Y/%m/%d"))

    return ", ".join(sorted(out))


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
        for target, j in json.load(f).items():
            publication = ""
            if metadata.PUBLICATIONS in j and j[metadata.PUBLICATIONS]:
                ps = Publications.from_json(j[metadata.PUBLICATIONS])
                publication = ps.highest_active_state if ps.active else "attempted"

            row = {
                TARGET: target,
                TITLE: sanitise(j.get(metadata.TITLE, "")),
                RAW_DATE: sanitise(j.get(metadata.DATE, "")),
                DATE: sanitise(parse_date(j[metadata.DATE])) if metadata.DATE in j else "",
                WORDCOUNT: int(j[metadata.WORDCOUNT]),
                POETRY_LINES: int(j[metadata.POETRY_LINES]),
                FINISHED: "yes" if metadata.FINISHED in j and j[metadata.FINISHED] else "no",
                PUBLICATION: publication,
                VERSION: j[metadata.DOCVERSION],
                STATUS: "DIRTY" if "dirty" in j[metadata.DOCVERSION] else "ok",
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
