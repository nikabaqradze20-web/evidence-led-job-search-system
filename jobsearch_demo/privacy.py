import re
from dataclasses import dataclass
from pathlib import Path


PATTERNS: dict[str, re.Pattern[str]] = {
    "personal_email": re.compile(r"(?i)\b[A-Z0-9._%+-]+@(?!example\.invalid\b)[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "phone_number": re.compile(r"(?<!\w)\+\d[\d ()-]{7,}\d(?!\w)"),
    "linkedin_profile": re.compile(r"(?i)linkedin\.com/(?:in|pub)/"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client_secret|refresh_token|password)\s*[:=]"),
    "private_key": re.compile(r"-----BEGIN [^-]+ PRIVATE KEY-----"),
    "absolute_windows_path": re.compile(r"[A-Za-z]:\\Users\\"),
}


@dataclass(frozen=True)
class PrivacyFinding:
    path: str
    pattern: str


def scan_paths(paths: list[Path], root: Path) -> list[PrivacyFinding]:
    findings: list[PrivacyFinding] = []
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
        elif path.is_file():
            files.append(path)

    for file_path in sorted(set(files)):
        text = file_path.read_text(encoding="utf-8", errors="replace")
        try:
            relative = str(file_path.relative_to(root))
        except ValueError:
            # Keep reports useful without exposing an absolute local path.
            relative = file_path.name
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(PrivacyFinding(path=relative, pattern=name))
    return findings
