import os
import os.path

from markdown.utils import test_utils


class TestGenDictionary(test_utils.ScriptTestCase):
    def test_gen_dictionary(self) -> None:
        in_file_1 = os.path.join(self.tmpdir(), "in1.dic")
        self.dump_file(in_file_1, "foo\nbar\n")

        in_file_2 = os.path.join(self.tmpdir(), "in2.dic")
        self.dump_file(in_file_2, "foo\nbaz\n")

        out_file = os.path.join(self.tmpdir(), "out.dic")

        self.run_script(
            args=[
                out_file,
                in_file_1,
                in_file_2,
            ],
        )

        self.assertEqual(self.load_file(out_file), "bar\nbaz\nfoo\n")


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
