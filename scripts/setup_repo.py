#!/usr/bin/env python3
"""Configure the GitHub repository itself — not its issues.

The template writes files; this script makes GitHub enforce what they
say. A CONTRIBUTING.md that promises every branch is reviewed, on a
repository where `main` accepts a direct push, is an intention.

    python3 scripts/setup_repo.py
    python3 scripts/setup_repo.py --dry-run

Five things, in this order:

  1. the labels of .github/labels.yml — the `type:` and `status:`
     families, which the issue templates apply and which nothing else
     creates. The `epic:`, `prio:`, `pts:` and `batch:` families are NOT
     here: scripts/create_issues.py generates them from the
     specification. See docs/LABELS.md;
  2. GitHub's nine stock labels, deleted — `enhancement`, `question`,
     `wontfix`, `good first issue`… A repository nobody cleaned carries
     more labels it did not choose than labels it did. A stock label
     still carried by an issue is KEPT, and the script says so: deleting
     it would silently strip that issue;
  3. the wiki, enabled;
  4. the pull-request settings — squash only, branch deleted on merge;
  5. `main` protected — no force-push, no deletion, and an approving
     review on every pull request.

ON A SOLO PROJECT, requiring an approving review is theatre: GitHub
never lets you approve your own pull request, so every merge becomes an
administrator bypass, and a rule bypassed at every merge teaches that
rules are bypassed. The script detects a solo repository — `ROLES.md` is
absent, `bin/kickoff` having removed it — and requires zero reviews
instead. What remains protected is what still means something alone: no
force-push, no deletion of the branch. Override either way with
`--reviews N`.

Idempotent: run it as often as you like.

WHAT MAY LEGITIMATELY FAIL — branch protection is unavailable on a
PRIVATE repository on a free GitHub plan. That is a refusal, not a bug:
the script says so and carries on. Everything else works on any plan.

REQUIREMENT — the gh token needs the `repo` scope, and branch protection
needs administration rights on the repository.

Runs on a plain Python 3, no dependency: labels.yml is parsed as the
flat list it is, on purpose.
"""

import argparse
import json
import sys
from pathlib import Path

from kickoff_lib import gh, repo

ROOT = Path(__file__).resolve().parent.parent
LABELS = ROOT / ".github" / "labels.yml"
REPO = repo()


def read_labels():
    """The `- name:` / `color:` / `description:` entries of labels.yml.

    Deliberately not a YAML parser: the file is a flat list, and adding a
    dependency to a template that must run anywhere is a bad trade.
    """
    if not LABELS.exists():
        sys.exit(f"{LABELS.relative_to(ROOT)} is missing")

    entries, current = [], None
    for raw in LABELS.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- name:"):
            if current:
                entries.append(current)
            current = {"name": unquote(line.partition(":")[2])}
        elif current and line.startswith(("color:", "description:")):
            key, _, value = line.partition(":")
            current[key.strip()] = unquote(value)
    if current:
        entries.append(current)
    return entries


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


# The labels GitHub creates with every repository. None of them is ours,
# none of them is in labels.yml, and on a fresh repository they outnumber
# the set the project actually chose. They are removed rather than left to
# rot: a label that exists is a label someone will eventually apply.
GITHUB_STOCK_LABELS = [
    "bug", "documentation", "duplicate", "enhancement", "good first issue",
    "help wanted", "invalid", "question", "wontfix",
]


def labels_in_use():
    """Every label carried by at least one issue, open or closed."""
    result = gh(["issue", "list", "--repo", REPO, "--state", "all",
                 "--limit", "1000", "--json", "labels"], check=False)
    if result.returncode != 0:
        return None
    return {label["name"]
            for issue in json.loads(result.stdout)
            for label in issue["labels"]}


def remove_stock_labels(dry_run):
    """Delete GitHub's defaults — except any an issue still carries.

    `bug` is the one that matters: the template used to apply it, and this
    template now applies `type:bug`. Deleting a label strips it from every
    issue that has it, with no warning and no undo, so a stock label still
    in use is reported and left alone. Rename it by hand, or keep it.
    """
    declared = {label["name"] for label in read_labels()}
    in_use = labels_in_use()
    if in_use is None:
        print("  SKIP    stock labels — could not read the issues")
        return

    for name in GITHUB_STOCK_LABELS:
        if name in declared:
            continue
        if name in in_use:
            print(f"  KEPT    {name} — still carried by an issue; "
                  f"relabel those issues first")
            continue
        if dry_run:
            print(f"  delete  {name}")
            continue
        result = gh(["label", "delete", name, "--repo", REPO, "--yes"],
                    check=False)
        if result.returncode == 0:
            print(f"  deleted {name}")
        elif "not found" in result.stderr.lower():
            print(f"  absent  {name}")
        else:
            print(f"  FAILED  {name} — {result.stderr.strip()}")


