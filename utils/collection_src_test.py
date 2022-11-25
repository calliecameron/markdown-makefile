from typing import Any, Dict, List, Tuple
import json
import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestCollectionSrc(unittest.TestCase):

    def dump_file(self, filename: str, content: Dict[str, Any]) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f)

    def load_file(self, filename: str) -> str:
        with open(filename, encoding='utf-8') as f:
            return f.read()

    def run_script(
            self, title: str, author: str, date: str, metadata: List[Tuple[str, Dict[str, Any]]]
    ) -> str:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        dep_args = []
        for i, m in enumerate(metadata):
            target, data = m
            filename = os.path.join(test_tmpdir, f'metadata_{i+1}.json')
            self.dump_file(filename, data)
            dep_args += ['--dep', target, filename]

        out_file = os.path.join(test_tmpdir, 'out.md')

        subprocess.run([
            sys.executable,
            SCRIPT,
        ] + dep_args + [
            title,
            author,
            date,
            out_file,
        ], check=True)

        return self.load_file(out_file)

    def test_collection_src_simple(self) -> None:
        out = self.run_script(
            'The Title',
            'The Author',
            '',
            [
                (
                    'foo',
                    {
                        'title': 'Foo',
                        'author': ['Bar'],
                    },
                ),
            ])

        self.assertEqual(out, """% The Title
% The Author

# Foo

### Bar

!include //foo
""")

    def test_collection_src_complex(self) -> None:
        out = self.run_script(
            'The Title',
            'The Author',
            '1 January',
            [
                (
                    'foo',
                    {
                        'title': 'Foo',
                        'author': ['The Author'],
                        'date': '2 January',
                    },
                ),
                (
                    'bar',
                    {
                        'title': 'Bar',
                        'author': ['Baz'],
                        'date': '3 January',
                    },
                ),
                (
                    'baz',
                    {
                        'title': 'Baz',
                        'author': ['The Author'],
                        'date': '',
                    },
                ),
            ])

        self.assertEqual(out, """% The Title
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
""")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
