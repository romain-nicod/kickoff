#!/usr/bin/env python3
"""Tag a deployed version and publish its GitHub release.

Run it AFTER the project's deployment script has put the merge commit of
the `[Déploiement] vX.Y.Z` pull request in production, and checked it:

    python3 scripts/publish_release.py --dry-run
    python3 scripts/publish_release.py                  # origin/main
    python3 scripts/publish_release.py --commit <sha>   # the deployed commit

In this order, stopping at the first failure before anything remote is
written:

  1. reads VERSION and CHANGELOG.md AT THE DEPLOYED COMMIT, not in the
     working tree: the release describes what runs in production;
  2. checks that the commit is on origin/main, that the version reads
     MAJOR.MINOR.PATCH, and that CHANGELOG.md holds a `## vX.Y.Z — date`
     section with the three headings of the delivery method;
  3. creates the annotated tag vX.Y.Z on that commit and pushes it;
  4. creates the GitHub release from that section, word for word, with
     `gh release create --verify-tag --notes-file`.

Idempotent: a tag already on that commit is reused, a release that
already exists is left alone. A tag on ANOTHER commit is a refusal: a
published version is never moved — the next one gets a new number.

Requires git and gh authenticated on the account owning the repository.
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from kickoff_lib import repo

ROOT = Path(__file__).resolve().parent.parent

HEADINGS = [
    "### User stories et fonctionnalités déployées",
    "### Corrections, outillage et documentation",
    "### À savoir",
]


def run(args, check=True):
    """Run a command at the repository root; stop the script on failure."""
    result = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    if check and result.returncode != 0:
        sys.exit(f"failed: {' '.join(args)}\n{result.stderr.strip()}")
    return result


def release_notes(changelog, version):
    """The body of the `## vX.Y.Z — …` section, without its heading line.

    The section ends at the next level-2 heading. The model section kept
    in an HTML comment at the top of the file never matches: it reads
    `vX.Y.Z`, not digits.
    """
    heading = re.compile(rf"^## v{re.escape(version)}\s+[—-]\s+\S.*$", re.M)
    match = heading.search(changelog)
    if not match:
        sys.exit(f"CHANGELOG.md has no `## v{version} — JJ/MM/AAAA` section "
                 "at this commit")

    rest = changelog[match.end():]
    following = re.search(r"^## ", rest, re.M)
    body = (rest[:following.start()] if following else rest).strip()

    missing = [h for h in HEADINGS if not re.search(rf"^{re.escape(h)}\s*$",
                                                   body, re.M)]
    if missing:
        sys.exit("the v%s section lacks: %s" % (version, ", ".join(missing)))
    return body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit", default="origin/main",
                        help="the commit running in production "
                             "(default: origin/main)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Reading only: brings the remote tags and main up to date locally, so
    # the checks below see what GitHub sees.
    run(["git", "fetch", "--quiet", "--tags", "origin"])

    sha = run(["git", "rev-parse", "--verify",
               f"{args.commit}^{{commit}}"]).stdout.strip()
    if run(["git", "merge-base", "--is-ancestor", sha, "origin/main"],
           check=False).returncode != 0:
        sys.exit(f"{sha} is not on origin/main: only a merged commit is "
                 "deployed")

    version = run(["git", "show", f"{sha}:VERSION"]).stdout.strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"VERSION reads {version!r} at {sha[:7]}, expected "
                 "MAJOR.MINOR.PATCH")
    if version == "0.0.0":
        sys.exit("VERSION is still 0.0.0: open the [Déploiement] pull "
                 "request first (docs/DEPLOIEMENT.md)")

    tag = f"v{version}"
    notes = release_notes(run(["git", "show", f"{sha}:CHANGELOG.md"]).stdout,
                          version)
    target = repo()

    tagged = run(["git", "rev-parse", "-q", "--verify",
                  f"refs/tags/{tag}^{{commit}}"], check=False).stdout.strip()
    if tagged and tagged != sha:
        sys.exit(f"{tag} already points at {tagged[:7]}, not {sha[:7]}. A "
                 "published version is never moved: bump VERSION instead.")
    on_remote = bool(run(["git", "ls-remote", "--tags", "origin",
                          f"refs/tags/{tag}"]).stdout.strip())
    released = run(["gh", "release", "view", tag, "--repo", target],
                   check=False).returncode == 0

    print(f"\n{target} · {tag} · commit {sha[:7]}")
    print(f"  tag      {'present' if tagged else 'to create'}"
          f"{', pushed' if on_remote else ', to push'}")
    print(f"  release  {'present — left alone' if released else 'to create'}")
    print("\n--- release notes ---\n" + notes + "\n---------------------")

    if args.dry_run:
        print("\nDry run — nothing was written.")
        return

    if not tagged:
        run(["git", "tag", "-a", tag, sha, "-m", tag])
        print(f"  created tag {tag}")
    if not on_remote:
        run(["git", "push", "--quiet", "origin", f"refs/tags/{tag}"])
        print(f"  pushed tag {tag}")

    if released:
        print(f"\nRelease {tag} already exists: nothing more to do.")
        return

    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8",
                                     delete=False) as handle:
        handle.write(notes + "\n")
        notes_file = handle.name
    created = run(["gh", "release", "create", tag, "--repo", target,
                   "--verify-tag", "--title", tag,
                   "--notes-file", notes_file])
    Path(notes_file).unlink(missing_ok=True)
    print(f"\nRelease published: {created.stdout.strip()}")


if __name__ == "__main__":
    main()
