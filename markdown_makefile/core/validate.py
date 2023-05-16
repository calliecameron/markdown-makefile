from typing import cast, Any, Dict, FrozenSet, List, NoReturn
import json
import sys
from markdown_makefile.utils.publications import Publications


def fail(msg: str) -> NoReturn:
    sys.stderr.write("ERROR: " + msg)
    sys.exit(1)


def fail_metadata(msg: str) -> NoReturn:
    fail("invalid metadata: " + msg)


def validate_str(s: str) -> None:
    if "'" in s or '"' in s:
        fail(
            (
                "markdown parsing failed: '%s'\n\n"
                "Found quotes that weren't converted to smart quotes. Replace them with "
                "backslash-escaped literal curly quotes (“ ” ‘ ’).\n"
            )
            % s
        )


def walk_dict(ast: Dict[str, Any]) -> None:
    if "t" in ast and ast["t"] == "Str":
        validate_str(ast["c"])
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
    if "blocks" in j:
        walk_list(j["blocks"])
    if "meta" in j and "title" in j["meta"]:
        walk_dict(j["meta"]["title"])


def assert_is_list(j: Dict[str, Any], msg: str) -> None:
    if j["t"] != "MetaList":
        fail_metadata(msg)


def assert_is_dict(j: Dict[str, Any], msg: str) -> None:
    if j["t"] != "MetaMap":
        fail_metadata(msg)


def assert_is_string(j: Dict[str, Any], msg: str) -> None:
    if j["t"] != "MetaInlines":
        fail_metadata(msg)


def assert_no_conflicts(key: str, keys: FrozenSet[str], not_allowed: FrozenSet[str]) -> None:
    if key in keys and len(keys & not_allowed) > 0:
        fail_metadata(
            "when '%s' is in a publication item, %s cannot also be specified" % (key, not_allowed)
        )


def validate_publications(j: Dict[str, Any]) -> None:
    if "meta" not in j or "publications" not in j["meta"]:
        return
    ps_raw = j["meta"]["publications"]

    def dict_to_json(elem: Dict[str, Any]) -> Dict[str, Any]:
        out = {}  # type: Dict[str, Any]
        for k, e in elem["c"].items():
            if e["t"] == "MetaList":
                out[k] = list_to_json(e)
            elif e["t"] == "MetaInlines":
                out[k] = inlines_to_json(e)
            else:
                fail_metadata(
                    "failed to parse publications: unknown type %s in dict. %s"
                    % (e["t"], str(ps_raw))
                )
        return out

    def list_to_json(elem: Dict[str, Any]) -> List[Any]:
        out = []  # type: List[Any]
        for e in elem["c"]:
            if e["t"] == "MetaList":
                out.append(list_to_json(e))
            elif e["t"] == "MetaInlines":
                out.append(inlines_to_json(e))
            else:
                fail_metadata(
                    "failed to parse publications: unknown type %s in list. %s"
                    % (e["t"], str(ps_raw))
                )
        return out

    def inlines_to_json(elem: Dict[str, Any]) -> str:
        if len(elem["c"]) == 1 and elem["c"][0]["t"] == "Str":
            return cast(str, elem["c"][0]["c"])
        return str(elem["c"])

    assert_is_list(ps_raw, "'publications' must be a list")
    ps = []
    for p in ps_raw["c"]:
        assert_is_dict(p, "item in 'publications' must be a dict")
        ps.append(dict_to_json(p))

    try:
        Publications.from_json(ps)
    except ValueError as e:
        fail_metadata("failed to parse publications: %s" % str(e))


def validate_notes(j: Dict[str, Any]) -> None:
    if "meta" not in j or "notes" not in j["meta"]:
        return
    notes = j["meta"]["notes"]
    assert_is_string(notes, "'notes' must be a string")


def validate() -> None:
    raw = sys.stdin.read()
    j = json.loads(raw)
    validate_text(j)
    validate_publications(j)
    validate_notes(j)
    sys.stdout.write(raw)


if __name__ == "__main__":
    validate()
