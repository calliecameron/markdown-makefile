from markdown.utils import test_utils


class TestAddTitle(test_utils.PandocLuaFilterTestCase):
    def test_existing_title(self) -> None:
        j = self.run_filter("% The Title")
        self.assertEqual(
            j["meta"]["title"],
            {
                "t": "MetaInlines",
                "c": [{"t": "Str", "c": "The"}, {"t": "Space"}, {"t": "Str", "c": "Title"}],
            },
        )

    def test_no_title(self) -> None:
        j = self.run_filter("")
        self.assertEqual(
            j["meta"]["title"],
            {
                "t": "MetaString",
                "c": "[Untitled]",
            },
        )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
