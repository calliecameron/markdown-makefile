import os
import os.path
import sys
import unittest

import markdown_makefile.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = """% The Title
---
blah: yay
---

# Foo bar

Baz quux test yay.
"""


class TestWriteMetadata(unittest.TestCase):
    def test_write_metadata(self) -> None:
        test_tmpdir = markdown_makefile.utils.test_utils.tmpdir()
        metadata_out_file = os.path.join(test_tmpdir, "metadata.json")

        markdown_makefile.utils.test_utils.pandoc_lua_filter(
            PANDOC, FILTER, DOC, [f"--metadata=metadata-out-file:{metadata_out_file}"]
        )

        with open(metadata_out_file, encoding="utf-8") as f:
            self.assertEqual(f.read(), '{"blah":"yay","title":"The Title"}')


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
