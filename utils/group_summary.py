import argparse
import csv
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file")
    parser.add_argument("--dep", action="append", nargs=2, default=[])
    args = parser.parse_args()

    with open(args.out_file, "w", newline="", encoding="utf-8") as outfile:
        out = csv.DictWriter(outfile, ["target", "title", "wordcount", "version", "status"])
        out.writeheader()

        for target, metadata in args.dep:
            with open(metadata, encoding="utf-8") as f:
                j = json.load(f)
            out.writerow(
                {
                    "target": target,
                    "title": j["title"] if "title" in j else "",
                    "wordcount": j["wordcount"],
                    "version": j["docversion"],
                    "status": "DIRTY" if "dirty" in j["docversion"] else "ok",
                }
            )


if __name__ == "__main__":
    main()
