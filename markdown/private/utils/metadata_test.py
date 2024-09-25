import unittest

from markdown.private.utils.metadata import InputMetadata, ParsedDates


class TestMetadata(unittest.TestCase):
    def test_author(self) -> None:
        self.assertEqual(InputMetadata().author, [])
        self.assertEqual(InputMetadata(author="foo").author, ["foo"])
        self.assertEqual(InputMetadata(author=["foo", "bar"]).author, ["foo", "bar"])

        with self.assertRaises(ValueError):
            InputMetadata(author=2)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            InputMetadata(author=[])

    def test_parsed_dates(self) -> None:
        self.assertEqual(
            ParsedDates.model_validate(
                {
                    "parsed-dates": ["2020/01/01", "2021", "2021/03", "2024/06/23"],
                },
            ).parsed_dates,
            ["2020/01/01", "2021", "2021/03", "2024/06/23"],
        )

        with self.assertRaises(ValueError):
            ParsedDates.model_validate({"parsed-dates": ["2020/01/01 10:30:00"]})

        with self.assertRaises(ValueError):
            ParsedDates.model_validate({"parsed-dates": ["2020/01/01", "2020/01/01"]})

        with self.assertRaises(ValueError):
            ParsedDates.model_validate(
                {
                    "parsed-dates": ["2024/06/23", "2020/01/01"],
                },
            )


if __name__ == "__main__":
    unittest.main()
