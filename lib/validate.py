#!/usr/bin/env python3

from typing import Any, Dict, List
import json
import sys


def validate_str(s: str) -> None:
    if "'" in s or '"' in s:
        sys.stderr.write(
            "Found quotes that weren't converted to smart quotes. Replace them with "
            "backslash-escaped literal curly quotes (“ ” ‘ ’).\n")
        sys.exit(1)


def walk_dict(ast: Dict[str, Any]) -> None:
    if 't' in ast and ast['t'] == 'Str':
        validate_str(ast['c'])
        return
    for _, v in sorted(ast.items()):
        if isinstance(v, list):
            walk_list(v)
        elif isinstance(v, dict):
            walk_dict(v)


def walk_list(ast: List[Any]) -> None:
    for v in ast:
        if isinstance(v, list):
            walk_list(v)
        elif isinstance(v, dict):
            walk_dict(v)


def validate() -> None:
    raw = sys.stdin.read()
    j = json.loads(raw)
    if 'blocks' in j:
        walk_list(j['blocks'])
    if 'meta' in j and 'title' in j['meta']:
        walk_dict(j['meta']['title'])
    sys.stdout.write(raw)


if __name__ == '__main__':
    validate()
