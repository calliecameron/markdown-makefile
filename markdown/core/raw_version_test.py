import os
import os.path
import subprocess

from markdown.utils import test_utils


class TestRawVersion(test_utils.ScriptTestCase):
    def run_script(self, content: str, package: str) -> str:  # type: ignore[override]
        in_file = os.path.join(self.tmpdir(), "in.txt")
        self.dump_file(in_file, content)

        out_file = os.path.join(self.tmpdir(), "out.json")

        super().run_script(
            args=[
                in_file,
                out_file,
                package,
            ],
        )

        return self.load_file(out_file)

    def test_raw_version(self) -> None:
        self.assertEqual(
            self.run_script(
                """STABLE_VERSION_A_SOLIDUS_B 10
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""",
                "a/b",
            ),
            """{
    "repo": "/foo/.git",
    "version": "10"
}""",
        )

    def test_raw_version_root_package(self) -> None:
        self.assertEqual(
            self.run_script(
                """STABLE_VERSION_ 10
STABLE_REPO_ /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""",
                "",
            ),
            """{
    "repo": "/foo/.git",
    "version": "10"
}""",
        )

    def test_raw_version_fails(self) -> None:
        # Missing version
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script(
                """STABLE_PANDOC_VERSION 1.2.3
STABLE_REPO_A_SOLIDUS_B /foo/.git
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""",
                "a/b",
            )

        # Missing repo
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script(
                """STABLE_PANDOC_VERSION 1.2.3
STABLE_VERSION_A_SOLIDUS_B 10
STABLE_VERSION_B 11
STABLE_REPO_B /bar/.git
""",
                "a/b",
            )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
