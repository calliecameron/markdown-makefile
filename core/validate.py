#!/usr/bin/env python3

from typing import Any, Dict, FrozenSet, List
import datetime
import json
import sys

VENUE = 'venue'
PAID = 'paid'
NOTES = 'notes'
SUBMITTED = 'submitted'
REJECTED = 'rejected'
WITHDRAWN = 'withdrawn'
SELF_PUBLISHED = 'self-published'
ACCEPTED = 'accepted'
PUBLISHED = 'published'
URLS = 'urls'

PUBLICATION_STR_KEYS = [
    VENUE,
    PAID,
    NOTES,
]

PUBLICATION_DATE_KEYS = [
    SUBMITTED,
    REJECTED,
    WITHDRAWN,
    SELF_PUBLISHED,
    ACCEPTED,
    PUBLISHED,
]

PUBLICATION_KEYS = frozenset(
    PUBLICATION_STR_KEYS + PUBLICATION_DATE_KEYS + [URLS]
)


def fail(msg: str) -> None:
    sys.stderr.write('ERROR: ' + msg)
    sys.exit(1)


def fail_metadata(msg: str) -> None:
    fail('invalid metadata: ' + msg)


def validate_str(s: str) -> None:
    if "'" in s or '"' in s:
        fail(
            ("markdown parsing failed: '%s'\n\n"
             "Found quotes that weren't converted to smart quotes. Replace them with "
             "backslash-escaped literal curly quotes (“ ” ‘ ’).\n") % s)


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


def assert_no_conflicts(key: str, keys: FrozenSet[str], not_allowed: FrozenSet[str]) -> None:
    if key in keys and len(keys & not_allowed) > 0:
        fail_metadata(
            "when '%s' is in a publication item, %s cannot also be specified" % (key, not_allowed))


def validate_publications(j: Dict[str, Any]) -> None:
    if 'meta' not in j or 'publications' not in j['meta']:
        return
    ps = j['meta']['publications']
    assert_is_list(ps, "'publications' must be a list")
    for p in ps['c']:
        assert_is_dict(p, "item in 'publications' must be a dict")
        data = p['c']
        keys = frozenset(data.keys())
        if not keys.issubset(PUBLICATION_KEYS):
            fail_metadata("unknown keys %s in 'publications' item" % (keys - PUBLICATION_KEYS))

        if VENUE not in keys:
            fail_metadata("'%s' is required in 'publications' item" % VENUE)

        if not keys & frozenset(PUBLICATION_DATE_KEYS):
            fail_metadata("at least one of %s is required in 'publications' item" %
                          PUBLICATION_DATE_KEYS)

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

        if URLS in data:
            urls = data[URLS]
            assert_is_list(urls, "'%s' in 'publications' item must be a list" % URLS)
            for url in urls['c']:
                assert_is_string(url, "'%s' item in 'publications' item must be a string" % URLS)

        mutually_exclusive = frozenset([ACCEPTED, REJECTED, WITHDRAWN, SELF_PUBLISHED])
        if len(keys & mutually_exclusive) > 1:
            fail_metadata("%s in 'publications' item are mutually exclusive" % mutually_exclusive)

        assert_no_conflicts(
            SELF_PUBLISHED, keys,
            frozenset([SUBMITTED, REJECTED, WITHDRAWN, ACCEPTED, PUBLISHED]))
        assert_no_conflicts(
            PUBLISHED, keys,
            frozenset([REJECTED, WITHDRAWN, SELF_PUBLISHED]))


def validate_notes(j: Dict[str, Any]) -> None:
    if 'meta' not in j or 'notes' not in j['meta']:
        return
    notes = j['meta']['notes']
    assert_is_string(notes, "'notes' must be a string")


def validate() -> None:
    raw = sys.stdin.read()
    j = json.loads(raw)
    validate_text(j)
    validate_publications(j)
    validate_notes(j)
    sys.stdout.write(raw)


if __name__ == '__main__':
    validate()
