from typing import Any, Dict
import json
import os
import os.path
import subprocess
import sys
import unittest
import utils.test_utils

# pylint: disable=line-too-long

SCRIPT = ''


class TestPublications(unittest.TestCase):

    def dump_file(self, filename: str, content: Dict[str, Any]) -> None:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content, f)

    def test_publications(self) -> None:
        test_tmpdir = utils.test_utils.tmpdir()

        metadata1 = os.path.join(test_tmpdir, 'metadata1.json')
        self.dump_file(
            metadata1,
            {
                'title': 'Foo <Bar>',
                'wordcount': '10',
                'docversion': 'bar',
                'publications': [
                    {
                        'venue': 'Foo',
                        'submitted': '2022-12-13',
                        'published': '2022-12-14',
                    },
                    {
                        'venue': 'Bar',
                        'submitted': '2022-10-13',
                        'rejected': '2022-10-14',
                    },
                ]
            })

        metadata2 = os.path.join(test_tmpdir, 'metadata2.json')
        self.dump_file(
            metadata2,
            {
                'title': 'Baz',
                'wordcount': '20',
                'docversion': 'quux, dirty',
                'publications': [
                    {
                        'venue': 'Foo',
                        'submitted': '2022-11-13',
                        'self-published': '2022-11-14',
                    },
                ]
            })

        outfile = os.path.join(test_tmpdir, "out.html")

        subprocess.run([
            sys.executable,
            SCRIPT,
            outfile,
            '--dep',
            '//foo:bar',
            metadata1,
            '--dep',
            '//baz:quux',
            metadata2
        ], check=True)

        with open(outfile, encoding='utf-8') as f:
            self.assertEqual(
                f.read(),
                """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Publications</title>
<style>
table { border-collapse: collapse; }
th, td { border: 1px solid; padding: 5px; }
.submitted { background-color: #ffff00; }
.rejected { background-color: #ff6d6d; }
.withdrawn { background-color: #ff972f; }
.accepted { background-color: #729fcf; }
.self-published { background-color: #158466; }
.published { background-color: #81d41a; }
</style>
</head>
<body>
<h1>Publications</h1>
<table>
<thead>
<tr>
<th>Target</th>
<th>Title</th>
<th>Wordcount</th>
<th style="border-right: 3px solid">Notes</th>
<th>Bar</th>
<th>Foo</th>
</tr>
</thead>
<tbody>
<tr>
<td>//baz:quux</td>
<td>Baz</td>
<td>20</td>
<td style="border-right: 3px solid"></td>
<td></td>
<td class="self-published" title="//baz:quux, Foo">2022-11-13 Submitted<br>2022-11-14 Self-published</td>
</tr>
<tr>
<td>//foo:bar</td>
<td>Foo &lt;Bar&gt;</td>
<td>10</td>
<td style="border-right: 3px solid"></td>
<td class="rejected" title="//foo:bar, Bar">2022-10-13 Submitted<br>2022-10-14 Rejected</td>
<td class="published" title="//foo:bar, Foo">2022-12-13 Submitted<br>2022-12-14 Published</td>
</tr>
</tbody>
</table>
<h2>Details</h2>
<h3>//baz:quux</h3>
<code><pre>{
    "docversion": "quux, dirty",
    "publications": [
        {
            "self-published": "2022-11-14",
            "submitted": "2022-11-13",
            "venue": "Foo"
        }
    ],
    "title": "Baz",
    "wordcount": "20"
}</pre></code>
<h3>//foo:bar</h3>
<code><pre>{
    "docversion": "bar",
    "publications": [
        {
            "published": "2022-12-14",
            "submitted": "2022-12-13",
            "venue": "Foo"
        },
        {
            "rejected": "2022-10-14",
            "submitted": "2022-10-13",
            "venue": "Bar"
        }
    ],
    "title": "Foo &lt;Bar&gt;",
    "wordcount": "10"
}</pre></code>
</body>
</html>
""")  # noqa: E501


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Not enough args')
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
