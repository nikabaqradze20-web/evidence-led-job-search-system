import csv
import json
import re
from collections import defaultdict
from pathlib import Path

from .email_parser import parse_email_file
from .models import Posting
from .privacy import scan_paths


def _normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def _vacancy_id(posting: Posting) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", f"{posting.company}-{posting.title}".lower()).strip("-")
    return f"{slug}_2026-08-03"


def _write_discovered(path: Path, postings: list[Posting]) -> None:
    lines = ["# Synthetic discovered vacancies", "", "Generated from public synthetic email fixtures.", ""]
    for posting in postings:
        lines.append(
            f"- **{posting.title}** — {posting.company} — {posting.source} — "
            f"{posting.source_url} — {posting.match_reason}."
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_tracker(path: Path, postings: list[Posting]) -> None:
    fieldnames = [
        "vacancy_id",
        "company",
        "job_title",
        "status",
        "recommendation",
        "date_found",
        "deadline",
        "source_url",
        "next_action",
        "notes",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for posting in postings:
            writer.writerow(
                {
                    "vacancy_id": _vacancy_id(posting),
                    "company": posting.company,
                    "job_title": posting.title,
                    "status": "new",
                    "recommendation": "",
                    "date_found": "2026-08-03",
                    "deadline": "unknown",
                    "source_url": posting.source_url,
                    "next_action": "review",
                    "notes": "synthetic pipeline output",
                }
            )


def run_pipeline(input_dir: Path, output_dir: Path, run_id: str = "synthetic-demo") -> dict:
    """Run the local public demo and return a serializable run summary."""

    output_dir.mkdir(parents=True, exist_ok=True)
    all_postings: list[Posting] = []
    source_summary: dict[str, dict[str, object]] = {}

    for email_path in sorted(input_dir.glob("*.txt")):
        email_format, postings = parse_email_file(email_path)
        source = postings[0].source if postings else email_path.name
        source_summary[source] = {"format": email_format, "postings_found": len(postings)}
        all_postings.extend(postings)

    seen: set[tuple[str, str]] = set()
    unique: list[Posting] = []
    duplicates = 0
    for posting in all_postings:
        key = (_normalize(posting.company), _normalize(posting.title))
        if key in seen:
            duplicates += 1
            continue
        seen.add(key)
        unique.append(posting)

    extraction = {
        "run_id": run_id,
        "sources": source_summary,
        "postings": [posting.to_dict() for posting in unique],
        "deduplication": {
            "within_run_duplicates": duplicates,
            "already_seen": 0,
            "kept": len(unique),
        },
    }
    (output_dir / "extraction-output.json").write_text(json.dumps(extraction, indent=2) + "\n", encoding="utf-8")
    _write_discovered(output_dir / "discovered.md", unique)
    _write_tracker(output_dir / "tracker.csv", unique)

    scanned_files = [input_dir, output_dir / "extraction-output.json", output_dir / "discovered.md", output_dir / "tracker.csv"]
    findings = scan_paths(scanned_files, root=output_dir.parent)
    privacy_report = {
        "clean": not findings,
        "findings": [{"path": item.path, "pattern": item.pattern} for item in findings],
    }
    (output_dir / "privacy-report.json").write_text(json.dumps(privacy_report, indent=2) + "\n", encoding="utf-8")

    return {
        "run_id": run_id,
        "postings_found": len(all_postings),
        "duplicates_removed": duplicates,
        "postings_kept": len(unique),
        "privacy_clean": not findings,
        "output_dir": str(output_dir),
    }
