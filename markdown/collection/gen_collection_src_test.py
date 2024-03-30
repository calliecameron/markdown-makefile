import json
import os
import os.path
from collections.abc import Mapping, Sequence
from typing import Any

from markdown.utils import test_utils


class TestGenCollectionSrc(test_utils.ScriptTestCase):
    def dump_file(self, filename: str, content: Mapping[str, Any]) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(content, f)

    def load_file(self, filename: str) -> str:
        with open(filename, encoding="utf-8") as f:
            return f.read()

    def run_script(  # type: ignore[override]
        self,
        title: str,
        author: str,
        date: str,
        metadata: Sequence[tuple[str, Mapping[str, Any]]],
    ) -> str:
        metadata_out = {}
        dep_args = []
        for target, data in metadata:
            metadata_out[target] = data
            dep_args += ["--dep", target]

        metadata_file = os.path.join(self.tmpdir(), "metadata.json")
        self.dump_file(metadata_file, metadata_out)

        out_file = os.path.join(self.tmpdir(), "out.md")

        super().run_script(
            args=[
                *dep_args,
                title,
                author,
                date,
                metadata_file,
                out_file,
            ],
        )

        return self.load_file(out_file)

    def test_gen_collection_src_simple(self) -> None:
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
                        "starts-with-text": "",
                    },
                ),
            ],
        )

        self.assertEqual(
            out,
            """---
author:
- The Author
title: The Title
---

::: nospellcheck

# Foo

**Bar**

:::

!include //foo
""",
        )

    def test_gen_collection_src_complex(self) -> None:
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
                        "starts-with-text": "",
                    },
                ),
                (
                    "bar",
                    {
                        "title": "Bar",
                        "author": "Baz",
                        "date": "3 January",
                        "starts-with-text": "t",
                    },
                ),
                (
                    "baz",
                    {
                        "title": "Baz",
                        "author": ["The Author"],
                        "date": "",
                        "starts-with-text": "",
                    },
                ),
            ],
        )

        self.assertEqual(
            out,
            """---
author:
- The Author
date: 1 January
title: The Title
---

::: nospellcheck

# Foo

**2 January**

:::

!include //foo

::: nospellcheck

# Bar

**Baz, 3 January**

&nbsp;

:::

!include //bar

::: nospellcheck

# Baz

:::

!include //baz
""",
        )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
