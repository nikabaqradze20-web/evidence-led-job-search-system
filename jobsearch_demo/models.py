from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Posting:
    """A normalized vacancy candidate extracted from a source email."""

    title: str
    company: str
    location: str
    source: str
    source_url: str
    match_reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
