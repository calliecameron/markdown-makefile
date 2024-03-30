from markdown.utils import test_utils


class TestStartsWithText(test_utils.PandocLuaFilterTestCase):
    def test_starts_with_text(self) -> None:
        j = self.run_filter("Foo")
        self.assertEqual(j["meta"]["starts-with-text"]["c"], "t")

        j = self.run_filter("# Foo\n\nBar.")
        self.assertEqual(j["meta"]["starts-with-text"]["c"], "")

        j = self.run_filter(
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
        self.assertEqual(j["meta"]["starts-with-text"]["c"], "t")

        j = self.run_filter(
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
        self.assertEqual(j["meta"]["starts-with-text"]["c"], "")


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
