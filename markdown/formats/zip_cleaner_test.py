import os
import os.path
import subprocess

from markdown.utils import test_utils


class TestZipCleaner(test_utils.ScriptTestCase):
    def test_zip_cleaner(self) -> None:
        txt_file = os.path.join(self.tmpdir(), "in.txt")
        self.dump_file(txt_file, "foo\n")

        in_file = os.path.join(self.tmpdir(), "in.zip")

        subprocess.run(
            [
                "zip",
                in_file,
                txt_file,
            ],
            check=True,
        )

        output = subprocess.run(
            [
                "zipinfo",
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
                in_file,
                out_file,
            ],
        )

        output = subprocess.run(
            [
                "zipinfo",
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
