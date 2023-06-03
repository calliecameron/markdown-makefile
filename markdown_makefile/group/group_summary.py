from typing import Any, Dict, List
import argparse
import csv
import json
import sys
from abc import ABC
import tabulate
from dateparser.date import DateDataParser
from dateparser.search import search_dates
from markdown_makefile.utils.publications import Publications


class Sorter(ABC):
    def __init__(self, reverse: bool, key: str) -> None:
        super().__init__()
        self._reverse = reverse
        self._key = key

    def sort(self, data: List[Dict[str, Any]]) -> None:
        data.sort(key=lambda elem: elem[self._key], reverse=self._reverse)  # type: ignore


class Target(Sorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(reverse, "target")


class Date(Sorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, "date")


class Wordcount(Sorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, "wordcount")


class PoetryLines(Sorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, "poetry lines")


class Finished(Sorter):
    def __init__(self, reverse: bool) -> None:
        super().__init__(not reverse, "finished")


def parse_date(date: str, reverse: bool) -> str:
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

    return ", ".join(sorted(out, reverse=not reverse))


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
        const=Target,
        dest="sorter",
        default=Target,
        help="sort by target",
    )
    sorters.add_argument(
        "--date", action="store_const", const=Date, dest="sorter", help="sort by date"
    )
    sorters.add_argument(
        "--wordcount",
        action="store_const",
        const=Wordcount,
        dest="sorter",
        help="sort by wordcount",
    )
    sorters.add_argument(
        "--poetry_lines",
        action="store_const",
        const=PoetryLines,
        dest="sorter",
        help="sort by poetry lines",
    )
    sorters.add_argument(
        "--finished", action="store_const", const=Finished, dest="sorter", help="sort by finished"
    )
    args = parser.parse_args()

    data = []  # type: List[Dict[str, Any]]
    with open(args.in_file, encoding="utf-8") as f:
        for target, j in json.load(f).items():
            if not args.filter or args.filter in target:
                publication = ""
                if "publications" in j and j["publications"]:
                    ps = Publications.from_json(j["publications"])
                    if ps.active:
                        publication = ps.highest_active_state
                    else:
                        publication = "attempted"

                data.append(
                    {
                        "target": target,
                        "title": sanitise(j["title"]) if "title" in j else "",
                        "raw date": sanitise(j["date"]) if "date" in j else "",
                        "date": sanitise(parse_date(j["date"], args.reverse))
                        if "date" in j
                        else "",
                        "wordcount": int(j["wordcount"]),
                        "poetry lines": int(j["poetry-lines"]),
                        "finished": "yes" if "finished" in j and j["finished"] else "no",
                        "publication": publication,
                        "version": j["docversion"],
                        "status": "DIRTY" if "dirty" in j["docversion"] else "ok",
                    }
                )

    args.sorter(args.reverse).sort(data)

    if args.raw:
        out = csv.DictWriter(
            sys.stdout,
            [
                "target",
                "title",
                "raw date",
                "date",
                "wordcount",
                "poetry lines",
                "finished",
                "publication",
                "version",
                "status",
            ],
        )
        out.writeheader()
        out.writerows(data)
    else:
        print(tabulate.tabulate(data, headers="keys", tablefmt="github"))


if __name__ == "__main__":
    main()
