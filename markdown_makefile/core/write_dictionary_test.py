import os
import os.path
import subprocess
import sys
import unittest

import markdown_makefile.utils.test_utils

SCRIPT = ""


class TestWriteDictionary(unittest.TestCase):
    def test_write_dictionary(self) -> None:
        test_tmpdir = markdown_makefile.utils.test_utils.tmpdir()

        in_file_1 = os.path.join(test_tmpdir, "in1.dic")
        with open(in_file_1, "w", encoding="utf-8") as f:
            f.write("foo\nbar\n")

        in_file_2 = os.path.join(test_tmpdir, "in2.dic")
        with open(in_file_2, "w", encoding="utf-8") as f:
            f.write("foo\nbaz\n")

        out_file = os.path.join(test_tmpdir, "out.dic")

        subprocess.run(
            [
                SCRIPT,
                out_file,
                in_file_1,
                in_file_2,
            ],
            check=True,
        )

        with open(out_file, encoding="utf-8") as f:
            self.assertEqual(f.read(), "bar\nbaz\nfoo\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
