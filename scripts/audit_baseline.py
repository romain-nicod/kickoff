#!/usr/bin/env python3
"""Prove the baseline of baseline.yml on every repository of the account.

A rule written in a document decays without anyone noticing. This script
reads the manifest and, for each repository, runs the check each entry
names — so a decision taken once is verified on its own, including on the
repositories created after it was taken.

    python3 scripts/audit_baseline.py
    python3 scripts/audit_baseline.py --repo romain-nicod/kickoff
    python3 scripts/audit_baseline.py --only licence-present,required-checks
    python3 scripts/audit_baseline.py --out ~/reports/baseline.md

WHAT IT READS, AND WHAT IT NEEDS

  * GitHub, through `gh` — the repository's settings, its protection, its
    labels. Needs the `repo` scope, and administration rights to read
    branch protection;
  * the local clone, for everything that lives in the files and in the
    history. A repository with no clone under --clones is reported as
    `no clone`, never as a pass. An absent check is not a green one.

🔴 THE REPORT IS PRIVATE. It names which repository is late, so it must
not land in a repository: the script REFUSES to write inside a Git work
tree. The script is public, its output is not.

WHAT IT CANNOT SEE — printed at the end of every run, on purpose:

  * the history of a repository it has no clone of;
  * whether a green check was green yesterday: it says today, not since;
  * the three entries with `check: none`, which it counts apart and never
    turns into a pass;
  * anything no pattern describes — a passphrase in plain words, an
    internal identifier. A check that finds nothing has found nothing.

Exit code: 1 if a blocking entry fails anywhere, 0 otherwise. The exit
code carries the decision, so nothing is piped after this command.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from kickoff_lib import gh  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "baseline.yml"
LABELS = ROOT / ".github" / "labels.yml"
# The roots where clones live on this machine. `~/Documents/Claude` and
# `~/.claude` are listed because two repositories are clones of themselves
# at a root: the vault, and the Claude configuration.
DEFAULT_CLONES = [Path.home() / "Documents" / "Claude",
                  Path.home() / "Documents" / "Claude" / "code",
                  Path.home() / "Documents" / "Claude" / "projects",
                  Path.home() / ".claude"]

# The generic documents of this template. A copy of one of them in a
# project repository is a second truth, which is what no-copied-method-docs
# looks for. DESIGN_CHECKLIST.md is absent on purpose: a project fills it
# in for its own product, so its copy is the deliverable.
GENERIC_DOCS = {
    "BOARD.md", "CODE_HYGIENE.md", "DEPLOYMENT.md", "DEPLOIEMENT.md",
    "ENVIRONMENTS.md", "LABELS.md", "NAMING.md", "PARALLEL_WORK.md",
    "PRD.md", "PROMPTS.md", "QUALITY.md", "RECETTE.md", "SCHEMA.md",
    "SECRETS.md", "SYSTEM_DESIGN.md", "TESTS.md", "WIKI.md",
}

# Markers of French, not a grammar. Two stopword hits or one accent
# typical of French makes a subject suspect: it finds French, it never
# proves English.
FR_WORDS = re.compile(
    r"\b(le|la|les|des|une|pour|avec|dans|sur|qui|est|pas|plus|sans|sont|"
    r"leur|cette|chaque|aucun|tout|toute|donc|mais|puis)\b", re.I)
FR_ACCENTS = re.compile(r"[éèêàçùûîôœ]", re.I)

PASS, FAIL, SKIP = "pass", "fail", "skip"


# --------------------------------------------------------------------------
# the manifest, and the labels, read as the flat lists they are
# --------------------------------------------------------------------------

def unquote(value):
    return value.strip().strip('"').strip("'")


def read_manifest():
    """The `- id:` blocks of baseline.yml, in file order.

    Deliberately not a YAML parser, for the reason .github/labels.yml
    gives: a template that must run anywhere does not earn a dependency.
    """
    if not MANIFEST.exists():
        sys.exit(f"{MANIFEST.name} is missing")
    keys = ("statement:", "severity:", "when:", "check:", "proof:", "note:")
    entries, current = [], None
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- id:"):
            if current:
                entries.append(current)
            current = {"id": unquote(line.partition(":")[2])}
        elif current and line.startswith(keys):
            key, _, value = line.partition(":")
            current[key.strip()] = unquote(value)
    if current:
        entries.append(current)
    missing = [e["id"] for e in entries if "check" not in e]
    if missing:
        sys.exit(f"entries without a check key: {', '.join(missing)}")
    return entries


def declared_labels():
    if not LABELS.exists():
        return set()
    return {unquote(line.partition(":")[2])
            for line in LABELS.read_text(encoding="utf-8").splitlines()
            if line.strip().startswith("- name:")}


# --------------------------------------------------------------------------
# facts: GitHub on one side, the clone on the other
# --------------------------------------------------------------------------

def template_slug():
    """`owner/name` of the repository this script lives in, lowercased."""
    if not hasattr(template_slug, "value"):
        url = git(ROOT, "remote", "get-url", "origin") or ""  # noqa: E501
        found = re.search(r"[:/]([\w.-]+/[\w.-]+?)(?:\.git)?\s*$", url)
        template_slug.value = found.group(1).lower() if found else ""
    return template_slug.value


def git(path, *args):
    """git inside a clone. Returns stdout, or None when git refuses."""
    result = subprocess.run(["git", "-C", str(path), *args],
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def repositories(owner, limit):
    """Every repository of the account, through REST.

    🔴 Deliberately NOT `gh repo list`: that command goes through GraphQL,
    whose hourly allowance is a separate bucket from REST's, and a shared
    one. The first full run of this audit died on `API rate limit already
    exceeded` while `gh api rate_limit` reported five thousand REST calls
    still available. Everything else here is REST, so the discovery is too.

    `/user/repos` is used when the owner is the authenticated account,
    because it is the only listing that returns private repositories.
    """
    login = api("user", jq=".login")
    if login and login == owner:
        path = f"user/repos?affiliation=owner&per_page=100"
    else:
        path = f"users/{owner}/repos?per_page=100"
    result = gh(["api", "--paginate", path], check=False)
    if result.returncode != 0:
        sys.exit("could not list the repositories.\n"
                 f"  gh said: {(result.stderr or '').strip()}")
    raw = json.loads("[" + result.stdout.replace("][", ",") + "]"
                     if result.stdout.lstrip().startswith("[[")
                     else result.stdout)
    repos = [r for r in raw if r["owner"]["login"] == owner][:limit]
    return sorted((normalise(r) for r in repos), key=lambda r: r["name"])


def normalise(rest):
    """A REST repository, under the names the checks already use."""
    licence = rest.get("license") or None
    language = rest.get("language") or None
    return {
        "name": rest["name"],
        "visibility": "PRIVATE" if rest.get("private") else "PUBLIC",
        "isArchived": bool(rest.get("archived")),
        "isFork": bool(rest.get("fork")),
        "licenseInfo": {"key": licence["key"]} if licence else None,
        "primaryLanguage": {"name": language} if language else None,
    }


def api(path, jq=None):
    """A REST read. None when GitHub refuses — the caller says why."""
    return api_with_status(path, jq)[0]


def api_with_status(path, jq=None):
    """(body, http status). The status is what tells a 404 from a 403.

    It matters here: on `branches/main/protection`, a 404 means the branch
    is NOT protected — a real failure — while a 403 means the plan or the
    token refuses to answer, which says nothing about the repository. A
    single `None` would have conflated the two, and the first run of this
    audit did exactly that.
    """
    args = ["api", path]
    if jq:
        args += ["--jq", jq]
    result = gh(args, check=False)
    if result.returncode == 0:
        return result.stdout.strip(), 200
    found = re.search(r"HTTP (\d{3})", result.stderr or "")
    return None, int(found.group(1)) if found else 0


def clone_index(roots, depth=3):
    """{owner/name: path} of every main clone found under `roots`.

    🔴 Keyed by the remote, never by the folder name. The first run of this
    audit matched folders to repository names and missed ten of twenty-six
    clones, because a folder is named by hand: `site-pef-blog` lives in
    `pef-blog`, and `sysadmin-macstudio-ops` lives outside `code/`
    altogether. Ten repositories reported as `no clone` is not a detail —
    it is a third of the account getting no file and no history check.

    A worktree carries a `.git` FILE pointing into its main clone; only a
    real `.git` directory is taken, so a worktree never shadows the clone
    it belongs to.
    """
    index = {}
    for root in roots:
        root = Path(root).expanduser()
        if not root.is_dir():
            continue
        for level in range(0, depth + 1):
            pattern = ".git" if level == 0 else \
                "/".join(["*"] * level) + "/.git"
            for git_dir in root.glob(pattern):
                if not git_dir.is_dir():
                    continue
                url = git(git_dir.parent, "remote", "get-url", "origin") or ""
                found = re.search(r"[:/]([\w.-]+/[\w.-]+?)(?:\.git)?\s*$",
                                  url)
                if found:
                    index.setdefault(found.group(1).lower(), git_dir.parent)
    return index


class Context:
    """Everything the checks of one repository share, fetched once."""

    def __init__(self, owner, meta, clones):
        self.owner = owner
        self.meta = meta
        self.name = meta["name"]
        self.slug = f"{owner}/{self.name}"
        self.clone = clones.get(self.slug.lower())
        self._cache = {}

    def settings(self):
        if "settings" not in self._cache:
            raw = api(f"repos/{self.slug}")
            self._cache["settings"] = json.loads(raw) if raw else None
        return self._cache["settings"]

    def protection(self):
        """(rules or None, http status). 404 means simply not protected."""
        if "protection" not in self._cache:
            raw, status = api_with_status(
                f"repos/{self.slug}/branches/main/protection")
            self._cache["protection"] = (
                json.loads(raw) if raw else None, status)
        return self._cache["protection"]

    def labels(self):
        if "labels" not in self._cache:
            raw = api(f"repos/{self.slug}/labels?per_page=100",
                      jq="[.[].name]")
            self._cache["labels"] = set(json.loads(raw)) if raw else None
        return self._cache["labels"]

    def commits(self):
        """(subject, body) of every commit, or None without a clone."""
        if "commits" not in self._cache:
            out = None
            if self.clone:
                out = git(self.clone, "log", "--no-merges",
                          "--format=%s%x1f%b%x1e")
            self._cache["commits"] = (
                [tuple(part.strip() for part in
                       (c.lstrip("\n").split("\x1f") + [""])[:2])
                 for c in out.split("\x1e") if c.strip()]
                if out is not None else None)
        return self._cache["commits"]

    def workflows(self):
        if not self.clone:
            return None
        folder = self.clone / ".github" / "workflows"
        if not folder.is_dir():
            return []
        return [(p.name, p.read_text(encoding="utf-8", errors="replace"))
                for p in sorted(folder.glob("*.yml"))]

    def tracked(self):
        if "tracked" not in self._cache:
            out = git(self.clone, "ls-files") if self.clone else None
            self._cache["tracked"] = out.splitlines() if out else None
        return self._cache["tracked"]


# --------------------------------------------------------------------------
# the checks — one per `check:` of the manifest
# --------------------------------------------------------------------------

def licence_present(ctx):
    """Blocking on a public repository, where the absence is a real bar."""
    if ctx.meta.get("visibility") != "PUBLIC":
        return SKIP, "private — see the private-repository entry"
    info = ctx.meta.get("licenseInfo")
    if not info:
        return FAIL, "public with no licence: All Rights Reserved, so " \
                     "nobody may legally reuse it"
    return PASS, info.get("key", "?")


def licence_decided(ctx):
    """A finding on a private repository: a decision, not a bar.

    Splitting the two is what makes `blocking` mean something. Eleven
    private repositories have no licence, and that is a choice waiting to
    be written, not a breach: nothing is exposed. Reported in the same run
    as the public ones would have drowned the real signal.
    """
    if ctx.meta.get("visibility") == "PUBLIC":
        return SKIP, "public — see the public-repository entry"
    info = ctx.meta.get("licenseInfo")
    if not info:
        return FAIL, "no licence decided yet"
    return PASS, info.get("key", "?")


CC_KEYS = {"cc-by-4.0", "cc-by-sa-4.0", "cc0-1.0", "cc-by-nc-4.0"}


def licence_fits_software(ctx):
    info = ctx.meta.get("licenseInfo") or {}
    key = info.get("key", "")
    language = (ctx.meta.get("primaryLanguage") or {}).get("name")
    if not language:
        return SKIP, "no code detected by GitHub"
    if key in CC_KEYS:
        return FAIL, f"{key} on a {language} repository"
    return PASS, key or "none"


def merge_settings(ctx):
    settings = ctx.settings()
    if settings is None:
        return SKIP, "GitHub refused to read the settings"
    wrong = []
    if settings.get("allow_squash_merge"):
        wrong.append("squash allowed")
    if not settings.get("allow_merge_commit"):
        wrong.append("merge commit refused")
    if not settings.get("delete_branch_on_merge"):
        wrong.append("head branch kept")
    return (FAIL, ", ".join(wrong)) if wrong else (PASS, "merge commit only")


def main_protected(ctx):
    rules, status = ctx.protection()
    if status == 404:
        return FAIL, "main accepts a force-push and a deletion"
    if rules is None:
        return SKIP, f"GitHub answered {status} — plan or rights, not the repo"
    return PASS, "protected"


def required_checks(ctx):
    protection, status = ctx.protection()
    if status == 404:
        return FAIL, "no protection at all, so no required check"
    if protection is None:
        return SKIP, f"GitHub answered {status}"
    required = protection.get("required_status_checks") or {}
    contexts = required.get("contexts") or [
        c.get("context") for c in required.get("checks", [])]
    if not contexts:
        return FAIL, "protection exists and requires no check"
    return PASS, ", ".join(c for c in contexts if c)


def labels_declared(ctx):
    have = ctx.labels()
    if have is None:
        return SKIP, "labels unreadable"
    want = declared_labels()
    missing = sorted(want - have)
    return (FAIL, "missing: " + ", ".join(missing)) if missing \
        else (PASS, f"{len(want)} declared labels present")


def agents_md_present(ctx):
    if not ctx.clone:
        return SKIP, "no clone"
    return (PASS, "present") if (ctx.clone / "AGENTS.md").exists() \
        else (FAIL, "no AGENTS.md at the root")


_SLUG_CACHE = {}


def _live_name(slug):
    """The repository's name today — different means it was renamed."""
    if slug not in _SLUG_CACHE:
        _SLUG_CACHE[slug] = api(f"repos/{slug}", jq=".full_name")
    return _SLUG_CACHE[slug]


