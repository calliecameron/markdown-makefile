import json
import os
import os.path
import subprocess
import sys
import unittest
from collections.abc import Mapping, Sequence

import markdown.utils.test_utils

SCRIPT = ""


class TestCombineDepsMetadata(unittest.TestCase):
    def dump_file(self, filename: str, content: Mapping[str, str]) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(content, f)

    def load_file(self, filename: str) -> str:
        with open(filename, encoding="utf-8") as f:
            return f.read()

    def run_script(self, metadata: Sequence[Mapping[str, str]]) -> str:
        test_tmpdir = markdown.utils.test_utils.tmpdir()

        metadata_args = []
        for i, d in enumerate(metadata):
            filename = os.path.join(test_tmpdir, f"metadata_{i+1}.json")
            self.dump_file(filename, d)
            metadata_args.append(("--metadata_file", f"dep{i+1}", filename))

        out_file = os.path.join(test_tmpdir, "out.json")

        subprocess.run(
            [
                sys.executable,
                SCRIPT,
                out_file,
            ]
            + [a for sublist in metadata_args for a in sublist],
            check=True,
        )

        return self.load_file(out_file)

    def test_empty(self) -> None:
        self.assertEqual(self.run_script([]), "{}")

    def test_non_empty(self) -> None:
        self.assertEqual(
            self.run_script(
                [
                    {"a": "b", "c": "d"},
                    {"a": "z", "c": "y"},
                ],
            ),
            """{
    "dep1": {
        "a": "b",
        "c": "d"
    },
    "dep2": {
        "a": "z",
        "c": "y"
    }
}""",
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
