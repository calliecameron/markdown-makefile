from panflute import MetaString

from markdown.utils import test_utils

DOC = """% The Title

# Foo bar

Baz quux test yay.
"""


class TestWordcount(test_utils.PandocLuaFilterTestCase):
    def test_wordcount(self) -> None:
        doc = self.run_filter(DOC)
        self.assertEqual(doc.metadata["wordcount"], MetaString("6"))


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
