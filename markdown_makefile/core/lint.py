import sys
from pymarkdown.main import PyMarkdownLint  # type: ignore

out_file = sys.argv[1]
del sys.argv[1]

PyMarkdownLint().main()

with open(out_file, mode="w", encoding="utf-8") as f:
    f.write("OK\n")
