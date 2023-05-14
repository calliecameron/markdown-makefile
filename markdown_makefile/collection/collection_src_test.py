from typing import Any, Dict, List, Tuple
import json
import os
import os.path
import subprocess
import sys
import unittest
import markdown_makefile.utils.test_utils


SCRIPT = ""


class TestCollectionSrc(unittest.TestCase):
    def dump_file(self, filename: str, content: Dict[str, Any]) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(content, f)

    def load_file(self, filename: str) -> str:
        with open(filename, encoding="utf-8") as f:
            return f.read()

    def run_script(
        self, title: str, author: str, date: str, metadata: List[Tuple[str, Dict[str, Any]]]
    ) -> str:
        test_tmpdir = markdown_makefile.utils.test_utils.tmpdir()

        metadata_out = {}
        dep_args = []
        for target, data in metadata:
            metadata_out[target] = data
            dep_args += ["--dep", target]

        metadata_file = os.path.join(test_tmpdir, "metadata.json")
        self.dump_file(metadata_file, metadata_out)

        out_file = os.path.join(test_tmpdir, "out.md")

        subprocess.run(
            [
                sys.executable,
                SCRIPT,
            ]
            + dep_args
            + [
                title,
                author,
                date,
                metadata_file,
                out_file,
            ],
            check=True,
        )

        return self.load_file(out_file)

    def test_collection_src_simple(self) -> None:
        out = self.run_script(
            "The Title",
            "The Author",
            "",
            [
                (
                    "foo",
                    {
                        "title": "Foo",
                        "author": ["Bar"],
                    },
                ),
            ],
        )

        self.assertEqual(
            out,
            """% The Title
% The Author

# Foo

### Bar

!include //foo
""",
        )

    def test_collection_src_complex(self) -> None:
        out = self.run_script(
            "The Title",
            "The Author",
            "1 January",
            [
                (
                    "foo",
                    {
                        "title": "Foo",
                        "author": ["The Author"],
                        "date": "2 January",
                    },
                ),
                (
                    "bar",
                    {
                        "title": "Bar",
                        "author": ["Baz"],
                        "date": "3 January",
                    },
                ),
                (
                    "baz",
                    {
                        "title": "Baz",
                        "author": ["The Author"],
                        "date": "",
                    },
                ),
            ],
        )

        self.assertEqual(
            out,
            """% The Title
% The Author
% 1 January

# Foo

### 2 January

!include //foo

# Bar

### Baz, 3 January

!include //bar

# Baz

!include //baz
""",
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
