import sys
import unittest

import markdown.utils.test_utils

PANDOC = ""
FILTER = ""


class TestValidateIDs(unittest.TestCase):
    def test_success(self) -> None:
        markdown.utils.test_utils.pandoc_lua_filter(
            PANDOC,
            FILTER,
            """
```
foo
```

``` {#foo}
foo
```

::: bar
foo
:::

::: {#foo .bar}
foo
:::

![image](bar.jpg "An image"){.foo width=50%}

![image](bar.jpg "An image"){#foo .foo width=50%}

# Foo

# Foo {#foo}

`foo`

`foo`{#foo}

Foo ![image](bar.jpg "An image"){.foo width=50%}

Foo ![image](bar.jpg "An image"){#foo .foo width=50%}

[foo](http://example.com "bar")

[foo](http://example.com "bar"){#foo}

[foo]{.bar}

[foo]{#foo .bar}
""",
        )

    def test_failure(self) -> None:
        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                """``` {#__foo}
foo
```
""",
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                """::: {.foo #__foo}
foo
:::
""",
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                '![image](bar.jpg "An image"){#__foo .foo width=50%}',
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                "# Foo {#__foo}",
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                "`foo`{#__foo}",
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                'Foo ![image](bar.jpg "An image"){#__foo .foo width=50%}',
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                '[foo](http://example.com "bar"){#__foo}',
            )

        with self.assertRaises(ValueError):
            markdown.utils.test_utils.pandoc_lua_filter(
                PANDOC,
                FILTER,
                "[foo]{#__foo .bar}",
            )


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        raise ValueError("Not enough args")
    PANDOC = sys.argv[1]
    del sys.argv[1]
    FILTER = sys.argv[1]
    del sys.argv[1]
    unittest.main()
