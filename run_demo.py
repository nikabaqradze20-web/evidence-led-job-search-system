import argparse
import json
from pathlib import Path

from jobsearch_demo.pipeline import run_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the synthetic public job-search pipeline.")
    parser.add_argument("--input", type=Path, default=Path("sample-data/emails"), help="Synthetic email directory")
    parser.add_argument("--output", type=Path, default=Path("demo-output"), help="Output directory")
    args = parser.parse_args()

    summary = run_pipeline(args.input, args.output)
    print(json.dumps(summary, indent=2))
    return 0 if summary["privacy_clean"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
