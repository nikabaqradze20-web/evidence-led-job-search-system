import json
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class EmailThread:
    thread_id: str
    plaintext_body: str
    source_path: str


class ClaudeConnector(Protocol):
    """Small boundary matching the operations used by the private workflow."""

    def search_threads(self, query: str) -> list[EmailThread]:
        ...

    def search_jobs(self, search_term: str, location: str) -> list[dict[str, str]]:
        ...


class FixtureClaudeConnector:
    """Offline stand-in for Claude-connected Gmail and Indeed tools.

    It never performs network access. The public repository uses this class to
    demonstrate the adapter boundary while keeping credentials out of source.
    """

    def __init__(self, email_dir: Path, indeed_fixture: Path | None = None) -> None:
        self.email_dir = email_dir
        self.indeed_fixture = indeed_fixture

    def search_threads(self, query: str) -> list[EmailThread]:
        return [
            EmailThread(
                thread_id=path.stem,
                plaintext_body=path.read_text(encoding="utf-8"),
                source_path=str(path),
            )
            for path in sorted(self.email_dir.glob("*.txt"))
        ]

    def search_jobs(self, search_term: str, location: str) -> list[dict[str, str]]:
        if self.indeed_fixture is None or not self.indeed_fixture.exists():
            return []
        results = json.loads(self.indeed_fixture.read_text(encoding="utf-8"))
        return [
            result
            for result in results
            if search_term.lower() in result.get("matched_term", "").lower()
            and location.lower() in result.get("location", "").lower()
        ]
