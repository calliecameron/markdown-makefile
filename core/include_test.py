import json
import os
import os.path
import sys
import unittest
import utils.test_utils

PANDOC = ""
FILTER = ""

DOC1 = """# Foo

Hello.
"""

DOC2 = """# Start

!include %s

Bar.
"""

DOC2_INC = """---
increment-included-headers: t
---
# Start

!include %s

Bar.
"""


class TestInclude(unittest.TestCase):
    def test_include(self) -> None:
        test_tmpdir = utils.test_utils.tmpdir()

        doc1 = utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC1)
        self.assertEqual(
            doc1,
            {
                "blocks": [
                    {"c": [1, ["foo", [], []], [{"c": "Foo", "t": "Str"}]], "t": "Header"},
                    {"c": [{"c": "Hello.", "t": "Str"}], "t": "Para"},
                ],
                "meta": {},
                "pandoc-api-version": [1, 22, 2, 1],
            },
        )
        doc1_file = os.path.join(test_tmpdir, "doc1.json")
        with open(doc1_file, "w", encoding="utf-8") as f:
            json.dump(doc1, f)

        doc2 = utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC2 % doc1_file)
        self.assertEqual(
            doc2,
            {
                "blocks": [
                    {"c": [1, ["start", [], []], [{"c": "Start", "t": "Str"}]], "t": "Header"},
                    {"c": [1, ["foo", [], []], [{"c": "Foo", "t": "Str"}]], "t": "Header"},
                    {"c": [{"c": "Hello.", "t": "Str"}], "t": "Para"},
                    {"c": [{"c": "Bar.", "t": "Str"}], "t": "Para"},
                ],
                "meta": {},
                "pandoc-api-version": [1, 22, 2, 1],
            },
        )

        doc2_inc = utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC2_INC % doc1_file)
        self.assertEqual(
            doc2_inc,
            {
                "blocks": [
                    {"c": [1, ["start", [], []], [{"c": "Start", "t": "Str"}]], "t": "Header"},
                    {"c": [2, ["foo", [], []], [{"c": "Foo", "t": "Str"}]], "t": "Header"},
                    {"c": [{"c": "Hello.", "t": "Str"}], "t": "Para"},
                    {"c": [{"c": "Bar.", "t": "Str"}], "t": "Para"},
                ],
                "meta": {},
                "pandoc-api-version": [1, 22, 2, 1],
            },
        )

    def test_include_fails(self) -> None:
        test_tmpdir = utils.test_utils.tmpdir()
        bad_file = os.path.join(test_tmpdir, "bad.json")

        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC2 % bad_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
