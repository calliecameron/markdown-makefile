import sys
import unittest
import markdown_makefile.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = "Foo ![image](bar.jpg) bar"


class TestSpellcheckFilter(unittest.TestCase):
    def test_cleanup(self) -> None:
        j = markdown_makefile.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC)
        self.assertEqual("", j["blocks"][0]["c"][2]["c"][2][0])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
