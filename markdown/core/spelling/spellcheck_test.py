import os
import os.path
import subprocess
from collections.abc import Sequence

from markdown.utils import test_utils

DOC = """The Title

Test text baz Quux shouldn’t fail
"""  # noqa: RUF001


class TestWriteDictionary(test_utils.ScriptTestCase):
    def run_spellcheck(self, doc: str, dictionary: Sequence[str]) -> str:
        in_file = os.path.join(self.tmpdir(), "in.md")
        self.dump_file(in_file, doc)

        dict_file = os.path.join(self.tmpdir(), "in.dic")
        self.dump_file(dict_file, "\n".join(dictionary) + "\n")

        out_file = os.path.join(self.tmpdir(), "out.txt")

        self.run_script(
            args=[
                dict_file,
                in_file,
                out_file,
                "en_GB",
            ],
        )

        return self.load_file(out_file)

    def test_spellcheck(self) -> None:
        self.assertEqual(self.run_spellcheck(DOC, ["baz", "Quux"]), "OK\n")

    def test_spellcheck_fails(self) -> None:
        try:
            self.run_spellcheck(DOC, [])
            self.fail()
        except subprocess.CalledProcessError as e:
            self.assertEqual(
                e.stderr,
                """ERROR: found misspelled words; correct them or add them to the dictionary:

baz
Quux

""",
            )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
