from markdown.utils import test_utils

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
finished: true
---

“Foo” ‘bar’
"""  # noqa: RUF001

GOOD2 = """---
title: “Hello” ‘world’
author: Foo's name
date: 10 June 2023
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
finished: true
---

“Foo” ‘bar’
"""  # noqa: RUF001


class TestValidate(test_utils.PandocFilterTestCase):
    def test_validate_succeeds(self) -> None:
        self.run_filter(GOOD)
        self.run_filter(GOOD2)

    def test_validate_fails(self) -> None:
        with self.assertRaises(ValueError):
            self.run_filter("% '")
        with self.assertRaises(ValueError):
            self.run_filter('% "')

        with self.assertRaises(ValueError):
            self.run_filter("'")
        with self.assertRaises(ValueError):
            self.run_filter('"')

        # Unknown key
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
foo: bar
---
        """,
            )

        # Wrong type (should be string)
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
title:
- foo
---
        """,
            )

        # Wrong type (should be list of string or string)
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
author:
- true
---
        """,
            )

        # Wrong type (should be list of string or string)
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
author: true
---
        """,
            )

        # Wrong type (should be string)
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
date: true
---
        """,
            )

        # Wrong type (should be list)
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications: foo
---
""",
            )

        # Unknown key
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- foo: bar
---
""",
            )

        # Missing required key
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- notes: foo
---
""",
            )

        # Missing required key
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- venue: bar
---
""",
            )

        # Wrong type (should be string)
        with self.assertRaises(ValueError):
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
                """
---
publications:
- venue: foo
  submitted: foo
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- venue: foo
  accepted: foo
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- venue: foo
  rejected: foo
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- venue: foo
  withdrawn: foo
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- venue: foo
  abandoned: foo
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
publications:
- venue: foo
  published: foo
---
""",
            )
        with self.assertRaises(ValueError):
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
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
            self.run_filter(
                """
---
notes:
- foo
---
""",
            )

        # Wrong type (should be bool)
        with self.assertRaises(ValueError):
            self.run_filter(
                """
---
finished: foo
---
""",
            )


if __name__ == "__main__":
    test_utils.PandocFilterTestCase.main()
