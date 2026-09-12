# Architecture Decision Records

One wiki page per structural decision, `ADR-NNNN-<slug>.md`, numbered,
never deleted, written in `docs/wiki/` in the pull request that takes
the decision. A decision
that is reversed gets a new record saying so — the old one stays, with
its status changed to `Superseded by 000X`.

**What deserves an ADR**: a choice that would surprise someone reading
the code, that would be expensive to reverse, or that two of you
disagreed about. Not "we used the framework's default" — everybody does.
Yes to "we replaced the ingestion pipeline with a hand-curated dataset".

**Format**: copy [`ADR-0000-template.md`](ADR-0000-template.md), fill it in,
keep it under a page. An ADR nobody reads is a paragraph nobody wrote.

| # | Decision | Status |
|---|---|---|
| | | |
