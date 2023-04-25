from typing import Any, Dict, List
import argparse
import html
import json

VENUE = "venue"
SUBMITTED = "submitted"
REJECTED = "rejected"
WITHDRAWN = "withdrawn"
ABANDONED = "abandoned"
SELF_PUBLISHED = "self-published"
ACCEPTED = "accepted"
PUBLISHED = "published"


STATES = [SUBMITTED, REJECTED, WITHDRAWN, ABANDONED, ACCEPTED, SELF_PUBLISHED, PUBLISHED]


def generate_header(venues: List[str]) -> List[str]:
    out = [
        "<thead>",
        "<tr>",
        "<th>Target</th>",
        "<th>Title</th>",
        "<th>Wordcount</th>",
        '<th style="border-right: 3px solid">Notes</th>',
    ]
    for v in venues:
        out.append("<th>%s</th>" % html.escape(v, quote=False))
    out += ["</tr>", "</thead>"]
    return out


def generate_row(target: str, data: Dict[str, Any], venues: List[str]) -> List[str]:
    ps = {}
    for p in data["publications"]:
        ps[p[VENUE]] = p

    states = set()
    for p in ps.values():
        if SUBMITTED in p and REJECTED not in p and WITHDRAWN not in p and ABANDONED not in p:
            states.add(SUBMITTED)
        if ACCEPTED in p:
            states.add(ACCEPTED)
        if SELF_PUBLISHED in p:
            states.add(SELF_PUBLISHED)
        if PUBLISHED in p:
            states.add(PUBLISHED)

    class_attr = ""
    for state in (PUBLISHED, SELF_PUBLISHED, ACCEPTED, SUBMITTED):
        if state in states:
            class_attr = state
            break

    out = [
        "<tr>",
        '<td class="%s"><a href="#%s">%s</a></td>'
        % (class_attr, html.escape(target), html.escape(target, quote=False)),
        "<td>%s</td>" % html.escape(data.get("title", ""), quote=False),
        "<td>%s</td>" % html.escape(data.get("wordcount", ""), quote=False),
        '<td style="border-right: 3px solid">%s</td>'
        % html.escape(data.get("notes", ""), quote=False),
    ]

    for v in sorted(venues):
        if v in ps:
            out.append(generate_cell(target, ps[v]))
        else:
            out.append("<td></td>")

    out.append("</tr>")
    return out


def generate_cell(target: str, p: Dict[str, Any]) -> str:
    content = []
    latest = ""
    for state in STATES:
        if state in p:
            content.append(p[state] + " " + state.capitalize())
            latest = state
    return '<td class="%s" title="%s"><a href="#%s">%s</a></td>' % (
        latest,
        html.escape(target + ", " + p[VENUE]),
        html.escape(target),
        "<br>".join([html.escape(c, quote=False) for c in content]),
    )


def generate_table(data: Dict[str, Any]) -> List[str]:
    out = ["<table>"]

    venue_set = set()
    for target in data:
        if "publications" in data[target]:
            for p in data[target]["publications"]:
                if VENUE in p:
                    venue_set.add(p[VENUE])
    venues = sorted(venue_set)

    out += generate_header(venues)

    out.append("<tbody>")
    for target in sorted(data):
        if "publications" in data[target] and data[target]["publications"]:
            out += generate_row(target, data[target], venues)
    out += ["</tbody>", "</table>"]

    return out


def generate_details(data: Dict[str, Any]) -> List[str]:
    out = ["<h2>Details</h2>"]
    for target in sorted(data):
        if "publications" in data[target] and data[target]["publications"]:
            out += [
                '<h3 id="%s">%s</h3>' % (html.escape(target), html.escape(target, quote=False)),
                "<code><pre>%s</pre></code>"
                % html.escape(json.dumps(data[target], sort_keys=True, indent=4), quote=False),
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
        ".submitted { background-color: #ffff00; }",
        ".rejected { background-color: #ff6d6d; }",
        ".withdrawn { background-color: #ff972f; }",
        ".abandoned { background-color: #cccccc; }",
        ".accepted { background-color: #729fcf; }",
        ".self-published { background-color: #158466; }",
        ".published { background-color: #81d41a; }",
        "</style>",
        "</head>",
    ]


def generate_body(data: Dict[str, Any]) -> List[str]:
    out = [
        "<body>",
        "<h1>Publications</h1>",
    ]
    out += generate_table(data)
    out += generate_details(data)
    out += ["</body>"]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out_file")
    parser.add_argument("--dep", action="append", nargs=2, default=[])
    args = parser.parse_args()

    data = {}

    for target, metadata in args.dep:
        with open(metadata, encoding="utf-8") as f:
            data[target] = json.load(f)

    out = [
        "<!doctype html>",
        '<html lang="en-GB">',
    ]

    out += generate_head()
    out += generate_body(data)

    out += [
        "</html>",
    ]

    with open(args.out_file, "w", encoding="utf-8") as outfile:
        outfile.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
