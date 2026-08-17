#!/usr/bin/env python3
"""Shared helpers for the backlog scripts.

The repository is deduced from `git remote get-url origin`, so no script
carries a hard-coded name: they survive a fork and a rename.
"""

import re
import subprocess
import sys


def repo():
    """owner/name of the origin remote."""
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"],
                             capture_output=True, text=True,
                             check=True).stdout.strip()
    except subprocess.CalledProcessError:
        sys.exit("no `origin` remote — add one, or pass --repo owner/name")

    match = re.search(r"[:/]([^/:]+/[^/]+?)(?:\.git)?$", url)
    if not match:
        sys.exit(f"cannot read owner/name from the origin remote: {url}")
    return match.group(1)


def owner():
    return repo().split("/")[0]


def gh(args, check=True):
    result = subprocess.run(["gh"] + args, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"failed: gh {' '.join(args)}\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result
