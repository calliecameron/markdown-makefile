import unittest

from markdown.utils.metadata import InputMetadata


class TestMetadata(unittest.TestCase):
    def test_author(self) -> None:
        self.assertEqual(InputMetadata().author, [])
        self.assertEqual(InputMetadata(author="foo").author, ["foo"])
        self.assertEqual(InputMetadata(author=["foo", "bar"]).author, ["foo", "bar"])

        with self.assertRaises(ValueError):
            InputMetadata(author=2)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            InputMetadata(author=[])


if __name__ == "__main__":
    unittest.main()
