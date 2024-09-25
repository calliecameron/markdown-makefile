import argparse
import json

from markdown.private.utils.metadata import Version

REPO_KEY = "STABLE_WORKSPACE_PARENT_REPO"
VERSION_KEY = "STABLE_WORKSPACE_PARENT_VERSION"


def from_version_file(file: str) -> Version:
    with open(file, encoding="utf-8") as f:
        return Version.model_validate_json(f.read())


def from_info_file(file: str) -> Version:
    version = ""
    repo = ""

    with open(file, encoding="utf-8") as f:
        for line in f:
            if line.startswith(REPO_KEY):
                repo = line[len(REPO_KEY) :].strip()
            elif line.startswith(VERSION_KEY):
                version = line[len(VERSION_KEY) :].strip()

    if not version or not repo:
        return Version(
            version="unversioned",
            repo="unversioned",
        )

    return Version(
        version=version,
        repo=repo,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--version_file")
    group.add_argument("--info_file")
    parser.add_argument("outfile")
    args = parser.parse_args()

    if args.version_file:
        version = from_version_file(args.version_file)
    elif args.info_file:
        version = from_info_file(args.info_file)
    else:
        raise ValueError("Neither version file specified")

    with open(args.outfile, mode="w", encoding="utf-8") as f:
        json.dump(
            version.model_dump(
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
