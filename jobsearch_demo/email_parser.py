import re
from pathlib import Path

from .models import Posting


URL_RE = re.compile(r"https?://[^\s>]+")
SEPARATOR_RE = re.compile(r"^-{5,}$")
MARKER_RE = re.compile(r"^(view job:|read the full job description:)", re.IGNORECASE)


def _nonempty(lines: list[str]) -> list[str]:
    return [line.strip() for line in lines if line.strip()]


def _source(text: str, fallback: str) -> str:
    match = re.search(r"(?im)^From:\s*(.+)$", text)
    return match.group(1).strip() if match else fallback


def _format(text: str) -> str:
    return "digest" if any(SEPARATOR_RE.match(line.strip()) for line in text.splitlines()) else "single-posting"


def parse_email(text: str, fallback_source: str = "unknown") -> tuple[str, list[Posting]]:
    """Parse the two public synthetic alert shapes.

    The parser intentionally stays small and explicit. It expects each posting to
    place title, company, and location immediately before its detail-link marker.
    """

    lines = text.splitlines()
    source = _source(text, fallback_source)
    postings: list[Posting] = []

    for index, line in enumerate(lines):
        if not MARKER_RE.match(line.strip()):
            continue

        marker = line.strip()
        url_match = URL_RE.search(marker)
        if not url_match:
            for next_line in lines[index + 1 :]:
                url_match = URL_RE.search(next_line.strip())
                if url_match:
                    break
                if next_line.strip() and SEPARATOR_RE.match(next_line.strip()):
                    break
        if not url_match:
            continue

        previous = _nonempty(lines[:index])
        if len(previous) < 3:
            continue
        title, company, location = previous[-3:]
        if title.lower() in {"good match", "hot job"}:
            continue

        postings.append(
            Posting(
                title=title,
                company=company,
                location=location,
                source=source,
                source_url=url_match.group(0),
                match_reason="matched synthetic profile terms from the source alert",
            )
        )

    return _format(text), postings


def parse_email_file(path: Path) -> tuple[str, list[Posting]]:
    return parse_email(path.read_text(encoding="utf-8"), fallback_source=path.name)
