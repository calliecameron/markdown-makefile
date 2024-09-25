import os
import os.path

from markdown.private.utils import test_utils


class TestGenStandardLintInput(test_utils.ScriptTestCase):
    def run_script(  # type: ignore[override]
        self,
        content: str,
    ) -> str:
        in_file = os.path.join(self.tmpdir(), "in.md")
        self.dump_file(in_file, content)

        out_file = os.path.join(self.tmpdir(), "out.md")

        super().run_script(
            args=[
                in_file,
                out_file,
            ],
        )

        return self.load_file(out_file)

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
