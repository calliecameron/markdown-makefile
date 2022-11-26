from typing import Any, Dict
import json
import os
import os.path
import subprocess
import sys
import unittest
import utils.test_utils


SCRIPT = ''


class TestSummary(unittest.TestCase):

    def dump_file(self, filename: str, content: Dict[str, Any]) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f)

    def run_script(
            self, title: str, wordcount: int, version: str, header: bool
    ) -> str:
        test_tmpdir = utils.test_utils.tmpdir()

        metadata = os.path.join(test_tmpdir, 'metadata.json')
        self.dump_file(
            metadata,
            {
                'title': title,
                'wordcount': str(wordcount),
                'docversion': version,
            })

        args = [
            sys.executable,
            SCRIPT,
            '//foo:bar',
            metadata,
        ]
        if header:
            args.append('--header')

        output = subprocess.run(args, check=True, capture_output=True, encoding='utf-8')

        return output.stdout

    def test_summary(self) -> None:
        self.assertEqual(
            self.run_script('Foo', 10, 'bar', False),
            '//foo:bar,Foo,10,ok\n')

        self.assertEqual(
            self.run_script('Foo', 10, 'bar, dirty', True),
            'target,title,wordcount,status\n//foo:bar,Foo,10,DIRTY\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
