import re
import string
import unicodedata


def _normalised_char_name(char: str) -> str:
    if len(char) != 1:
        raise ValueError(f"char must be a single character, got '{char}'")
    valid = frozenset(string.ascii_uppercase + "_")
    return "".join([c for c in unicodedata.name(char) if c in valid])


def package_key(path: str) -> str:
    # Keys can only contain uppercase letters and underscores.
    path = path.upper().replace("_", "__")
    valid = frozenset(string.ascii_uppercase + "_")
    parts = []
    for c in path:
        if c in valid:
            parts.append(c)
        else:
            parts.append("_" + _normalised_char_name(c) + "_")
    return "".join(parts)


def version_key(key: str) -> str:
    return "STABLE_VERSION_" + key


def repo_key(key: str) -> str:
    return "STABLE_REPO_" + key


def _validate_package(package: str) -> None:
    valid = string.ascii_letters + string.digits + "/-.@_"
    for c in package:
        if c not in valid:
            raise ValueError(f"Invalid character '{c}' in package: {package}")
    if package.startswith("/"):
        raise ValueError(f"Packages must not start with a '/': {package}")
    if package.endswith("/"):
        raise ValueError(f"Packages must not end with a '/': {package}")
    if "//" in package:
        raise ValueError(f"Packages must not contain '//': {package}")


def _validate_target(target: str) -> None:
    # We deliberately exclude closing parenthesis from this list, even though
    # it's valid according to the bazel spec, because it messes up markdown
    # image handling.
    valid = string.ascii_letters + string.digits + "%-@^_\"#$&'(*-+,;<=>?[]{|}~/."
    for c in target:
        if c not in valid:
            raise ValueError(f"Invalid character '{c}' in target: {target}")
    if target.startswith("/"):
        raise ValueError(f"Targets must not start with a '/': {target}")
    if target.endswith("/"):
        raise ValueError(f"Targets must not end with a '/': {target}")
    if "//" in target:
        raise ValueError(f"Targets must not contain '//': {target}")
    if ".." in target.split("/"):
        raise ValueError(f"Targets must not contain up-level references '..': {target}")
    if "." in target.split("/"):
        raise ValueError(f"Targets must not contain current-directory references '.': {target}")


def canonicalise_label(label: str, current_package: str) -> tuple[str, str]:
    if not label and not current_package:
        raise ValueError("Label or current package must be specified")

    match = re.fullmatch(r"((?P<absolute>//)(?P<package>[^:]*))?:?(?P<target>[^:]+)?", label)
    if match is None:
        raise ValueError(f"Invalid label '{label}'")

    absolute = bool(match.groupdict()["absolute"])
    package = match.groupdict()["package"] or ""
    target = match.groupdict()["target"] or ""
    _validate_package(current_package)
    _validate_package(package)
    _validate_target(target)

    if not package and not target:
        raise ValueError("Either package or target must be specified")
    if package and not target:
        target = package.split("/")[-1]
    if target and not package and not absolute:
        package = current_package

    return package, target
