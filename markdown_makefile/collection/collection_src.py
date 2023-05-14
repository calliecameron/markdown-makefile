import argparse
import json


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

    output = [
        f"% {args.title}",
        f"% {main_author}",
    ]
    if args.date:
        output.append(f"% {args.date}")
    output.append("")

    with open(args.metadata_file, encoding="utf-8") as f:
        metadata = json.load(f)

    for target in args.dep:
        j = metadata[target]
        output += [f'# {j["title"]}', ""]
        author = j["author"][0]
        print_author = author != args.author
        print_date = "date" in j and j["date"]
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
