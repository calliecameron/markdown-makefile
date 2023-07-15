import argparse
import csv
import json
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List

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


class Sorter(ABC):
    def __init__(self, reverse: bool) -> None:
        super().__init__()
        self._reverse = reverse

    @abstractmethod
    def key(self, elem: Dict[str, Any]) -> Any:
        raise NotImplementedError

    def sort(self, data: List[Dict[str, Any]]) -> None:
        data.sort(key=self.key, reverse=self._reverse)


class SimpleSorter(Sorter):
    def __init__(self, reverse: bool, key: str) -> None:
        super().__init__(reverse)
        self._reverse = reverse
        self._key = key

    def key(self, elem: Dict[str, Any]) -> Any:
        return elem[self._key]


class TargetSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(reverse, TARGET)


class TitleSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(reverse, TITLE)


class DateSorter(Sorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse)

    def key(self, elem: Dict[str, Any]) -> Any:
        return ", ".join(sorted([d.strip() for d in elem[DATE].split(",")], reverse=self._reverse))


class WordcountSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, WORDCOUNT)


class PoetryLinesSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, POETRY_LINES)


class FinishedSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, FINISHED)


class PublicationSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(reverse, PUBLICATION)


class VersionSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(reverse, VERSION)


class StatusSorter(SimpleSorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(reverse, STATUS)


def parse_date(date: str) -> str:
    settings = {"DATE_ORDER": "DMY", "PARSERS": ["custom-formats", "absolute-time"]}
    parser = DateDataParser(["en"], ["en-GB"], settings=settings)  # type: ignore

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


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarise the contents of the group")
    parser.add_argument("in_file")
    parser.add_argument("--filter", help="include only entries whose target contains this string")
    parser.add_argument(
        "--raw", action="store_true", help="output CSV instead of a human-readable table"
    )
    parser.add_argument("--reverse", action="store_true", help="reverse sorting direction")
    sorters = parser.add_mutually_exclusive_group()
    sorters.add_argument(
        "--target",
        action="store_const",
        const=TargetSorter,
        dest="sorter",
        default=TargetSorter,
        help="sort by target",
    )
    sorters.add_argument(
        "--title",
        action="store_const",
        const=TitleSorter,
        dest="sorter",
        help="sort by title",
    )
    sorters.add_argument(
        "--date", action="store_const", const=DateSorter, dest="sorter", help="sort by date"
    )
    sorters.add_argument(
        "--wordcount",
        action="store_const",
        const=WordcountSorter,
        dest="sorter",
        help="sort by wordcount",
    )
    sorters.add_argument(
        "--poetry_lines",
        action="store_const",
        const=PoetryLinesSorter,
        dest="sorter",
        help="sort by poetry lines",
    )
    sorters.add_argument(
        "--finished",
        action="store_const",
        const=FinishedSorter,
        dest="sorter",
        help="sort by finished",
    )
    sorters.add_argument(
        "--publication",
        action="store_const",
        const=PublicationSorter,
        dest="sorter",
        help="sort by publication",
    )
    sorters.add_argument(
        "--version",
        action="store_const",
        const=VersionSorter,
        dest="sorter",
        help="sort by version",
    )
    sorters.add_argument(
        "--status",
        action="store_const",
        const=StatusSorter,
        dest="sorter",
        help="sort by status",
    )
    args = parser.parse_args()

    data = []  # type: List[Dict[str, Any]]
    with open(args.in_file, encoding="utf-8") as f:
        for target, j in json.load(f).items():
            if not args.filter or args.filter in target:
                publication = ""
                if metadata.PUBLICATIONS in j and j[metadata.PUBLICATIONS]:
                    ps = Publications.from_json(j[metadata.PUBLICATIONS])
                    if ps.active:
                        publication = ps.highest_active_state
                    else:
                        publication = "attempted"

                data.append(
                    {
                        TARGET: target,
                        TITLE: sanitise(j.get(metadata.TITLE, "")),
                        RAW_DATE: sanitise(j.get(metadata.DATE, "")),
                        DATE: sanitise(parse_date(j[metadata.DATE])) if metadata.DATE in j else "",
                        WORDCOUNT: int(j[metadata.WORDCOUNT]),
                        POETRY_LINES: int(j[metadata.POETRY_LINES]),
                        FINISHED: "yes"
                        if metadata.FINISHED in j and j[metadata.FINISHED]
                        else "no",
                        PUBLICATION: publication,
                        VERSION: j[metadata.DOCVERSION],
                        STATUS: "DIRTY" if "dirty" in j[metadata.DOCVERSION] else "ok",
                    }
                )

    args.sorter(args.reverse).sort(data)

    if args.raw:
        out = csv.DictWriter(
            sys.stdout,
            [
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
            ],
        )
        out.writeheader()
        out.writerows(data)
    else:
        print(tabulate.tabulate(data, headers="keys", tablefmt="github"))


if __name__ == "__main__":
    main()
