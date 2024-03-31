from panflute import (
    BlockQuote,
    BulletList,
    Caption,
    CodeBlock,
    Definition,
    DefinitionItem,
    DefinitionList,
    Div,
    Figure,
    Header,
    HorizontalRule,
    Image,
    LineBlock,
    LineItem,
    ListItem,
    Note,
    OrderedList,
    Para,
    Plain,
    Str,
)

from markdown.utils import test_utils


class TestParagraphAnnotations(test_utils.PandocLuaFilterTestCase):
    maxDiff = None

    def test_success(self) -> None:
        doc = self.run_filter(
            """
Foo

> Foo
>
> Bar

Foo

* Foo

  Bar

* Baz

Foo

```
Foo
```

Foo

Foo
  ~ Bar
  ~ Baz

Quux
  ~ Yay

Foo

![Foo](bar.jpg)

Foo

| Foo
| Bar

Foo

Foo^[Footnote]

Foo

1. Foo

   Bar

2. Baz

Foo

# Foo

Foo

Bar

* * *

::: foo
::: otherparagraph
Foo
:::
:::

Bar

&nbsp;

Foo

::: firstparagraph
Bar
:::
""",
        )

        self.assertEqual(
            list(doc.content),
            [
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                BlockQuote(Para(Str("Foo")), Para(Str("Bar"))),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                BulletList(
                    ListItem(Para(Str("Foo")), Para(Str("Bar"))),
                    ListItem(Para(Str("Baz"))),
                ),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                CodeBlock("Foo"),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                DefinitionList(
                    DefinitionItem(
                        [Str("Foo")],
                        [Definition(Plain(Str("Bar"))), Definition(Plain(Str("Baz")))],
                    ),
                    DefinitionItem(
                        [Str("Quux")],
                        [Definition(Plain(Str("Yay")))],
                    ),
                ),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                Figure(
                    Plain(Image(Str("Foo"), url="bar.jpg")),
                    caption=Caption(Plain(Str("Foo"))),
                ),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                LineBlock(
                    LineItem(Str("Foo")),
                    LineItem(Str("Bar")),
                ),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                Div(Para(Str("Foo"), Note(Para(Str("Footnote")))), classes=["otherparagraph"]),
                Div(Para(Str("Foo")), classes=["otherparagraph"]),
                OrderedList(
                    ListItem(Para(Str("Foo")), Para(Str("Bar"))),
                    ListItem(Para(Str("Baz"))),
                ),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                Header(Str("Foo"), level=1),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                Div(Para(Str("Bar")), classes=["otherparagraph"]),
                HorizontalRule(),
                Div(Div(Para(Str("Foo")), classes=["firstparagraph"]), classes=["foo"]),
                Div(Para(Str("Bar")), classes=["otherparagraph"]),
                Div(Para(Str("\u00A0")), classes=["blankline"]),
                Div(Para(Str("Foo")), classes=["firstparagraph"]),
                Div(Para(Str("Bar")), classes=["otherparagraph"]),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
