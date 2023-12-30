import sys
import unittest

import markdown_makefile.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = """% The Title

# Foo bar

Baz quux test yay.
"""


class TestWordcount(unittest.TestCase):
    def test_wordcount(self) -> None:
        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC)
        self.assertEqual(j["meta"]["wordcount"]["c"], "6")


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
