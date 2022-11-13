import unittest
import base_metadata


class TestBaseMetadata(unittest.TestCase):

    def test_version(self) -> None:
        v = base_metadata.Version.from_dict({'version': '1', 'repo': 'foo'})
        self.assertEqual(v.version, '1')
        self.assertEqual(v.repo, 'foo')
        self.assertEqual(v.to_dict(), {'version': '1', 'repo': 'foo'})

    def test_get_version(self) -> None:
        base = base_metadata.Version('1', 'foo')
        clean = base_metadata.Version('2', 'bar')
        dirty = base_metadata.Version('3-dirty', 'baz')
        unversioned = base_metadata.Version('unversioned', 'quux')
        dirty_same_repo = base_metadata.Version('4-dirty', 'foo')
        unversioned_same_repo = base_metadata.Version('unversioned', 'foo')

        self.assertEqual(base_metadata.get_version(base, {}).version, '1')
        self.assertEqual(base_metadata.get_version(base, {}).repo, 'foo')
        self.assertEqual(base_metadata.get_version(base, {'a': clean}).version, '1')
        self.assertEqual(base_metadata.get_version(base, {'a': clean}).repo, 'foo')
        self.assertEqual(base_metadata.get_version(base, {
            'a': clean,
            'b': dirty_same_repo,
            'c': unversioned_same_repo
        }).version, '1, dirty deps, unversioned deps')
        self.assertEqual(base_metadata.get_version(base, {
            'a': clean,
            'b': dirty_same_repo,
            'c': unversioned_same_repo
        }).repo, 'foo')
        with self.assertRaises(ValueError):
            base_metadata.get_version(base, {'a': dirty})
        with self.assertRaises(ValueError):
            base_metadata.get_version(base, {'a': unversioned})

    def test_get_metadata(self) -> None:
        self.assertEqual(base_metadata.get_metadata('foo'), {'docversion': 'foo',
                                                             'subject': 'Version: foo',
                                                             'lang': 'en-GB'})


if __name__ == '__main__':
    unittest.main()
