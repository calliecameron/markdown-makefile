import csv
import os
import os.path
import subprocess
import sys
import unittest
import utils.test_utils


SCRIPT = ""

DATA = [
    {
        "target": "test1:foo",
        "title": "Foo",
        "date": "A",
        "wordcount": "10",
        "version": "1",
        "status": "ok",
    },
    {
        "target": "test1:bar",
        "title": "Bar",
        "date": "B",
        "wordcount": "5",
        "version": "2",
        "status": "bad",
    },
    {
        "target": "test2:baz",
        "title": "Baz",
        "date": "C",
        "wordcount": "20",
        "version": "3",
        "status": "ok",
    },
]


class TestSummaryPrint(unittest.TestCase):
    def run_script(self, filter_arg: str, raw: bool, wordcount: bool) -> str:
        test_tmpdir = utils.test_utils.tmpdir()
        filename = os.path.join(test_tmpdir, "in.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f, ["target", "title", "date", "wordcount", "version", "status"]
            )
            writer.writeheader()
            writer.writerows(DATA)

        args = [sys.executable, SCRIPT, filename]
        if filter_arg:
            args += ["--filter", filter_arg]
        if raw:
            args.append("--raw")
        if wordcount:
            args.append("--wordcount")

        return subprocess.run(
            args,
            check=True,
            capture_output=True,
            encoding="utf-8",
        ).stdout

    def test_summary_print(self) -> None:
        self.assertEqual(
            self.run_script("", raw=False, wordcount=False),
            """| target    | title   | date   |   wordcount |   version | status   |
|-----------|---------|--------|-------------|-----------|----------|
| test1:foo | Foo     | A      |          10 |         1 | ok       |
| test1:bar | Bar     | B      |           5 |         2 | bad      |
| test2:baz | Baz     | C      |          20 |         3 | ok       |
""",
        )
        self.assertEqual(
            self.run_script("", raw=False, wordcount=True),
            """| target    | title   | date   |   wordcount |   version | status   |
|-----------|---------|--------|-------------|-----------|----------|
| test2:baz | Baz     | C      |          20 |         3 | ok       |
| test1:foo | Foo     | A      |          10 |         1 | ok       |
| test1:bar | Bar     | B      |           5 |         2 | bad      |
""",
        )
        self.assertEqual(
            self.run_script("", raw=True, wordcount=False),
            """target,title,date,wordcount,version,status
test1:foo,Foo,A,10,1,ok
test1:bar,Bar,B,5,2,bad
test2:baz,Baz,C,20,3,ok
""",
        )
        self.assertEqual(
            self.run_script("", raw=True, wordcount=True),
            """target,title,date,wordcount,version,status
test2:baz,Baz,C,20,3,ok
test1:foo,Foo,A,10,1,ok
test1:bar,Bar,B,5,2,bad
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=False, wordcount=False),
            """| target    | title   | date   |   wordcount |   version | status   |
|-----------|---------|--------|-------------|-----------|----------|
| test1:foo | Foo     | A      |          10 |         1 | ok       |
| test1:bar | Bar     | B      |           5 |         2 | bad      |
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=False, wordcount=True),
            """| target    | title   | date   |   wordcount |   version | status   |
|-----------|---------|--------|-------------|-----------|----------|
| test1:foo | Foo     | A      |          10 |         1 | ok       |
| test1:bar | Bar     | B      |           5 |         2 | bad      |
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=True, wordcount=False),
            """target,title,date,wordcount,version,status
test1:foo,Foo,A,10,1,ok
test1:bar,Bar,B,5,2,bad
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=True, wordcount=True),
            """target,title,date,wordcount,version,status
test1:foo,Foo,A,10,1,ok
test1:bar,Bar,B,5,2,bad
""",
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
