#!/usr/bin/env python3
"""Publish the version journal as the project's wiki release notes page.

    python3 scripts/wiki_release_notes.py            # writes the page
    python3 scripts/wiki_release_notes.py --check    # fails if out of date

CHANGELOG.md stays the single source: every released version has its
section there, and that section IS the release note (docs/DEPLOYMENT.md).
This script copies those sections into docs/wiki/Release-notes.md, which
`.github/workflows/wiki.yml` publishes to the repository wiki at merge — so
the people who use the product read the same words as the GitHub release,
without anybody writing them twice.

Run it in the `[Déploiement] vX.Y.Z` branch, right after CHANGELOG.md is
updated, and commit the page with it. `--check` is for CI: it fails when the
page and the journal disagree, which is how a hand-edited page is caught.
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"
PAGE = ROOT / "docs" / "wiki" / "Release-notes.md"

HEADER = """# Release notes

What reached production, version by version, most recent first.

> Page produced by `scripts/wiki_release_notes.py` from `CHANGELOG.md`, which
> is authoritative. A change made here is overwritten at the next publication.
"""

NO_VERSION = "\n*No version is deployed to production yet.*\n"

# A released section: `## vX.Y.Z — DD/MM/YYYY`, as publish_release.py reads it.
SECTION = re.compile(r"^## v\d+\.\d+\.\d+ ", re.MULTILINE)


def sections(journal):
    """Everything from the first version heading on, comments left out."""
    journal = re.sub(r"<!--.*?-->", "", journal, flags=re.DOTALL)
    match = SECTION.search(journal)
    return journal[match.start():].strip() if match else ""


def page(journal):
    body = sections(journal)
    return HEADER + ("\n" + body + "\n" if body else NO_VERSION)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="compare only, write nothing")
    arguments = parser.parse_args()

    if not CHANGELOG.exists():
        sys.exit(f"{CHANGELOG} is missing.")

    wanted = page(CHANGELOG.read_text(encoding="utf-8"))
    current = PAGE.read_text(encoding="utf-8") if PAGE.exists() else None

    if arguments.check:
        if current == wanted:
            print(f"{PAGE.relative_to(ROOT)} is up to date.")
            return 0
        sys.exit(f"{PAGE.relative_to(ROOT)} no longer matches CHANGELOG.md: "
                 "run `python3 scripts/wiki_release_notes.py` again and commit the page.")

    if current == wanted:
        print(f"{PAGE.relative_to(ROOT)} is already up to date.")
        return 0

    PAGE.parent.mkdir(parents=True, exist_ok=True)
    PAGE.write_text(wanted, encoding="utf-8")
    print(f"{PAGE.relative_to(ROOT)} written from CHANGELOG.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
