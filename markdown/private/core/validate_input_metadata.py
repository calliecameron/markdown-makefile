import argparse
import json

from markdown.private.utils.metadata import InputMetadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")
    args = parser.parse_args()

    with open(args.in_file, encoding="utf-8") as f:
        metadata = InputMetadata.model_validate_json(f.read())

    with open(args.out_file, mode="w", encoding="utf-8") as f:
        json.dump(
            metadata.model_dump(
                mode="json",
                by_alias=True,
                exclude_unset=True,
                exclude_defaults=True,
            ),
            f,
            sort_keys=True,
            indent=4,
        )


if __name__ == "__main__":
    main()
