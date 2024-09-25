from markdown.private.utils import test_utils


class TestValidateQuotes(test_utils.PandocLuaFilterTestCase):
    def test_success(self) -> None:
        self.run_filter(
            """---
title: "“Foo” ‘bar’"
author: "\\"Foo\\" 'bar'"
---

“Test” ‘text’
""",  # noqa: RUF001
        )

    def test_failure(self) -> None:
        with self.assertRaises(ValueError):
            self.run_filter(
                """---
title: "Foo's title"
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
                """---
title: "\"Foo\""
---
""",
            )

        with self.assertRaises(ValueError):
            self.run_filter("'")
        with self.assertRaises(ValueError):
            self.run_filter('"')


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
