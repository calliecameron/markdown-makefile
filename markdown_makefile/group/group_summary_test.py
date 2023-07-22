import json
import os
import os.path
import subprocess
import sys
import unittest
from collections.abc import Sequence

import markdown_makefile.utils.test_utils

# pylint: disable=line-too-long

SCRIPT = ""

DATA = {
    "test1:foo": {
        "title": "Foo",
        "date": "2022",
        "wordcount": "10",
        "poetry-lines": "3",
        "finished": True,
        "docversion": "bar",
        "publications": [
            {
                "venue": "foo",
                "submitted": "2023-05-18",
                "accepted": "2023-05-18",
                "published": "2023-05-18",
            },
        ],
    },
    "test1:bar": {
        "title": "Bar\nbaz",
        "wordcount": "5",
        "poetry-lines": "0",
        "docversion": "quux, dirty",
    },
    "test2:baz": {
        "title": "Baz",
        "date": "from August 2020 to 1 March 2023",
        "wordcount": "20",
        "poetry-lines": "5",
        "finished": False,
        "docversion": "baz",
        "publications": [
            {
                "venue": "baz",
                "submitted": "2023-05-18",
                "rejected": "2023-05-18",
            },
        ],
    },
}


class TestSummary(unittest.TestCase):
    maxDiff = None

    def run_script(self, args: Sequence[str]) -> str:
        test_tmpdir = markdown_makefile.utils.test_utils.tmpdir()
        filename = os.path.join(test_tmpdir, "in.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(DATA, f)

        return subprocess.run(
            [sys.executable, SCRIPT, filename] + list(args),
            check=True,
            capture_output=True,
            encoding="utf-8",
        ).stdout

    def test_summary_pretty(self) -> None:
        self.assertEqual(
            self.run_script([]),
            """
| target    | title    | raw date                         | date                |   wordcount |   poetry lines | finished   | publication   | version     | status   |
|-----------|----------|----------------------------------|---------------------|-------------|----------------|------------|---------------|-------------|----------|
| test1:bar | Bar\\nbaz |                                  |                     |           5 |              0 | no         |               | quux, dirty | DIRTY    |
| test1:foo | Foo      | 2022                             | 2022                |          10 |              3 | yes        | published     | bar         | ok       |
| test2:baz | Baz      | from August 2020 to 1 March 2023 | 2020/08, 2023/03/01 |          20 |              5 | no         | attempted     | baz         | ok       |
""".lstrip(),  # noqa: E501
        )

    def test_summary_raw(self) -> None:
        self.assertEqual(
            self.run_script(["--raw"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--include-target", "test1"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--exclude-target", "test1"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--include-target", "test1", "--exclude-title", "ba.*"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-target"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-target", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-title"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-title", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-raw-date"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-raw-date", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-date"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-date", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-wordcount"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-wordcount", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-poetry-lines"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-poetry-lines", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-finished"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-finished", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-publication"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-publication", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-version"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-version", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-status"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
""",
        )

        self.assertEqual(
            self.run_script(["--raw", "--sort-status", "--reverse"]),
            """target,title,raw date,date,wordcount,poetry lines,finished,publication,version,status
test1:foo,Foo,2022,2022,10,3,yes,published,bar,ok
test2:baz,Baz,from August 2020 to 1 March 2023,"2020/08, 2023/03/01",20,5,no,attempted,baz,ok
test1:bar,Bar\\nbaz,,,5,0,no,,"quux, dirty",DIRTY
""",
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
