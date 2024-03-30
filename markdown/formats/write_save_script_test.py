import os
import os.path

from markdown.utils import test_utils


class TestWriteSaveScript(test_utils.ScriptTestCase):
    def run_script(self, package: str) -> str:  # type: ignore[override]
        out_file = os.path.join(self.tmpdir(), "out.sh")

        super().run_script(
            args=[
                out_file,
                package,
            ],
        )

        with open(out_file, encoding="utf-8") as f:
            return f.read()

    def test_write_save_script(self) -> None:
        self.assertEqual(
            self.run_script("foo"),
            """#!/bin/bash

set -eu

OUTPUT_DIR="foo/output"
SAVE_DIR="${BUILD_WORKSPACE_DIRECTORY}/foo/saved"

mkdir -p "${SAVE_DIR}"
cd "${OUTPUT_DIR}"
cp -t "${SAVE_DIR}" *
cd "${SAVE_DIR}"
chmod u=rw,go= *
""",
        )

    def test_write_save_script_root_package(self) -> None:
        self.assertEqual(
            self.run_script(""),
            """#!/bin/bash

set -eu

OUTPUT_DIR="output"
SAVE_DIR="${BUILD_WORKSPACE_DIRECTORY}/saved"

mkdir -p "${SAVE_DIR}"
cd "${OUTPUT_DIR}"
cp -t "${SAVE_DIR}" *
cd "${SAVE_DIR}"
chmod u=rw,go= *
""",
        )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
