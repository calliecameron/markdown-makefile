import os
import os.path
import subprocess
from collections.abc import Mapping, Sequence

import markdown.core.version
from markdown.utils import test_utils


class TestVersion(test_utils.ScriptTestCase):
    def test_version(self) -> None:
        v = markdown.core.version.Version.from_dict(
            {"docversion": "1", "repo": "foo"},
        )
        self.assertEqual(v.version, "1")
        self.assertEqual(v.repo, "foo")
        self.assertEqual(v.to_dict(), {"docversion": "1", "repo": "foo"})

    def test_get_version(self) -> None:
        base = markdown.core.version.Version("1", "foo")
        clean = markdown.core.version.Version("2", "bar")
        dirty = markdown.core.version.Version("3-dirty", "baz")
        unversioned = markdown.core.version.Version("unversioned", "quux")
        dirty_same_repo = markdown.core.version.Version("4-dirty", "foo")
        unversioned_same_repo = markdown.core.version.Version("unversioned", "foo")

        self.assertEqual(
            markdown.core.version.get_version(base, {}, "").version,
            "1",
        )
        self.assertEqual(markdown.core.version.get_version(base, {}, "").repo, "foo")
        self.assertEqual(
            markdown.core.version.get_version(base, {"a": clean}, "").version,
            "1",
        )
        self.assertEqual(
            markdown.core.version.get_version(base, {"a": clean}, "").repo,
            "foo",
        )
        self.assertEqual(
            markdown.core.version.get_version(
                base,
                {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
                "",
            ).version,
            "1, dirty deps, unversioned deps",
        )
        self.assertEqual(
            markdown.core.version.get_version(
                base,
                {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
                "",
            ).repo,
            "foo",
        )
        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": dirty}, "")
        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": unversioned}, "")

        self.assertEqual(
            markdown.core.version.get_version(base, {}, "OVERRIDE").version,
            "OVERRIDE",
        )
        self.assertEqual(
            markdown.core.version.get_version(base, {}, "OVERRIDE").repo,
            "foo",
        )
        self.assertEqual(
            markdown.core.version.get_version(
                base,
                {"a": clean},
                "OVERRIDE",
            ).version,
            "OVERRIDE",
        )
        self.assertEqual(
            markdown.core.version.get_version(base, {"a": clean}, "OVERRIDE").repo,
            "foo",
        )
        self.assertEqual(
            markdown.core.version.get_version(
                base,
                {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
                "OVERRIDE",
            ).version,
            "OVERRIDE",
        )
        self.assertEqual(
            markdown.core.version.get_version(
                base,
                {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
                "OVERRIDE",
            ).repo,
            "foo",
        )
        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": dirty}, "OVERRIDE")
        with self.assertRaises(ValueError):
            markdown.core.version.get_version(base, {"a": unversioned}, "OVERRIDE")

    def test_get_metadata(self) -> None:
        self.assertEqual(
            markdown.core.version.get_metadata("foo", "bar"),
            {
                "docversion": "foo",
                "subject": "Version: foo",
                "repo": "bar",
            },
        )
        self.assertEqual(
            markdown.core.version.get_metadata("foo", "bar"),
            {
                "docversion": "foo",
                "subject": "Version: foo",
                "repo": "bar",
            },
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
            {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
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
            {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
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
            {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
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
                {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
                {
                    "dep1": {"docversion": "2, dirty", "repo": "baz"},
                    "dep2": {"docversion": "3", "repo": "quux"},
                },
                ["--version_override", "override"],
            )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
