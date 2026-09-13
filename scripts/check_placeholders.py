#!/usr/bin/env python3
"""Find the template's blank spaces that were never filled in.

`kickoff` ships documents with holes in them on purpose: an empty bullet,
a budget table with no figures, a `bash` block with no command. That is
the point of a template — it asks the questions instead of answering them
badly.

🔴 The failure mode is that nobody answers, and nobody notices. On
`agromalibio-v2-by-aigmented`, ten of them survived into a finished
project: the whole stack table, five README sections, and the AGENTS.md
section its own comment called worth more than the rest of the file.
Everything else about the project was green — the suite, the linter, the
security scan — and not one of those gates can see a heading with nothing
under it.

So this is the gate that can. Run it once the project is filled in, and
again before the first deployment pull request:

    python3 scripts/check_placeholders.py

It exits 1 when it finds one, and names the file and the line. Nothing
here is a matter of taste: every pattern it looks for is a hole the
template deliberately left.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Documents that are supposed to be filled in. The wiki pages and the
# changelog are written from scratch, so a blank line in them means nothing.
TRACKED = [
    "README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md",
    "GOLDEN_RULES.md",
]
TRACKED_GLOBS = ["docs/*.md"]

# An empty list item: "-", "- 🔴", "1.", "* ".
EMPTY_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s*(?:🔴|⚠️|✅)?\s*$")

# A bare marker on a line of its own: "🔴". The AGENTS.md of that project
# carried THREE of them under its absolute rules, with no list marker in
# front — so EMPTY_ITEM, which needs one, walked straight past all three.
# Found on 26/08/2026, where the script answered "Nothing left blank" to a
# file with three empty rules and an empty stack table in it.
BARE_MARKER = re.compile(r"^\s*(?:🔴|⚠️|✅)\s*$")

# A value left as a comment: "board : <!-- URL du Project -->". The
# AGENTS.md template asks for its board URL, production URL and deployment
# script this way, and a comment renders as nothing — the line reads as
# filled in on GitHub while it says nothing at all.
COMMENT_VALUE = re.compile(r":\s*<!--.*?-->")

# What bin/kickoff writes when kickoff.yml gives no vault folder.
TO_FILL_IN = re.compile(r"TO FILL IN")

# A table row whose cells are all blank: "| Application | |".
EMPTY_ROW = re.compile(r"^\s*\|(?:[^|]*\|)+\s*$")


def is_empty_row(line):
    if not EMPTY_ROW.match(line):
        return False
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if len(cells) < 2:
        return False
    # A separator row (|---|---|) is not a hole.
    if all(set(cell) <= set("-: ") and cell for cell in cells):
        return False
    # A row with NOTHING in it at all — "| | |" — is the shape the stack
    # table ships as, and the earlier version of this function missed it:
    # it required the first cell to be filled, reading a row as "a name
    # plus a hole". A row that is all hole is still a hole.
    if not any(cells):
        return True
    # Otherwise the first cell names the row and the hole is after it.
    return bool(cells[0]) and not any(cells[1:])


def empty_code_blocks(lines):
    """A fenced block with nothing but blank lines inside it."""
    found, fence, start, body = [], None, 0, []
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if fence is None:
            if stripped.startswith("```"):
                fence, start, body = stripped, number, []
            continue
        if stripped.startswith("```"):
            if not any(entry.strip() for entry in body):
                found.append((start, f"empty `{fence.strip('`') or 'code'}` block"))
            fence = None
            continue
        body.append(line)
    return found


def scan(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    problems = []
    for number, line in enumerate(lines, start=1):
        if EMPTY_ITEM.match(line) and line.strip():
            problems.append((number, f"empty list item: {line.strip()!r}"))
        elif BARE_MARKER.match(line):
            problems.append((number, f"a marker with no rule after it: {line.strip()!r}"))
        elif is_empty_row(line):
            problems.append((number, f"table row with nothing in it: {line.strip()!r}"))
        elif COMMENT_VALUE.search(line):
            problems.append((number, f"a value left as a comment: {COMMENT_VALUE.search(line).group(0)!r}"))
        elif TO_FILL_IN.search(line):
            problems.append((number, "marked TO FILL IN"))
    problems += empty_code_blocks(lines)
    return sorted(problems)


def targets():
    seen = []
    for name in TRACKED:
        path = ROOT / name
        if path.exists():
            seen.append(path)
    for pattern in TRACKED_GLOBS:
        seen += sorted(p for p in ROOT.glob(pattern) if p.is_file())
    return seen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true",
                        help="print nothing when everything is filled in")
    args = parser.parse_args()

    total = 0
    for path in targets():
        problems = scan(path)
        if not problems:
            continue
        total += len(problems)
        relative = path.relative_to(ROOT)
        for number, what in problems:
            print(f"{relative}:{number}  {what}")

    if total:
        print(f"\n{total} place(s) the template left for you and nobody filled.",
              file=sys.stderr)
        print("Fill them, or delete the section — a heading with nothing "
              "under it is worse than no heading.", file=sys.stderr)
        return 1

    if not args.quiet:
        print("Nothing left blank.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
