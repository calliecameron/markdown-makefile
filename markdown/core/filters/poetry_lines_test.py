from markdown.utils import test_utils

DOC = """% The Title

| Foo
| Bar

# Foo bar

> | Blah

Baz quux test yay.

> Foo
> Bar

> | Baz
> | Quux

"""


class TestPoetryLines(test_utils.PandocLuaFilterTestCase):
    def test_linecount(self) -> None:
        j = self.run_filter(DOC)
        self.assertEqual(j["meta"]["poetry-lines"]["c"], "3")


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
