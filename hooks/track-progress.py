#!/usr/bin/env python3
"""
PostToolUse hook to track file operations during Dojo challenges.
Updates session.json with actions taken for analytics.
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

DOJO_DIR = Path.home() / ".claude" / "dojo"
SESSION_FILE = DOJO_DIR / "session.json"
PROGRESS_FILE = DOJO_DIR / "progress.json"


def ensure_dojo_dir():
    """Create dojo directory if it doesn't exist."""
    DOJO_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filepath):
    """Load JSON file, return None if doesn't exist."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save_json(filepath, data):
    """Save data to JSON file."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def update_streak(progress):
    """Update streak based on last active date."""
    today = datetime.now().strftime("%Y-%m-%d")
    last_active = progress.get("streak", {}).get("lastActiveDate")

    if last_active == today:
        # Already active today, no change
        return progress

    if last_active:
        last_date = datetime.strptime(last_active, "%Y-%m-%d")
        today_date = datetime.strptime(today, "%Y-%m-%d")
        diff_days = (today_date - last_date).days

        if diff_days == 1:
            # Consecutive day, increment streak
            progress["streak"]["current"] = progress["streak"].get("current", 0) + 1
        elif diff_days > 1:
            # Streak broken
            progress["streak"]["current"] = 1
    else:
        # First activity
        progress["streak"]["current"] = 1

    # Update longest streak
    current = progress["streak"]["current"]
    longest = progress["streak"].get("longest", 0)
    progress["streak"]["longest"] = max(current, longest)
    progress["streak"]["lastActiveDate"] = today

    return progress


def main():
    """Main hook handler."""
    ensure_dojo_dir()

    # Read hook input from stdin
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Load current session
    session = load_json(SESSION_FILE)
    if not session or not session.get("currentChallenge"):
        # No active challenge, nothing to track
        return

    # Track relevant actions
    action = None

    if tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        action = {
            "type": "file_created",
            "path": file_path,
            "timestamp": datetime.now().isoformat()
        }

    elif tool_name == "Edit":
        file_path = tool_input.get("file_path", "")
        action = {
            "type": "file_edited",
            "path": file_path,
            "timestamp": datetime.now().isoformat()
        }

    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        if "git" in command:
            action = {
                "type": "git_command",
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
        elif any(cmd in command for cmd in ["rm ", "mv ", "cp ", "mkdir"]):
            action = {
                "type": "file_operation",
                "command": command,
                "timestamp": datetime.now().isoformat()
            }

    if action:
        # Add action to session
        if "actions" not in session:
            session["actions"] = []
        session["actions"].append(action)
        session["lastActionAt"] = datetime.now().isoformat()
        save_json(SESSION_FILE, session)

    # Update last active timestamp in progress
    progress = load_json(PROGRESS_FILE)
    if progress:
        progress["lastActiveAt"] = datetime.now().isoformat()
        progress = update_streak(progress)
        save_json(PROGRESS_FILE, progress)


if __name__ == "__main__":
    main()
