from panflute import MetaInlines, MetaString, Space, Str

from markdown.utils import test_utils


class TestAddTitle(test_utils.PandocLuaFilterTestCase):
    def test_existing_title(self) -> None:
        doc = self.run_filter(
            """---
title: The Title
---
""",
        )
        self.assertEqual(
            doc.metadata["title"],
            MetaInlines(Str("The"), Space(), Str("Title")),
        )

    def test_no_title(self) -> None:
        doc = self.run_filter("")
        self.assertEqual(
            doc.metadata["title"],
            MetaString("[Untitled]"),
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
