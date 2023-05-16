from typing import Any, Dict, List
import argparse
import html
import json
from markdown_makefile.utils.publications import (
    Publication,
    Publications,
    SUBMITTED,
    ACCEPTED,
    REJECTED,
    WITHDRAWN,
    ABANDONED,
    SELF_PUBLISHED,
    PUBLISHED,
)


def generate_header(venues: List[str]) -> List[str]:
    out = [
        "<thead>",
        "<tr>",
        '<th title="Target">Target</th>',
        '<th title="Title">Title</th>',
        '<th title="Wordcount">Wordcount</th>',
        '<th style="border-right: 3px solid" title="Notes">Notes</th>',
    ]
    for v in venues:
        out.append('<th title="%s">%s</th>' % (html.escape(v), html.escape(v, quote=False)))
    out += ["</tr>", "</thead>"]
    return out


def generate_row(
    target: str, data: Publications, venues: List[str], raw: Dict[str, Any]
) -> List[str]:
    ps = {}
    for p in data.publications:
        ps[p.venue] = p

    title = raw.get("title", "")
    wordcount = raw.get("wordcount", "")
    notes = raw.get("notes", "")

    class_attr = ""
    if data.active:
        class_attr = data.highest_active_state

    out = [
        "<tr>",
        '<td class="%s" title="%s"><a href="#%s">%s</a></td>'
        % (class_attr, html.escape(target), html.escape(target), html.escape(target, quote=False)),
        '<td title="%s">%s</td>' % (html.escape(title), html.escape(title, quote=False)),
        '<td title="%s">%s</td>'
        % (
            html.escape(wordcount),
            html.escape(wordcount, quote=False),
        ),
        '<td style="border-right: 3px solid" title="%s">%s</td>'
        % (html.escape(notes), html.escape(notes, quote=False)),
    ]

    for v in sorted(venues):
        if v in ps:
            out.append(generate_cell(target, ps[v]))
        else:
            out.append("<td></td>")

    out.append("</tr>")
    return out


def generate_cell(target: str, p: Publication) -> str:
    content = []
    for date in p.dates.dates:
        content.append(date.date_str() + " " + date.state.capitalize())
    return '<td class="%s" title="%s"><a href="#%s">%s</a></td>' % (
        p.dates.latest.state,
        html.escape(target + ", " + p.venue),
        html.escape(target),
        "<br>".join([html.escape(c, quote=False) for c in content]),
    )


def generate_table(data: Dict[str, Publications], raw: Dict[str, Any]) -> List[str]:
    out = ["<table>"]

    venue_set = set()
    for target, ps in data.items():
        for p in ps.publications:
            venue_set.add(p.venue)
    venues = sorted(venue_set)

    out += generate_header(venues)

    out.append("<tbody>")
    for target, ps in sorted(data.items()):
        out += generate_row(target, ps, venues, raw[target])
    out += ["</tbody>", "</table>"]

    return out


def generate_details(raw: Dict[str, Any]) -> List[str]:
    out = ["<h2>Details</h2>"]
    for target in sorted(raw):
        if "publications" in raw[target] and raw[target]["publications"]:
            out += [
                '<h3 id="%s">%s</h3>' % (html.escape(target), html.escape(target, quote=False)),
                "<code><pre>%s</pre></code>"
                % html.escape(json.dumps(raw[target], sort_keys=True, indent=4), quote=False),
            ]
    return out


def generate_head() -> List[str]:
    return [
        "<head>",
        '<meta charset="utf-8">',
        "<title>Publications</title>",
        "<style>",
        "table { border-collapse: collapse; }",
        "th, td { border: 1px solid; padding: 5px; }",
        "a:link { color: black; }",
        "a:visited { color: black; }",
        ".%s { background-color: #ffff00; }" % SUBMITTED,
        ".%s { background-color: #ff6d6d; }" % REJECTED,
        ".%s { background-color: #ff972f; }" % WITHDRAWN,
        ".%s { background-color: #cccccc; }" % ABANDONED,
        ".%s { background-color: #729fcf; }" % ACCEPTED,
        ".%s { background-color: #158466; }" % SELF_PUBLISHED,
        ".%s { background-color: #81d41a; }" % PUBLISHED,
        "</style>",
        "</head>",
    ]


def generate_body(data: Dict[str, Publications], raw: Dict[str, Any]) -> List[str]:
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

    data = {
        k: Publications.from_json(v["publications"]) for k, v in j.items() if "publications" in v
    }

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
