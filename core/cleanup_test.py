import sys
import unittest
import test_utils

FILTER = ''

DOC = """---
title: Foo
repo: bar
---

"""


class TestCleanup(unittest.TestCase):

    def test_cleanup(self) -> None:
        j = test_utils.pandoc_lua_filter(FILTER, DOC)
        self.assertNotIn('repo', j['meta'])


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