def agents_md_names_live_repos(ctx):
    if not ctx.clone:
        return SKIP, "no clone"
    path = ctx.clone / "AGENTS.md"
    if not path.exists():
        return SKIP, "no AGENTS.md"
    text = path.read_text(encoding="utf-8", errors="replace")
    slugs = {f"{o}/{n.rstrip('.')}" for o, n in re.findall(
        r"github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", text)
        if n not in ("wiki",)}
    stale = []
    for slug in sorted(slugs):
        if "{{" in slug:
            continue
        live = _live_name(slug)
        if live and live.lower() != slug.lower():
            stale.append(f"{slug} -> {live}")
    return (FAIL, "renamed: " + "; ".join(stale)) if stale \
        else (PASS, f"{len(slugs)} repository name(s) current")


def no_copied_method_docs(ctx):
    if not ctx.clone:
        return SKIP, "no clone"
    if ctx.slug.lower() == template_slug():
        # The template itself: it is supposed to carry these documents.
        # Recognised through its own remote, not through a folder name —
        # this script runs from a worktree, whose folder is named after
        # the branch — and not through a file, which would only work once
        # that file is merged.
        return SKIP, "this is the template itself"
    folder = ctx.clone / "docs"
    if not folder.is_dir():
        return PASS, "no docs/ folder"
    copies = sorted(p.name for p in folder.glob("*.md")
                    if p.name in GENERIC_DOCS)
    if not copies:
        return PASS, "no generic document copied"
    drifted = sum(1 for name in copies
                  if (ROOT / "docs" / name).exists()
                  and (ROOT / "docs" / name).read_text(encoding="utf-8",
                                                       errors="replace")
                  != (folder / name).read_text(encoding="utf-8",
                                               errors="replace"))
    return FAIL, f"{len(copies)} copies, {drifted} already drifted"


