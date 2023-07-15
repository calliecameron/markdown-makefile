import sys
import unittest

import markdown_makefile.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = """% The Title

| Foo
| Bar

# Foo bar

> | Blah

Baz quux test yay.

> Foo
> Bar

> | Baz
> | Quux

"""


class TestPoetryLines(unittest.TestCase):
    def test_linecount(self) -> None:
        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC)
        self.assertEqual(j["meta"]["poetry-lines"]["c"], "3")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
