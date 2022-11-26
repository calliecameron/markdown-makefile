import sys
from mypy import api

result = api.run(sys.argv[1:])  # pylint: disable=c-extension-no-member

if result[0]:
    print('\nType checking report:\n')
    print(result[0])

if result[1]:
    print('\nError report:\n')
    print(result[1])

print('\nExit status:', result[2])

sys.exit(result[2])
