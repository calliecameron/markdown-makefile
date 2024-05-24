from panflute import Div, Header, Para, Str

from markdown.utils import test_utils


class TestRemoveCollectionSeparatorsBeforeHeaders(test_utils.PandocLuaFilterTestCase):
    def test_success(self) -> None:
        doc = self.run_filter(
            """::: collectionseparator
&nbsp;
:::

Foo

::: collectionseparator
&nbsp
:::

::: foo
# Foo
:::
""",
        )

        self.assertEqual(
            list(doc.content),
            [
                Para(Str("\u00a0")),
                Para(Str("Foo")),
                Div(Header(Str("Foo"), level=1), classes=["foo"]),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
