import os
import os.path
from collections.abc import Mapping, Sequence
from typing import Any

from markdown.utils import test_utils


class TestGenCollectionSrc(test_utils.ScriptTestCase):
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
        self.dump_json(metadata_file, metadata_out)

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
                        "wordcount": "10",
                        "poetry-lines": "0",
                        "lang": "en-GB",
                        "docversion": "foo",
                        "repo": "bar",
                        "subject": "baz",
                        "source-hash": "1",
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

::: collectionseparator
&nbsp;
:::

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
                        "wordcount": "10",
                        "poetry-lines": "0",
                        "lang": "en-GB",
                        "docversion": "foo",
                        "repo": "bar",
                        "subject": "baz",
                        "source-hash": "1",
                    },
                ),
                (
                    "bar",
                    {
                        "title": "Bar",
                        "author": "Baz",
                        "date": "3 January",
                        "wordcount": "10",
                        "poetry-lines": "0",
                        "lang": "en-GB",
                        "docversion": "foo",
                        "repo": "bar",
                        "subject": "baz",
                        "source-hash": "1",
                    },
                ),
                (
                    "baz",
                    {
                        "title": "Baz",
                        "author": ["The Author"],
                        "date": "",
                        "wordcount": "10",
                        "poetry-lines": "0",
                        "lang": "en-GB",
                        "docversion": "foo",
                        "repo": "bar",
                        "subject": "baz",
                        "source-hash": "1",
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

::: collectionseparator
&nbsp;
:::

:::

!include //foo

::: nospellcheck

# Bar

**Baz, 3 January**

::: collectionseparator
&nbsp;
:::

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
