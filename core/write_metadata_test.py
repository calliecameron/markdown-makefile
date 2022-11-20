import os
import os.path
import sys
import unittest
import test_utils

FILTER = ''

DOC = """% The Title
---
blah: yay
---

# Foo bar

Baz quux test yay.
"""


class TestWriteMetadata(unittest.TestCase):

    def test_write_metadata(self) -> None:
        test_tmpdir = os.getenv('TEST_TMPDIR')
        metadata_out_file = os.path.join(test_tmpdir, 'metadata.json')

        test_utils.pandoc_lua_filter(
            FILTER, DOC, [f'--metadata=metadata-out-file:{metadata_out_file}'])

        with open(metadata_out_file, encoding='utf-8') as f:
            self.assertEqual(f.read(), '{"blah":"yay","title":"The Title"}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
