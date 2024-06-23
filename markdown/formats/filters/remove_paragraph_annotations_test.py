from panflute import Div, Para, Str

from markdown.utils import test_utils


class TestRemoveParagraphAnnotations(test_utils.PandocLuaFilterTestCase):
    def test_success(self) -> None:
        doc = self.run_filter(
            """
::: firstparagraph
Foo
:::

::: foo
::: otherparagraph
Bar
:::
:::

::: blankline
Baz
:::

Quux
""",
        )

        self.assertEqual(
            list(doc.content),
            [
                Para(Str("Foo")),
                Div(Para(Str("Bar")), classes=["foo"]),
                Para(Str("Baz")),
                Para(Str("Quux")),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
