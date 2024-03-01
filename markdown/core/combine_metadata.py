import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file")
    parser.add_argument("--metadata_file", action="append", nargs=2, default=[])
    args = parser.parse_args()

    out = {}
    for target, metadata_file in args.metadata_file:
        with open(metadata_file, encoding="utf-8") as f:
            out[target] = json.load(f)

    with open(args.out_file, mode="w", encoding="utf-8") as f:
        json.dump(out, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
