# Evidence-Led Job Search System

This repository is the public portfolio edition of a private, evidence-led job-search workflow developed with Claude Code. It connects job-alert discovery, vacancy extraction, fit evaluation, tracking, and application-material tailoring while keeping all external actions under human control.

All candidate, vacancy, employer, and application content in this repository is synthetic.

## How it works

1. When manually invoked, Claude searches connected Gmail job-alert emails and job platforms for new vacancies.
2. Relevant vacancies are extracted and converted into structured records.
3. Duplicate vacancies are identified and the tracker is updated.
4. Each vacancy is evaluated against the candidate profile and evidence library.
5. Suitable vacancies are presented for human review.
6. After approval, the system selects supporting evidence and drafts a tailored CV and cover letter.
7. The human reviews all claims and submits the application manually.

In the private workflow, Gmail and job-platform access is provided through account-specific Claude connections. The public repository uses synthetic fixtures and contains no credentials or live application data.

## What it demonstrates

- A source-of-truth profile and evidence library.
- Normalized vacancy records with explicit uncertainty.
- Requirement-by-requirement fit evaluation.
- Evidence selection before drafting application materials.
- Vacancy-specific CV and cover-letter workflows with explicit claim boundaries.
- Human approval gates before external actions.
- Plain-file persistence that remains inspectable in Git and VS Code.

## Architecture

```mermaid
flowchart LR
    A[Gmail alerts and job-platform results]
    B[Extract, normalize, and deduplicate]
    C[Create vacancy record]
    D[Evaluate fit against profile and evidence]
    E{Human decision}
    F[Select evidence and tailor CV and cover letter]
    G{Human factual review}
    H[Submit manually and update tracker]

    A --> B --> C --> D --> E
    E -->|Approve| F --> G -->|Approve| H
    E -->|Reject| H
```
## Folder map

| Path | Purpose |
|---|---|
| `skills/` | Public prompt/workflow specifications for the core stages |
| `sample-data/` | Synthetic inputs suitable for demonstrations |
| `examples/` | Synthetic downstream outputs |
| `templates/` | Minimal reusable file contracts |
| `WALKTHROUGH.md` | End-to-end synthetic demonstration |
| `ARCHITECTURE.md` | State model, controls, and design decisions |
| `PRIVACY.md` | Publication and redaction policy |
| `jobsearch_demo/` | Dependency-free local parser, pipeline, privacy scanner, and connector boundary |
| `run_demo.py` | Local command-line entry point |
| `tests/` | Standard-library unit tests |

## Deliberate scope

This portfolio edition is a reviewable design and synthetic demonstration, not a live connector package. The private system uses account-specific job-alert sources through Claude; those integrations, credentials, real vacancies, personal contact details, and historical tracker rows are intentionally absent here. The email fixtures and extraction JSON show the intended boundary without claiming a production parser.

## Run the local demo

The code uses only the Python standard library. From the repository root:

```powershell
python run_demo.py --input sample-data/emails --output demo-output
python -m unittest discover -s tests -v
```

The demo writes `extraction-output.json`, `discovered.md`, `tracker.csv`, and `privacy-report.json` to the selected output directory. It does not connect to Gmail, call Indeed, send messages, or submit applications.

## Claude connector boundary

`jobsearch_demo/connector.py` defines the small interface the private Claude-connected workflow would need: `search_threads()` for Gmail-like threads and `search_jobs()` for Indeed-like results. `FixtureClaudeConnector` implements the same shape with local synthetic fixtures only. It performs no network access and contains no credentials.

## Design principles

1. Evidence before prose.
2. Missing evidence is reported, not silently filled.
3. Transferable capability is separated from direct sector experience.
4. Recommendations are gated by administrative blockers and essential requirements.
5. Drafting never implies submission.
6. Every generated artifact has a clear owner and overwrite rule.
