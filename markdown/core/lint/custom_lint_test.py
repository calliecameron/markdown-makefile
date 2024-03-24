import os
import os.path
import subprocess
import sys
import unittest

import markdown.core.lint.custom_lint
import markdown.utils.test_utils

SCRIPT = ""

GOOD = """Foo bar.

\\“Lots \\”of \\‘quotes\\’.

Some -- dashes---
"""  # noqa: RUF001


class TestCustomLint(unittest.TestCase):
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

    def run_script(
        self,
        content: str,
    ) -> None:
        test_tmpdir = markdown.utils.test_utils.tmpdir()

        in_file = os.path.join(test_tmpdir, "in.md")
        with open(in_file, "w", encoding="utf-8") as f:
            f.write(content)

        out_file = os.path.join(test_tmpdir, "out.txt")

        subprocess.run(
            [
                sys.executable,
                SCRIPT,
                in_file,
                out_file,
            ],
            check=True,
        )

        with open(out_file, encoding="utf-8") as f:
            self.assertEqual(f.read(), "OK\n")

    def test_main(self) -> None:
        self.run_script(GOOD)

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script("“")


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
