from panflute import MetaString

from markdown.private.utils import test_utils


class TestAddSubject(test_utils.PandocLuaFilterTestCase):
    def test_version(self) -> None:
        doc = self.run_filter(
            """---
version: Foo
---
""",
        )
        self.assertEqual(doc.metadata["subject"], MetaString("Version: Foo"))

    def test_no_version(self) -> None:
        doc = self.run_filter("")
        self.assertNotIn("subject", doc.metadata)


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
