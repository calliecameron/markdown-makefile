import sys

from pymarkdown.main import PyMarkdownLint

out_file = sys.argv[1]
del sys.argv[1]

try:
    PyMarkdownLint().main()
except SystemExit as e:
    if not e.code:
        with open(out_file, mode="w", encoding="utf-8") as f:
            f.write("OK\n")
    raise
