import argparse
import json
from markdown_makefile.utils.metadata import parse_author


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        metadata = json.load(f)

    if "title" in metadata:
        title = metadata["title"]
    else:
        title = "[Untitled]"

    author = parse_author(metadata)
    if not author:
        author = "[Unknown]"

    out = {
        "short_title": title,
        "author_lastname": author.split()[-1],
        "contact_name": author,
        "contact_address": "`\\n`{=tex}",
        "contact_city_state_zip": "`\\n`{=tex}",
        "contact_phone": "`\\n`{=tex}",
        "contact_email": "`\\n`{=tex}",
    }

    if "title" not in metadata:
        out["title"] = title
    if "author" not in metadata:
        out["author"] = [author]

    with open(args.outfile, "w", encoding="utf-8") as f:
        json.dump(out, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
