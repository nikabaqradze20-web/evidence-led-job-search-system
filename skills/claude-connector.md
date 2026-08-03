# Claude connector boundary

The private workflow has access to Gmail and Indeed through Claude. This public repository does not include that account connection.

`jobsearch_demo/connector.py` defines the public boundary:

- `search_threads(query)` returns Gmail-like plaintext threads.
- `search_jobs(search_term, location)` returns Indeed-like result records.

`FixtureClaudeConnector` is an offline implementation backed by `sample-data/emails/` and `sample-data/indeed-results.json`. A future private adapter could call Claude tools at this boundary without changing the parser or downstream output contracts.

No credentials, MCP configuration, network calls, or account identifiers belong in this repository.
