import argparse
import csv
import sys
import tabulate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("--filter")
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--wordcount", action="store_true")
    args = parser.parse_args()

    data = []
    with open(args.in_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not args.filter or args.filter in row["target"]:
                data.append(row)

    if args.wordcount:
        data.sort(key=lambda r: int(r["wordcount"]), reverse=True)

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
