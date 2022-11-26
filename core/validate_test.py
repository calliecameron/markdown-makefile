import sys
import unittest
import utils.test_utils


PANDOC = ''
FILTER = ''

GOOD = """% “Hello” ‘world’
% Foo's name

“Foo” ‘bar’
"""


class TestValidate(unittest.TestCase):

    def test_validate_succeeds(self) -> None:
        utils.test_utils.pandoc_filter(PANDOC, FILTER, GOOD)

    def test_validate_fails(self) -> None:
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, "% '")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, '% "')

        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, "'")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, '"')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError('Not enough args')
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
