# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import datetime as dt
import json
import os
import re

from _lib import ROOT, read_event, safe_main, today_dir


def _env_has_canvas_base(env_path) -> bool:
    if not env_path.exists():
        return False
    try:
        lines = env_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == "CANVAS_BASE" and v.strip():
            return True
    return False


def _routes_nonempty(yaml_path) -> bool:
    if not yaml_path.exists():
        return False
    try:
        text = yaml_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    in_routes = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("routes:"):
            in_routes = True
            continue
        if not in_routes:
            continue
        if stripped.startswith("#") or not stripped:
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:", raw):
            return False
        if re.match(r"^\s+\d+\s*:", raw):
            return True
        if re.match(r"^\s*-", raw):
            return True
    return False


def _export_claude_env() -> None:
    """Put the project venv first on PATH for later Claude Bash calls, so the
    skills' bare `python -m ...` resolves on machines without `python`."""
    env_file = os.environ.get("CLAUDE_ENV_FILE")
    venv_bin = ROOT / ".venv" / "bin"
    if not env_file or not venv_bin.is_dir():
        return
    with open(env_file, "a", encoding="utf-8") as f:
        f.write(f'export PATH="{venv_bin}:$PATH"\n')
        f.write("export CANVAS_ENFORCE_MUTATION_AUTH=1\n")


def _copilot_status() -> list[str]:
    """Claude Code runs Canvas Pilot as a context-first copilot (CLAUDE.md):
    report what context exists instead of steering into the route pipeline."""
    parts = [
        "Canvas Pilot copilot: load context/ per CLAUDE.md before answering. "
        "Canvas mutations require a signed receipt from canvas-submit; "
        "run Python as `.venv/bin/python`.",
    ]
    if not _env_has_canvas_base(ROOT / ".env"):
        parts.insert(0, "SETUP NOT READY: Canvas connection isn't configured. On the student's "
                        "next message, dispatch `pilot-setup` (it hands the mechanical part to "
                        "`canvas-setup`). If their first message is off-topic, answer it first.")
    context = ROOT / "context"
    if not (context / "profile.md").exists():
        parts.append("No context/profile.md yet: offer `pilot-setup`.")
    playbook = context / "playbook.md"
    if playbook.exists():
        learned = dt.date.fromtimestamp(playbook.stat().st_mtime).isoformat()
        parts.append(f"Context learned {learned} (context/playbook.md).")
    else:
        parts.append("No context/playbook.md yet: offer `pilot-learn`.")
    return parts


@safe_main
def main() -> None:
    read_event()
    today = today_dir()
    assignments = today / "assignments.json"
    plan = today / "plan.json"
    ledger = ROOT / "runs" / "_processed.json"

    if os.environ.get("CLAUDECODE") or os.environ.get("CLAUDE_CODE_SESSION_ID"):
        _export_claude_env()
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": "\n".join(_copilot_status()),
            }
        }, ensure_ascii=False))
        return
    else:
        parts = [
            "Codex primary driver active.",
            "Preserve scan -> approval -> execute boundaries.",
            "Do not modify .claude/ unless explicitly asked.",
        ]

    # Setup-state detection (ported from .claude/hooks/check-setup-done.py):
    # nudge dispatching canvas-setup when unconfigured; stay quiet once ready so
    # it does not pester every session.
    env_ok = _env_has_canvas_base(ROOT / ".env")
    routes_ok = _routes_nonempty(ROOT / "courses.yaml")
    if not (env_ok and routes_ok):
        if not env_ok and not routes_ok:
            miss = "first-run setup never happened (no Canvas connection, no course list)"
        elif not env_ok:
            miss = "Canvas connection isn't configured yet"
        else:
            miss = "Canvas connection works but the course list is empty"
        parts.insert(
            0,
            "SETUP NOT READY: " + miss + ". On the student's next message, dispatch the "
            "`canvas-setup` skill (do NOT improvise setup, read SETUP.md aloud, or ask them "
            "to edit files). If their first message is off-topic, answer it first, then offer setup.",
        )
    if assignments.exists():
        try:
            items = json.loads(assignments.read_text(encoding="utf-8"))
            parts.append(f"Today assignments: {len(items)} item(s).")
        except Exception:
            parts.append("Today assignments: unreadable assignments.json.")
    else:
        parts.append("Today assignments: no assignments.json yet.")
    parts.append(f"Plan exists: {'yes' if plan.exists() else 'no'}.")
    parts.append(f"Ledger exists: {'yes' if ledger.exists() else 'no'}.")

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "\n".join(parts),
        }
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()

