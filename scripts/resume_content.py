"""Validate explicit candidate content without rewriting or inferring facts."""

import json
import re
from pathlib import Path

SECTIONS = ("summary", "education", "experience", "skills", "achievements", "languages")
PROSE_SMELLS = re.compile(
    r"\b(?:responsible\s+for|helped\s+with|passionate|dynamic|results[- ]driven|hardworking)\b",
    re.IGNORECASE,
)
US_FORMS = re.compile(
    r"\b(?:organized|organizing|analyzed|analyzing|recognized|recognizing|centered)\b",
    re.IGNORECASE,
)


class ContentError(ValueError):
    """Candidate input needs an explicit correction before generation."""


def text(value, path, *, prose=False):
    if not isinstance(value, str) or not value.strip():
        raise ContentError(f"{path}: expected a non-empty string.")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ContentError(f"{path}: control characters and manual line breaks are not supported.")
    if "\u2014" in value:
        raise ContentError(f"{path}: em dashes are not permitted; supply the approved wording.")
    if prose and PROSE_SMELLS.search(value):
        raise ContentError(f"{path}: contains a prohibited style phrase; supply the approved wording.")
    if prose and US_FORMS.search(value):
        raise ContentError(f"{path}: review British spelling; no automatic rewrite was applied.")


def text_list(value, path, *, prose=False):
    if not isinstance(value, list):
        raise ContentError(f"{path}: expected an array.")
    for index, item in enumerate(value):
        text(item, f"{path}[{index}]", prose=prose)


def object_fields(value, required, optional, path):
    if not isinstance(value, dict):
        raise ContentError(f"{path}: expected an object.")
    if set(value) - set(required) - set(optional):
        raise ContentError(f"{path}: unknown property; input will not be silently discarded.")
    missing = set(required) - set(value)
    if missing:
        raise ContentError(f"{path}: missing required field(s): {', '.join(sorted(missing))}.")


def validate_content(candidate):
    object_fields(candidate, ("schema_version", "name"), ("headline", "contact", *SECTIONS), "candidate")
    if type(candidate["schema_version"]) is not int or candidate["schema_version"] != 1:
        raise ContentError("schema_version: only integer version 1 is supported.")
    text(candidate["name"], "name")
    for key in ("headline", "contact"):
        if key in candidate:
            text_list(candidate[key], key)
    if "summary" in candidate:
        text(candidate["summary"], "summary", prose=True)
    if "achievements" in candidate:
        text_list(candidate["achievements"], "achievements", prose=True)

    specifications = {
        "education": (("qualification", "institution", "dates"), ("location", "details")),
        "experience": (("title", "company", "dates", "bullets"), ("location",)),
        "skills": (("category", "items"), ()),
        "languages": (("language", "level"), ()),
    }
    for section, (required, optional) in specifications.items():
        if section not in candidate:
            continue
        if not isinstance(candidate[section], list):
            raise ContentError(f"{section}: expected an array.")
        for index, entry in enumerate(candidate[section]):
            path = f"{section}[{index}]"
            object_fields(entry, required, optional, path)
            for field, value in entry.items():
                field_path = f"{path}.{field}"
                if field in {"bullets", "details", "items"}:
                    text_list(value, field_path, prose=field in {"bullets", "details"})
                    if field == "items" and not value:
                        raise ContentError(f"{field_path}: at least one skill is required.")
                else:
                    # Official titles, institutions, employers, and tool names
                    # are copied literally, not edited by a prose word list.
                    text(value, field_path)
    return candidate


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ContentError("Duplicate JSON properties are not permitted.")
        result[key] = value
    return result


def load_content(path):
    path = Path(path)
    if path.stat().st_size > 2 * 1024 * 1024:
        raise ContentError("Candidate JSON exceeds the 2 MiB input limit.")
    try:
        candidate = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ContentError("Candidate input is not valid UTF-8 JSON.") from error
    return validate_content(candidate)


def content_fragments(candidate):
    """Yield every supplied text value, including repeated facts, for export QA."""
    if isinstance(candidate, str):
        yield candidate
    elif isinstance(candidate, list):
        for item in candidate:
            yield from content_fragments(item)
    elif isinstance(candidate, dict):
        for key, value in candidate.items():
            if key != "schema_version":
                yield from content_fragments(value)
