from markdown.utils import test_utils


class TestCleanup(test_utils.PandocLuaFilterTestCase):
    def test_cleanup(self) -> None:
        j = self.run_filter(
            """---
title: Foo
repo: bar
---

""",
        )
        self.assertNotIn("repo", j["meta"])


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
