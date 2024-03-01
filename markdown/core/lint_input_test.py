import os
import os.path
import subprocess
import sys
import unittest

import markdown.utils.test_utils

SCRIPT = ""


class TestLintInput(unittest.TestCase):
    def run_script(
        self,
        content: str,
    ) -> str:
        test_tmpdir = markdown.utils.test_utils.tmpdir()

        in_file = os.path.join(test_tmpdir, "in.md")
        with open(in_file, "w", encoding="utf-8") as f:
            f.write(content)

        out_file = os.path.join(test_tmpdir, "out.md")

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
    if len(sys.argv) < 2:  # noqa: PLR2004
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
