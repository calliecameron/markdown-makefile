import sys
import unittest
import test_utils

FILTER = ''


class TestStartsWithText(unittest.TestCase):

    def test_starts_with_text(self) -> None:
        j = test_utils.pandoc_lua_filter(FILTER, 'Foo')
        self.assertEqual(j['meta']['starts-with-text']['c'], 't')

        j = test_utils.pandoc_lua_filter(FILTER, '# Foo\n\nBar.')
        self.assertEqual(j['meta']['starts-with-text']['c'], '')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
