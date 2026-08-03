import json
import tempfile
import unittest
from pathlib import Path

from jobsearch_demo.email_parser import parse_email_file
from jobsearch_demo.connector import FixtureClaudeConnector
from jobsearch_demo.pipeline import run_pipeline
from jobsearch_demo.privacy import scan_paths


ROOT = Path(__file__).resolve().parents[1]
EMAIL_DIR = ROOT / "sample-data" / "emails"


class PipelineTests(unittest.TestCase):
    def test_digest_fixture_contains_two_postings(self) -> None:
        email_format, postings = parse_email_file(EMAIL_DIR / "linkedin-alert.txt")
        self.assertEqual(email_format, "digest")
        self.assertEqual(len(postings), 2)
        self.assertEqual(postings[0].company, "Northstar Insights")

    def test_single_posting_fixture_contains_one_posting(self) -> None:
        email_format, postings = parse_email_file(EMAIL_DIR / "stepstone-alert.txt")
        self.assertEqual(email_format, "single-posting")
        self.assertEqual(len(postings), 1)
        self.assertEqual(postings[0].title, "Research Analyst")

    def test_pipeline_writes_deterministic_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "output"
            summary = run_pipeline(EMAIL_DIR, output_dir)
            self.assertEqual(summary["postings_found"], 3)
            self.assertEqual(summary["duplicates_removed"], 0)
            self.assertTrue(summary["privacy_clean"])
            extraction = json.loads((output_dir / "extraction-output.json").read_text(encoding="utf-8"))
            self.assertEqual(len(extraction["postings"]), 3)
            self.assertTrue((output_dir / "tracker.csv").exists())

    def test_public_fixtures_are_privacy_clean(self) -> None:
        findings = scan_paths([ROOT / "sample-data", ROOT / "examples"], root=ROOT)
        self.assertEqual(findings, [])

    def test_fixture_connector_matches_claude_boundary_without_network(self) -> None:
        connector = FixtureClaudeConnector(
            EMAIL_DIR,
            ROOT / "sample-data" / "indeed-results.json",
        )
        threads = connector.search_threads("newer_than:1d")
        jobs = connector.search_jobs("research analyst", "Germany")
        self.assertEqual(len(threads), 2)
        self.assertEqual(len(jobs), 1)
        self.assertEqual(threads[0].thread_id, "linkedin-alert")


if __name__ == "__main__":
    unittest.main()