def default_branch():
    result = gh(["repo", "view", REPO, "--json", "defaultBranchRef"])
    return json.loads(result.stdout)["defaultBranchRef"]["name"]


def apply_labels(dry_run):
    for label in read_labels():
        name = label["name"]
        if dry_run:
            print(f"  label   {name}")
            continue
        # --force updates an existing label instead of failing, which is
        # what makes a second run harmless.
        result = gh(["label", "create", name, "--repo", REPO, "--force",
                     "--color", label.get("color", "6E665B"),
                     "--description", label.get("description", "")],
                    check=False)
        state = "label  " if result.returncode == 0 else "FAILED "
        print(f"  {state} {name}")
        if result.returncode != 0:
            print(f"          {result.stderr.strip()}")


def enable_wiki(dry_run):
    if dry_run:
        print("  wiki    enabled")
        return
    result = gh(["repo", "edit", REPO, "--enable-wiki"], check=False)
    if result.returncode == 0:
        print("  wiki    enabled")
    else:
        print(f"  FAILED  wiki — {result.stderr.strip()}")


def pull_request_settings(dry_run):
    """Squash only, and the branch deleted once merged.

    One commit per story on `main` keeps the history readable as a list
    of stories; a merge commit per story does not.
    """
    flags = ["--enable-squash-merge", "--enable-merge-commit=false",
             "--enable-rebase-merge=false", "--delete-branch-on-merge"]
    if dry_run:
        print("  PRs     squash only, branch deleted on merge")
        return
    result = gh(["repo", "edit", REPO] + flags, check=False)
    if result.returncode == 0:
        print("  PRs     squash only, branch deleted on merge")
    else:
        print(f"  FAILED  PR settings — {result.stderr.strip()}")


def required_reviews(asked):
    """How many approving reviews a pull request needs.

    `--reviews` wins. Otherwise: none if nobody else can review.
    """
    if asked is not None:
        return asked
    solo = not (ROOT / "ROLES.md").exists()
    if solo:
        print("  solo repository (no ROLES.md) — 0 review required, "
              "since you cannot approve your own PR")
    return 0 if solo else 1


def protect_default_branch(branch, reviews, dry_run):
    if dry_run:
        print(f"  branch  {branch} protected — {reviews} review(s), "
              f"no force-push")
        return

    payload = json.dumps({
        "required_status_checks": None,
        "enforce_admins": False,
        "required_pull_request_reviews":
            {"required_approving_review_count": reviews} if reviews else None,
        "restrictions": None,
        "allow_force_pushes": False,
        "allow_deletions": False,
    })
    result = gh(["api", "-X", "PUT", "-H", "Accept: application/vnd.github+json",
                 f"repos/{REPO}/branches/{branch}/protection",
                 "--input", "-"], check=False, stdin=payload)

    if result.returncode == 0:
        print(f"  branch  {branch} protected — {reviews} review(s), "
              f"no force-push, no deletion")
        return

    error = result.stderr.strip()
    print(f"  SKIP    {branch} is NOT protected")
    if "Upgrade to GitHub Pro" in error or "404" in error:
        print("          GitHub does not offer branch protection on a "
              "PRIVATE repository")
        print("          on a free plan. Three options, in this order: make "
              "the repository")
        print("          public, take a paid plan, or hold the rule by hand "
              "— nothing")
        print("          will enforce it technically.")
    elif "403" in error:
        print("          the gh token lacks administration rights on this "
              "repository.")
        print("          Run: gh auth refresh -s repo --hostname github.com")
    else:
        print(f"          {error}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--reviews", type=int, default=None,
                        help="approving reviews required on a pull request "
                             "(default: 0 on a solo repository, 1 otherwise)")
    args = parser.parse_args()

    branch = default_branch()
    print(f"\n{REPO} · default branch {branch}\n")

    # Never assume `main`: a repository created before 2020, or from a
    # `git init` on a machine whose init.defaultBranch is still master,
    # would silently get no protection at all.
    if branch != "main":
        print(f"  ⚠️  the default branch is `{branch}`, not `main`. Every "
              f"document here")
        print(f"      says `main` — rename it, or the two disagree.\n")

    print("Labels")
    apply_labels(args.dry_run)
    print("GitHub's stock labels")
    remove_stock_labels(args.dry_run)
    print("Wiki")
    enable_wiki(args.dry_run)
    print("Pull requests")
    pull_request_settings(args.dry_run)
    print("Branch protection")
    protect_default_branch(branch, required_reviews(args.reviews), args.dry_run)

    if args.dry_run:
        print("\nDry run — nothing was written.")
        return

    print("""
Done. What is left for you:

  The wiki is enabled but empty — GitHub creates its first page only
  when a human writes one. Open the Wiki tab and paste the plan of
  docs/WIKI.md, or the tab stays a dead link.
""")


if __name__ == "__main__":
    main()
