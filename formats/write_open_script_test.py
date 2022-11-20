import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestWriteOpenScript(unittest.TestCase):

    def test_write_open_script(self) -> None:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        out_file = os.path.join(test_tmpdir, 'out.sh')

        subprocess.run([
            SCRIPT,
            'foo',
            'bar',
            out_file,
        ], check=True)

        with open(out_file, encoding='utf-8') as f:
            self.assertEqual(f.read(), """#!/bin/bash

FILE_TO_OPEN="${0}.runfiles/foo/bar"

xdg-open "${FILE_TO_OPEN}"
""")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
