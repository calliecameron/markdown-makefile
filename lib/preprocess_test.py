import unittest
import preprocess


GOOD = """Foo bar.

!include %s

!include %s

\\“Lots \\”of \\‘quotes\\’.

Some -- dashes---
"""


class TestPreprocess(unittest.TestCase):

    def test_process_include(self) -> None:
        self.assertEqual(preprocess.process_include('!include'), None)
        self.assertEqual(preprocess.process_include('!include foo'), None)
        self.assertEqual(preprocess.process_include('!include //:bar'), None)
        self.assertEqual(preprocess.process_include('!include //foo/bar'), 'foo/bar:bar')
        self.assertEqual(preprocess.process_include('!include //foo/bar:baz'), 'foo/bar:baz')

    def test_preprocess(self) -> None:
        data = (GOOD % ('//foo:bar', '//baz:quux')).split('\n')
        self.assertEqual(preprocess.preprocess(
            data, {'foo:bar': 'foo/bar.json', 'baz:quux': 'baz/quux.json'}), [])
        self.assertEqual('\n'.join(data), GOOD % ('foo/bar.json', 'baz/quux.json'))

        data = (GOOD % ('//foo:bar', '//blah:yay')).split('\n')
        self.assertNotEqual(preprocess.preprocess(
            data, {'foo:bar': 'foo/bar.json', 'baz:quux': 'baz/quux.json'}), [])
        self.assertEqual('\n'.join(data), GOOD % ('foo/bar.json', '//blah:yay'))

        self.assertNotEqual(preprocess.preprocess(['“'], {}), [])
        self.assertNotEqual(preprocess.preprocess(['”'], {}), [])
        self.assertNotEqual(preprocess.preprocess(['‘'], {}), [])
        self.assertNotEqual(preprocess.preprocess(['’'], {}), [])
        self.assertNotEqual(preprocess.preprocess(['–'], {}), [])
        self.assertNotEqual(preprocess.preprocess(['—'], {}), [])
        self.assertNotEqual(preprocess.preprocess(['…'], {}), [])


if __name__ == '__main__':
    unittest.main()
