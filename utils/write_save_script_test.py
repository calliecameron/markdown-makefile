import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestWriteSaveScript(unittest.TestCase):

    def test_write_save_script(self) -> None:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        out_file = os.path.join(test_tmpdir, 'out.sh')

        subprocess.run([
            SCRIPT,
            'foo',
            out_file,
        ], check=True)

        with open(out_file, encoding='utf-8') as f:
            self.assertEqual(f.read(), """#!/bin/bash

set -eu

OUTPUT_DIR="foo/output"
SAVE_DIR="${BUILD_WORKSPACE_DIRECTORY}/foo/saved"

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
