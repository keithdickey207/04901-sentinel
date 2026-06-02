#!/usr/bin/env python3
"""
bounty/parsers.py
Vulnerability feed parsers for the 04901 Bug Bounty Hunter.

Currently focuses on NVD for real recent CVEs. Easily extensible
with more sources (vendor bulletins, GitHub Advisories, etc.).

Provides standardized target dicts for the monitor/hunter.
"""

import json
import gzip
import io
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any

import requests

# User agent to be polite to APIs
UA = "04901-Bounty-Hunter/0.2 (personal research tool; +https://github.com/keithdickey207/04901-sentinel)"


def _http_get(url: str, timeout: int = 25) -> requests.Response:
    headers = {"User-Agent": UA, "Accept": "application/json"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp


def get_nvd_recent(days: int = 3, min_cvss: float = 0.0, max_results: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch recently modified CVEs from NVD 2.0 API (no key required for light use).

    Returns list of standardized vuln dicts.
    Note: NVD has rate limits for unauthenticated use (~5 req / 30s window).
    For heavy use, get a free NVD API key and add it via env or header.
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=days)

    # NVD 2.0 expects ISO8601 with milliseconds, UTC
    start_str = start.strftime("%Y-%m-%dT%H:%M:%S.000")
    end_str = now.strftime("%Y-%m-%dT%H:%M:%S.000")

    url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0/"
        f"?lastModStartDate={start_str}&lastModEndDate={end_str}"
        f"&resultsPerPage={min(max_results, 100)}"
    )

    try:
        resp = _http_get(url)
        data = resp.json()
    except Exception as e:
        print(f"[parsers] NVD API error: {e}")
        return []

    vulns: List[Dict[str, Any]] = []
    for item in data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        cve_id = cve.get("id", "N/A")

        # Descriptions
        descs = cve.get("descriptions", [])
        desc = next((d.get("value", "") for d in descs if d.get("lang") == "en"), "")

        # CVSS / Severity (prefer v3.1)
        severity = "UNKNOWN"
        cvss_score = 0.0
        metrics = cve.get("metrics", {})
        for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
            if key in metrics and metrics[key]:
                m = metrics[key][0].get("cvssData", {})
                cvss_score = m.get("baseScore", 0.0)
                severity = m.get("baseSeverity", key.replace("cvssMetric", "V"))
                break

        if cvss_score < min_cvss:
            continue

        # Rough "component" from first configuration (very simplified)
        configs = cve.get("configurations", [])
        component = "Multiple Products / Unknown"
        if configs:
            # Best effort: look for cpeMatch
            for node in configs:
                for match in node.get("nodes", []):
                    for cpe in match.get("cpeMatch", []):
                        if cpe.get("criteria"):
                            # e.g. cpe:2.3:a:vendor:product:...
                            parts = cpe["criteria"].split(":")
                            if len(parts) > 4:
                                component = f"{parts[3]}:{parts[4]}".replace("*", "any")[:60]
                                break
                    if component != "Multiple Products / Unknown":
                        break
                if component != "Multiple Products / Unknown":
                    break

        published = cve.get("published") or cve.get("lastModified") or now.isoformat()

        vulns.append({
            "cve_id": cve_id,
            "source": "NVD",
            "component": component,
            "severity": f"{severity} ({cvss_score})" if cvss_score else severity,
            "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
            "discovered_at": published,
            "raw_text_payload": (desc or "No English description available.")[:2500],
        })

    return vulns[:max_results]


def get_mock_vulns() -> List[Dict[str, Any]]:
    """Deterministic sample targets for testing / offline use."""
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "cve_id": "CVE-2025-9999",
            "source": "NVD",
            "component": "examplecorp:webapp",
            "severity": "CRITICAL (9.8)",
            "link": "https://nvd.nist.gov/vuln/detail/CVE-2025-9999",
            "discovered_at": now,
            "raw_text_payload": "Unauthenticated remote code execution via crafted HTTP request in the admin API endpoint. Affects all versions before 2.3.4.",
        },
        {
            "cve_id": "CVE-2025-1234",
            "source": "NVD",
            "component": "acme:auth-service",
            "severity": "HIGH (8.1)",
            "link": "https://nvd.nist.gov/vuln/detail/CVE-2025-1234",
            "discovered_at": now,
            "raw_text_payload": "Improper input validation in JWT handling allows privilege escalation when certain claims are missing.",
        },
    ]


def get_all_new_vulns(use_mock: bool = False, days: int = 3, min_cvss: float = 7.0) -> List[Dict[str, Any]]:
    """
    Main entry point used by the hunter/monitor.

    Returns a list of vuln targets in the expected shape for generate_report + ledger.
    """
    if use_mock:
        return get_mock_vulns()

    real = get_nvd_recent(days=days, min_cvss=min_cvss)
    if not real:
        print("[parsers] No real results (rate limit or network). Falling back to mock for demo.")
        return get_mock_vulns()
    return real


if __name__ == "__main__":
    # Quick self-test
    print("Testing parsers (mock mode)...")
    for v in get_all_new_vulns(use_mock=True):
        print(f"  - {v['cve_id']} | {v['severity']} | {v['component']}")
    print("\nTrying real NVD (may be rate limited)...")
    real = get_all_new_vulns(use_mock=False, days=1, min_cvss=0)
    print(f"Real results returned: {len(real)}")