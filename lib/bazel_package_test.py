import unittest
import bazel_package

# pylint: disable=protected-access


class TestBazelPackage(unittest.TestCase):

    def test_normalised_char_name(self) -> None:
        self.assertEqual(bazel_package._normalised_char_name('/'), 'SOLIDUS')
        with self.assertRaises(ValueError):
            bazel_package._normalised_char_name('ab')
        with self.assertRaises(ValueError):
            bazel_package._normalised_char_name('')

    def test_package_key(self) -> None:
        self.assertEqual(bazel_package.package_key('a-b_/cd'), 'A_HYPHENMINUS_B___SOLIDUS_CD')

    def test_version_key(self) -> None:
        self.assertEqual(bazel_package.version_key('foo'), 'STABLE_VERSION_foo')

    def test_repo_key(self) -> None:
        self.assertEqual(bazel_package.repo_key('foo'), 'STABLE_REPO_foo')

    def test_validate_package(self) -> None:
        bazel_package._validate_package('')
        bazel_package._validate_package('a')
        bazel_package._validate_package('abc/DEF123-.@_')

        with self.assertRaises(ValueError):
            bazel_package._validate_package('!')
        with self.assertRaises(ValueError):
            bazel_package._validate_package('/a')
        with self.assertRaises(ValueError):
            bazel_package._validate_package('a/')
        with self.assertRaises(ValueError):
            bazel_package._validate_package('a//b')

    def test_validate_target(self) -> None:
        bazel_package._validate_target('')
        bazel_package._validate_target('a')
        bazel_package._validate_target('abc/DEF123%-@^_"#$&\'()*-+,;<=>?[]{|}~/.a')

        with self.assertRaises(ValueError):
            bazel_package._validate_target('!')
        with self.assertRaises(ValueError):
            bazel_package._validate_target('/a')
        with self.assertRaises(ValueError):
            bazel_package._validate_target('a/')
        with self.assertRaises(ValueError):
            bazel_package._validate_target('a//b')
        with self.assertRaises(ValueError):
            bazel_package._validate_target('a/../b')
        with self.assertRaises(ValueError):
            bazel_package._validate_target('a/./b')

    def test_canonicalise_label(self):
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('', '')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('a', '')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('/', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('//', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('//:', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label(':', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('a:', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('a/', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('/a', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('//a:b:c', 'a')
        with self.assertRaises(ValueError):
            bazel_package.canonicalise_label('!', 'a')

        self.assertEqual(bazel_package.canonicalise_label('//a', 'z'), ('a', 'a'))
        self.assertEqual(bazel_package.canonicalise_label('//a/b', 'z'), ('a/b', 'b'))
        self.assertEqual(bazel_package.canonicalise_label('//a:', 'z'), ('a', 'a'))
        self.assertEqual(bazel_package.canonicalise_label('//a:b', 'z'), ('a', 'b'))
        self.assertEqual(bazel_package.canonicalise_label('//a/b:c/d', 'z'), ('a/b', 'c/d'))
        self.assertEqual(bazel_package.canonicalise_label('//:a', 'z'), ('', 'a'))
        self.assertEqual(bazel_package.canonicalise_label('//:a/b', 'z'), ('', 'a/b'))
        self.assertEqual(bazel_package.canonicalise_label(':a/b', 'z'), ('z', 'a/b'))
        self.assertEqual(bazel_package.canonicalise_label('a/b', 'z'), ('z', 'a/b'))


if __name__ == '__main__':
    unittest.main()
