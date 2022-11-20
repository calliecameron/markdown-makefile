import sys
import unittest
import test_utils


FILTER = ''

GOOD = """% “Hello” ‘world’
% Foo's name

“Foo” ‘bar’
"""


class TestValidate(unittest.TestCase):

    def test_validate_succeeds(self) -> None:
        test_utils.pandoc_filter(FILTER, GOOD)

    def test_validate_fails(self) -> None:
        with self.assertRaises(ValueError):
            test_utils.pandoc_filter(FILTER, "% '")
        with self.assertRaises(ValueError):
            test_utils.pandoc_filter(FILTER, '% "')

        with self.assertRaises(ValueError):
            test_utils.pandoc_filter(FILTER, "'")
        with self.assertRaises(ValueError):
            test_utils.pandoc_filter(FILTER, '"')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
