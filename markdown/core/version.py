import argparse
import json
from collections.abc import Mapping

from markdown.utils.metadata import Version


def get_version(
    raw_version: Version,
    dep_versions: Mapping[str, Version],
    version_override: str,
    repo_override: str,
) -> Version:
    dirty_deps = []
    unversioned_deps = []

    for target, version in sorted(dep_versions.items()):
        if "dirty" in version.version:
            dirty_deps.append((target, version))
        if "unversioned" in version.version:
            unversioned_deps.append((target, version))

    version = Version(
        version=(
            version_override
            if version_override
            else (
                raw_version.version
                + (", dirty deps" if dirty_deps else "")
                + (", unversioned deps" if unversioned_deps else "")
            )
        ),
        repo=raw_version.repo,
    )

    # Dirty or unversioned deps in the same repo are OK
    bad_dirty_deps = [t for (t, v) in dirty_deps if v.repo != version.repo]
    bad_unversioned_deps = [t for (t, v) in unversioned_deps if v.repo != version.repo]

    if bad_dirty_deps or bad_unversioned_deps:
        msg = ["Target has dirty or unversioned deps"]
        if bad_dirty_deps:
            msg.append("Dirty deps:")
            msg += ["  " + dep for dep in bad_dirty_deps]
        if bad_unversioned_deps:
            msg.append("Unversioned deps:")
            msg += ["  " + dep for dep in bad_unversioned_deps]
        raise ValueError("\n".join(msg))

    if repo_override:
        version = Version(
            version=version.version,
            repo=repo_override,
        )

    return version


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_version_file")
    parser.add_argument("deps_metadata_file")
    parser.add_argument("metadata_out_file")
    parser.add_argument("--version_override", default="")
    parser.add_argument("--repo_override", default="")
    args = parser.parse_args()

    with open(args.raw_version_file, encoding="utf-8") as f:
        raw_version = Version.model_validate_json(f.read())

    dep_versions = {}
    with open(args.deps_metadata_file, encoding="utf-8") as f:
        for target, metadata in json.load(f).items():
            dep_versions[target] = Version(version=metadata["version"], repo=metadata["repo"])

    version = get_version(raw_version, dep_versions, args.version_override, args.repo_override)

    with open(args.metadata_out_file, mode="w", encoding="utf-8") as f:
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
