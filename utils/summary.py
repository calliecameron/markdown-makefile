import argparse
import csv
import json
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('metadata')
    parser.add_argument('--header', action='store_true')
    args = parser.parse_args()

    with open(args.metadata, encoding='utf-8') as f:
        j = json.load(f)

    out = csv.DictWriter(sys.stdout, ['target', 'title', 'wordcount', 'status'])

    if args.header:
        out.writeheader()

    out.writerow({
        'target': args.target,
        'title': j['title'] if 'title' in j else '',
        'wordcount': j['wordcount'],
        'status': 'DIRTY' if 'dirty' in j['docversion'] else 'ok',
    })


if __name__ == '__main__':
    main()
