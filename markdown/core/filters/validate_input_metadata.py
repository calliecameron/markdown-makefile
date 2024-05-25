import panflute

from markdown.utils.metadata import InputMetadata


def main() -> None:
    doc = panflute.load()
    InputMetadata.model_validate(doc.get_metadata())
    panflute.dump(doc)


if __name__ == "__main__":
    main()
