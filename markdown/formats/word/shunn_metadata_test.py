import os
import os.path
from collections.abc import Mapping
from typing import Any

from markdown.utils import test_utils


class TestShunnMetadata(test_utils.ScriptTestCase):
    def run_shunn_metadata(self, metadata: Mapping[str, Any]) -> str:
        in_file = os.path.join(self.tmpdir(), "in.json")
        self.dump_json(in_file, metadata)

        out_file = os.path.join(self.tmpdir(), "out.json")

        self.run_script(
            args=[
                in_file,
                out_file,
            ],
        )

        return self.load_file(out_file)

    def test_shunn_metadata(self) -> None:
        self.assertEqual(
            self.run_shunn_metadata(
                {
                    "title": "The Title",
                    "author": ["An Author"],
                    "wordcount": "10",
                    "poetry-lines": "0",
                    "lang": "en-GB",
                    "docversion": "foo",
                    "repo": "bar",
                    "source-hash": "1",
                },
            ),
            """{
    "author_lastname": "Author",
    "contact_address": "`\\\\n`{=tex}",
    "contact_city_state_zip": "`\\\\n`{=tex}",
    "contact_email": "`\\\\n`{=tex}",
    "contact_name": "An Author",
    "contact_phone": "`\\\\n`{=tex}",
    "short_title": "The Title"
}""",
        )

    def test_shunn_metadata_no_title(self) -> None:
        self.assertEqual(
            self.run_shunn_metadata(
                {
                    "author": "An Author",
                    "wordcount": "10",
                    "poetry-lines": "0",
                    "lang": "en-GB",
                    "docversion": "foo",
                    "repo": "bar",
                    "source-hash": "1",
                },
            ),
            """{
    "author_lastname": "Author",
    "contact_address": "`\\\\n`{=tex}",
    "contact_city_state_zip": "`\\\\n`{=tex}",
    "contact_email": "`\\\\n`{=tex}",
    "contact_name": "An Author",
    "contact_phone": "`\\\\n`{=tex}",
    "short_title": "[Untitled]",
    "title": "[Untitled]"
}""",
        )

    def test_shunn_metadata_no_author(self) -> None:
        self.assertEqual(
            self.run_shunn_metadata(
                {
                    "title": "The Title",
                    "wordcount": "10",
                    "poetry-lines": "0",
                    "lang": "en-GB",
                    "docversion": "foo",
                    "repo": "bar",
                    "source-hash": "1",
                },
            ),
            """{
    "author": [
        "[Unknown]"
    ],
    "author_lastname": "[Unknown]",
    "contact_address": "`\\\\n`{=tex}",
    "contact_city_state_zip": "`\\\\n`{=tex}",
    "contact_email": "`\\\\n`{=tex}",
    "contact_name": "[Unknown]",
    "contact_phone": "`\\\\n`{=tex}",
    "short_title": "The Title"
}""",
        )


if __name__ == "__main__":
    test_utils.ScriptTestCase.main()
