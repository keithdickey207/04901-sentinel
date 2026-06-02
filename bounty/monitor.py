#!/usr/bin/env python3
"""
bounty/monitor.py
04901 Bug Bounty Hunter — Local vulnerability monitor & research dossier generator.

Watches public feeds (primarily NVD), deduplicates via a local ledger,
and produces high-quality Markdown research reports ready for your
personal bug bounty workflow.

Usage:
    python -m bounty.monitor --help
    python bounty/monitor.py --mock
    python bounty/monitor.py --days 2 --min-cvss 8.0
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any

# Allow running as script or module
try:
    from . import parsers
except ImportError:
    import parsers  # type: ignore

STORAGE_DIR = os.path.join(os.path.dirname(__file__), "storage")
LEDGER_FILE = os.path.join(STORAGE_DIR, "ledger.json")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "reports")


def init_storage() -> None:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(STORAGE_DIR, exist_ok=True)
    if not os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, "w") as f:
            json.dump({}, f, indent=2)


def is_already_tracked(cve_id: str) -> bool:
    if cve_id == "N/A" or "RELEASE" in cve_id:
        return False
    try:
        with open(LEDGER_FILE, "r") as f:
            ledger = json.load(f)
        return cve_id in ledger
    except Exception:
        return False


def save_to_ledger(cve_id: str, platform: str) -> None:
    try:
        with open(LEDGER_FILE, "r") as f:
            ledger = json.load(f)
    except Exception:
        ledger = {}

    ledger[cve_id] = {
        "platform": platform,
        "tracked_at": datetime.now().isoformat(),
        "simulation_state": "pending",
        "notes": "",
    }

    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)


def generate_report(target: Dict[str, Any]) -> str:
    """Generate a rich, bug-bounty-researcher-friendly Markdown dossier."""
    safe_name = target["cve_id"].replace("/", "-").replace("\\", "-")
    filename = f"{target['source'].lower()}_{safe_name}.md"
    filepath = os.path.join(REPORTS_DIR, filename)

    discovered = target.get("discovered_at", datetime.now().isoformat())
    raw = target.get("raw_text_payload", "No raw advisory text captured.")

    content = f"""# {target['cve_id']} — {target['source']} Research Dossier

**Component:** {target['component']}  
**Severity:** {target['severity']}  
**Reference:** [{target['link']}]({target['link']})  
**Discovered Locally:** {discovered}

---

## 🔬 Systems Architecture Overview

**Target Component:** {target['component']}

**Raw Advisory Context:**

{raw}

---

## 📊 Severity & Impact Analysis

- **CVSS / Vector:** {target['severity']}
- **Attack Vector (inferred):** Likely network / remote for high/critical scores. Validate against the official advisory.
- **Impact:** Confidentiality / Integrity / Availability — review the full NVD / vendor page for the exact CIA triad.
- **Exploit Maturity:** Check CISA KEV, Exploit-DB, and GitHub PoCs.

## 🛠️ Local Simulation Playbook

### Recommended Environment
- Match the exact security patch level / version range mentioned in the advisory.
- Use containerized or virtualized targets (Docker, Android Emulator, QEMU, etc.).
- Enable debug symbols, ASAN/UBSAN, or enhanced logging where available.

### Testing Focus
- Reproduce the vulnerability conditions described.
- Capture detailed logs (`adb logcat`, browser devtools, `strace`, `tcpdump`, application logs).
- Identify the exact code path / endpoint / feature that triggers the bug.
- Look for similar patterns in related components (supply-chain / transitive deps).

### Bounty Hunter Tips
- Scope check: Is the affected product / version in the program's in-scope assets?
- Duplicate check: Search the program's HackerOne/Bugcrowd/Intigriti submissions + disclosed reports.
- Write-up angle: Focus on business impact + realistic attacker scenario.
- Chaining potential: Can this be combined with other issues for higher severity?

---

## 🔗 Additional Research Links (manual)

- NVD: {target['link']}
- Vendor security page / bulletin (search the component name + CVE)
- Exploit-DB / GitHub search for `{target['cve_id']}`
- CISA Known Exploited Vulnerabilities (KEV) catalog
- Shodan / Censys for internet-exposed instances (if applicable)

---

*Generated 100% locally on {datetime.now().isoformat()} by 04901-bounty-hunter*
*This is a research aid only. Always follow the target program's policy and responsible disclosure rules.*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Improved report saved: {filepath}")
    return filepath


def main() -> None:
    parser = argparse.ArgumentParser(
        description="04901 Bug Bounty Hunter — monitor feeds and generate research dossiers."
    )
    parser.add_argument(
        "--mock", action="store_true",
        help="Use built-in mock vulnerabilities (offline / testing)"
    )
    parser.add_argument(
        "--days", type=int, default=3,
        help="How many days back to look for new vulns (real NVD mode)"
    )
    parser.add_argument(
        "--min-cvss", type=float, default=7.0,
        help="Minimum CVSS score to consider (real mode)"
    )
    parser.add_argument(
        "--limit", type=int, default=15,
        help="Max number of candidates to process this run"
    )
    args = parser.parse_args()

    print(f"[*] Starting 04901 Bug Bounty Hunter at {datetime.now()}")
    init_storage()

    targets: List[Dict[str, Any]] = parsers.get_all_new_vulns(
        use_mock=args.mock,
        days=args.days,
        min_cvss=args.min_cvss,
    )
    print(f"[*] Found {len(targets)} candidate targets from parsers")

    new_count = 0
    for target in targets[: args.limit]:
        cve = target.get("cve_id", "N/A")
        if is_already_tracked(cve):
            continue

        print(f"[+] New target: {cve} ({target.get('severity')}) — {target.get('component')}")
        generate_report(target)
        save_to_ledger(cve, target.get("source", "unknown"))
        new_count += 1

    print(f"\n[✓] Run complete. Added {new_count} new research reports.")
    print(f"    Reports directory: {REPORTS_DIR}")
    print(f"    Ledger: {LEDGER_FILE}")


if __name__ == "__main__":
    main()