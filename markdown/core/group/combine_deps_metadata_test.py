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
                    {
                        "wordcount": "10",
                        "poetry-lines": "0",
                        "lang": "en-GB",
                        "docversion": "foo",
                        "repo": "bar",
                        "source-hash": "quux",
                    },
                    {
                        "wordcount": "20",
                        "poetry-lines": "10",
                        "lang": "en-US",
                        "docversion": "blah",
                        "repo": "yay",
                        "source-hash": "yay2",
                    },
                ],
            ),
            """{
    "dep1": {
        "docversion": "foo",
        "lang": "en-GB",
        "poetry-lines": 0,
        "repo": "bar",
        "source-hash": "quux",
        "wordcount": 10
    },
    "dep2": {
        "docversion": "blah",
        "lang": "en-US",
        "poetry-lines": 10,
        "repo": "yay",
        "source-hash": "yay2",
        "wordcount": 20
    }
}""",
        )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
