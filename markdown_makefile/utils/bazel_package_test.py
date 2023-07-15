import unittest

import markdown_makefile.utils.bazel_package

# pylint: disable=protected-access


class TestBazelPackage(unittest.TestCase):
    def test_normalised_char_name(self) -> None:
        self.assertEqual(
            markdown_makefile.utils.bazel_package._normalised_char_name("/"), "SOLIDUS"
        )
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._normalised_char_name("ab")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._normalised_char_name("")

    def test_package_key(self) -> None:
        self.assertEqual(
            markdown_makefile.utils.bazel_package.package_key("a-b_/cd"),
            "A_HYPHENMINUS_B___SOLIDUS_CD",
        )
        self.assertEqual(markdown_makefile.utils.bazel_package.package_key(""), "")

    def test_version_key(self) -> None:
        self.assertEqual(
            markdown_makefile.utils.bazel_package.version_key("foo"), "STABLE_VERSION_foo"
        )
        self.assertEqual(markdown_makefile.utils.bazel_package.version_key(""), "STABLE_VERSION_")

    def test_repo_key(self) -> None:
        self.assertEqual(markdown_makefile.utils.bazel_package.repo_key("foo"), "STABLE_REPO_foo")
        self.assertEqual(markdown_makefile.utils.bazel_package.repo_key(""), "STABLE_REPO_")

    def test_validate_package(self) -> None:
        markdown_makefile.utils.bazel_package._validate_package("")
        markdown_makefile.utils.bazel_package._validate_package("a")
        markdown_makefile.utils.bazel_package._validate_package("abc/DEF123-.@_")

        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_package("!")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_package("/a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_package("a/")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_package("a//b")

    def test_validate_target(self) -> None:
        markdown_makefile.utils.bazel_package._validate_target("")
        markdown_makefile.utils.bazel_package._validate_target("a")
        markdown_makefile.utils.bazel_package._validate_target(
            "abc/DEF123%-@^_\"#$&'(*-+,;<=>?[]{|}~/.a"
        )

        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_target("!")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_target("/a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_target("a/")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_target("a//b")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_target("a/../b")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package._validate_target("a/./b")

    def test_canonicalise_label(self) -> None:
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("", "")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("/", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("//", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("//:", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label(":", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("a:", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("a/", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("/a", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("//a:b:c", "a")
        with self.assertRaises(ValueError):
            markdown_makefile.utils.bazel_package.canonicalise_label("!", "a")

        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//a", "z"), ("a", "a")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//a/b", "z"), ("a/b", "b")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//a:", "z"), ("a", "a")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//a:b", "z"), ("a", "b")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//a/b:c/d", "z"),
            ("a/b", "c/d"),
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//:a", "z"), ("", "a")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("//:a/b", "z"), ("", "a/b")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label(":a/b", "z"), ("z", "a/b")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("a/b", "z"), ("z", "a/b")
        )
        self.assertEqual(
            markdown_makefile.utils.bazel_package.canonicalise_label("a", ""), ("", "a")
        )


if __name__ == "__main__":
    unittest.main()
