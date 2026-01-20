#!/usr/bin/env python3
"""
Simple HTTP server for the Dojo dashboard.
Serves the dashboard and provides API for progress data.
"""
import http.server
import json
import os
import socketserver
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

PORT = 3847
DASHBOARD_DIR = Path(__file__).parent.parent / "dashboard"
DOJO_DIR = Path.home() / ".claude" / "dojo"


class DojoDashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for dashboard and API requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)

        # API endpoints
        if parsed.path == "/api/progress":
            self.send_progress()
        elif parsed.path == "/api/challenges":
            self.send_challenges()
        else:
            # Serve static files
            super().do_GET()

    def send_progress(self):
        """Send progress.json data."""
        progress_file = DOJO_DIR / "progress.json"

        if progress_file.exists():
            with open(progress_file) as f:
                data = json.load(f)
        else:
            # Return empty progress
            data = {
                "xp": {"total": 0, "level": 1, "toNextLevel": 100},
                "streak": {"current": 0, "longest": 0},
                "challenges": {},
                "modules": {},
                "badges": [],
                "stats": {"totalChallengesCompleted": 0}
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_challenges(self):
        """Send challenge index data."""
        challenges_dir = Path(__file__).parent.parent / "challenges"
        index_file = challenges_dir / "index.json"

        if index_file.exists():
            with open(index_file) as f:
                data = json.load(f)
        else:
            data = {"modules": [], "challengeDetails": {}}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        """Suppress logging for cleaner output."""
        pass


def main():
    """Start the dashboard server."""
    # Ensure dashboard directory exists
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

    with socketserver.TCPServer(("", PORT), DojoDashboardHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🥋 Dojo Dashboard running at {url}")
        print("   Press Ctrl+C to stop")

        # Open browser
        webbrowser.open(url)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")


if __name__ == "__main__":
    main()
