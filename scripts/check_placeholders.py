#!/usr/bin/env python3
"""Find the template's blank spaces that were never filled in.

`kickoff` ships documents with holes in them on purpose: an empty
bullet under "structural decisions", a stack table with no rows, a
`bash` block with no command. That is the point of a template — it asks
the questions instead of answering them badly.

🔴 The failure mode is that nobody answers, and nobody notices. On
`agromalibio-v2-by-aigmented`, ten of them survived into a finished
project: the whole stack table, sections 1, 2, 7, 8 and 11 of the
README, and the AGENTS.md section whose own comment calls it worth more
than the rest of the file combined. Everything else about the project
was green — 860 examples, a clean linter, a silent security scan — and
not one of those gates can see a heading with nothing under it.

So this is the gate that can. Run it before the first pull request, and
again before going live:

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

# Documents that are supposed to be filled in. Everything else — the
# specification, the ADRs, the wiki — is written from scratch, so a
# blank line in it means nothing.
TRACKED = [
    "README.md", "AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md",
    "DOR_DOD.md", "GOLDEN_RULES.md",
]
TRACKED_GLOBS = ["docs/*.md"]

# An empty list item: "-", "- 🔴", "1.", "* ". The template writes these
# in pairs under a comment explaining what goes in them.
EMPTY_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s*(?:🔴|⚠️|✅)?\s*$")

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
    # The first cell names the row; the hole is everything after it.
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
        elif is_empty_row(line):
            problems.append((number, f"table row with nothing in it: {line.strip()!r}"))
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
