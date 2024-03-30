import os
import os.path
import subprocess

import markdown.core.lint.custom_lint
from markdown.utils import test_utils

GOOD = """Foo bar.

\\“Lots \\”of \\‘quotes\\’.

Some -- dashes---
"""  # noqa: RUF001


class TestCustomLint(test_utils.ScriptTestCase):
    def test_lint(self) -> None:
        # OK
        self.assertEqual(markdown.core.lint.custom_lint.lint(GOOD.split("\n")), [])

        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["“"]), [])
        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["”"]), [])
        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["‘"]), [])  # noqa: RUF001
        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["’"]), [])  # noqa: RUF001
        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["–"]), [])  # noqa: RUF001
        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["—"]), [])
        self.assertNotEqual(markdown.core.lint.custom_lint.lint(["…"]), [])

    def run_script(  # type: ignore[override]
        self,
        content: str,
    ) -> None:
        in_file = os.path.join(self.tmpdir(), "in.md")
        with open(in_file, "w", encoding="utf-8") as f:
            f.write(content)

        out_file = os.path.join(self.tmpdir(), "out.txt")

        super().run_script(
            args=[
                in_file,
                out_file,
            ],
        )

        with open(out_file, encoding="utf-8") as f:
            self.assertEqual(f.read(), "OK\n")

    def test_main(self) -> None:
        self.run_script(GOOD)

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script("“")


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