def _pr_workflows(ctx):
    """Workflows a pull request starts. None without a clone."""
    found = ctx.workflows()
    if found is None:
        return None
    return [(name, text) for name, text in found
            if re.search(r"^\s*pull_request:?\s*$", text, re.M)]


def ci_concurrency(ctx):
    found = _pr_workflows(ctx)
    if found is None:
        return SKIP, "no clone"
    if not found:
        return SKIP, "no pull-request workflow"
    bad = [name for name, text in found
           if not re.search(r"^concurrency:", text, re.M)
           or "cancel-in-progress" not in text]
    return (FAIL, "without concurrency: " + ", ".join(bad)) if bad \
        else (PASS, f"{len(found)} workflow(s) cancel their own runs")


def ci_installs_once(ctx):
    found = _pr_workflows(ctx)
    if found is None:
        return SKIP, "no clone"
    if not found:
        return SKIP, "no pull-request workflow"
    worst, where = 0, None
    for name, text in found:
        count = len(re.findall(r"uses:\s*(?:ruby/setup-ruby|actions/setup-node"
                               r"|actions/setup-python)", text))
        if count > worst:
            worst, where = count, name
    if worst > 1:
        return FAIL, f"{worst} toolchain installs in {where}"
    return PASS, f"{worst} install per run"


