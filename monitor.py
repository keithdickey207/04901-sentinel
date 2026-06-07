#!/usr/bin/env python3
"""
04901 Bug Bounty Hunter — convenience runner (repo root level).

Run this from inside the 04901-sentinel directory (works on desktop and in Termux on your phone):

    python monitor.py --help
    python monitor.py --mock
    python monitor.py --days 1 --min-cvss 8

This thin wrapper keeps the top-level `monitor.py` experience consistent
whether you're on your main machine or have the full toolkit on your Pixel.
"""

import sys
from pathlib import Path

# When running from the repo root, bounty/ is a direct sibling
BOUNTY_DIR = Path(__file__).parent / "bounty"
if not BOUNTY_DIR.exists():
    print("[!] bounty/ directory not found. Are you running from the 04901-sentinel repo root?")
    sys.exit(1)

sys.path.insert(0, str(BOUNTY_DIR))

try:
    import monitor as bounty_monitor
except ImportError as e:
    print("[!] Could not load bounty hunter from bounty/monitor.py")
    print("    Make sure the repo is fully cloned and up to date.")
    print(f"    Error: {e}")
    sys.exit(1)


def main():
    print("[*] 04901 monitor.py (repo root) → using bounty/ implementation")
    bounty_monitor.main()


if __name__ == "__main__":
    main()