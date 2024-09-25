import unittest

from markdown.private.utils import bazel_package

# ruff: noqa: SLF001


class TestBazelPackage(unittest.TestCase):
    def test_validate_package(self) -> None:
        bazel_package._validate_package("")
        bazel_package._validate_package("a")
        bazel_package._validate_package("abc/DEF123-.@_")

        with self.assertRaises(ValueError):
            bazel_package._validate_package("!")
        with self.assertRaises(ValueError):
            bazel_package._validate_package("/a")
        with self.assertRaises(ValueError):
            bazel_package._validate_package("a/")
        with self.assertRaises(ValueError):
            bazel_package._validate_package("a//b")

    def test_validate_target(self) -> None:
        bazel_package._validate_target("")
        bazel_package._validate_target("a")
        bazel_package._validate_target(
            "abc/DEF123%-@^_\"#$&'(*-+,;<=>?[]{|}~/.a",
        )

        with self.assertRaises(ValueError):
            bazel_package._validate_target("!")
        with self.assertRaises(ValueError):
            bazel_package._validate_target("/a")
        with self.assertRaises(ValueError):
            bazel_package._validate_target("a/")
        with self.assertRaises(ValueError):
            bazel_package._validate_target("a//b")
        with self.assertRaises(ValueError):
            bazel_package._validate_target("a/../b")
        with self.assertRaises(ValueError):
            bazel_package._validate_target("a/./b")

    def test_canonicalise_label(self) -> None:
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("", "")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("/", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("//", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("//:", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label(":", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("a:", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("a/", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("/a", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("//a:b:c", "a")
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label("!", "a")

        self.assertEqual(
            bazel_package.canonicalise_label("//a", "z"),
            ("a", "a"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("//a/b", "z"),
            ("a/b", "b"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("//a:", "z"),
            ("a", "a"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("//a:b", "z"),
            ("a", "b"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("//a/b:c/d", "z"),
            ("a/b", "c/d"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("//:a", "z"),
            ("", "a"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("//:a/b", "z"),
            ("", "a/b"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label(":a/b", "z"),
            ("z", "a/b"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("a/b", "z"),
            ("z", "a/b"),
        )
        self.assertEqual(
            bazel_package.canonicalise_label("a", ""),
            ("", "a"),
        )


if __name__ == "__main__":
    unittest.main()
