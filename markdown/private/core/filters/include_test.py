import os
import os.path

from panflute import Header, Para, Str

from markdown.private.utils import test_utils

DOC1 = """# Foo

Hello.
"""

DOC2 = """# Start

!include %s

Bar.
"""

DOC2_INC = """---
increment-included-headers: t
---
# Start

!include %s

Bar.
"""


class TestInclude(test_utils.PandocLuaFilterTestCase):
    def test_include(self) -> None:
        doc1 = self.run_filter(DOC1)
        self.assertEqual(
            list(doc1.content),
            [
                Header(Str("Foo"), level=1),
                Para(Str("Hello.")),
            ],
        )
        self.assertEqual(dict(doc1.metadata), {})
        doc1_file = os.path.join(self.tmpdir(), "doc1.json")
        self.dump_doc(doc1_file, doc1)

        doc2 = self.run_filter(
            DOC2 % doc1_file,
        )
        self.assertEqual(
            list(doc2.content),
            [
                Header(Str("Start"), level=1),
                Header(Str("Foo"), level=1),
                Para(Str("Hello.")),
                Para(Str("Bar.")),
            ],
        )
        self.assertEqual(dict(doc2.metadata), {})

        doc2_inc = self.run_filter(
            DOC2_INC % doc1_file,
        )
        self.assertEqual(
            list(doc2_inc.content),
            [
                Header(Str("Start"), level=1),
                Header(Str("Foo"), level=2),
                Para(Str("Hello.")),
                Para(Str("Bar.")),
            ],
        )
        self.assertEqual(dict(doc2_inc.metadata), {})

    def test_include_fails(self) -> None:
        bad_file = os.path.join(self.tmpdir(), "bad.json")

        with self.assertRaises(ValueError):
            self.run_filter(DOC2 % bad_file)


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
