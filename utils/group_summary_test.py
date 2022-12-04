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

    def test_summary(self) -> None:
        test_tmpdir = utils.test_utils.tmpdir()

        metadata1 = os.path.join(test_tmpdir, 'metadata1.json')
        self.dump_file(
            metadata1,
            {
                'title': 'Foo',
                'wordcount': '10',
                'docversion': 'bar',
            })

        metadata2 = os.path.join(test_tmpdir, 'metadata2.json')
        self.dump_file(
            metadata2,
            {
                'title': 'Baz',
                'wordcount': '20',
                'docversion': 'quux, dirty',
            })

        outfile = os.path.join(test_tmpdir, "out.csv")

        subprocess.run([
            sys.executable,
            SCRIPT,
            outfile,
            '--dep',
            '//foo:bar',
            metadata1,
            '--dep',
            '//baz:quux',
            metadata2
        ], check=True)

        with open(outfile, encoding='utf-8') as f:
            self.assertEqual(
                f.read(),
                """target,title,wordcount,version,status
//foo:bar,Foo,10,bar,ok
//baz:quux,Baz,20,"quux, dirty",DIRTY
""")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
