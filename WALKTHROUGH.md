# Synthetic walkthrough

This walkthrough shows the intended public demo without requiring Gmail, Indeed, employer accounts, or private candidate data.

## 1. Start with synthetic alert emails

The files in `sample-data/emails/` imitate two source formats:

- a digest containing multiple postings;
- a single-posting alert with an opaque detail URL.

The inputs are deliberately marked synthetic and use `example.invalid` links.

## 2. Extract and normalize

`examples/extraction-output.json` is the expected extraction result for the two email fixtures. It records the source, extracted title, company, location, link, and match reason. `examples/normalized-vacancy.md` shows how one extracted posting becomes a structured vacancy record.

## 3. Track state

`examples/tracker-state.csv` demonstrates that discovery, review, approval, and rejection are separate states. The tracker is an index; the detailed reasoning remains in the fit-evaluation and evidence-selection artifacts.

## 4. Evaluate before drafting

The synthetic vacancy is evaluated in `examples/fit-evaluation.md`. The recommendation is `apply — realistic stretch` because the core research capability is evidenced while commercial-sector experience remains a bounded gap.

## 5. Select evidence

`examples/evidence-selection.md` maps essential requirements to source evidence and records claims that must not be made.

## 6. Draft application materials

- `examples/tailored-cv.md` demonstrates a concise, one-page-oriented CV structure.
- `examples/cover-letter.md` demonstrates contextual reasoning rather than repeating the CV.
- Both are synthetic drafts and require human review before any real use.

## 7. What is not demonstrated

This walkthrough does not connect to Gmail, call Indeed, send messages, submit applications, or claim deterministic parsing. Those boundaries are part of the portfolio design rather than hidden implementation gaps.

