from typing import Any, Dict
import json
import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestMsMetadata(unittest.TestCase):

    def run_ms_metadata(self, metadata: Dict[str, Any]) -> str:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        in_file = os.path.join(test_tmpdir, 'in.json')
        with open(in_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f)

        out_file = os.path.join(test_tmpdir, 'out.json')

        subprocess.run([
            sys.executable,
            SCRIPT,
            in_file,
            out_file,
        ], check=True)

        with open(out_file, encoding='utf-8') as f:
            return f.read()

    def test_ms_metadata(self) -> None:
        self.assertEqual(self.run_ms_metadata(
            {'title': 'The Title', 'author': ['An Author']}),
            """{
    "author_lastname": "Author",
    "contact_address": "`\\\\n`{=tex}",
    "contact_city_state_zip": "`\\\\n`{=tex}",
    "contact_email": "`\\\\n`{=tex}",
    "contact_name": "An Author",
    "contact_phone": "`\\\\n`{=tex}",
    "short_title": "The Title"
}""")

    def test_ms_metadata_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_ms_metadata({'author': ['An Author']})
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_ms_metadata({'title': 'The Title'})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