def ci_paths_ignore(ctx):
    found = _pr_workflows(ctx)
    if found is None:
        return SKIP, "no clone"
    if not found:
        return SKIP, "no pull-request workflow"
    if any("paths-ignore" in text or "paths:" in text for _, text in found):
        return PASS, "a path filter exists"
    return FAIL, "no path filter: a documentation change runs the suite"


def _french(subject):
    return bool(FR_ACCENTS.search(subject)) or \
        len(FR_WORDS.findall(subject)) >= 2


def commits_in_english(ctx):
    commits = ctx.commits()
    if commits is None:
        return SKIP, "no clone"
    if not commits:
        return SKIP, "no commit"
    french = [s for s, _ in commits if _french(s)]
    if not french:
        return PASS, f"{len(commits)} subjects, no French marker"
    share = 100 * len(french) // len(commits)
    return FAIL, f"{len(french)}/{len(commits)} subjects ({share}%), " \
                 f"e.g. {french[0][:48]!r}"


LOCAL_PATHS = re.compile(r"/Users/|ObsiClaud|Documents/Claude")


def history_local_paths(ctx):
    commits = ctx.commits()
    if commits is None:
        return SKIP, "no clone"
    hits = [s for s, b in commits if LOCAL_PATHS.search(s + "\n" + b)]
    return (FAIL, f"{len(hits)} message(s) carry a local path") if hits \
        else (PASS, f"{len(commits)} messages, none")


