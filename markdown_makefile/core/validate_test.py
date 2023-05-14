import sys
import unittest
import markdown_makefile.utils.test_utils


PANDOC = ""
FILTER = ""

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
  notes: foo bar
notes: baz quux
---

“Foo” ‘bar’
"""


class TestValidate(unittest.TestCase):
    def test_validate_succeeds(self) -> None:
        markdown_makefile.utils.test_utils.pandoc_filter(PANDOC, FILTER, GOOD)

    def test_validate_fails(self) -> None:
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(PANDOC, FILTER, "% '")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(PANDOC, FILTER, '% "')

        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(PANDOC, FILTER, "'")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(PANDOC, FILTER, '"')

        # Wrong type (should be list)
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications: foo
---
""",
            )

        # Unknown key
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- foo: bar
---
""",
            )

        # Missing required key
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- notes: foo
---
""",
            )

        # Missing required key
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: bar
---
""",
            )

        # Wrong type (should be string)
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue:
  - foo
  submitted: 2022-10-10
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  submitted: 2022-10-10
  paid:
  - foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  submitted: 2022-10-10
  notes:
  - foo
---
""",
            )

        # Wrong type (should be date)
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  submitted: foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  accepted: foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  rejected: foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  withdrawn: foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  abandoned: foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  published: foo
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: foo
---
""",
            )

        # Wrong type (should be list)
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  submitted: 2022-10-10
  urls: foo
---
""",
            )

        # Wrong type (should be list of string)
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  submitted: 2022-10-10
  urls:
  - foo: bar
---
""",
            )

        # Mutually exclusive keys
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  accepted: 2022-12-01
  rejected: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  accepted: 2022-12-01
  withdrawn: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  accepted: 2022-12-01
  abandoned: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  rejected: 2022-12-01
  withdrawn: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  rejected: 2022-12-01
  abandoned: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  rejected: 2022-12-01
  published: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  withdrawn: 2022-12-01
  published: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  abandoned: 2022-12-01
  published: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: 2022-12-01
  published: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: 2022-12-01
  submitted: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: 2022-12-01
  rejected: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: 2022-12-01
  withdrawn: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: 2022-12-01
  abandoned: 2022-12-02
---
""",
            )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
publications:
- venue: foo
  self-published: 2022-12-01
  accepted: 2022-12-02
---
""",
            )

        # Wrong type (should be string)
        with self.assertRaises(ValueError):
            markdown_makefile.utils.test_utils.pandoc_filter(
                PANDOC,
                FILTER,
                """
---
notes:
- foo
---
""",
            )


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
