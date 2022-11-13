#!/usr/bin/env python3

import argparse
import json
import bazel_package


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument('package')
    args = parser.parse_args()

    pandoc_version_key = bazel_package.PANDOC_VERSION_KEY + ' '
    key = bazel_package.package_key(args.package)
    version_key = bazel_package.version_key(key) + ' '
    repo_key = bazel_package.repo_key(key) + ' '

    pandoc_version = ''
    version = ''
    repo = ''

    with open(args.infile, encoding='utf-8') as f:
        for line in f:
            if line.startswith(pandoc_version_key):
                pandoc_version = line[len(pandoc_version_key):].strip()
            elif line.startswith(version_key):
                version = line[len(version_key):].strip()
            elif line.startswith(repo_key):
                repo = line[len(repo_key):].strip()

    if not pandoc_version:
        raise ValueError('Pandoc version not found')
    if not version:
        raise ValueError('Package version not found')
    if not repo:
        raise ValueError('Package repo not found')

    with open(args.outfile, mode='w', encoding='utf-8') as f:
        json.dump({
            'pandoc_version': pandoc_version,
            'version': version,
            'repo': repo,
        }, f, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
