import os
import os.path
import subprocess
from collections.abc import Mapping
from typing import Any

from markdown.utils import test_utils


class TestValidateOutputMetadata(test_utils.ScriptTestCase):
    def run_script(  # type: ignore[override]
        self,
        content: Mapping[str, Any],
    ) -> None:
        in_file = os.path.join(self.tmpdir(), "in.json")
        self.dump_json(in_file, content)

        out_file = os.path.join(self.tmpdir(), "out.txt")

        super().run_script(
            args=[
                in_file,
                out_file,
            ],
        )

        self.assertEqual(self.load_file(out_file), "OK\n")

    def test_good(self) -> None:
        self.run_script(
            {
                "wordcount": 10,
                "poetry-lines": "10",
                "lang": "en-GB",
                "docversion": "foo",
                "repo": "bar",
                "subject": "baz",
                "source-hash": "quux",
            },
        )

    def test_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script({})


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
