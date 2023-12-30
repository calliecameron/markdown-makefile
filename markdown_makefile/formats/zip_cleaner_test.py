import os
import os.path
import subprocess
import sys
import unittest

import markdown_makefile.utils.test_utils

SCRIPT = ""


class TestZipCleaner(unittest.TestCase):
    def test_zip_cleaner(self) -> None:
        test_tmpdir = markdown_makefile.utils.test_utils.tmpdir()

        txt_file = os.path.join(test_tmpdir, "in.txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("foo\n")

        in_file = os.path.join(test_tmpdir, "in.zip")

        subprocess.run(
            [
                "zip",
                in_file,
                txt_file,
            ],
            check=True,
        )

        output = subprocess.run(
            [
                "zipinfo",
                "-T",
                in_file,
            ],
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertNotIn("19800101", output.stdout)

        out_file = os.path.join(test_tmpdir, "out.zip")

        subprocess.run(
            [
                SCRIPT,
                in_file,
                out_file,
            ],
            check=True,
        )

        output = subprocess.run(
            [
                "zipinfo",
                "-T",
                out_file,
            ],
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertIn("19800101", output.stdout)


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
