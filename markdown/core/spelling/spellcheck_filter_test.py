import sys
import unittest

import markdown.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = """Foo ![image](bar.jpg) bar

!include foobarbaz

Another [foobarbaz]{.nospellcheck} [line]{.foo}

::: {.nospellcheck}
foobarbaz
:::
"""


class TestSpellcheckFilter(unittest.TestCase):
    def test_cleanup(self) -> None:
        j = markdown.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC)
        self.assertEqual(len(j["blocks"]), 2)
        self.assertEqual("", j["blocks"][0]["c"][2]["c"][2][0])
        self.assertEqual("line", j["blocks"][1]["c"][3]["c"][1][0]["c"])


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
