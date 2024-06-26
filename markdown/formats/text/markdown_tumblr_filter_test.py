from panflute import Para, Space, Str

from markdown.utils import test_utils


class TestMarkdownTumblrFilter(test_utils.PandocLuaFilterTestCase):
    def test_markdown_tumblr_filter(self) -> None:
        doc = self.run_filter(
            """\\<Foo\\>

* * *

Bar
""",
        )
        self.assertEqual(
            list(doc.content),
            [
                Para(Str("&lt;Foo&gt;")),
                Para(Str("&#x002a;"), Space(), Str("&#x002a;"), Space(), Str("&#x002a;")),
                Para(Str("Bar")),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
