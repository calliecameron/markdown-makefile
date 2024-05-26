import argparse
import hashlib
import json

from markdown.utils.metadata import MetadataMap, SourceHash


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src_file")
    parser.add_argument("deps_metadata_file")
    parser.add_argument("metadata_out_file")
    args = parser.parse_args()

    dep_hashes = {}
    with open(args.deps_metadata_file, encoding="utf-8") as f:
        for target, metadata in MetadataMap.model_validate_json(f.read()).items():
            dep_hashes[target] = metadata.source_hash

    with open(args.src_file, encoding="utf-8") as f:
        src = f.read()

    hash_input = json.dumps(dep_hashes, sort_keys=True, indent=4) + src
    hash_output = hashlib.md5(hash_input.encode("utf-8")).hexdigest()

    with open(args.metadata_out_file, "w", encoding="utf-8") as f:
        json.dump(
            SourceHash.model_validate({"source-hash": hash_output}).model_dump(
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
