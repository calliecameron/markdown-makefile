import os
import os.path
import subprocess
from collections.abc import Sequence

import markdown.core.preprocess
from markdown.utils import test_utils

GOOD = """Foo bar.

!include %s

!include %s

An image ![foo](%s "bar"){.baz} goes here.
"""


class TestPreprocess(test_utils.ScriptTestCase):
    def test_process_include(self) -> None:
        deps = {
            "foo:bar": "foo/bar.json",
            "baz:quux": "baz/quux.json",
        }

        # No include
        line, used, problem = markdown.core.preprocess.process_include(
            "foo bar",
            deps,
            "foo",
        )
        self.assertEqual(line, "foo bar")
        self.assertIsNone(used)
        self.assertIsNone(problem)

        # Good include
        line, used, problem = markdown.core.preprocess.process_include(
            "!include :bar",
            deps,
            "foo",
        )
        self.assertEqual(line, "!include foo/bar.json")
        self.assertEqual(used, "foo:bar")
        self.assertIsNone(problem)

        # Good include with extra spaces
        line, used, problem = markdown.core.preprocess.process_include(
            "!include     :bar",
            deps,
            "foo",
        )
        self.assertEqual(line, "!include foo/bar.json")
        self.assertEqual(used, "foo:bar")
        self.assertIsNone(problem)

        # Try to use unknown dependency
        line, used, problem = markdown.core.preprocess.process_include(
            "!include :baz",
            deps,
            "foo",
        )
        self.assertEqual(line, "!include :baz")
        self.assertEqual(used, "foo:baz")
        self.assertIsNotNone(problem)

        # Invalid include
        line, used, problem = markdown.core.preprocess.process_include(
            "!include",
            deps,
            "foo",
        )
        self.assertEqual(line, "!include")
        self.assertIsNone(used)
        self.assertIsNotNone(problem)

        # Invalid label
        line, used, problem = markdown.core.preprocess.process_include(
            "!include a:b:",
            deps,
            "foo",
        )
        self.assertEqual(line, "!include a:b:")
        self.assertIsNone(used)
        self.assertIsNotNone(problem)

    def test_process_images(self) -> None:
        images = {
            "foo:bar": "foo/bar.jpg",
            "baz/quux:quux": "baz/quux/quux.png",
        }

        # No images
        line, used, problems = markdown.core.preprocess.process_images(
            "Foo bar baz quux [link](foo)",
            images,
            "foo",
        )
        self.assertEqual(line, "Foo bar baz quux [link](foo)")
        self.assertEqual(used, frozenset())
        self.assertEqual(problems, [])

        # One image
        line, used, problems = markdown.core.preprocess.process_images(
            "Foo ![bar](//foo:bar)",
            images,
            "foo",
        )
        self.assertEqual(line, "Foo ![bar](foo/bar.jpg)")
        self.assertEqual(used, frozenset(["foo:bar"]))
        self.assertEqual(problems, [])

        # One image, title and attributes
        line, used, problems = markdown.core.preprocess.process_images(
            'Foo ![bar](//foo:bar "baz\\quux"){.quux}',
            images,
            "foo",
        )
        self.assertEqual(line, 'Foo ![bar](foo/bar.jpg "baz\\quux"){.quux}')
        self.assertEqual(used, frozenset(["foo:bar"]))
        self.assertEqual(problems, [])

        # Multiple images and duplicates
        line, used, problems = markdown.core.preprocess.process_images(
            'Foo ![bar](:bar) bar ![quux](//baz/quux) baz ![bar](:bar) ![bar](:bar "baz"){.quux}',
            images,
            "foo",
        )
        self.assertEqual(
            line,
            "Foo ![bar](foo/bar.jpg) bar ![quux](baz/quux/quux.png) baz ![bar](foo/bar.jpg) "
            '![bar](foo/bar.jpg "baz"){.quux}',
        )
        self.assertEqual(used, frozenset(["foo:bar", "baz/quux:quux"]))
        self.assertEqual(problems, [])

        # Try to use unknown image
        line, used, problems = markdown.core.preprocess.process_images(
            "Foo ![bar](:bar) bar ![quux](:quux)",
            images,
            "foo",
        )
        self.assertEqual(line, "Foo ![bar](:bar) bar ![quux](:quux)")
        self.assertEqual(used, frozenset(["foo:bar", "foo:quux"]))
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0][0], 21)

        # Invalid label
        line, used, problems = markdown.core.preprocess.process_images(
            "Foo ![bar](:bar:)",
            images,
            "foo",
        )
        self.assertEqual(line, "Foo ![bar](:bar:)")
        self.assertEqual(used, frozenset())
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0][0], 4)

    def test_check_strict_deps(self) -> None:
        # OK
        self.assertIsNone(
            markdown.core.preprocess.check_strict_deps(
                frozenset(["a", "b"]),
                frozenset(["a", "b"]),
                "foo",
            ),
        )

        # Used but not declared
        self.assertIsNotNone(
            markdown.core.preprocess.check_strict_deps(
                frozenset(["a", "b"]),
                frozenset(["a"]),
                "foo",
            ),
        )

        # Declared but not used
        self.assertIsNotNone(
            markdown.core.preprocess.check_strict_deps(
                frozenset(["a"]),
                frozenset(["a", "b"]),
                "foo",
            ),
        )

        # Both
        self.assertIsNotNone(
            markdown.core.preprocess.check_strict_deps(
                frozenset(["a", "c"]),
                frozenset(["a", "d"]),
                "foo",
            ),
        )

    def test_preprocess(self) -> None:
        deps = {
            "foo:bar": "foo/bar.json",
            "baz:quux": "baz/quux.json",
        }
        images = {
            "a:yay": "a/yay.jpg",
        }

        # OK
        data = (GOOD % ("//foo:bar", "//baz:quux", ":yay")).split("\n")
        problems = markdown.core.preprocess.preprocess(data, deps, images, "a")
        self.assertEqual(problems, [])
        self.assertEqual("\n".join(data), GOOD % ("foo/bar.json", "baz/quux.json", "a/yay.jpg"))

        # Bad include and bad image
        data = (GOOD % ("//foo:bar", "//blah:yay", "//baz:quux")).split("\n")
        problems = markdown.core.preprocess.preprocess(data, deps, images, "a")
        self.assertEqual(len(problems), 4)
        self.assertEqual("\n".join(data), GOOD % ("foo/bar.json", "//blah:yay", "//baz:quux"))

    def run_script(  # type: ignore[override]
        self,
        content: str,
        current_package: str,
        deps: Sequence[tuple[str, str]],
        images: Sequence[tuple[str, str]],
    ) -> str:
        in_file = os.path.join(self.tmpdir(), "in.md")
        self.dump_file(in_file, content)

        out_file = os.path.join(self.tmpdir(), "out.md")

        dep_args = []
        for dep, file in deps:
            dep_args += ["--dep", dep, file]

        image_args = []
        for image, file in images:
            image_args += ["--image", image, file]

        super().run_script(
            args=[
                in_file,
                out_file,
                current_package,
                *dep_args,
                *image_args,
            ],
        )

        return self.load_file(out_file)

    def test_main(self) -> None:
        output = self.run_script(
            GOOD % (":bar", "//baz:quux", ":foo"),
            "a",
            [("a:bar", "a/bar.json"), ("baz:quux", "baz/quux.json")],
            [("a:foo", "a/foo.jpg")],
        )
        self.assertEqual(output, GOOD % ("a/bar.json", "baz/quux.json", "a/foo.jpg"))

    def test_main_root_package(self) -> None:
        output = self.run_script(
            GOOD % (":bar", "//baz:quux", ":foo"),
            "",
            [(":bar", "bar.json"), ("baz:quux", "baz/quux.json")],
            [(":foo", "foo.jpg")],
        )
        self.assertEqual(output, GOOD % ("bar.json", "baz/quux.json", "foo.jpg"))

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script("!include", "a", [], [])


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
