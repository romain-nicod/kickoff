# Defects

**Every error an agent makes, on every project, becomes a `[DEFECT]` issue.** Decided by Romain
on 27/09/2026, after the same step (`bin/ci` and its `ci/local` status) was skipped twice.

A **bug** is the product doing the wrong thing. A **defect** is the work done the wrong way: a
step skipped, a rule ignored, a claim reported without being checked, a file written in the wrong
place, a command that did something other than announced.

## When

In the session that made the error, **as soon as it is noticed** — by the agent or by Romain —
and before the fix. The fix comes after; the ticket is what survives the conversation.

## Where

- In the repository of the project, on the `.github/ISSUE_TEMPLATE/defect.md` template, label
  `type:defect`.
- An error with no repository (the vault, `~/.claude`, a machine): in `romain-nicod/kickoff`.

## What it says

1. **What happened** — facts, date, who noticed it, links.
2. **Impact** — what it cost or could have cost.
3. **Why** — the cause, and why the existing rule did not stop it.
4. **Previous occurrences** — linked; a repeat means the previous prevention failed.
5. **Prevention** — preferably a mechanism (a check that fails, a hook, a template field)
   rather than one more sentence in a document.

## The daily review

A scheduled agent reads the open `type:defect` issues of every repository of the account, every
day:

1. On each defect without a proposal, it comments a **remediation**: the change, the file, the
   reason it would have prevented this occurrence. It groups defects of the same kind.
2. On each defect labelled `remediation:validée` by Romain, it applies the remediation in a pull
   request (never merged by the agent) and links it.
3. It writes a summary in the vault: what was proposed, what waits for Romain.

🔴 **Romain alone validates.** The agent proposes, never applies an unvalidated remediation, and
never closes a defect: Romain closes it once the remediation is merged.
