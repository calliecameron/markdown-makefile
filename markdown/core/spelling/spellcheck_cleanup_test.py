from markdown.utils import test_utils

DOC = """
Test [foo]{.nospellcheck} [bar]{.foo} baz

::: {.nospellcheck}
foo
:::
"""


class TestSpellcheckCleanup(test_utils.PandocLuaFilterTestCase):
    def test_cleanup(self) -> None:
        j = self.run_filter(DOC)
        self.assertEqual(2, len(j["blocks"]))
        self.assertEqual("foo", j["blocks"][0]["c"][2]["c"])
        self.assertEqual("bar", j["blocks"][0]["c"][4]["c"][1][0]["c"])
        self.assertEqual("baz", j["blocks"][0]["c"][6]["c"])
        self.assertEqual("foo", j["blocks"][1]["c"][0]["c"])


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
