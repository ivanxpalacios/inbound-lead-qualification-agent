#!/usr/bin/env python3
"""Block Claude Code from writing to the paths I write myself (see AGENTS.md).

Runs as a PreToolUse hook. Exit code 2 blocks the tool call and shows stderr to Claude.
"""

import json
import os
import re
import shlex
import sys

PROTECTED_PREFIXES = (
    "backend/src/rackwise/domain/",
    "backend/src/rackwise/ingest/",
    "backend/src/rackwise/queue/",
    "backend/src/rackwise/pipeline/",
    "backend/src/rackwise/agent/",
    "backend/src/rackwise/tools/",
    "backend/src/rackwise/llm/",
    "backend/src/rackwise/limits/",
    "backend/src/rackwise/crm/",
    "backend/src/rackwise/scoring/",
    "backend/src/rackwise/rag/",
    "backend/src/rackwise/mcp_server/",
    "backend/migrations/versions/",
    "backend/tests/",
    "frontend/src/lib/",
    "evals/",
    "prompts/",
    ".claude/hooks/",
)
PROTECTED_FILES = (
    "LEARNING_LOG.md",
    ".claude/settings.json",
    ".claude/settings.local.json",
)
# Exceptions inside protected directories: AI-generated synthetic data and fixtures.
ALLOWED_PREFIXES = (
    "evals/rendered/",
    "backend/tests/fixtures/",
)

# Shell commands that modify files named in their arguments.
WRITING_COMMANDS = re.compile(
    r"(^|[\s;&|(])(sed\s+(-[a-zA-Z]*\s+)*-i|cp|mv|rm|rmdir|truncate|touch|ln|patch|install|tee"
    r"|git\s+(checkout|restore|apply|mv|rm))\b"
)
# Output redirection targets: `> file`, `>> file`. Skips fd redirects like `2>&1`.
REDIRECT_TARGET = re.compile(r"(?:^|[^0-9&>])>{1,2}\s*([^\s;|&<>]+)")


def project_relative(path: str, project_dir: str, cwd: str) -> str | None:
    if not path:
        return None
    absolute = path if os.path.isabs(path) else os.path.join(cwd, path)
    relative = os.path.relpath(os.path.realpath(absolute), os.path.realpath(project_dir))
    if relative.startswith(".."):
        return None
    return relative.replace(os.sep, "/")


def is_protected(relative: str | None) -> bool:
    if relative is None:
        return False
    as_dir = relative.rstrip("/") + "/"
    if any(as_dir.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        return False
    if relative in PROTECTED_FILES:
        return True
    return any(as_dir.startswith(prefix) for prefix in PROTECTED_PREFIXES)


def bash_targets(command: str) -> list[str]:
    targets = REDIRECT_TARGET.findall(command)
    if WRITING_COMMANDS.search(command):
        try:
            targets.extend(shlex.split(command))
        except ValueError:
            targets.extend(command.split())
    return targets


def block(path: str) -> None:
    print(
        f"Blocked: '{path}' is a protected path. AGENTS.md says the user writes this code "
        "themselves. Give a hint from the hint ladder (AGENTS.md section 3) instead of "
        "writing it.",
        file=sys.stderr,
    )
    sys.exit(2)


def main() -> None:
    event = json.load(sys.stdin)
    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {}) or {}
    cwd = event.get("cwd") or os.getcwd()
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", cwd)

    if tool_name == "Bash":
        candidates = bash_targets(tool_input.get("command", ""))
    else:
        candidates = [tool_input.get("file_path", ""), tool_input.get("notebook_path", "")]

    for candidate in candidates:
        if is_protected(project_relative(candidate, project_dir, cwd)):
            block(candidate)


if __name__ == "__main__":
    main()