# An attribution, not a filename. `CLAUDE.md` and `~/.claude/` name files
# of Romain's own configuration: writing them down is not a mention of the
# assistant, and the first run of this audit counted six of them as
# violations next to forty-five real ones.
ASSISTANT = re.compile(
    r"co-authored-by|anthropic|copilot"
    r"|(?<![/.])claude(?![./-])\b", re.I)


def history_assistant_mention(ctx):
    commits = ctx.commits()
    if commits is None:
        return SKIP, "no clone"
    hits = [s for s, b in commits if ASSISTANT.search(s + "\n" + b)]
    return (FAIL, f"{len(hits)} message(s) mention the assistant") if hits \
        else (PASS, f"{len(commits)} messages, none")


# 🔴 `.keep` files are EXCLUDED, and that is not a detail: Rails tracks
# `log/.keep`, `tmp/.keep` and `storage/.keep` on purpose, which is what the
# `!.keep` negations of its .gitignore are for. Without this exclusion the
# check failed on all six Rails applications, blocking, for files that are
# supposed to be there — a red result on correct repositories teaches that
# red means nothing.
RUNTIME = re.compile(r"^(log|tmp|storage|node_modules)/"
                     r"|(^|/)\.env$|master\.key$|\.pem$|(^|/)id_rsa$")
