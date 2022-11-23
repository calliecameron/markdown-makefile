from typing import List, Tuple
import os
import os.path
import subprocess
import sys
import unittest
import preprocess


SCRIPT = ''

GOOD = """Foo bar.

!include %s

!include %s

\\“Lots \\”of \\‘quotes\\’.

Some -- dashes---
"""


class TestPreprocess(unittest.TestCase):

    def test_process_include(self) -> None:
        self.assertEqual(preprocess.get_include('foo bar', 'a'), None)
        with self.assertRaises(ValueError):
            preprocess.get_include('!include', 'a')
        with self.assertRaises(ValueError):
            preprocess.get_include('!include ', 'a')
        with self.assertRaises(ValueError):
            preprocess.get_include('!include a:b:c', 'a')
        self.assertEqual(preprocess.get_include('!include foo', ''), ':foo')
        self.assertEqual(preprocess.get_include('!include foo', 'a'), 'a:foo')
        self.assertEqual(preprocess.get_include('!include  :foo', 'a'), 'a:foo')
        self.assertEqual(preprocess.get_include('!include //:bar', 'a'), ':bar')
        self.assertEqual(preprocess.get_include('!include //foo:bar', 'a'), 'foo:bar')
        self.assertEqual(preprocess.get_include('!include //foo', 'a'), 'foo:foo')

    def test_preprocess(self) -> None:
        data = (GOOD % ('//foo:bar', '//baz:quux')).split('\n')
        self.assertEqual(preprocess.preprocess(
            data, {'foo:bar': 'foo/bar.json', 'baz:quux': 'baz/quux.json'}, 'a'), [])
        self.assertEqual('\n'.join(data), GOOD % ('foo/bar.json', 'baz/quux.json'))

        data = (GOOD % (':bar', '//blah:yay')).split('\n')
        self.assertNotEqual(preprocess.preprocess(
            data, {':bar': 'bar.json', 'baz:quux': 'baz/quux.json'}, ''), [])
        self.assertEqual('\n'.join(data), GOOD % ('bar.json', '//blah:yay'))

        self.assertNotEqual(preprocess.preprocess(['“'], {}, 'a'), [])
        self.assertNotEqual(preprocess.preprocess(['”'], {}, 'a'), [])
        self.assertNotEqual(preprocess.preprocess(['‘'], {}, 'a'), [])
        self.assertNotEqual(preprocess.preprocess(['’'], {}, 'a'), [])
        self.assertNotEqual(preprocess.preprocess(['–'], {}, 'a'), [])
        self.assertNotEqual(preprocess.preprocess(['—'], {}, 'a'), [])
        self.assertNotEqual(preprocess.preprocess(['…'], {}, 'a'), [])

    def run_script(self, content: str, current_package: str, deps: List[Tuple[str, str]]) -> str:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        in_file = os.path.join(test_tmpdir, 'in.md')
        with open(in_file, 'w', encoding='utf-8') as f:
            f.write(content)

        out_file = os.path.join(test_tmpdir, 'out.md')

        dep_args = []
        for dep, file in deps:
            dep_args += ['--dep', dep, file]

        subprocess.run([
            sys.executable,
            SCRIPT,
            in_file,
            out_file,
            current_package,
        ] + dep_args, check=True)

        with open(out_file, encoding='utf-8') as f:
            return f.read()

    def test_main(self) -> None:
        output = self.run_script(
            GOOD % (':bar', '//baz:quux'),
            'a',
            [('a:bar', 'a/bar.json'), ('baz:quux', 'baz/quux.json')])
        self.assertEqual(output, GOOD % ('a/bar.json', 'baz/quux.json'))

    def test_main_root_package(self) -> None:
        output = self.run_script(
            GOOD % (':bar', '//baz:quux'),
            '',
            [(':bar', 'bar.json'), ('baz:quux', 'baz/quux.json')])
        self.assertEqual(output, GOOD % ('bar.json', 'baz/quux.json'))

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script(
                '“',
                'a',
                [])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
