# Skill: discover vacancies

## Purpose

Build a reviewable shortlist from approved vacancy sources without evaluating fit or mutating the vacancy inbox.

## Required controls

1. Use only configured sources and preserve source links.
2. Extract title, employer, location, work mode, and a traceable match reason.
3. Deduplicate within the run and against prior discovery, inbox, and tracker records.
4. Filter only by explicit policy rules; retain ambiguous candidates for review.
5. Report before/after counts and already-seen items.

## Output

Write a dated shortlist. Discovery does not approve, reject, ingest, or contact anyone.

