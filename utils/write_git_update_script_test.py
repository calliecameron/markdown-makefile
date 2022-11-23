import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestWriteGitUpdateScript(unittest.TestCase):

    def run_script(self, package: str) -> str:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        out_file = os.path.join(test_tmpdir, 'out.sh')

        subprocess.run([
            SCRIPT,
            out_file,
            package,
        ], check=True)

        with open(out_file, encoding='utf-8') as f:
            return f.read()

    def test_write_git_update_script(self) -> None:
        self.assertEqual(self.run_script('foo'), """#!/bin/bash

set -eu

DATA_DIR="${PWD}/foo/"
SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}/foo/"
GIT_DIR="${SOURCE_DIR}.git"
BIN_DIR="${SOURCE_DIR}.bin"

if [ ! -d "${GIT_DIR}" ]; then
    echo "ERROR: package 'foo' is not the root of a git repo" >&2
    exit 1
fi

cd "${DATA_DIR}"
mkdir -p "${BIN_DIR}"
cp -t "${BIN_DIR}" docdump pdfdump zipdump
cd "${BIN_DIR}"
chmod u=rwx *

cd "${DATA_DIR}"
cp default_gitattributes "${SOURCE_DIR}.gitattributes"
cp default_gitconfig "${SOURCE_DIR}.gitconfig"
cp default_gitignore "${SOURCE_DIR}.gitignore"
cd "${SOURCE_DIR}"
chmod u=rw .gitattributes .gitconfig .gitignore
git config --local include.path ../.gitconfig
""")

    def test_write_git_update_script_root_package(self) -> None:
        self.assertEqual(self.run_script(''), """#!/bin/bash

set -eu

DATA_DIR="${PWD}/"
SOURCE_DIR="${BUILD_WORKSPACE_DIRECTORY}/"
GIT_DIR="${SOURCE_DIR}.git"
BIN_DIR="${SOURCE_DIR}.bin"

if [ ! -d "${GIT_DIR}" ]; then
    echo "ERROR: package '' is not the root of a git repo" >&2
    exit 1
fi

cd "${DATA_DIR}"
mkdir -p "${BIN_DIR}"
cp -t "${BIN_DIR}" docdump pdfdump zipdump
cd "${BIN_DIR}"
chmod u=rwx *

cd "${DATA_DIR}"
cp default_gitattributes "${SOURCE_DIR}.gitattributes"
cp default_gitconfig "${SOURCE_DIR}.gitconfig"
cp default_gitignore "${SOURCE_DIR}.gitignore"
cd "${SOURCE_DIR}"
chmod u=rw .gitattributes .gitconfig .gitignore
git config --local include.path ../.gitconfig
""")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
