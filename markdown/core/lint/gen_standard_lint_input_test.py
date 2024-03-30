import os
import os.path

from markdown.utils import test_utils


class TestGenStandardLintInput(test_utils.ScriptTestCase):
    def run_script(  # type: ignore[override]
        self,
        content: str,
    ) -> str:
        in_file = os.path.join(self.tmpdir(), "in.md")
        with open(in_file, "w", encoding="utf-8") as f:
            f.write(content)

        out_file = os.path.join(self.tmpdir(), "out.md")

        super().run_script(
            args=[
                in_file,
                out_file,
            ],
        )

        with open(out_file, encoding="utf-8") as f:
            return f.read()

    def test_simple(self) -> None:
        self.assertEqual(
            self.run_script(
                """Foo
bar

# baz
""",
            ),
            """Foo
bar

# baz
""",
        )

    def test_complex(self) -> None:
        self.assertEqual(
            self.run_script(
                """---
title: foo
author: bar
---

Foo

bar

# baz

---
date: a
---

""",
            ),
            """<!-- -->
<!-- -->
<!-- -->
<!-- -->

Foo

bar

# baz

---
date: a
---

""",
        )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
