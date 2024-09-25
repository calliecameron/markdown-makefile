import os
import os.path
import subprocess
from collections.abc import Mapping, Sequence

from markdown.private.core.version import get_version
from markdown.private.utils import test_utils
from markdown.private.utils.metadata import Version


class TestVersion(test_utils.ScriptTestCase):
    def test_get_version(self) -> None:
        base = Version(version="1", repo="foo")
        clean = Version(version="2", repo="bar")
        dirty = Version(version="3-dirty", repo="baz")
        unversioned = Version(version="unversioned", repo="quux")
        dirty_same_repo = Version(version="4-dirty", repo="foo")
        unversioned_same_repo = Version(version="unversioned", repo="foo")

        v = get_version(base, {}, "", "")
        self.assertEqual(v.version, "1")
        self.assertEqual(v.repo, "foo")

        v = get_version(base, {"a": clean}, "", "")
        self.assertEqual(v.version, "1")
        self.assertEqual(v.repo, "foo")

        v = get_version(
            base,
            {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
            "",
            "",
        )
        self.assertEqual(v.version, "1, dirty deps, unversioned deps")
        self.assertEqual(v.repo, "foo")

        with self.assertRaises(ValueError):
            get_version(base, {"a": dirty}, "", "")
        with self.assertRaises(ValueError):
            get_version(base, {"a": unversioned}, "", "")

        v = get_version(base, {}, "OVERRIDE", "")
        self.assertEqual(v.version, "OVERRIDE")
        self.assertEqual(v.repo, "foo")

        v = get_version(base, {"a": clean}, "OVERRIDE", "")
        self.assertEqual(v.version, "OVERRIDE")
        self.assertEqual(v.repo, "foo")

        v = get_version(
            base,
            {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo},
            "OVERRIDE",
            "",
        )
        self.assertEqual(v.version, "OVERRIDE")
        self.assertEqual(v.repo, "foo")

        v = get_version(base, {}, "", "OVERRIDE")
        self.assertEqual(v.version, "1")
        self.assertEqual(v.repo, "OVERRIDE")

        with self.assertRaises(ValueError):
            get_version(base, {"a": dirty}, "OVERRIDE", "OVERRIDE")
        with self.assertRaises(ValueError):
            get_version(base, {"a": unversioned}, "OVERRIDE", "OVERRIDE")

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
            {"version": "foo", "repo": "bar"},
            {},
            [],
        )

        self.assertEqual(
            metadata_out,
            """{
    "repo": "bar",
    "version": "foo"
}""",
        )

    def test_main_complex(self) -> None:
        metadata_out = self.run_script(
            {"version": "foo", "repo": "bar"},
            {
                "dep1": {"version": "2, dirty", "repo": "bar"},
                "dep2": {"version": "3", "repo": "quux"},
            },
            [],
        )

        self.assertEqual(
            metadata_out,
            """{
    "repo": "bar",
    "version": "foo, dirty deps"
}""",
        )

    def test_main_version_override(self) -> None:
        metadata_out = self.run_script(
            {"version": "foo", "repo": "bar"},
            {
                "dep1": {"version": "2, dirty", "repo": "bar"},
                "dep2": {"version": "3", "repo": "quux"},
            },
            ["--version_override", "override"],
        )

        self.assertEqual(
            metadata_out,
            """{
    "repo": "bar",
    "version": "override"
}""",
        )

    def test_main_repo_override(self) -> None:
        metadata_out = self.run_script(
            {"version": "foo", "repo": "bar"},
            {
                "dep1": {"version": "2, dirty", "repo": "bar"},
                "dep2": {"version": "3", "repo": "quux"},
            },
            ["--repo_override", "override"],
        )

        self.assertEqual(
            metadata_out,
            """{
    "repo": "override",
    "version": "foo, dirty deps"
}""",
        )

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script(
                {"version": "foo", "repo": "bar"},
                {
                    "dep1": {"version": "2, dirty", "repo": "baz"},
                    "dep2": {"version": "3", "repo": "quux"},
                },
                ["--version_override", "override"],
            )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
