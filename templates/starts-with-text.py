#!/usr/bin/env python3

import json
import sys

ast = json.loads(sys.stdin.read())

if ('blocks' in ast and
    ast['blocks'] and
    't' in ast['blocks'][0] and
    ast['blocks'][0]['t'] != 'Header'):
    print('t')
