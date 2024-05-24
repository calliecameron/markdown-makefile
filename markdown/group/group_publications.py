import argparse
import html
import json
from collections.abc import Mapping, Sequence
from typing import Any

from markdown.utils.metadata import NOTES, PUBLICATIONS, TITLE, WORDCOUNT
from markdown.utils.publications import (
    ABANDONED,
    ACCEPTED,
    PUBLISHED,
    REJECTED,
    SELF_PUBLISHED,
    SUBMITTED,
    WITHDRAWN,
    Publication,
    Publications,
)


def generate_header(venues: Sequence[str]) -> list[str]:
    return [
        "<thead>",
        "<tr>",
        '<th title="Target">Target</th>',
        '<th title="Title">Title</th>',
        '<th title="Wordcount">Wordcount</th>',
        '<th style="border-right: 3px solid" title="Notes">Notes</th>',
        *[f'<th title="{html.escape(v)}">{html.escape(v, quote=False)}</th>' for v in venues],
        "</tr>",
        "</thead>",
    ]


def generate_row(
    target: str,
    data: Publications,
    venues: Sequence[str],
    raw: Mapping[str, Any],
) -> list[str]:
    ps = {}
    for p in data.publications:
        ps[p.venue] = p

    title = raw.get(TITLE, "")
    wordcount = raw.get(WORDCOUNT, "")
    notes = raw.get(NOTES, "")

    class_attr = ""
    if data.active:
        class_attr = data.highest_active_state

    out = [
        "<tr>",
        f'<td class="{class_attr}" title="{html.escape(target)}">'
        f'<a href="#{html.escape(target)}">{html.escape(target, quote=False)}</a></td>',
        f'<td title="{html.escape(title)}">{html.escape(title, quote=False)}</td>',
        f'<td title="{html.escape(wordcount)}">{html.escape(wordcount, quote=False)}</td>',
        f'<td style="border-right: 3px solid" title="{html.escape(notes)}">'
        f"{html.escape(notes, quote=False)}</td>",
    ]

    for v in sorted(venues):
        if v in ps:
            out.append(generate_cell(target, ps[v]))
        else:
            out.append("<td></td>")

    out.append("</tr>")
    return out


def generate_cell(target: str, p: Publication) -> str:
    content = [date.date_str() + " " + date.state.capitalize() for date in p.dates.dates]
    return (
        f'<td class="{p.dates.latest.state}" title="{html.escape(target + ", " + p.venue)}">'
        f'<a href="#{html.escape(target)}">'
        f'{"<br>".join([html.escape(c, quote=False) for c in content])}</a></td>'
    )


def generate_table(data: Mapping[str, Publications], raw: Mapping[str, Any]) -> list[str]:
    out = ["<table>"]

    venue_set = set()
    for ps in data.values():
        for p in ps.publications:
            venue_set.add(p.venue)
    venues = sorted(venue_set)

    out += generate_header(venues)

    out.append("<tbody>")
    for target, ps in sorted(data.items()):
        out += generate_row(target, ps, venues, raw[target])
    out += ["</tbody>", "</table>"]

    return out


def generate_details(raw: Mapping[str, Any]) -> list[str]:
    out = ["<h2>Details</h2>"]
    for target in sorted(raw):
        if PUBLICATIONS in raw[target] and raw[target][PUBLICATIONS]:
            out += [
                f'<h3 id="{html.escape(target)}">{html.escape(target, quote=False)}</h3>',
                "<code><pre>{}</pre></code>".format(  # noqa: UP032
                    html.escape(json.dumps(raw[target], sort_keys=True, indent=4), quote=False),
                ),
            ]
    return out


def generate_head() -> list[str]:
    return [
        "<head>",
        '<meta charset="utf-8">',
        "<title>Publications</title>",
        "<style>",
        "table { border-collapse: collapse; }",
        "th, td { border: 1px solid; padding: 5px; }",
        "a:link { color: black; }",
        "a:visited { color: black; }",
        f".{SUBMITTED} {{ background-color: #ffff00; }}",
        f".{REJECTED} {{ background-color: #ff6d6d; }}",
        f".{WITHDRAWN} {{ background-color: #ff972f; }}",
        f".{ABANDONED} {{ background-color: #cccccc; }}",
        f".{ACCEPTED} {{ background-color: #729fcf; }}",
        f".{SELF_PUBLISHED} {{ background-color: #158466; }}",
        f".{PUBLISHED} {{ background-color: #81d41a; }}",
        "</style>",
        "</head>",
    ]


def generate_body(data: Mapping[str, Publications], raw: Mapping[str, Any]) -> list[str]:
    out = [
        "<body>",
        "<h1>Publications</h1>",
    ]
    out += generate_table(data, raw)
    out += generate_details(raw)
    out += ["</body>"]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("metadata_file")
    parser.add_argument("out_file")
    args = parser.parse_args()

    with open(args.metadata_file, encoding="utf-8") as f:
        j = json.load(f)

    data = {k: Publications.from_json(v[PUBLICATIONS]) for k, v in j.items() if PUBLICATIONS in v}

    out = [
        "<!doctype html>",
        '<html lang="en-GB">',
    ]

    out += generate_head()
    out += generate_body(data, j)

    out += [
        "</html>",
    ]

    with open(args.out_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
