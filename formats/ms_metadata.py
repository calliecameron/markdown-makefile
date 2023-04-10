import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()

    with open(args.infile, encoding="utf-8") as f:
        metadata = json.load(f)

    if "title" not in metadata:
        raise ValueError("Document title must be set")
    if "author" not in metadata:
        raise ValueError("Document author must be set")

    out = {
        "short_title": metadata["title"],
        "author_lastname": metadata["author"][0].split()[-1],
        "contact_name": metadata["author"][0],
        "contact_address": "`\\n`{=tex}",
        "contact_city_state_zip": "`\\n`{=tex}",
        "contact_phone": "`\\n`{=tex}",
        "contact_email": "`\\n`{=tex}",
    }

    with open(args.outfile, "w", encoding="utf-8") as f:
        json.dump(out, f, sort_keys=True, indent=4)


if __name__ == "__main__":
    main()
