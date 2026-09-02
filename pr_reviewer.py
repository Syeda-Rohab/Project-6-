#!/usr/bin/env python
"""
pr_reviewer.py — the "doorbell" review logic.

Scans the diff between base and head for two classic planted-bug
patterns:
  1. A deleted null/None check (a line containing "is None" or
     "is not None" that was removed).
  2. An off-by-one risk in a bounds check (a comparison against
     len(...) that was changed).

This runs automatically inside a GitHub Actions workflow triggered by
the `pull_request` event — nobody types a prompt. That's the event
heartbeat (Concept 7).
"""

import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


def review(base, head):
    diff = run(f"git diff {base} {head} -- '*.py' ':(exclude)pr_reviewer.py'")
    lines = diff.splitlines()

    findings = []

    for line in lines:
        if line.startswith("-") and not line.startswith("---"):
            content = line[1:].strip()
            if "is None" in content or "is not None" in content:
                findings.append(f"Possible deleted null-check — this line was removed: `{content}`")

        if line.startswith("+") and not line.startswith("+++"):
            content = line[1:].strip()
            if "len(" in content and any(op in content for op in [">=", "<=", ">", "<"]):
                findings.append(f"Possible off-by-one risk in a bounds check — new line: `{content}`")

    return findings


def main():
    base, head = sys.argv[1], sys.argv[2]
    findings = review(base, head)

    print("## Automated PR Review (Doorbell Loop)\n")
    if findings:
        print("This automated reviewer found potential issues in this PR:\n")
        for f in sorted(set(findings)):
            print(f"- ⚠️ {f}")
        print("\nPlease double check these before merging.")
    else:
        print("No obvious issues found by the automated checks.")
        print("(This is a heuristic reviewer, not a substitute for a human review.)")


if __name__ == "__main__":
    main()
