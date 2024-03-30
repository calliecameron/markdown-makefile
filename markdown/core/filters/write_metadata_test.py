import os
import os.path

from markdown.utils import test_utils

DOC = """% The Title
---
blah: yay
---

# Foo bar

Baz quux test yay.
"""


class TestWriteMetadata(test_utils.PandocLuaFilterTestCase):
    def test_write_metadata(self) -> None:
        metadata_out_file = os.path.join(self.tmpdir(), "metadata.json")

        self.run_filter(
            DOC,
            [f"--metadata=metadata-out-file:{metadata_out_file}"],
        )

        with open(metadata_out_file, encoding="utf-8") as f:
            self.assertEqual(f.read(), '{"blah":"yay","title":"The Title"}')


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
