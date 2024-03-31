from panflute import Para, Str

from markdown.utils import test_utils


class TestRemoveCollectionSeparators(test_utils.PandocLuaFilterTestCase):
    def test_success(self) -> None:
        doc = self.run_filter(
            """
Foo

::: collectionseparator
&nbsp;
:::

Bar
""",
        )

        self.assertEqual(
            list(doc.content),
            [
                Para(Str("Foo")),
                Para(Str("Bar")),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
