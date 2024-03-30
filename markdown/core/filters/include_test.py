import json
import os
import os.path

from markdown.utils import test_utils

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


class TestInclude(test_utils.PandocLuaFilterTestCase):
    def test_include(self) -> None:
        doc1 = self.run_filter(DOC1)
        self.assertEqual(
            doc1,
            {
                "blocks": [
                    {"c": [1, ["", [], []], [{"c": "Foo", "t": "Str"}]], "t": "Header"},
                    {"c": [{"c": "Hello.", "t": "Str"}], "t": "Para"},
                ],
                "meta": {},
                "pandoc-api-version": [1, 23],
            },
        )
        doc1_file = os.path.join(self.tmpdir(), "doc1.json")
        with open(doc1_file, "w", encoding="utf-8") as f:
            json.dump(doc1, f)

        doc2 = self.run_filter(
            DOC2 % doc1_file,
        )
        self.assertEqual(
            doc2,
            {
                "blocks": [
                    {"c": [1, ["", [], []], [{"c": "Start", "t": "Str"}]], "t": "Header"},
                    {"c": [1, ["", [], []], [{"c": "Foo", "t": "Str"}]], "t": "Header"},
                    {"c": [{"c": "Hello.", "t": "Str"}], "t": "Para"},
                    {"c": [{"c": "Bar.", "t": "Str"}], "t": "Para"},
                ],
                "meta": {},
                "pandoc-api-version": [1, 23],
            },
        )

        doc2_inc = self.run_filter(
            DOC2_INC % doc1_file,
        )
        self.assertEqual(
            doc2_inc,
            {
                "blocks": [
                    {"c": [1, ["", [], []], [{"c": "Start", "t": "Str"}]], "t": "Header"},
                    {"c": [2, ["", [], []], [{"c": "Foo", "t": "Str"}]], "t": "Header"},
                    {"c": [{"c": "Hello.", "t": "Str"}], "t": "Para"},
                    {"c": [{"c": "Bar.", "t": "Str"}], "t": "Para"},
                ],
                "meta": {},
                "pandoc-api-version": [1, 23],
            },
        )

    def test_include_fails(self) -> None:
        bad_file = os.path.join(self.tmpdir(), "bad.json")

        with self.assertRaises(ValueError):
            self.run_filter(DOC2 % bad_file)


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
