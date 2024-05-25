import json
import sys
from collections.abc import Mapping
from typing import Any, NoReturn, cast

from markdown.utils.metadata import (
    AUTHOR,
    DATE,
    FINISHED,
    IDENTIFIER,
    INCREMENT_INCLUDED_HEADERS,
    LANG,
    NOTES,
    PUBLICATIONS,
    TITLE,
    USER_KEYS,
)
from markdown.utils.publications import Publications

KNOWN_KEYS = USER_KEYS | frozenset(
    [
        # Keys added during processing
        IDENTIFIER,
        INCREMENT_INCLUDED_HEADERS,
        LANG,
    ],
)

META_BOOL = "MetaBool"
META_INLINES = "MetaInlines"
META_LIST = "MetaList"
META_DICT = "MetaMap"

META_TYPE_NAMES = {
    META_BOOL: "bool",
    META_INLINES: "string",
    META_LIST: "list",
    META_DICT: "dict",
}


def fail(msg: str) -> NoReturn:
    sys.stderr.write("ERROR: " + msg)
    sys.exit(1)


def fail_metadata(msg: str) -> NoReturn:
    fail("invalid metadata: " + msg)


def assert_is_type(j: Mapping[str, Any], meta_type: str, msg: str) -> None:
    if j["t"] != meta_type:
        fail_metadata(msg)


def assert_is_list(j: Mapping[str, Any], msg: str) -> None:
    assert_is_type(j, META_LIST, msg)


def assert_is_dict(j: Mapping[str, Any], msg: str) -> None:
    assert_is_type(j, META_DICT, msg)


def assert_is_string(j: Mapping[str, Any], msg: str) -> None:
    assert_is_type(j, META_INLINES, msg)


def assert_is_bool(j: Mapping[str, Any], msg: str) -> None:
    assert_is_type(j, META_BOOL, msg)


def assert_meta_item_is_type(
    j: Mapping[str, Any],
    key: str,
    meta_type: str,
) -> dict[str, Any] | None:
    if "meta" not in j or key not in j["meta"]:
        return None
    item = j["meta"][key]
    assert_is_type(
        item,
        meta_type,
        f"metadata item '{key}' must be a {META_TYPE_NAMES[meta_type]}",
    )
    return cast(dict[str, Any], item)


def assert_meta_item_is_list(j: Mapping[str, Any], key: str) -> dict[str, Any] | None:
    return assert_meta_item_is_type(j, key, META_LIST)


def assert_meta_item_is_dict(j: Mapping[str, Any], key: str) -> dict[str, Any] | None:
    return assert_meta_item_is_type(j, key, META_DICT)


def assert_meta_item_is_string(j: Mapping[str, Any], key: str) -> dict[str, Any] | None:
    return assert_meta_item_is_type(j, key, META_INLINES)


def assert_meta_item_is_bool(j: Mapping[str, Any], key: str) -> dict[str, Any] | None:
    return assert_meta_item_is_type(j, key, META_BOOL)


def validate_keys(j: Mapping[str, Any]) -> None:
    if "meta" not in j:
        return
    unknown_keys = frozenset(j["meta"].keys()) - KNOWN_KEYS
    if unknown_keys:
        fail("unknown metadata keys: " + ", ".join(sorted(unknown_keys)))


def validate_publications(j: Mapping[str, Any]) -> None:
    ps_raw = assert_meta_item_is_list(j, PUBLICATIONS)
    if not ps_raw:
        return

    def dict_to_json(elem: Mapping[str, Any]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for k, e in elem["c"].items():
            if e["t"] == META_LIST:
                out[k] = list_to_json(e)
            elif e["t"] == META_INLINES:
                out[k] = inlines_to_json(e)
            else:
                fail_metadata(
                    f"failed to parse publications: unknown type {e['t']} in dict. {ps_raw}",
                )
        return out

    def list_to_json(elem: Mapping[str, Any]) -> list[Any]:
        out: list[Any] = []
        for e in elem["c"]:
            if e["t"] == META_LIST:
                out.append(list_to_json(e))
            elif e["t"] == META_INLINES:
                out.append(inlines_to_json(e))
            else:
                fail_metadata(
                    f"failed to parse publications: unknown type {e['t']} in list. {ps_raw}",
                )
        return out

    def inlines_to_json(elem: Mapping[str, Any]) -> str:
        if len(elem["c"]) == 1 and elem["c"][0]["t"] == "Str":
            return cast(str, elem["c"][0]["c"])
        return str(elem["c"])

    ps = []
    for p in ps_raw["c"]:
        assert_is_dict(p, "item in 'publications' must be a dict")
        ps.append(dict_to_json(p))

    try:
        Publications.model_validate_json(json.dumps(ps))
    except ValueError as e:
        fail_metadata(f"failed to parse publications: {e}")


def validate_author(j: Mapping[str, Any]) -> None:
    if "meta" not in j or AUTHOR not in j["meta"]:
        return

    author = j["meta"][AUTHOR]
    msg = "metadata item 'author' must be a list of strings or a string"

    if author["t"] not in (META_LIST, META_INLINES):
        fail(msg)

    if author["t"] == META_LIST:
        for a in author["c"]:
            assert_is_string(a, msg)


def validate() -> None:
    raw = sys.stdin.read()
    j = json.loads(raw)
    validate_keys(j)
    assert_meta_item_is_string(j, TITLE)
    validate_author(j)
    assert_meta_item_is_string(j, DATE)
    assert_meta_item_is_string(j, NOTES)
    assert_meta_item_is_bool(j, FINISHED)
    validate_publications(j)
    sys.stdout.write(raw)


if __name__ == "__main__":
    validate()
