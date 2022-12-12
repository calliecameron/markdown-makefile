from typing import Any, Dict, List
import argparse
import json

STATES = ['submitted', 'rejected', 'withdrawn', 'accepted', 'published']


def generate_header(venues: List[str]) -> List[str]:
    out = [
        '<thead>',
        '<tr>',
        '<th>Target</th>',
        '<th>Title</th>',
        '<th>Wordcount</th>',
        '<th>Notes</th>'
    ]
    for v in venues:
        out.append('<th>%s</th>' % v)
    out += [
        '</tr>',
        '</thead>'
    ]
    return out


def generate_row(target: str, data: Dict[str, Any], venues: List[str]) -> List[str]:
    out = [
        '<tr>',
        '<td>%s</td>' % target,
        '<td>%s</td>' % data.get('title', ''),
        '<td>%s</td>' % data.get('wordcount', ''),
        '<td>%s</td>' % data.get('notes', ''),
    ]

    ps = {}
    for p in data['publications']:
        ps[p['venue']] = p

    for v in sorted(venues):
        if v in ps:
            out.append(generate_cell(target, ps[v]))
        else:
            out.append('<td></td>')

    out.append('</tr>')
    return out


def generate_cell(target: str, p: Dict[str, Any]) -> str:
    content = []
    latest = ''
    for state in STATES:
        if state in p:
            content.append(p[state] + ' ' + state.title())
            latest = state
    return '<td class="%s" title="%s">%s</td>' % (
        latest, target + ', ' + p['venue'], '<br>'.join(content))


def generate_table(data: Dict[str, Any]) -> List[str]:
    out = ['<table>']

    venue_set = set()
    for target in data:
        if 'publications' in data[target]:
            for p in data[target]['publications']:
                if 'venue' in p:
                    venue_set.add(p['venue'])
    venues = sorted(venue_set)

    out += generate_header(venues)

    out.append('<tbody>')
    for target in sorted(data):
        if 'publications' in data[target] and data[target]['publications']:
            out += generate_row(target, data[target], venues)
    out += ['</tbody>', '</table>']

    return out


def generate_details(data: Dict[str, Any]) -> List[str]:
    out = ['<h2>Details</h2>']
    for target in sorted(data):
        if 'publications' in data[target] and data[target]['publications']:
            out += [
                '<h3>%s</h3>' % target,
                '<code><pre>%s</pre></code>' % json.dumps(data[target], sort_keys=True, indent=4),
            ]
    return out


def generate_head() -> List[str]:
    return [
        '<head>',
        '<meta charset="utf-8">',
        '<title>Publications</title>',
        '<style>',
        'table { border-collapse: collapse; }',
        'th, td { border: 1px solid; padding: 5px; }',
        '.submitted { background-color: #ffff00; }',
        '.rejected { background-color: #ff6d6d; }',
        '.withdrawn { background-color: #ff972f; }',
        '.accepted { background-color: #729fcf; }',
        '.published { background-color: #81d41a; }',
        '</style>',
        '</head>',
    ]


def generate_body(data: Dict[str, Any]) -> List[str]:
    out = [
        '<body>',
        '<h1>Publications</h1>',
    ]
    out += generate_table(data)
    out += generate_details(data)
    out += ['</body>']
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('out_file')
    parser.add_argument('--dep', action='append', nargs=2, default=[])
    args = parser.parse_args()

    data = {}

    for target, metadata in args.dep:
        with open(metadata, encoding='utf-8') as f:
            data[target] = json.load(f)

    out = [
        '<!doctype html>',
        '<html lang="en-GB">',
    ]

    out += generate_head()
    out += generate_body(data)

    out += [
        '</html>',
    ]

    with open(args.out_file, 'w', encoding='utf-8') as outfile:
        outfile.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
