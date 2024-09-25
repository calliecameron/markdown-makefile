from markdown.private.utils import test_utils


class TestCleanupMetadata(test_utils.PandocLuaFilterTestCase):
    def test_all_true(self) -> None:
        doc = self.run_filter(
            """---
title: Foo
notes: test
finished: true
publications: foo
wordcount: 100
poetry-lines: 10
repo: foo
parsed-dates:
- foo
---
""",
        )
        self.assertEqual(frozenset(doc.metadata.keys()), frozenset(["title"]))

    def test_all_false(self) -> None:
        doc = self.run_filter(
            """---
title: Foo
notes: test
finished: false
publications: foo
wordcount: 100
poetry-lines: 10
repo: foo
parsed-dates: []
---
""",
        )
        self.assertEqual(frozenset(doc.metadata.keys()), frozenset(["title"]))

    def test_none(self) -> None:
        doc = self.run_filter(
            """---
title: Foo
---
""",
        )
        self.assertEqual(frozenset(doc.metadata.keys()), frozenset(["title"]))


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
