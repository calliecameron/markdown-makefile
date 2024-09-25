import argparse
import json
from typing import Any

from markdown.private.utils.metadata import OutputMetadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        metadata = OutputMetadata.model_validate_json(f.read())

    title = metadata.title if metadata.title else "[Untitled]"
    author = metadata.author[0] if metadata.author else "[Unknown]"

    out: dict[str, Any] = {
        "short_title": title,
        "author_lastname": author.split()[-1],
        "contact_name": author,
        "contact_address": "`\\n`{=tex}",
        "contact_city_state_zip": "`\\n`{=tex}",
        "contact_phone": "`\\n`{=tex}",
        "contact_email": "`\\n`{=tex}",
    }

    if not metadata.title:
        out["title"] = title
    if not metadata.author:
        out["author"] = [author]

    with open(args.outfile, "w", encoding="utf-8") as f:
        json.dump(out, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
