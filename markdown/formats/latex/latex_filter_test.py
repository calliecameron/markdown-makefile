from panflute import Div, Para, RawBlock, Str

from markdown.utils import test_utils


class TestLatexFilter(test_utils.PandocLuaFilterTestCase):
    def test_latex_filter(self) -> None:
        doc = self.run_filter(
            """Foo

* * *

::: firstparagraph
Bar
:::
""",
        )
        self.assertEqual(
            list(doc.content),
            [
                Para(Str("Foo")),
                RawBlock("\\begin{center}* * *\\end{center}", "latex"),
                RawBlock(
                    """\\makeatletter
\\@afterindentfalse
\\@afterheading
\\makeatother
""",
                    "latex",
                ),
                Div(Para(Str("Bar")), classes=["firstparagraph"]),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
