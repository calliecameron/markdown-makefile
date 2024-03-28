import sys
import unittest

import markdown.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = """
Test [foo]{.nospellcheck} [bar]{.foo} baz

::: {.nospellcheck}
foo
:::
"""


class TestSpellcheckCleanup(unittest.TestCase):
    def test_cleanup(self) -> None:
        j = markdown.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC)
        self.assertEqual(2, len(j["blocks"]))
        self.assertEqual("foo", j["blocks"][0]["c"][2]["c"])
        self.assertEqual("bar", j["blocks"][0]["c"][4]["c"][1][0]["c"])
        self.assertEqual("baz", j["blocks"][0]["c"][6]["c"])
        self.assertEqual("foo", j["blocks"][1]["c"][0]["c"])


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
