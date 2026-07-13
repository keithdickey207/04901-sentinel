#!/usr/bin/env python3
"""
04901 Sentinel — Cyber defense layer feed.
Publishes CVE threat count to sovereign defense bus.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SENTINEL_ROOT = Path(__file__).resolve().parent
DEFENSE_ROOT = Path.home() / "projects" / "sovereign-defense"
sys.path.insert(0, str(DEFENSE_ROOT))

from defense_publish import publish

LEDGER = SENTINEL_ROOT / "bounty" / "storage" / "ledger.json"


def count_cve_alerts(min_cvss: float = 7.0) -> tuple[int, str | None]:
    if not LEDGER.exists():
        return 0, None
    try:
        ledger = json.loads(LEDGER.read_text())
        high = [k for k, v in ledger.items() if v.get("cvss", 0) >= min_cvss]
        latest = high[-1] if high else None
        return len(high), latest
    except Exception:
        return 0, None


def feed_defense_bus() -> None:
    count, latest = count_cve_alerts()
    publish("defense.cyber", "cyber", cve_alerts=count, latest_cve=latest)
    print(f"[DEFENSE] Cyber layer: {count} CVE alerts → bus :2372")


if __name__ == "__main__":
    feed_defense_bus()