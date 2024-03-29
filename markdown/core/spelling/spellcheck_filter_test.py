import sys
import unittest

import markdown.utils.test_utils

PANDOC = ""
FILTER = ""

DOC = """```python
print("foo")
```

    print("foo")

::: nospellcheck
foobarbaz
:::

::: foo
bar
:::

![image](bar.jpg "An image"){.foo width=50%}

# Foo {#foo}

## Bar {#bar}

!include foobarbaz

One `two` three

Foo ![image](bar.jpg "An image"){.foo width=50%} bar

Foo <http://example.com>

Bar [foo](http://example.com "bar"){.foo}

[Small]{.smallcaps}

Another [foobarbaz]{.nospellcheck} [line]{.foo}
"""


class TestSpellcheckFilter(unittest.TestCase):
    def test_cleanup(self) -> None:
        j = markdown.utils.test_utils.pandoc_lua_filter(PANDOC, FILTER, DOC)

        self.assertEqual(len(j["blocks"]), 10)

        # (removed) fenced code block
        # (removed) indented code block
        # (removed) nospellcheck div

        # 0: div: unwrap
        self.assertEqual(
            j["blocks"][0]["c"],
            [{"t": "Str", "c": "bar"}],
        )

        # 1: figure: remove target and attributes
        self.assertEqual(
            j["blocks"][1]["c"],
            [
                ["", [], []],
                [None, [{"t": "Plain", "c": [{"t": "Str", "c": "image"}]}]],
                [
                    {
                        "t": "Plain",
                        "c": [
                            {
                                "t": "Image",
                                "c": [["", [], []], [{"t": "Str", "c": "image"}], ["", "An image"]],
                            },
                        ],
                    },
                ],
            ],
        )

        # 2: h1: remove attributes
        self.assertEqual(
            j["blocks"][2]["c"],
            [1, ["", [], []], [{"t": "Str", "c": "Foo"}]],
        )

        # 3: h2: remove attributes
        self.assertEqual(
            j["blocks"][3]["c"],
            [2, ["", [], []], [{"t": "Str", "c": "Bar"}]],
        )

        # (removed) include

        # 4: inline code: remove
        self.assertEqual(
            j["blocks"][4]["c"],
            [{"t": "Str", "c": "One"}, {"t": "Space"}, {"t": "Space"}, {"t": "Str", "c": "three"}],
        )

        # 5: inline image: remove target and attributes
        self.assertEqual(
            j["blocks"][5]["c"],
            [
                {"t": "Str", "c": "Foo"},
                {"t": "Space"},
                {
                    "t": "Image",
                    "c": [["", [], []], [{"t": "Str", "c": "image"}], ["", "An image"]],
                },
                {"t": "Space"},
                {"t": "Str", "c": "bar"},
            ],
        )

        # 6: automatic link: remove
        self.assertEqual(
            j["blocks"][6]["c"],
            [{"t": "Str", "c": "Foo"}, {"t": "Space"}],
        )

        # 7: inline link: remove target and attributes
        self.assertEqual(
            j["blocks"][7]["c"],
            [
                {"t": "Str", "c": "Bar"},
                {"t": "Space"},
                {"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "foo"}], ["", "bar"]]},
            ],
        )

        # 8: smallcaps: unwrap
        self.assertEqual(j["blocks"][8]["c"], [{"t": "Str", "c": "Small"}])

        # 9: span: remove nospellcheck, unwrap others
        self.assertEqual(
            j["blocks"][9]["c"],
            [
                {"t": "Str", "c": "Another"},
                {"t": "Space"},
                {"t": "Space"},
                {"t": "Str", "c": "line"},
            ],
        )


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
