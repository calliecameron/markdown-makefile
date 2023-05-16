import sys
import unittest
import markdown_makefile.utils.test_utils

PANDOC = ""
FILTER = ""


class TestAddTitle(unittest.TestCase):
    def test_existing_title(self) -> None:
        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, "% The Title")
        self.assertEqual(
            j["meta"]["title"],
            {
                "t": "MetaInlines",
                "c": [{"t": "Str", "c": "The"}, {"t": "Space"}, {"t": "Str", "c": "Title"}],
            },
        )

    def test_no_title(self) -> None:
        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, "")
        self.assertEqual(
            j["meta"]["title"],
            {
                "t": "MetaString",
                "c": "[Untitled]",
            },
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
