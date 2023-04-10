from typing import Dict, List, Tuple
import json
import os
import os.path
import subprocess
import sys
import unittest
import core.base_metadata
import utils.test_utils


SCRIPT = ""


class TestBaseMetadata(unittest.TestCase):
    def test_version(self) -> None:
        v = core.base_metadata.Version.from_dict({"docversion": "1", "repo": "foo"})
        self.assertEqual(v.version, "1")
        self.assertEqual(v.repo, "foo")
        self.assertEqual(v.to_dict(), {"docversion": "1", "repo": "foo"})

    def test_get_version(self) -> None:
        base = core.base_metadata.Version("1", "foo")
        clean = core.base_metadata.Version("2", "bar")
        dirty = core.base_metadata.Version("3-dirty", "baz")
        unversioned = core.base_metadata.Version("unversioned", "quux")
        dirty_same_repo = core.base_metadata.Version("4-dirty", "foo")
        unversioned_same_repo = core.base_metadata.Version("unversioned", "foo")

        self.assertEqual(core.base_metadata.get_version(base, {}, "").version, "1")
        self.assertEqual(core.base_metadata.get_version(base, {}, "").repo, "foo")
        self.assertEqual(core.base_metadata.get_version(base, {"a": clean}, "").version, "1")
        self.assertEqual(core.base_metadata.get_version(base, {"a": clean}, "").repo, "foo")
        self.assertEqual(
            core.base_metadata.get_version(
                base, {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo}, ""
            ).version,
            "1, dirty deps, unversioned deps",
        )
        self.assertEqual(
            core.base_metadata.get_version(
                base, {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo}, ""
            ).repo,
            "foo",
        )
        with self.assertRaises(ValueError):
            core.base_metadata.get_version(base, {"a": dirty}, "")
        with self.assertRaises(ValueError):
            core.base_metadata.get_version(base, {"a": unversioned}, "")

        self.assertEqual(core.base_metadata.get_version(base, {}, "OVERRIDE").version, "OVERRIDE")
        self.assertEqual(core.base_metadata.get_version(base, {}, "OVERRIDE").repo, "foo")
        self.assertEqual(
            core.base_metadata.get_version(base, {"a": clean}, "OVERRIDE").version, "OVERRIDE"
        )
        self.assertEqual(core.base_metadata.get_version(base, {"a": clean}, "OVERRIDE").repo, "foo")
        self.assertEqual(
            core.base_metadata.get_version(
                base, {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo}, "OVERRIDE"
            ).version,
            "OVERRIDE",
        )
        self.assertEqual(
            core.base_metadata.get_version(
                base, {"a": clean, "b": dirty_same_repo, "c": unversioned_same_repo}, "OVERRIDE"
            ).repo,
            "foo",
        )
        with self.assertRaises(ValueError):
            core.base_metadata.get_version(base, {"a": dirty}, "OVERRIDE")
        with self.assertRaises(ValueError):
            core.base_metadata.get_version(base, {"a": unversioned}, "OVERRIDE")

    def test_get_metadata(self) -> None:
        self.assertEqual(
            core.base_metadata.get_metadata("foo", "bar", False),
            {
                "docversion": "foo",
                "subject": "Version: foo",
                "lang": "en-GB",
                "repo": "bar",
                "source-md5": "acbd18db4cc2f85cedef654fccc4a4d8",
            },
        )
        self.assertEqual(
            core.base_metadata.get_metadata("foo", "bar", True),
            {
                "docversion": "foo",
                "subject": "Version: foo",
                "lang": "en-GB",
                "repo": "bar",
                "source-md5": "acbd18db4cc2f85cedef654fccc4a4d8",
                "increment-included-headers": "t",
            },
        )

    def dump_file(self, filename: str, content: Dict[str, str]) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(content, f)

    def load_file(self, filename: str) -> str:
        with open(filename, encoding="utf-8") as f:
            return f.read()

    def run_script(
        self, raw_version: Dict[str, str], deps_versions: List[Dict[str, str]], args: List[str]
    ) -> Tuple[str, str]:
        test_tmpdir = utils.test_utils.tmpdir()

        raw_version_file = os.path.join(test_tmpdir, "raw_version.json")
        self.dump_file(raw_version_file, raw_version)

        dep_version_args = []
        for i, d in enumerate(deps_versions):
            filename = os.path.join(test_tmpdir, f"deps_versions_{i+1}.json")
            self.dump_file(filename, d)
            dep_version_args.append(("--dep_version_file", f"dep{i+1}", filename))

        dep_versions_out_file = os.path.join(test_tmpdir, "dep_versions_out.json")
        metadata_out_file = os.path.join(test_tmpdir, "metadata_out.json")

        subprocess.run(
            [
                sys.executable,
                SCRIPT,
                raw_version_file,
                dep_versions_out_file,
                metadata_out_file,
            ]
            + [a for sublist in dep_version_args for a in sublist]
            + args,
            check=True,
        )

        return (self.load_file(dep_versions_out_file), self.load_file(metadata_out_file))

    def test_main_simple(self) -> None:
        dep_versions_out, metadata_out = self.run_script(
            {"docversion": "foo", "repo": "bar", "pandoc_version": "1"}, [], []
        )

        self.assertEqual(dep_versions_out, "{}")

        self.assertEqual(
            metadata_out,
            """{
    "docversion": "foo",
    "lang": "en-GB",
    "repo": "bar",
    "source-md5": "acbd18db4cc2f85cedef654fccc4a4d8",
    "subject": "Version: foo"
}""",
        )

    def test_main_complex(self) -> None:
        dep_versions_out, metadata_out = self.run_script(
            {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
            [{"docversion": "2, dirty", "repo": "bar"}, {"docversion": "3", "repo": "quux"}],
            ["--increment_included_headers"],
        )

        self.assertEqual(
            dep_versions_out,
            """{
    "dep1": {
        "docversion": "2, dirty",
        "repo": "bar"
    },
    "dep2": {
        "docversion": "3",
        "repo": "quux"
    }
}""",
        )

        self.assertEqual(
            metadata_out,
            """{
    "docversion": "foo, dirty deps",
    "increment-included-headers": "t",
    "lang": "en-GB",
    "repo": "bar",
    "source-md5": "c316fdd35ec401840bfa345dd973f89e",
    "subject": "Version: foo, dirty deps"
}""",
        )

    def test_main_override(self) -> None:
        deps_versions_out, metadata_out = self.run_script(
            {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
            [{"docversion": "2, dirty", "repo": "bar"}, {"docversion": "3", "repo": "quux"}],
            ["--increment_included_headers", "--version_override", "override"],
        )

        self.assertEqual(
            deps_versions_out,
            """{
    "dep1": {
        "docversion": "2, dirty",
        "repo": "bar"
    },
    "dep2": {
        "docversion": "3",
        "repo": "quux"
    }
}""",
        )

        self.assertEqual(
            metadata_out,
            """{
    "docversion": "override",
    "increment-included-headers": "t",
    "lang": "en-GB",
    "repo": "bar",
    "source-md5": "e3b3f56615d1e5f2608d2f1130a7ef54",
    "subject": "Version: override"
}""",
        )

    def test_main_fails(self) -> None:
        with self.assertRaises(subprocess.CalledProcessError):
            self.run_script(
                {"docversion": "foo", "repo": "bar", "pandoc_version": "1"},
                [{"docversion": "2, dirty", "repo": "baz"}, {"docversion": "3", "repo": "quux"}],
                ["--increment_included_headers", "--version_override", "override"],
            )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
