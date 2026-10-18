#!/usr/bin/env python3
"""Create private drafts and explicitly copy selected notes into Jekyll."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from uuid import uuid4


class NoteError(ValueError):
    """A note needs an explicit correction before it can be published."""


def _scalar(value: str) -> str:
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as error:
            raise NoteError("Use a JSON-style quoted string in frontmatter.") from error
        if not isinstance(parsed, str):
            raise NoteError("Expected a string in frontmatter.")
        return parsed
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise NoteError("Invalid single-quoted frontmatter string.")
        return value[1:-1].replace("''", "'")
    if not value or value[0] in "[]{}&*!|>@`" or " #" in value or ": " in value:
        raise NoteError("Use a one-line quoted string in frontmatter.")
    return value


def _parse_note(text: str) -> tuple[dict[str, str], str]:
    lines = text.removeprefix("\ufeff").splitlines()
    metadata: dict[str, str] = {}
    if lines and lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError as error:
            raise NoteError("Frontmatter must end with a standalone --- line.") from error
        for line in lines[1:end]:
            match = re.fullmatch(r"(date|title|public):[ \t]*(.*)", line)
            if match:
                key, value = match.groups()
                if key in metadata:
                    raise NoteError(f"Duplicate frontmatter key: {key}")
                metadata[key] = value.strip() if key == "public" else _scalar(value.strip())
        lines = lines[end + 1 :]
    body = "\n".join(lines).strip()
    if not body:
        raise NoteError("Write at least one sentence before saving a note.")
    return metadata, body


def _timestamp(value: str | None = None) -> str:
    if value is None:
        parsed = datetime.now(timezone.utc)
    else:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise NoteError("date must be YYYY-MM-DD or an ISO8601 timestamp.") from error
        if len(value) == 10:
            parsed = parsed.replace(tzinfo=timezone.utc)
        elif parsed.tzinfo is None:
            raise NoteError("A timestamp must include Z or a UTC offset.")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _validate_public(body: str, title: str | None) -> None:
    text = "\n".join((title or "", body))
    if "{{" in text or "{%" in text:
        raise NoteError("Liquid syntax ({{ or {%) is unsupported by this Jekyll 3 site.")
    if "[[" in text or "![" in text:
        raise NoteError("Images and Obsidian [[wikilinks]] are unsupported; use a public web link.")
    if "{:" in text:
        raise NoteError("Kramdown attribute lists ({:) are unsupported; use plain Markdown.")
    if "%%" in text or re.search(r"<!--|</?[A-Za-z][\w-]*(?:\s|/?>)", text):
        raise NoteError("Raw HTML and Obsidian comments are unsupported; use plain Markdown.")
    if re.search(r"(?i)file:|obsidian:|/(?:Users|home|Volumes)/|(?<![A-Za-z0-9])[A-Z]:[\\/]", text):
        raise NoteError("Remove local file paths and local-app links before publishing.")
    targets = re.findall(
        r"\]\(\s*(<?[^\s)]*)|^\s{0,3}\[[^\]\n]+\]:\s*(\S+)|<([A-Za-z][\w+.-]*:[^<>]*)>",
        body,
        re.MULTILINE,
    )
    for inline_target, reference_target, autolink in targets:
        target = (inline_target or reference_target or autolink).lstrip("<")
        if not re.match(r"(?i)^(?:https?://|mailto:|#)", target):
            raise NoteError("Links must use https://, http://, mailto:, or #; relative paths are unsupported.")


def _read_source(source: Path) -> tuple[dict[str, str], str]:
    if source.suffix.lower() not in {".md", ".markdown"}:
        raise NoteError("Select one .md or .markdown file.")
    return _parse_note(source.read_text(encoding="utf-8"))


def _source_id(source: Path) -> str:
    digest = hashlib.sha256(str(source.resolve()).encode("utf-8")).hexdigest()[:24]
    return f"source-{digest}"


def _write_note(destination: Path, body: str, date_value: str, title: str | None, *, published: bool) -> Path:
    if title is not None and ("\n" in title or "\r" in title):
        raise NoteError("title must be a single line.")
    header = [
        "---",
        f"date: {json.dumps(date_value)}",
        f"published: {str(published).lower()}",
        "render_with_liquid: false",
    ]
    if title:
        header.append(f"title: {json.dumps(title, ensure_ascii=False)}")
    content = "\n".join([*header, "---", "", body, ""])
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8") as output:
            output.write(content)
    except FileExistsError as error:
        raise NoteError(
            f"Already exists: {destination.name}. Edit that file explicitly; "
            "this command never overwrites it."
        ) from error
    return destination


def create_draft(root: Path, text: str | None, source: Path | None, title: str | None) -> Path:
    """Save a private draft without changing any public note.

    Args:
        root: Repository directory.
        text: A short Markdown note, unless source is provided.
        source: One explicitly selected Markdown file.
        title: Optional title override.

    Returns:
        The newly created draft path.
    """
    if source:
        metadata, body = _read_source(source)
        note_id = _source_id(source)
    else:
        metadata, body = _parse_note(text or "")
        note_id = f"note-{uuid4().hex}"
    return _write_note(
        root / ".local" / "notes" / f"{note_id}.md",
        body,
        _timestamp(metadata.get("date")),
        title if title is not None else metadata.get("title"),
        published=False,
    )


def publish_draft(root: Path, source: Path) -> Path:
    """Copy one managed draft into the public collection without overwriting.

    Args:
        root: Repository directory.
        source: An existing Markdown draft inside .local/notes.

    Returns:
        The new public note path.
    """
    source = source.resolve()
    if source.parent != (root / ".local" / "notes").resolve() or not re.fullmatch(
        r"(?:note-[0-9a-f]{32}|source-[0-9a-f]{24})\.md", source.name
    ):
        raise NoteError("publish accepts drafts created by new; use import for an external note.")
    metadata, body = _read_source(source)
    _validate_public(body, metadata.get("title"))
    return _write_note(
        root / "_notes" / source.name,
        body,
        _timestamp(metadata.get("date")),
        metadata.get("title"),
        published=True,
    )


def import_note(root: Path, source: Path) -> Path:
    """Publish one external note only when its frontmatter says public: true.

    Args:
        root: Repository directory.
        source: One explicitly selected external Markdown file.

    Returns:
        The new public note path.
    """
    if source.resolve().parent == (root / "_notes").resolve():
        raise NoteError("This note is already in _notes; edit it explicitly.")
    metadata, body = _read_source(source)
    if metadata.get("public") != "true":
        raise NoteError("Import requires the exact top-level frontmatter line public: true.")
    _validate_public(body, metadata.get("title"))
    return _write_note(
        root / "_notes" / f"{_source_id(source)}.md",
        body,
        _timestamp(metadata.get("date")),
        metadata.get("title"),
        published=True,
    )


def main(argv: list[str] | None = None, *, root: Path | None = None) -> int:
    """Run the CLI, returning zero on success and two on an input error.

    Args:
        argv: Command arguments, or the process arguments when omitted.
        root: Repository directory override, used by isolated tests.

    Returns:
        The command's exit code.
    """
    parser = argparse.ArgumentParser(description="One sentence is enough. Save a private draft, then explicitly publish it.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    new_parser = subparsers.add_parser("new", help="create a private draft")
    new_parser.add_argument("text", nargs="?")
    new_parser.add_argument("--file", type=Path)
    new_parser.add_argument("--title")
    for command in ("publish", "import"):
        command_parser = subparsers.add_parser(command)
        command_parser.add_argument("source", type=Path)
    args = parser.parse_args(argv)
    root = (root or Path(__file__).resolve().parent.parent).resolve()
    try:
        if args.command == "new":
            if (args.text is None) == (args.file is None):
                raise NoteError("Provide either a sentence or --file, but not both.")
            destination = create_draft(root, args.text, args.file, args.title)
        elif args.command == "publish":
            destination = publish_draft(root, args.source)
        else:
            destination = import_note(root, args.source)
    except (NoteError, OSError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
