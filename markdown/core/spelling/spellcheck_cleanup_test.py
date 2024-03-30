from panflute import Para, Space, Span, Str

from markdown.utils import test_utils

DOC = """
Test [foo]{.nospellcheck} [bar]{.foo} baz

::: {.nospellcheck}
foo
:::
"""


class TestSpellcheckCleanup(test_utils.PandocLuaFilterTestCase):
    def test_cleanup(self) -> None:
        doc = self.run_filter(DOC)
        self.assertEqual(
            list(doc.content),
            [
                Para(
                    Str("Test"),
                    Space(),
                    Str("foo"),
                    Space(),
                    Span(Str("bar"), classes=["foo"]),
                    Space(),
                    Str("baz"),
                ),
                Para(Str("foo")),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
