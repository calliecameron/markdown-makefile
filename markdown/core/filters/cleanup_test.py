from markdown.utils import test_utils


class TestCleanup(test_utils.PandocLuaFilterTestCase):
    def test_cleanup(self) -> None:
        doc = self.run_filter(
            """---
title: Foo
repo: bar
---

""",
        )
        self.assertNotIn("repo", doc.metadata)


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
