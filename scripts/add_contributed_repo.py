#!/usr/bin/env python3
"""Add a repository to the contributed-project candidate list."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOS = ROOT / ".github" / "contributed-repos.json"
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def normalize_repo(value: str) -> str:
    repo = value.strip()
    if repo.startswith("https://github.com/"):
        repo = repo.removeprefix("https://github.com/")
    elif repo.startswith("http://github.com/"):
        repo = repo.removeprefix("http://github.com/")
    elif repo.startswith("git@github.com:"):
        repo = repo.removeprefix("git@github.com:")

    repo = repo.removesuffix(".git").strip("/")
    parts = repo.split("/")
    if len(parts) > 2:
        repo = "/".join(parts[:2])

    if not REPO_PATTERN.fullmatch(repo):
        raise ValueError("Repository must look like owner/name or a GitHub repo URL")
    return repo


def load_entries() -> list[dict[str, str]]:
    entries = json.loads(REPOS.read_text(encoding="utf-8"))
    normalized = []
    for entry in entries:
        repo = entry["repo"] if isinstance(entry, dict) else entry
        normalized.append({"repo": normalize_repo(repo)})
    return normalized


def write_entries(entries: list[dict[str, str]]) -> None:
    REPOS.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")


def add_repo(repo: str) -> bool:
    entries = load_entries()
    existing = {entry["repo"].lower() for entry in entries}
    if repo.lower() in existing:
        print(f"{repo} is already in {REPOS.relative_to(ROOT)}")
        return False

    entries.append({"repo": repo})
    write_entries(entries)
    print(f"Added {repo} to {REPOS.relative_to(ROOT)}")
    return True


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: add_contributed_repo.py owner/name", file=sys.stderr)
        return 2

    try:
        add_repo(normalize_repo(argv[1]))
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
