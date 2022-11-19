from typing import Dict
import argparse
import json
import yaml


class Version:
    def __init__(self, version: str, repo: str) -> None:
        super().__init__()
        self.version = version
        self.repo = repo

    def to_dict(self) -> Dict[str, str]:
        return {
            'version': self.version,
            'repo': self.repo,
        }

    @staticmethod
    def from_dict(d: Dict[str, str]) -> 'Version':
        return Version(d['version'], d['repo'])


def get_version(
        raw_version: Version, dep_versions: Dict[str, Version], version_override: str) -> Version:
    dirty_deps = []
    unversioned_deps = []

    for target, version in sorted(dep_versions.items()):
        if 'dirty' in version.version:
            dirty_deps.append((target, version))
        if 'unversioned' in version.version:
            unversioned_deps.append((target, version))

    version = Version(version_override if version_override else
                      (raw_version.version + (', dirty deps' if dirty_deps else '') +
                       (', unversioned deps' if unversioned_deps else '')), raw_version.repo)

    # Dirty or unversioned deps in the same repo are OK
    dirty_deps = [t for (t, v) in dirty_deps if v.repo != version.repo]
    unversioned_deps = [t for (t, v) in unversioned_deps if v.repo != version.repo]

    if dirty_deps or unversioned_deps:
        msg = ['Target has dirty or unversioned deps']
        if dirty_deps:
            msg.append('Dirty deps:')
            msg += ['  ' + dep for dep in dirty_deps]
        if unversioned_deps:
            msg.append('Unversioned deps:')
            msg += ['  ' + dep for dep in unversioned_deps]
        raise ValueError('\n'.join(msg))

    return version


def get_metadata(version: str, increment_included_headers: bool) -> Dict[str, str]:
    out = {
        'docversion': version,
        'subject': f'Version: {version}',
        'lang': 'en-GB',
    }
    if increment_included_headers:
        out['increment-included-headers'] = 't'
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('raw_version_file')
    parser.add_argument('version_out_file')
    parser.add_argument('dep_versions_out_file')
    parser.add_argument('metadata_out_file')
    parser.add_argument('--dep_version_file', action='append', nargs=2, default=[])
    parser.add_argument('--increment_included_headers', action='store_true')
    parser.add_argument('--version_override', default='')
    args = parser.parse_args()

    with open(args.raw_version_file, encoding='utf-8') as f:
        raw_version = Version.from_dict(json.load(f))

    dep_versions = {}
    for target, dep_version_file in args.dep_version_file:
        with open(dep_version_file, encoding='utf-8') as f:
            dep_versions[target] = Version.from_dict(json.load(f))

    version = get_version(raw_version, dep_versions, args.version_override)
    metadata = get_metadata(version.version, args.increment_included_headers)

    with open(args.version_out_file, mode='w', encoding='utf-8') as f:
        json.dump(version.to_dict(), f, sort_keys=True, indent=4)

    with open(args.dep_versions_out_file, mode='w', encoding='utf-8') as f:
        json.dump({t: v.to_dict() for t, v in dep_versions.items()}, f, sort_keys=True, indent=4)

    with open(args.metadata_out_file, mode='w', encoding='utf-8') as f:
        yaml.dump(metadata, f)


if __name__ == '__main__':
    main()