# 🔴 A placeholder is NOT a runtime file. Rails tracks `log/.keep`,
# `storage/.keep`, `tmp/.keep`, `tmp/pids/.keep` and `tmp/storage/.keep` on
# purpose — that is what the `!.keep` negations of its .gitignore are for.
# Checked against a real application rather than guessed: the first attempt
# excluded `.keep` only directly under the first folder, and `tmp/pids/.keep`
# still failed six Rails repositories, blocking, for files that must exist.
PLACEHOLDER = re.compile(r"(^|/)\.(keep|gitkeep)$")


def tracked_runtime_files(ctx):
    files = ctx.tracked()
    if files is None:
        return SKIP, "no clone"
    hits = [f for f in files
            if RUNTIME.search(f) and not PLACEHOLDER.search(f)]
    if hits:
        return FAIL, f"{len(hits)} tracked, e.g. {hits[0]}"
    return PASS, f"{len(files)} tracked files, none of them runtime"


# Named one by one rather than scraped from globals(): an entry whose
# `check:` is a typo must be reported as unknown, not silently matched to
# some other callable that happens to share the name.
CHECKS = {
    "licence_present": licence_present,
    "licence_decided": licence_decided,
    "licence_fits_software": licence_fits_software,
    "merge_settings": merge_settings,
    "main_protected": main_protected,
    "required_checks": required_checks,
    "labels_declared": labels_declared,
    "agents_md_present": agents_md_present,
    "agents_md_names_live_repos": agents_md_names_live_repos,
    "no_copied_method_docs": no_copied_method_docs,
    "ci_concurrency": ci_concurrency,
    "ci_installs_once": ci_installs_once,
    "ci_paths_ignore": ci_paths_ignore,
    "commits_in_english": commits_in_english,
    "history_local_paths": history_local_paths,
    "history_assistant_mention": history_assistant_mention,
    "tracked_runtime_files": tracked_runtime_files,
}


# --------------------------------------------------------------------------
# the run, and the report
# --------------------------------------------------------------------------

