from markdown.utils import test_utils


class TestValidateIDs(test_utils.PandocLuaFilterTestCase):
    def test_success(self) -> None:
        self.run_filter(
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
            self.run_filter(
                """``` {#__foo}
foo
```
""",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                """::: {.foo #__foo}
foo
:::
""",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                '![image](bar.jpg "An image"){#__foo .foo width=50%}',
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                "# Foo {#__foo}",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                "`foo`{#__foo}",
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                'Foo ![image](bar.jpg "An image"){#__foo .foo width=50%}',
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                '[foo](http://example.com "bar"){#__foo}',
            )

        with self.assertRaises(ValueError):
            self.run_filter(
                "[foo]{#__foo .bar}",
            )


if __name__ == "__main__":
    test_utils.PandocLuaFilterTestCase.main()
