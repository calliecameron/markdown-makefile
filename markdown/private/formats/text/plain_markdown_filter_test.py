from panflute import Header, Str

from markdown.private.utils import test_utils


class TestPlainMarkdownFilter(test_utils.PandocLuaFilterTestCase):
    def test_plain_markdown_filter(self) -> None:
        doc = self.run_filter(
            "# Foo {#h}",
        )
        self.assertEqual(
            list(doc.content),
            [Header(Str("Foo"), level=1)],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
