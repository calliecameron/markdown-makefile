import sys
from pdfminer.high_level import extract_text

print(extract_text(sys.argv[1]))