def inside_git_worktree(path):
    """True when path would land inside a repository. CA-04 refuses it."""
    result = subprocess.run(
        ["git", "-C", str(path.parent), "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip() == "true"


def run(entries, contexts):
    rows, blocking_failures = [], 0
    for ctx in contexts:
        for entry in entries:
            check = entry["check"]
            if check == "none":
                status, detail = SKIP, "nothing proves it yet"
            else:
                function = CHECKS.get(check)
                if function is None:
                    status, detail = SKIP, f"unknown check {check}"
                else:
                    status, detail = function(ctx)
            if status == FAIL and entry.get("severity") == "blocking":
                blocking_failures += 1
            rows.append((ctx.name, entry["id"], entry.get("severity", "?"),
                         status, detail))
    return rows, blocking_failures


MARK = {PASS: "ok", FAIL: "FAIL", SKIP: "--"}


def report(rows, entries, contexts, owner):
    out = ["# Baseline audit", "",
           f"Owner `{owner}` · {len(contexts)} repositories · "
           f"{len(entries)} entries of `baseline.yml`.", ""]
    per_entry = {}
    for _, entry_id, _, status, _ in rows:
        bucket = per_entry.setdefault(entry_id, {PASS: 0, FAIL: 0, SKIP: 0})
        bucket[status] += 1
    out += ["## By entry", "",
            "| Entry | severity | ok | FAIL | -- |", "|---|---|---|---|---|"]
    for entry in entries:
        counts = per_entry.get(entry["id"], {PASS: 0, FAIL: 0, SKIP: 0})
        out.append(f"| `{entry['id']}` | {entry.get('severity','?')} | "
                   f"{counts[PASS]} | {counts[FAIL]} | {counts[SKIP]} |")
    out += ["", "## Every failure, repository by repository", "",
            "| Repository | Entry | severity | What was found |",
            "|---|---|---|---|"]
    for name, entry_id, severity, status, detail in rows:
        if status == FAIL:
            # A pipe in the detail would break the Markdown row; escaped
            # outside the f-string, because a backslash inside one is a
            # syntax error before Python 3.12 and this script must run
            # anywhere.
            safe = detail.replace("|", "\\|")
            out.append(f"| `{name}` | `{entry_id}` | {severity} | {safe} |")
    out += ["", "## What this run could not see", "",
            "- a repository with no local clone: every file and history "
            "check is `--`, which is not a pass;",
            "- whether a green check was green yesterday — this says today;",
            "- the entries with `check: none`, counted apart and never green;",
            "- anything no pattern describes: a passphrase in plain words, "
            "an internal identifier. A check that finds nothing has found "
            "nothing.", ""]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--owner", default="romain-nicod")
    parser.add_argument("--repo", action="append", default=[],
                        help="OWNER/NAME, repeatable; default is every one")
    parser.add_argument("--only", default="",
                        help="comma-separated entry ids")
    parser.add_argument("--clones", type=Path, action="append",
                        default=None,
                        help="where clones live, repeatable "
                             "(default: code/ and projects/)")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--out", type=Path,
                        help="write the report here (never inside a repo)")
    parser.add_argument("--include-archived", action="store_true")
    args = parser.parse_args()

    entries = read_manifest()
    if args.only:
        wanted = {i.strip() for i in args.only.split(",")}
        unknown = wanted - {e["id"] for e in entries}
        if unknown:
            sys.exit(f"unknown entry id: {', '.join(sorted(unknown))}")
        entries = [e for e in entries if e["id"] in wanted]

    if args.out and inside_git_worktree(args.out.expanduser()):
        sys.exit("refused: the report names which repository is late and "
                 "would land inside a Git repository. Choose a path "
                 "outside any clone.")

    metas = repositories(args.owner, args.limit)
    if args.repo:
        names = {r.split("/")[-1] for r in args.repo}
        metas = [m for m in metas if m["name"] in names]
    if not args.include_archived:
        metas = [m for m in metas if not m.get("isArchived")]
    if not metas:
        sys.exit("no repository to audit")

    clones = clone_index(args.clones or DEFAULT_CLONES)
    print(f"{len(clones)} clones found by their remote")
    contexts = [Context(args.owner, m, clones) for m in metas]
    rows, blocking = run(entries, contexts)

    no_clone = [c.name for c in contexts if not c.clone]
    print(f"{len(contexts)} repositories, {len(entries)} entries, "
          f"{len(rows)} checks")
    failures = sum(1 for r in rows if r[3] == FAIL)
    print(f"  FAIL {failures}  ·  blocking {blocking}  ·  "
          f"ok {sum(1 for r in rows if r[3] == PASS)}  ·  "
          f"-- {sum(1 for r in rows if r[3] == SKIP)}")
    if no_clone:
        print(f"  no clone, so no file or history check: "
              f"{', '.join(no_clone)}")

    text = report(rows, entries, contexts, args.owner)
    if args.out:
        path = args.out.expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"  report: {path}")
    else:
        print()
        print(text)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
