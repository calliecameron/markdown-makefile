from panflute import Caption, Figure, Header, Image, Link, Para, Plain, Space, Str

from markdown.utils import test_utils

# ruff: noqa: ERA001

DOC = """```python
print("foo")
```

    print("foo")

::: nospellcheck
foobarbaz
:::

::: foo
bar
:::

![image](bar.jpg "An image"){.foo width=50%}

# Foo {#foo}

## Bar {#bar}

!include foobarbaz

One `two` three

Foo ![image](bar.jpg "An image"){.foo width=50%} bar

Foo <http://example.com>

Bar [foo](http://example.com "bar"){.foo}

[Small]{.smallcaps}

Another [foobarbaz]{.nospellcheck} [line]{.foo}
"""


class TestSpellcheckFilter(test_utils.PandocLuaFilterTestCase):
    def test_filter(self) -> None:
        doc = self.run_filter(DOC)
        self.assertEqual(
            list(doc.content),
            [
                # (removed) fenced code block
                # (removed) indented code block
                # (removed) nospellcheck div
                # div: unwrap
                Para(Str("bar")),
                # figure: remove target and attributes
                Figure(
                    Plain(Image(Str("image"), title="An image")),
                    caption=Caption(Plain(Str("image"))),
                ),
                # h1: remove attributes
                Header(Str("Foo"), level=1),
                # h2: remove attributes
                Header(Str("Bar"), level=2),
                # (removed) include
                # inline code: remove
                Para(Str("One"), Space(), Space(), Str("three")),
                # inline image: remove target and attributes
                Para(
                    Str("Foo"),
                    Space(),
                    Image(Str("image"), title="An image"),
                    Space(),
                    Str("bar"),
                ),
                # automatic link: remove
                Para(Str("Foo"), Space()),
                Para(Str("Bar"), Space(), Link(Str("foo"), title="bar")),
                # smallcaps: unwrap
                Para(Str("Small")),
                # span: remove nospellcheck, unwrap others
                Para(Str("Another"), Space(), Space(), Str("line")),
            ],
        )

    def test_filter_fails(self) -> None:
        with self.assertRaises(ValueError):
            self.run_filter(
                """``` {.nospellcheck}
foo
```""",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                '![image](bar.jpg "An image"){.foo .nospellcheck width=50%}',
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                "# Foo {.nospellcheck}",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                "`foo`{.nospellcheck}",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                'Foo ![image](bar.jpg "An image"){.foo .nospellcheck width=50%} bar',
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                '[foo](http://example.com "bar"){.foo .nospellcheck}',
            )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
