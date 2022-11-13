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


if __name__ == '__main__':
    unittest.main()
