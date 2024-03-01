import unittest

import markdown.utils.metadata


class TestMetadata(unittest.TestCase):
    def test_parse_author(self) -> None:
        self.assertEqual(markdown.utils.metadata.parse_author({}), "")
        self.assertEqual(markdown.utils.metadata.parse_author({"author": "Foo"}), "Foo")
        self.assertEqual(
            markdown.utils.metadata.parse_author({"author": ["Foo", "Bar"]}),
            "Foo",
        )

        with self.assertRaises(ValueError):
            markdown.utils.metadata.parse_author({"author": 2})

        with self.assertRaises(ValueError):
            markdown.utils.metadata.parse_author({"author": ["Foo", 2]})


if __name__ == "__main__":
    unittest.main()
