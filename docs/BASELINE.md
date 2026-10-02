# The baseline

What every repository of the account guarantees, and what proves it.

The list itself is [`baseline.yml`](../baseline.yml) at the root, read by
[`scripts/audit_baseline.py`](../scripts/audit_baseline.py). This page says why it
exists in that form, and what it deliberately does not do.

---

## Why a manifest, and not one more document

A rule written in prose is read once, on the day it is written. Nothing re-reads it,
and nothing notices when a repository drifts away from it.

Measured on 02/10/2026, across the account: **ten repositories carried their own copy
of this template's method documents** — twelve to seventeen documents each, around a
hundred and forty copies. Twelve of seventeen had already diverged in one of them, and
a repository created four days earlier already had five. No copy was declared
authoritative, so each was a candidate truth.

Adding another document would have reproduced exactly that. So the baseline is a list
of entries, each one naming **the command that proves it**, and a script that runs them
all.

## Three moments, not one

A rule applies at a moment. Mixing the three is what makes a checklist unusable.

| `when` | What it means | Who applies it |
|---|---|---|
| `birth` | True from the repository's first day | `scripts/setup_repo.py`, at creation |
| `always` | Re-proved continuously, because it decays | the scheduled audit |
| `publication` | Read the day the repository goes public | a human, once, with the machine's preparation |

The publication moment exists on its own because its risks are the ones no scanner
finds: an identifiable third party, the name of a private project, a figure that was
never meant to be read outside. A secret scan is blind to all three.

## What an entry carries

```yaml
- id: "required-checks"
  statement: "No pull request is mergeable without named checks green"
  severity: "blocking"
  when: "birth"
  check: "required_checks"
  proof: "gh api repos/OWNER/NAME/branches/main/protection --jq .required_status_checks"
  note: "..."
```

`severity` has two values and they mean different things. **`blocking`** makes the audit
exit non-zero: something is wrong now. **`finding`** is a gap to close, in its own time.
Keeping them apart is what stops `blocking` from becoming noise — the first run of the
audit called eleven private repositories without a licence `blocking`, next to a public
repository with none, and the signal that mattered drowned.

🔴 **An entry with `check: none` is not an invariant.** It is an intention waiting for a
check, the audit counts it apart, and it is never green. Three entries are in that state
on purpose: the scheduled secret scan, the publication gate, and the accepted French
names. A manifest that hides its holes is worse than a shorter one.

## Running it

```bash
python3 scripts/audit_baseline.py                      # every repository
python3 scripts/audit_baseline.py --repo OWNER/NAME     # one
python3 scripts/audit_baseline.py --only required-checks
python3 scripts/audit_baseline.py --out ~/reports/baseline.md
```

It reads GitHub through `gh` for the settings, and the **local clone** for everything
that lives in the files and in the history. Clones are found **by their remote, never by
their folder name**: a folder is named by hand, and matching names missed ten of
twenty-six clones on the first run — `site-pef-blog` lives in `pef-blog`, and
`sysadmin-macstudio-ops` lives outside `code/` altogether.

A repository with no clone is reported `--`, never as a pass. **An absent check is not a
green one.**

🔴 **The report is private, and the script enforces it.** It names which repository is
late, so writing it inside a Git work tree is refused. The script is public — that is the
point of it living here — its output is not.

## What it cannot see

Printed at the end of every run, so that nobody concludes more than it proves:

- the history of a repository it has no clone of;
- whether a green check was green yesterday: it says today, not since;
- the entries with `check: none`;
- anything no pattern describes — a passphrase in plain words, an internal identifier.
  **A check that finds nothing has found nothing.**

And one thing worth saying twice: a green `no-tracked-runtime-or-secret-files` says
nothing about the history. A secret committed once stays leaked; it is revoked and
rotated at the source, never removed by a `git rm`.

## What the first run found, 02/10/2026

Twenty-six repositories, twenty entries, five hundred and twenty checks. The figures are
in the private report; the shape of them belongs here, because it is why several of these
entries exist at all:

- **twenty-two repositories of twenty-six let a pull request merge with no required
  check.** `scripts/setup_repo.py` sends `required_status_checks: None`, so protection
  exists and requires nothing. On one project this let two breaking defects reach `main`
  in a single day;
- **sixteen leave `main` unprotected**, and eighteen still allow a squash merge;
- **nineteen carry a commit that mentions the assistant**, mostly `Co-Authored-By:`
  lines — the rule of 12/09/2026 was written, never enforced;
- **ten carry a Creative Commons licence on code**, which says nothing about source,
  patents or warranty;
- **twenty-four are missing at least one label** the issue templates apply. GitHub drops
  a missing label silently, which is how the `[DEFECT]` rule became unapplicable on a
  repository without anyone seeing an error.

Four of those five are things that were already decided. None of them was verified.
