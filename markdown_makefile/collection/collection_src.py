import argparse
import json
import yaml
from markdown_makefile.utils.metadata import AUTHOR, DATE, TITLE, parse_author


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("title")
    parser.add_argument("author")
    parser.add_argument("date")
    parser.add_argument("metadata_file")
    parser.add_argument("out_file")
    parser.add_argument("--dep", action="append", default=[])
    args = parser.parse_args()

    main_author = args.author

    main_metadata = {TITLE: args.title, AUTHOR: [main_author]}
    if args.date:
        main_metadata[DATE] = args.date

    output = ["---"]
    output += yaml.dump(main_metadata).strip().split("\n")
    output.append("---")
    output.append("")

    with open(args.metadata_file, encoding="utf-8") as f:
        metadata = json.load(f)

    for target in args.dep:
        j = metadata[target]
        output += [f"# {j[TITLE]}", ""]
        author = parse_author(j)
        print_author = author != args.author
        print_date = DATE in j and j[DATE]
        tagline = []
        if print_author:
            tagline.append(author)
        if print_date:
            tagline.append(j["date"])
        if tagline:
            output += ["### " + ", ".join(tagline), ""]
        output += [f"!include //{target}", ""]

    with open(args.out_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    main()
