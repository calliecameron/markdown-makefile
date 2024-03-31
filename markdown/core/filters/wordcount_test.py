from panflute import MetaString

from markdown.utils import test_utils

DOC = """---
title: The Title
---

# Foo bar

Baz quux test yay.

&nbsp;

Test-text -- test text--- ' " test's , text “ ” ‘ ’ – — … .
"""  # noqa: RUF001


class TestWordcount(test_utils.PandocLuaFilterTestCase):
    def test_wordcount(self) -> None:
        doc = self.run_filter(DOC)
        self.assertEqual(doc.metadata["wordcount"], MetaString("11"))


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
