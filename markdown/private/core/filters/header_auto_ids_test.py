from panflute import Header, Str

from markdown.private.utils import test_utils


class TestHeaderAutoIDs(test_utils.PandocLuaFilterTestCase):
    def test_success(self) -> None:
        doc = self.run_filter(
            """
# Foo {#foo}

### Bar

# Baz

## Quux {#__quux}

### Yay
""",
        )

        self.assertEqual(
            list(doc.content),
            [
                Header(Str("Foo"), level=1, identifier="foo"),
                Header(Str("Bar"), level=3, identifier="__h3_1"),
                Header(Str("Baz"), level=1, identifier="__h1_2"),
                Header(Str("Quux"), level=2, identifier="__h2_1"),
                Header(Str("Yay"), level=3, identifier="__h3_2"),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
