import sys
import unittest
import test_utils

FILTER = ''

DOC = """% The Title

# Foo bar

Baz quux test yay.
"""


class TestWordcount(unittest.TestCase):

    def test_wordcount(self) -> None:
        j = test_utils.pandoc_lua_filter(FILTER, DOC)
        self.assertEqual(j['meta']['wordcount']['c'], '6')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
