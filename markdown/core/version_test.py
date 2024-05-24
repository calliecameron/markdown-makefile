import os
import os.path
import subprocess
from collections.abc import Mapping, Sequence

import markdown.core.version
from markdown.utils import test_utils
from markdown.utils.metadata import Version, VersionMetadata


class TestVersion(test_utils.ScriptTestCase):
    def test_get_version(self) -> None:
        base = Version(docversion="1", repo="foo")
        clean = Version(docversion="2", repo="bar")
        dirty = Version(docversion="3-dirty", repo="baz")
        unversioned = Version(docversion="unversioned", repo="quux")
        dirty_same_repo = Version(docversion="4-dirty", repo="foo")
        unversioned_same_repo = Version(docversion="unversioned", repo="foo")

        v = markdown.core.version.get_version(base, {}, "")
        self.assertEqual(v.docversion, "1")
        self.assertEqual(v.repo, "foo")

        v = markdown.core.version.get_version(base, {"a": clean}, "")
        self.assertEqual(v.docversion, "1")
        self.assertEqual(v.repo, "foo")

        v = markdown.core.version.get_version(
            base,
            {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
            "",
        )
        self.assertEqual(v.docversion, "1, dirty deps, unversioned deps")
        self.assertEqual(v.repo, "foo")

        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": dirty}, "")
        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": unversioned}, "")

        v = markdown.core.version.get_version(base, {}, "OVERRIDE")
        self.assertEqual(v.docversion, "OVERRIDE")
        self.assertEqual(v.repo, "foo")

        v = markdown.core.version.get_version(base, {"a": clean}, "OVERRIDE")
        self.assertEqual(v.docversion, "OVERRIDE")
        self.assertEqual(v.repo, "foo")

        v = markdown.core.version.get_version(
            base,
            {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
            "OVERRIDE",
        )
        self.assertEqual(v.docversion, "OVERRIDE")
        self.assertEqual(v.repo, "foo")

        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": dirty}, "OVERRIDE")
        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": unversioned}, "OVERRIDE")

    def test_get_metadata(self) -> None:
        self.assertEqual(
            markdown.core.version.get_metadata(Version(docversion="foo", repo="bar")),
            VersionMetadata(docversion="foo", repo="bar", subject="Version: foo"),
        )

    def run_script(  # type: ignore[override]
        self,
        raw_version: Mapping[str, str],
        deps_metadata: Mapping[str, Mapping[str, str]],
        args: Sequence[str],
    ) -> str:
        raw_version_file = os.path.join(self.tmpdir(), "raw_version.json")
        self.dump_json(raw_version_file, raw_version)

        deps_metadata_file = os.path.join(self.tmpdir(), "deps_metadata.json")
        self.dump_json(deps_metadata_file, deps_metadata)

        metadata_out_file = os.path.join(self.tmpdir(), "metadata_out.json")

        super().run_script(
            args=[
                raw_version_file,
                deps_metadata_file,
                metadata_out_file,
                *args,
            ],
        )

        return self.load_file(metadata_out_file)

    def test_main_simple(self) -> None:
        metadata_out = self.run_script(
            {"docversion": "foo", "repo": "bar"},
            {},
            [],
        )

        self.assertEqual(
            metadata_out,
            """{
    "docversion": "foo",
    "repo": "bar",
    "subject": "Version: foo"
}""",
        )

    def test_main_complex(self) -> None:
        metadata_out = self.run_script(
            {"docversion": "foo", "repo": "bar"},
            {
                "dep1": {"docversion": "2, dirty", "repo": "bar"},
                "dep2": {"docversion": "3", "repo": "quux"},
            },
            [],
        )

        self.assertEqual(
            metadata_out,
            """{
    "docversion": "foo, dirty deps",
    "repo": "bar",
    "subject": "Version: foo, dirty deps"
}""",
        )

    def test_main_override(self) -> None:
        metadata_out = self.run_script(
            {"docversion": "foo", "repo": "bar"},
            {
                "dep1": {"docversion": "2, dirty", "repo": "bar"},
                "dep2": {"docversion": "3", "repo": "quux"},
            },
            ["--version_override", "override"],
        )

        self.assertEqual(
            metadata_out,
            """{
    "docversion": "override",
    "repo": "bar",
    "subject": "Version: override"
}""",
        )

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script(
                {"docversion": "foo", "repo": "bar"},
                {
                    "dep1": {"docversion": "2, dirty", "repo": "baz"},
                    "dep2": {"docversion": "3", "repo": "quux"},
                },
                ["--version_override", "override"],
            )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
