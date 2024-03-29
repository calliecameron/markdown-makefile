import os
import os.path
import subprocess
import sys
import unittest
from collections.abc import Sequence

import markdown.utils.test_utils

SCRIPT = ""

DOC = """The Title

Test text baz Quux shouldn’t fail
"""  # noqa: RUF001


class TestWriteDictionary(unittest.TestCase):
    def run_spellcheck(self, doc: str, dictionary: Sequence[str]) -> str:
        test_tmpdir = markdown.utils.test_utils.tmpdir()

        in_file = os.path.join(test_tmpdir, "in.md")
        with open(in_file, "w", encoding="utf-8") as f:
            f.write(doc)

        dict_file = os.path.join(test_tmpdir, "in.dic")
        with open(dict_file, "w", encoding="utf-8") as f:
            f.write("\n".join(dictionary) + "\n")

        out_file = os.path.join(test_tmpdir, "out.txt")

        subprocess.run(
            [
                SCRIPT,
                dict_file,
                in_file,
                out_file,
                "en_GB",
            ],
            stderr=subprocess.PIPE,
            check=True,
        )

        with open(out_file, encoding="utf-8") as f:
            return f.read()

    def test_spellcheck(self) -> None:
        self.assertEqual(self.run_spellcheck(DOC, ["baz", "Quux"]), "OK\n")

    def test_spellcheck_fails(self) -> None:
        try:
            self.run_spellcheck(DOC, [])
            self.fail()
        except subprocess.CalledProcessError as e:
            self.assertEqual(
                e.stderr.decode("utf-8"),
                """ERROR: found misspelled words; correct them or add them to the dictionary:

baz
Quux

""",
            )


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
