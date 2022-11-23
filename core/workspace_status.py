#!/usr/bin/env python3
"""Capture non-hermetic workspace info."""

from typing import Iterator, List, NamedTuple, Optional, Tuple
import contextlib
import datetime
import os
import os.path
import re
import subprocess
import bazel_package


EXPECTED_PANDOC_VERSION = '2.19.2'


@contextlib.contextmanager
def chdir(path: str) -> Iterator[None]:
    if not path:
        path = '.'
    original_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_dir)


class GitCommit(NamedTuple):
    repo_path: str
    commit: str
    dirty: bool
    timestamp: int

    def __str__(self) -> str:
        timestamp = datetime.datetime.fromtimestamp(
            self.timestamp, tz=datetime.timezone.utc)
        return f'{self.commit}{"-dirty" if self.dirty else ""}, {timestamp}'


def get_git_commit(path: str) -> Optional[GitCommit]:
    with chdir(path):
        try:
            repo_path = os.path.abspath(subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True, encoding='utf-8', check=True).stdout.strip())
        except subprocess.CalledProcessError:
            # Not a git repo
            return None

        try:
            commit = subprocess.run(
                ['git', 'describe', '--no-match', '--always', '--long'],
                capture_output=True, encoding='utf-8', check=True).stdout.strip()
        except subprocess.CalledProcessError:
            # New repo with no commits yet
            return None

        try:
            timestamp = int(subprocess.run(
                ['git', 'show', '--no-patch', '--no-notes', '--pretty=%ct', commit],
                capture_output=True, encoding='utf-8', check=True).stdout.strip())

            status = subprocess.run(
                ['git', 'status', '--porcelain', '-b'],
                capture_output=True, encoding='utf-8', check=True).stdout.strip()
            dirty = False
            for line in status.split('\n'):
                if re.fullmatch(r'##.*\[ahead.*\]', line) is not None or not line.startswith('##'):
                    dirty = True
                    break

        except subprocess.CalledProcessError:
            return None

    return GitCommit(repo_path, commit, dirty, timestamp)


def find_packages(root: str) -> List[str]:
    packages = []
    for dirpath, _, filenames in os.walk(root):
        if 'BUILD' in filenames:
            package = os.path.relpath(dirpath, root)
            if package == '.':
                package = ''
            packages.append(package)
    return sorted(packages)


def get_package_data(root: str) -> List[Tuple[str, str]]:
    out = []
    for path in find_packages(root):
        commit = get_git_commit(path)
        if commit:
            version = str(commit)
            repo = commit.repo_path
        else:
            version = 'unversioned'
            repo = 'unversioned'
        key = bazel_package.package_key(path)
        out.append((bazel_package.version_key(key), version))
        out.append((bazel_package.repo_key(key), repo))
    return out


def get_pandoc_version() -> Tuple[str, str]:
    try:
        output = subprocess.run(
            ['pandoc', '--version'],
            capture_output=True, encoding='utf-8', check=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        raise ValueError('Failed to get pandoc version') from e

    prefix = 'pandoc '
    for line in output.split('\n'):
        if line.startswith(prefix):
            version = line[len(prefix):]
            if version != EXPECTED_PANDOC_VERSION:
                raise ValueError(
                    f'Got pandoc version {version}; expected {EXPECTED_PANDOC_VERSION}')
            return bazel_package.PANDOC_VERSION_KEY, version

    raise ValueError('Failed to get pandoc version')


def main() -> None:
    data = [get_pandoc_version()] + get_package_data(os.getcwd())
    print('\n'.join([f'{key} {value}' for key, value in data]))


if __name__ == '__main__':
    main()
