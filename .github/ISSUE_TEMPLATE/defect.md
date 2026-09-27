---
name: Defect
about: An error in HOW the work was done (agent or process), not in what the product does
title: "[DEFECT] "
labels: "type:defect"
---

<!-- Title: [DEFECT] <the error, in a few words>. Filed by the agent that made the
     error, or noticed it, in the same session — before fixing anything else.
     A product misbehaving is a [BUG]; a step skipped, a rule ignored, a wrong claim,
     a check reported green without being run, is a [DEFECT]. -->

## What happened

<!-- Facts only: date and time, project, session, what was done or skipped, who
     noticed it and how. Link the PR, commit or log. -->

- Date:
- Noticed by:
- Where:

## Impact

<!-- What it cost or could have cost: a blocked merge, a lie in a report, lost
     work, a secret exposed. "None" is a valid answer if it is true. -->

## Why

<!-- The cause, not the symptom. Which rule existed and why it did not stop the
     error: unknown, not read, read but not applied, or no rule at all. -->

## Previous occurrences

<!-- Earlier defects of the same kind, linked. "First time" if none. A second
     occurrence means the previous prevention did not work: say why. -->

## Prevention

<!-- What would make it impossible, or at least visible, next time. Prefer a
     mechanism (a script that fails, a hook, a check in `bin/ci`, a template field)
     over a sentence in a document. Name the file to change. -->

## Remediation

<!-- Filled by the daily defect review: the proposed change, the file, the PR if
     one is opened. Romain validates by adding the `remediation:validée` label. -->

- [ ] Proposed
- [ ] Validated by Romain
- [ ] Applied (PR, commit or document linked)
