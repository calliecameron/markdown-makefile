#!/usr/bin/env python3

from typing import Any, Dict, List
import datetime
import json
import sys

STR_KEYS = [
    'venue',
    'paid',
    'note',
]

DATE_KEYS = [
    'submitted',
    'rejected',
    'withdrawn',
    'accepted',
    'published',
]

KEYS = frozenset(
    STR_KEYS + DATE_KEYS + ['urls']
)


def fail(msg: str) -> None:
    sys.stderr.write('ERROR: ' + msg)
    sys.exit(1)


def validate_str(s: str) -> None:
    if "'" in s or '"' in s:
        fail(
            "markdown parsing failed\n\n"
            "Found quotes that weren't converted to smart quotes. Replace them with "
            "backslash-escaped literal curly quotes (“ ” ‘ ’).\n")


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


def validate_text(j: Dict[str, Any]) -> None:
    if 'blocks' in j:
        walk_list(j['blocks'])
    if 'meta' in j and 'title' in j['meta']:
        walk_dict(j['meta']['title'])


def validate_publications(j: Dict[str, Any]) -> None:
    if 'meta' not in j or 'publications' not in j['meta']:
        return
    ps = j['meta']['publications']
    if ps['t'] != 'MetaList':
        fail("invalid metadata: 'publications' must be a list")
    for p in ps['c']:
        if p['t'] != 'MetaMap':
            fail("invalid metadata: item in 'publbications' must be a dict")
        data = p['c']
        keys = frozenset(data.keys())
        if not keys.issubset(KEYS):
            fail("invalid metadata: unknown keys %s in 'publications' item" % (keys - KEYS))

        for k in sorted(STR_KEYS):
            if k in data:
                if data[k]['t'] != 'MetaInlines':
                    fail("invalid metadata: '%s' in 'publications' item must be a string" % k)

        for k in sorted(DATE_KEYS):
            if k in data:
                if (data[k]['t'] != 'MetaInlines' or
                    len(data[k]['c']) != 1 or
                        data[k]['c'][0]['t'] != 'Str'):
                    fail("invalid metadata: '%s' in 'publications' item must be a string" % k)
                v = data[k]['c'][0]['c']
                try:
                    datetime.date.fromisoformat(v)
                except ValueError:
                    fail(
                        "invalid metadata: '%s' in 'publications' item must be a date; got '%s'" %
                        (k, v))

        if 'urls' in data:
            urls = data['urls']
            if urls['t'] != 'MetaList':
                fail("invalid metadata: 'urls' in 'publications' item must be a list")
            for url in urls['c']:
                if url['t'] != 'MetaInlines':
                    fail("invalid metadata: 'urls' item in 'publications' item must be a string")

        keys = frozenset(data.keys())
        if len(keys & frozenset(['accepted', 'rejected', 'withdrawn'])) > 1:
            fail("invalid metadata: 'accepted', 'rejected' and 'withdrawn' in 'publications' item "
                 "are mutually exclusive")

        if ('rejected' in keys or 'withdrawn' in keys) and 'published' in keys:
            fail("invalid metadata: 'published' cannot be specified for publication items that "
                 "were rejected or withdrawn")


def validate() -> None:
    raw = sys.stdin.read()
    j = json.loads(raw)
    validate_text(j)
    validate_publications(j)
    sys.stdout.write(raw)


if __name__ == '__main__':
    validate()
