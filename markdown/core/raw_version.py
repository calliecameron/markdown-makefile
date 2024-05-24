import argparse
import json

import markdown.utils.bazel_package
from markdown.utils.metadata import Version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("package")
    args = parser.parse_args()

    key = markdown.utils.bazel_package.package_key(args.package)
    version_key = markdown.utils.bazel_package.version_key(key) + " "
    repo_key = markdown.utils.bazel_package.repo_key(key) + " "

    version = ""
    repo = ""

    with open(args.infile, encoding="utf-8") as f:
        for line in f:
            if line.startswith(version_key):
                version = line[len(version_key) :].strip()
            elif line.startswith(repo_key):
                repo = line[len(repo_key) :].strip()

    if not version:
        raise ValueError("Package version not found")
    if not repo:
        raise ValueError("Package repo not found")

    with open(args.outfile, mode="w", encoding="utf-8") as f:
        json.dump(
            Version(
                docversion=version,
                repo=repo,
            ).model_dump(mode="json"),
            f,
            sort_keys=True,
            indent=4,
        )


if __name__ == "__main__":
    main()
