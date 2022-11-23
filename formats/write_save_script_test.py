import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestWriteSaveScript(unittest.TestCase):

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

    def test_write_save_script(self) -> None:
        self.assertEqual(self.run_script('foo'), """#!/bin/bash

set -eu

OUTPUT_DIR="foo/output"
SAVE_DIR="${BUILD_WORKSPACE_DIRECTORY}/foo/saved"

mkdir -p "${SAVE_DIR}"
cd "${OUTPUT_DIR}"
cp -t "${SAVE_DIR}" *
cd "${SAVE_DIR}"
chmod u=rw *
""")

    def test_write_save_script_root_package(self) -> None:
        self.assertEqual(self.run_script(''), """#!/bin/bash

set -eu

OUTPUT_DIR="output"
SAVE_DIR="${BUILD_WORKSPACE_DIRECTORY}/saved"

mkdir -p "${SAVE_DIR}"
cd "${OUTPUT_DIR}"
cp -t "${SAVE_DIR}" *
cd "${SAVE_DIR}"
chmod u=rw *
""")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
