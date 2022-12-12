#!/usr/bin/env python3

from typing import Any, Dict, List
import datetime
import json
import sys

PUBLICATION_STR_KEYS = [
    'venue',
    'paid',
    'notes',
]

PUBLICATION_DATE_KEYS = [
    'submitted',
    'rejected',
    'withdrawn',
    'accepted',
    'published',
]

PUBLICATION_KEYS = frozenset(
    PUBLICATION_STR_KEYS + PUBLICATION_DATE_KEYS + ['urls']
)


def fail(msg: str) -> None:
    sys.stderr.write('ERROR: ' + msg)
    sys.exit(1)


def fail_metadata(msg: str) -> None:
    fail('invalid metadata: ' + msg)


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


def assert_is_list(j: Dict[str, Any], msg: str) -> None:
    if j['t'] != 'MetaList':
        fail_metadata(msg)


def assert_is_dict(j: Dict[str, Any], msg: str) -> None:
    if j['t'] != 'MetaMap':
        fail_metadata(msg)


def assert_is_string(j: Dict[str, Any], msg: str) -> None:
    if j['t'] != 'MetaInlines':
        fail_metadata(msg)


def validate_publications(j: Dict[str, Any]) -> None:
    if 'meta' not in j or 'publications' not in j['meta']:
        return
    ps = j['meta']['publications']
    assert_is_list(ps, "'publications' must be a list")
    for p in ps['c']:
        assert_is_dict(p, "item in 'publbications' must be a dict")
        data = p['c']
        keys = frozenset(data.keys())
        if not keys.issubset(PUBLICATION_KEYS):
            fail_metadata("unknown keys %s in 'publications' item" % (keys - PUBLICATION_KEYS))

        for k in sorted(PUBLICATION_STR_KEYS):
            if k in data:
                assert_is_string(data[k], "'%s' in 'publications' item must be a string" % k)

        for k in sorted(PUBLICATION_DATE_KEYS):
            if k in data:
                if (data[k]['t'] != 'MetaInlines' or
                    len(data[k]['c']) != 1 or
                        data[k]['c'][0]['t'] != 'Str'):
                    fail_metadata("'%s' in 'publications' item must be a string" % k)
                v = data[k]['c'][0]['c']
                try:
                    datetime.date.fromisoformat(v)
                except ValueError:
                    fail_metadata("'%s' in 'publications' item must be a date; got '%s'" % (k, v))

        if 'urls' in data:
            urls = data['urls']
            assert_is_list(urls, "'urls' in 'publications' item must be a list")
            for url in urls['c']:
                assert_is_string(url, "'urls' item in 'publications' item must be a string")

        keys = frozenset(data.keys())
        if len(keys & frozenset(['accepted', 'rejected', 'withdrawn'])) > 1:
            fail_metadata("'accepted', 'rejected' and 'withdrawn' in 'publications' item "
                          "are mutually exclusive")

        if ('rejected' in keys or 'withdrawn' in keys) and 'published' in keys:
            fail_metadata("'published' cannot be specified for publication items that "
                          "were rejected or withdrawn")


def validate() -> None:
    raw = sys.stdin.read()
    j = json.loads(raw)
    validate_text(j)
    validate_publications(j)
    sys.stdout.write(raw)


if __name__ == '__main__':
    validate()
