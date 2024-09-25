import os
import os.path

from markdown.private.utils import test_utils

DOC = """---
title: The Title
blah: yay
---

# Foo bar

Baz quux test yay.
"""


class TestWriteMetadata(test_utils.PandocLuaFilterTestCase):
    def test_write_metadata(self) -> None:
        metadata_out_file = os.path.join(self.tmpdir(), "metadata.json")

        doc = self.run_filter(
            DOC,
            [f"--metadata=metadata-out-file:{metadata_out_file}"],
        )

        self.assertEqual(
            self.load_json(metadata_out_file),
            {
                "blah": "yay",
                "title": "The Title",
            },
        )

        self.assertNotIn("metadata-out-file", doc.metadata)


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
