import os
import os.path

from markdown.utils import test_utils


class TestWriteOpenScript(test_utils.ScriptTestCase):
    def test_write_open_script(self) -> None:
        out_file = os.path.join(self.tmpdir(), "out.sh")

        self.run_script(
            args=[
                "foo",
                "bar",
                out_file,
            ],
        )

        with open(out_file, encoding="utf-8") as f:
            self.assertEqual(
                f.read(),
                """#!/bin/bash

FILE_TO_OPEN="${0}.runfiles/foo/bar"

xdg-open "${FILE_TO_OPEN}"
""",
            )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
