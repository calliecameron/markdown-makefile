import argparse


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file")
    parser.add_argument("out_file")
    args = parser.parse_args()

    with open(args.in_file, encoding="utf-8") as in_file, open(
        args.out_file,
        mode="w",
        encoding="utf-8",
    ) as out_file:
        first_line = True
        in_front_matter = False

        for line in in_file:
            if first_line and line == "---\n":
                in_front_matter = True

            if in_front_matter:
                out_file.write("<!-- -->\n")
            else:
                out_file.write(line)

            if not first_line and line == "---\n":
                in_front_matter = False

            first_line = False


if __name__ == "__main__":
    main()
