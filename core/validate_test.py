import sys
import unittest
import utils.test_utils


PANDOC = ''
FILTER = ''

GOOD = """% “Hello” ‘world’
% Foo's name

---
publications:
- venue: Foo
  submitted: 2022-12-01
  accepted: 2022-12-02
  published: 2022-12-03
  paid: £10
  urls:
  - "http://example.com"
  note: foo bar
---

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

        # Wrong type (should be list)
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications: foo
---
""")

        # Unknown key
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- foo: bar
---
""")

        # Wrong type (should be string)
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- venue:
  - foo
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- paid:
  - foo
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- note:
  - foo
---
""")

        # Wrong type (should be date)
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- submitted: foo
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- accepted: foo
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- rejected: foo
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- withdrawn: foo
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- published: foo
---
""")

        # Wrong type (should be list)
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- urls: foo
---
""")

        # Wrong type (should be list of string)
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- urls:
  - foo: bar
---
""")

        # Mutually exclusive keys
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- accepted: 2022-12-01
  rejected: 2022-12-02
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- accepted: 2022-12-01
  withdrawn: 2022-12-02
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- rejected: 2022-12-01
  withdrawn: 2022-12-02
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- rejected: 2022-12-01
  published: 2022-12-02
---
""")
        with self.assertRaises(ValueError):
            utils.test_utils.pandoc_filter(PANDOC, FILTER, """
---
publications:
- withdrawn: 2022-12-01
  published: 2022-12-02
---
""")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise ValueError('Not enough args')
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
