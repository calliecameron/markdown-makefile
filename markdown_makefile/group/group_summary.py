from typing import Dict, List  # noqa: F401
import argparse
import csv
import json
import sys
import tabulate


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
                data.append(
                    {
                        "target": target,
                        "title": j["title"].replace("\n", "\\n") if "title" in j else "",
                        "date": j["date"].replace("\n", "\\n") if "date" in j else "",
                        "wordcount": j["wordcount"],
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
            sys.stdout, ["target", "title", "date", "wordcount", "version", "status"]
        )
        out.writeheader()
        out.writerows(data)
    else:
        print(tabulate.tabulate(data, headers="keys", tablefmt="github"))


if __name__ == "__main__":
    main()
