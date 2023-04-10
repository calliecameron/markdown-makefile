import os
import os.path
import subprocess
import sys
import unittest
import utils.test_utils


SCRIPT = ""


class TestWriteGroupSummaryScript(unittest.TestCase):
    def test_write_group_summary_script(self) -> None:
        test_tmpdir = utils.test_utils.tmpdir()

        out_file = os.path.join(test_tmpdir, "out.sh")

        subprocess.run(
            [
                SCRIPT,
                "foo",
                "bar",
                out_file,
            ],
            check=True,
        )

        with open(out_file, encoding="utf-8") as f:
            self.assertEqual(
                f.read(),
                """#!/bin/bash

set -eu

if [ "${1:-}" = '--raw' ]; then
    OUTPUT_TOOL=('cat')
else
    OUTPUT_TOOL=('csvlook' '-I')
fi

FILE_TO_OPEN="${0}.runfiles/foo/bar"

"${OUTPUT_TOOL[@]}" "${FILE_TO_OPEN}"
""",
            )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
