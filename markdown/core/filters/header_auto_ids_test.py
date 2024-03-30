import sys
import unittest

import markdown.utils.test_utils

PANDOC = ""
FILTER = ""


class TestHeaderAutoIDs(unittest.TestCase):
    def test_success(self) -> None:
        j = markdown.utils.test_utils.pandoc_lua_filter(
            PANDOC,
            FILTER,
            """
# Foo {#foo}

### Bar

# Baz

## Quux {#__quux}

### Yay
""",
        )

        self.assertEqual(len(j["blocks"]), 5)
        self.assertEqual(
            j["blocks"][0]["c"],
            [1, ["foo", [], []], [{"t": "Str", "c": "Foo"}]],
        )
        self.assertEqual(
            j["blocks"][1]["c"],
            [3, ["__h3_1", [], []], [{"t": "Str", "c": "Bar"}]],
        )
        self.assertEqual(
            j["blocks"][2]["c"],
            [1, ["__h1_2", [], []], [{"t": "Str", "c": "Baz"}]],
        )
        self.assertEqual(
            j["blocks"][3]["c"],
            [2, ["__h2_1", [], []], [{"t": "Str", "c": "Quux"}]],
        )
        self.assertEqual(
            j["blocks"][4]["c"],
            [3, ["__h3_2", [], []], [{"t": "Str", "c": "Yay"}]],
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
