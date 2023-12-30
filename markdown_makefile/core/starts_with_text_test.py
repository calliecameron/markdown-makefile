import sys
import unittest

import markdown_makefile.utils.test_utils

PANDOC = ""
FILTER = ""


class TestStartsWithText(unittest.TestCase):
    def test_starts_with_text(self) -> None:
        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, "Foo")
        self.assertEqual(j["meta"]["starts-with-text"]["c"], "t")

        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, "# Foo\n\nBar.")
        self.assertEqual(j["meta"]["starts-with-text"]["c"], "")


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
