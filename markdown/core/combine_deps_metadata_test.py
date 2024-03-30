import os
import os.path
from collections.abc import Mapping, Sequence

from markdown.utils import test_utils


class TestCombineDepsMetadata(test_utils.ScriptTestCase):
    def run_script(self, metadata: Sequence[Mapping[str, str]]) -> str:  # type: ignore[override]
        metadata_args = []
        for i, d in enumerate(metadata):
            filename = os.path.join(self.tmpdir(), f"metadata_{i+1}.json")
            self.dump_json(filename, d)
            metadata_args.append(("--metadata_file", f"dep{i+1}", filename))

        out_file = os.path.join(self.tmpdir(), "out.json")

        super().run_script(
            args=[out_file] + [a for sublist in metadata_args for a in sublist],
        )

        return self.load_file(out_file)

    def test_empty(self) -> None:
        self.assertEqual(self.run_script([]), "{}")

    def test_non_empty(self) -> None:
        self.assertEqual(
            self.run_script(
                [
                    {"a": "b", "c": "d"},
                    {"a": "z", "c": "y"},
                ],
            ),
            """{
    "dep1": {
        "a": "b",
        "c": "d"
    },
    "dep2": {
        "a": "z",
        "c": "y"
    }
}""",
        )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
