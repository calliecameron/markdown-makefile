import json

import panflute

from markdown.utils.metadata import InputMetadata


def main() -> None:
    doc = panflute.load()
    InputMetadata.model_validate_json(json.dumps(doc.get_metadata()))
    panflute.dump(doc)


if __name__ == "__main__":
    main()
