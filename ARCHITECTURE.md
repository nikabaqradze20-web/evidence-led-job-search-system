# Architecture and operating model

## Pipeline

1. **Discover**: collect candidate vacancies from approved sources and deduplicate them against discovery history, inbox records, and tracker rows. In the public edition, `sample-data/emails/` stands in for the Claude-connected mailbox.
2. **Ingest**: preserve the original vacancy text while separating essential requirements, desirable requirements, responsibilities, and practical conditions.
3. **Evaluate**: check administrative blockers first, then classify requirements and responsibilities against the evidence library.
4. **Review**: keep recommendation and approval as separate states. No downstream drafting starts until the user approves the vacancy.
5. **Select evidence**: map each essential requirement to the strongest verified source and record gaps and prohibited claims.
6. **Draft**: create a vacancy-specific CV and letter from the approved evidence selection.
7. **Track**: persist status, recommendation, next action, and source metadata in a small CSV index.

## Evidence taxonomy

Factual claims are classified as:

- **Evidenced**: directly supported by a named source.
- **Partially evidenced**: related support exists, but the claim is broader than the evidence.
- **Not evidenced**: the source set is silent; this is not treated as proof of absence.
- **Bounded**: a known limit is recorded, such as a method not yet run end to end.

For a requirement, the evaluator uses `strong match`, `partial match`, `not evidenced`, or `clear gap`. For motivations and working-style preferences it uses a separate scale so silence is not mistaken for a capability failure.

## State model

```text
new -> considering -> approved -> preparing -> applied -> interview -> offer
  \-> rejected
  \-> closed
```

The state model is intentionally conservative. A recommendation such as `apply` is not the same as approval, and approval is not the same as submission.

## File contracts

- Profile and evidence files are read-only source material.
- Vacancy records are immutable after ingestion unless the user explicitly requests a correction.
- Fit evaluations are persistent decision records.
- Evidence selections are the handoff between evaluation and drafting.
- Derived CVs and letters are created as new files and are never written back into the master profile.
- The tracker has one row per vacancy ID.

## Quality controls

- Exact source citation for substantive claims.
- Explicit administrative blocker section.
- No fabricated skills, dates, employers, metrics, or language levels.
- Distinct direct versus transferable experience.
- Required current-role coverage in tailored CVs.
- One-page and banned-phrase checks for CVs and letters.
- No external action without explicit approval.

## Why plain files

Markdown, YAML, and CSV keep the workflow portable, diffable, and easy to inspect. A database or service layer could improve scale, but would add operational complexity before the core reasoning and evidence controls are stable.

## Public-demo boundary

The synthetic email fixtures and `examples/extraction-output.json` make the discovery-to-record handoff inspectable without storing Gmail message IDs or connecting to an account. The public edition does not claim that extraction, deduplication, or validation are deterministic software components.
