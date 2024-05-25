import argparse

from markdown.utils.metadata import OutputMetadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")
    args = parser.parse_args()

    with open(args.in_file, encoding="utf-8") as f:
        OutputMetadata.model_validate_json(f.read())

    with open(args.out_file, mode="w", encoding="utf-8") as f:
        f.write("OK\n")


if __name__ == "__main__":
    main()
