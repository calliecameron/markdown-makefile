import os
import os.path
import subprocess
import sys
import unittest


SCRIPT = ''


class TestRawVersion(unittest.TestCase):

    def run_script(self, content: str, package: str) -> str:
        test_tmpdir = os.getenv('TEST_TMPDIR')

        in_file = os.path.join(test_tmpdir, 'in.txt')
        with open(in_file, 'w', encoding='utf-8') as f:
            f.write(content)

        out_file = os.path.join(test_tmpdir, 'out.json')

        subprocess.run([
            sys.executable,
            SCRIPT,
            in_file,
            out_file,
            package,
        ], check=True)

        with open(out_file, encoding='utf-8') as f:
            return f.read()

    def test_raw_version(self) -> None:
        self.assertEqual(self.run_script("""STABLE_PANDOC_VERSION 1.2.3
STABLE_VERSION_A_SOLIDUS_B 10
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""", 'a/b'), """{
    "docversion": "10",
    "pandoc_version": "1.2.3",
    "repo": "/foo/.git"
}""")

    def test_raw_version_fails(self) -> None:
        # Missing pandoc version
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script("""STABLE_VERSION_A_SOLIDUS_B 10
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""", 'a/b')

        # Missing version
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script("""STABLE_PANDOC_VERSION 1.2.3
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""", 'a/b')

        # Missing repo
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script("""STABLE_PANDOC_VERSION 1.2.3
STABLE_VERSION_A_SOLIDUS_B 10
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""", 'a/b')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
