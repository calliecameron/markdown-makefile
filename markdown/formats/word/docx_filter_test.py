from panflute import Para, RawBlock, Str

from markdown.utils import test_utils


class TestDocxFilter(test_utils.PandocLuaFilterTestCase):
    def test_docx_filter(self) -> None:
        doc = self.run_filter(
            """Foo

* * *

Bar
""",
        )
        self.assertEqual(
            list(doc.content),
            [
                Para(Str("Foo")),
                RawBlock(
                    """<w:p>
  <w:pPr>
    <w:pStyle w:val="HorizontalRule"/>
      <w:ind w:firstLine="0"/>
      <w:jc w:val="center"/>
  </w:pPr>
  <w:r>
    <w:t>* * *</w:t>
  </w:r>
</w:p>""",
                    "openxml",
                ),
                Para(Str("Bar")),
            ],
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
