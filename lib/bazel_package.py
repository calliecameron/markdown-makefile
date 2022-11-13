import string
import unicodedata


PANDOC_VERSION_KEY = 'STABLE_PANDOC_VERSION'


def _normalised_char_name(char: str) -> str:
    if len(char) != 1:
        raise ValueError(f"char must be a single character, got '{char}'")
    valid = frozenset(string.ascii_uppercase + '_')
    return ''.join([c for c in unicodedata.name(char) if c in valid])


def package_key(path: str) -> str:
    # Keys can only contain uppercase letters and underscores.
    path = path.upper().replace('_', '__')
    valid = frozenset(string.ascii_uppercase + '_')
    parts = []
    for c in path:
        if c in valid:
            parts.append(c)
        else:
            parts.append('_' + _normalised_char_name(c) + '_')
    return ''.join(parts)


def version_key(key: str) -> str:
    return 'STABLE_VERSION_' + key


def repo_key(key: str) -> str:
    return 'STABLE_REPO_' + key
