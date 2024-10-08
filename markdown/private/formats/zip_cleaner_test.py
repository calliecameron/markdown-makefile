import os
import os.path
import subprocess

from markdown.private.utils import test_utils


class TestZipCleaner(test_utils.ScriptTestCase):
    def test_zip_cleaner(self) -> None:
        strip_nondeterminism = self.test_args()[0]
        zipinfo = self.test_args()[1]
        zip_command = self.test_args()[2]

        txt_file = os.path.join(self.tmpdir(), "in.txt")
        self.dump_file(txt_file, "foo\n")

        in_file = os.path.join(self.tmpdir(), "in.zip")

        subprocess.run(
            [
                zip_command,
                in_file,
                txt_file,
            ],
            check=True,
        )

        output = subprocess.run(
            [
                zipinfo,
                "-T",
                in_file,
            ],
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertNotIn("19800101", output.stdout)

        out_file = os.path.join(self.tmpdir(), "out.zip")

        self.run_script(
            args=[
                strip_nondeterminism,
                in_file,
                out_file,
            ],
        )

        output = subprocess.run(
            [
                zipinfo,
                "-T",
                out_file,
            ],
            check=True,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertIn("19800101", output.stdout)


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
