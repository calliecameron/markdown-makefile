import json
import os
import os.path
import subprocess
import sys
import unittest
import markdown_makefile.utils.test_utils


SCRIPT = ""

DATA = {
    "test1:foo": {
        "title": "Foo",
        "date": "A",
        "wordcount": "10",
        "docversion": "bar",
    },
    "test1:bar": {
        "title": "Bar\nbaz",
        "wordcount": "5",
        "docversion": "quux, dirty",
    },
    "test2:baz": {
        "title": "Baz",
        "date": "C",
        "wordcount": "20",
        "docversion": "baz",
    },
}


class TestSummary(unittest.TestCase):
    maxDiff = None

    def run_script(self, filter_arg: str, raw: bool, wordcount: bool) -> str:
        test_tmpdir = markdown_makefile.utils.test_utils.tmpdir()
        filename = os.path.join(test_tmpdir, "in.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(DATA, f)

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
            """| target    | title    | date   |   wordcount | version     | status   |
|-----------|----------|--------|-------------|-------------|----------|
| test1:bar | Bar\\nbaz |        |           5 | quux, dirty | DIRTY    |
| test1:foo | Foo      | A      |          10 | bar         | ok       |
| test2:baz | Baz      | C      |          20 | baz         | ok       |
""",
        )

        self.assertEqual(
            self.run_script("", raw=False, wordcount=True),
            """| target    | title    | date   |   wordcount | version     | status   |
|-----------|----------|--------|-------------|-------------|----------|
| test2:baz | Baz      | C      |          20 | baz         | ok       |
| test1:foo | Foo      | A      |          10 | bar         | ok       |
| test1:bar | Bar\\nbaz |        |           5 | quux, dirty | DIRTY    |
""",
        )

        self.assertEqual(
            self.run_script("", raw=True, wordcount=False),
            """target,title,date,wordcount,version,status
test1:bar,Bar\\nbaz,,5,"quux, dirty",DIRTY
test1:foo,Foo,A,10,bar,ok
test2:baz,Baz,C,20,baz,ok
""",
        )
        self.assertEqual(
            self.run_script("", raw=True, wordcount=True),
            """target,title,date,wordcount,version,status
test2:baz,Baz,C,20,baz,ok
test1:foo,Foo,A,10,bar,ok
test1:bar,Bar\\nbaz,,5,"quux, dirty",DIRTY
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=False, wordcount=False),
            """| target    | title    | date   |   wordcount | version     | status   |
|-----------|----------|--------|-------------|-------------|----------|
| test1:bar | Bar\\nbaz |        |           5 | quux, dirty | DIRTY    |
| test1:foo | Foo      | A      |          10 | bar         | ok       |
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=False, wordcount=True),
            """| target    | title    | date   |   wordcount | version     | status   |
|-----------|----------|--------|-------------|-------------|----------|
| test1:foo | Foo      | A      |          10 | bar         | ok       |
| test1:bar | Bar\\nbaz |        |           5 | quux, dirty | DIRTY    |
""",
        )

        self.assertEqual(
            self.run_script("test1", raw=True, wordcount=False),
            """target,title,date,wordcount,version,status
test1:bar,Bar\\nbaz,,5,"quux, dirty",DIRTY
test1:foo,Foo,A,10,bar,ok
""",
        )
        self.assertEqual(
            self.run_script("test1", raw=True, wordcount=True),
            """target,title,date,wordcount,version,status
test1:foo,Foo,A,10,bar,ok
test1:bar,Bar\\nbaz,,5,"quux, dirty",DIRTY
""",
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Not enough args")
    SCRIPT = sys.argv[1]
    del sys.argv[1]
    unittest.main()
