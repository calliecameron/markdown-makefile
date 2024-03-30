from panflute import MetaString

from markdown.utils import test_utils


class TestStartsWithText(test_utils.PandocLuaFilterTestCase):
    def test_starts_with_text(self) -> None:
        doc = self.run_filter("Foo")
        self.assertEqual(doc.metadata["starts-with-text"], MetaString("t"))

        doc = self.run_filter("# Foo\n\nBar.")
        self.assertEqual(doc.metadata["starts-with-text"], MetaString(""))

        doc = self.run_filter(
            """::: foo
::: bar

:::
:::

::: foo
Foo
:::

# bar
""",
        )
        self.assertEqual(doc.metadata["starts-with-text"], MetaString("t"))

        doc = self.run_filter(
            """::: foo
::: bar

:::
:::

::: foo
# Foo
:::

bar
""",
        )
        self.assertEqual(doc.metadata["starts-with-text"], MetaString(""))


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
