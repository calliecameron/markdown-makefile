from typing import Dict
import argparse
import hashlib
import json


class Version:
    def __init__(self, version: str, repo: str) -> None:
        super().__init__()
        self.version = version
        self.repo = repo

    def to_dict(self) -> Dict[str, str]:
        return {
            "docversion": self.version,
            "repo": self.repo,
        }

    @staticmethod
    def from_dict(d: Dict[str, str]) -> "Version":
        return Version(d["docversion"], d["repo"])


def get_version(
    raw_version: Version, dep_versions: Dict[str, Version], version_override: str
) -> Version:
    dirty_deps = []
    unversioned_deps = []

    for target, version in sorted(dep_versions.items()):
        if "dirty" in version.version:
            dirty_deps.append((target, version))
        if "unversioned" in version.version:
            unversioned_deps.append((target, version))

    version = Version(
        version_override
        if version_override
        else (
            raw_version.version
            + (", dirty deps" if dirty_deps else "")
            + (", unversioned deps" if unversioned_deps else "")
        ),
        raw_version.repo,
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

    return version


def get_metadata(version: str, repo: str, increment_included_headers: bool) -> Dict[str, str]:
    out = {
        "docversion": version,
        "subject": f"Version: {version}",
        "lang": "en-GB",
        "repo": repo,
        "source-md5": hashlib.md5(version.encode("utf-8")).hexdigest(),
    }
    if increment_included_headers:
        out["increment-included-headers"] = "t"
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_version_file")
    parser.add_argument("deps_metadata_file")
    parser.add_argument("metadata_out_file")
    parser.add_argument("--increment_included_headers", action="store_true")
    parser.add_argument("--version_override", default="")
    args = parser.parse_args()

    with open(args.raw_version_file, encoding="utf-8") as f:
        raw_version = Version.from_dict(json.load(f))

    dep_versions = {}
    with open(args.deps_metadata_file, encoding="utf-8") as f:
        for target, metadata in json.load(f).items():
            dep_versions[target] = Version.from_dict(metadata)

    version = get_version(raw_version, dep_versions, args.version_override)
    metadata = get_metadata(version.version, version.repo, args.increment_included_headers)

    with open(args.metadata_out_file, mode="w", encoding="utf-8") as f:
        json.dump(metadata, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
