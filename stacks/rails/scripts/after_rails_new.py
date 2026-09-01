#!/usr/bin/env python3
"""Put back what Le Wagon's `minimal` template deliberately removes.

    python3 scripts/after_rails_new.py
    python3 scripts/after_rails_new.py --dry-run

Run it ONCE, straight after:

    rails new -d postgresql -m .../minimal.rb --skip .

`minimal.rb` is a good template that knows nothing about this repository.
It does four things that are right for a bare `rails new` and wrong here,
and all four are silent:

  1. `remove_file ".github/workflows/ci.yml"` — it deletes Rails 8's
     generated CI, and takes ours with it. You find out when the first
     pull request has no checks.
  2. It overwrites `.rubocop.yml` with its own. The stack layer's config
     is gone, and the rules the golden rules refer to are not the rules
     that run.
  3. It appends `.env*` to `.gitignore`, AFTER our `!.env.example`. Git
     keeps the last matching rule, so the appended line swallows the very
     example file golden rule 28 depends on.
  4. `rails new` inside a repository that already has a `.gitignore` does
     not write Rails' own — so `tmp/`, `log/` and `storage/` are tracked.
     On the project this was written from, that was 1779 files.

None of the four is a bug in `minimal.rb`. All four are certain, on every
project, which is why this is a script and not a paragraph in a document.

Idempotent: run it twice and the second run reports nothing to do.
"""

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAILS_IGNORE = """
# Rails runtime — regenerated on every boot, never versioned.
# `rails new` does not write these when a .gitignore already exists.
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep
/tmp/pids/*
!/tmp/pids/
!/tmp/pids/.keep
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/
!/tmp/storage/.keep
/public/assets
/app/assets/builds/*
!/app/assets/builds/.keep
/vendor/bundle

# LAST, on purpose: the boilerplate appends `.env*` above, and git keeps
# the final matching rule. Without this line the example file that golden
# rule 28 depends on is ignored.
!.env.example
"""

GENERATORS = """
    # Minitest, the Rails default -- see docs/TESTS.md. We only turn
    # fixtures off for generated scaffolds; the framework itself is
    # already Minitest and needs no block.
      g.test_framework :test_unit, fixture: false
      g.factory_bot dir: "spec/factories"
    end
"""


def git(args, check=True):
    return subprocess.run(["git"] + args, capture_output=True, text=True,
                          cwd=ROOT, check=check)


def restore_deleted(path, dry_run):
    """Bring a file back from the commit before the one that deleted it."""
    if (ROOT / path).exists():
        return None

    log = git(["log", "--format=%H", "--diff-filter=D", "-1", "--", path],
              check=False)
    commit = log.stdout.strip()
    if not commit:
        return f"  WARNING  {path} is missing and git has no record of it"

    if dry_run:
        return f"  restore {path}"
    git(["checkout", f"{commit}^", "--", path])
    return f"  restored {path}"


def restore_overwritten(path, dry_run):
    """Bring back the version that preceded the boilerplate's own."""
    if not (ROOT / path).exists():
        return None

    log = git(["log", "--format=%H", "-2", "--", path], check=False)
    commits = log.stdout.split()
    if len(commits) < 2:
        return None

    current = (ROOT / path).read_text(encoding="utf-8", errors="replace")
    previous = git(["show", f"{commits[1]}:{path}"], check=False).stdout
    if current == previous:
        return None

    if dry_run:
        return f"  restore {path} (the boilerplate overwrote it)"
    git(["checkout", commits[1], "--", path])
    return f"  restored {path} — the boilerplate had overwritten it"


def fix_gitignore(dry_run):
    """Add only the rules that are missing, and put the negation last.

    Appending the whole block blindly duplicates whatever a previous run —
    or a careful human — already wrote. Two identical rules are harmless
    to git and confusing to read, and a .gitignore nobody can read is one
    nobody corrects.
    """
    path = ROOT / ".gitignore"
    text = path.read_text(encoding="utf-8")
    present = {line.strip() for line in text.splitlines()}

    missing = [line.strip() for line in RAILS_IGNORE.splitlines()
               if line.strip() and not line.strip().startswith("#")
               and line.strip() not in present
               and line.strip() != "!.env.example"]
    # The negation has to be LAST whatever else is there: git keeps the
    # final matching rule, and the boilerplate appends `.env*` above it.
    negation_last = text.rstrip().endswith("!.env.example")

    if not missing and negation_last:
        return None
    if dry_run:
        what = f"add {len(missing)} rule(s)" if missing else "no rule to add"
        tail = "" if negation_last else ", move !.env.example last"
        return f"  .gitignore: {what}{tail}"

    body = text.rstrip()
    if missing:
        body += ("\n\n# Rails runtime — regenerated on every boot, never "
                 "versioned.\n# `rails new` does not write these when a "
                 ".gitignore already exists.\n")
        body += "\n".join(missing)
    if not negation_last:
        body += ("\n\n# LAST, on purpose: the boilerplate appends `.env*` "
                 "above, and git\n# keeps the final matching rule. Without "
                 "this line the example file\n# that golden rule 28 depends "
                 "on is ignored.\n!.env.example")
    path.write_text(body + "\n", encoding="utf-8")
    return (f"  .gitignore: {len(missing)} rule(s) added, "
            "!.env.example put last")


def untrack_runtime(dry_run):
    tracked = git(["ls-files", "--cached", "log", "tmp", "storage",
                   "public/assets"], check=False).stdout.split()
    junk = [f for f in tracked if not f.endswith(".keep")]
    if not junk:
        return None
    if dry_run:
        return f"  untrack {len(junk)} runtime files"
    git(["rm", "-r", "--cached", "--quiet", "log", "tmp", "storage"],
        check=False)
    git(["add", "log", "tmp", "storage"], check=False)
    return f"  untracked {len(junk)} runtime files (the .keep files stay)"


def point_generators_at_minitest(dry_run):
    path = ROOT / "config" / "application.rb"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    if "g.test_framework :test_unit" in text:
        return None

    anchor = "    config.autoload_lib(ignore: %w[assets tasks])"
    if anchor not in text:
        return ("  WARNING  could not find where to declare the generators "
                "in config/application.rb — add the generators block by hand")
    if dry_run:
        return "  point the generators at Minitest in config/application.rb"
    path.write_text(text.replace(anchor, anchor + "\n" + GENERATORS, 1),
                    encoding="utf-8")
    return "  config/application.rb: generators point at Minitest"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not (ROOT / "config" / "application.rb").exists():
        sys.exit("No config/application.rb — run this after `rails new`.")

    print("\nPutting back what the boilerplate removed\n")
    done = [
        restore_deleted(".github/workflows/ci.yml", args.dry_run),
        restore_overwritten(".rubocop.yml", args.dry_run),
        fix_gitignore(args.dry_run),
        untrack_runtime(args.dry_run),
        point_generators_at_minitest(args.dry_run),
    ]
    reported = [line for line in done if line]
    print("\n".join(reported) if reported else "  nothing to do")

    if args.dry_run:
        print("\nDry run — nothing was written.")
        return

    print("""
Left for you, because they need a decision rather than a default:

  1. Add the gems the specification needs. Minitest is already there —
     it is the Rails default — so this is only what the stories call for.
  2. bundle install, then write your first test under test/
  3. Commit. Read the diff first: the boilerplate's own commit is large,
     and this script has just changed what is in it.
""")


if __name__ == "__main__":
    main()
