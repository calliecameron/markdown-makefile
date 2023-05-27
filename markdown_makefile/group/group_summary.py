from typing import Dict, List  # noqa: F401
import argparse
import csv
import json
import sys
import tabulate
from dateparser.date import DateDataParser
from dateparser.search import search_dates
from markdown_makefile.utils.publications import Publications


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
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("--filter")
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--wordcount", action="store_true")
    args = parser.parse_args()

    data = []  # type: List[Dict[str, str]]
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
                        "raw_date": sanitise(j["date"]) if "date" in j else "",
                        "date": sanitise(parse_date(j["date"])) if "date" in j else "",
                        "wordcount": j["wordcount"],
                        "publication": publication,
                        "version": j["docversion"],
                        "status": "DIRTY" if "dirty" in j["docversion"] else "ok",
                    }
                )

    if args.wordcount:
        data.sort(key=lambda r: int(r["wordcount"]), reverse=True)
    else:
        data.sort(key=lambda r: r["target"])

    if args.raw:
        out = csv.DictWriter(
            sys.stdout,
            [
                "target",
                "title",
                "raw_date",
                "date",
                "wordcount",
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
