# 04901-sentinel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/keithdickey207/04901-sentinel/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/keithdickey207/04901-sentinel?style=social)](https://github.com/keithdickey207/04901-sentinel)
[![GitHub](https://img.shields.io/badge/GitHub-keithdickey207/04901-sentinel-181717?logo=github)](https://github.com/keithdickey207/04901-sentinel)

**Personal 04901 toolkit: satellite visibility tracker + bug bounty research hunter.**

- `src/sentinel_daemon.py` — Real-time NORAD 39634 tracker & alerting daemon (Maine ground station).
- `bounty/` — Bug bounty hunter: monitors public vuln feeds (NVD), dedups, and auto-generates detailed research dossiers.

Both tools are designed for lightweight, local-first, always-on personal use with minimal dependencies.

---

## Features

**Sentinel tracker**
- Live tracking with SGP4/SDP4 via `ephem`
- Auto TLE refresh from CelesTrak
- Horizon alerts + resilient daemon mode

**Bug Bounty Hunter**
- Real NVD CVE feed monitoring (or offline mock mode)
- Automatic deduplication via local ledger
- Rich, ready-to-use research dossier generator with simulation playbook and bounty tips
- Easy to extend with additional parsers (HackerOne, vendor bulletins, etc.)

**Phone Telemetry (Termux / Pixel)**
- `phone/pixel_shipper.py` — Lightweight GPS location shipper that runs on your Android phone (Termux + termux-location) and streams lat/lon updates to a daemon over TCP.
- Update your phone from GitHub with a simple `git pull` on the device (see phone/README.md).

**Shared**
- One-shot install script for the satellite daemon
- Extensible `zero_vacuum.py` stub (encrypted logging + ntfy push notifications)

## Observer Location (Sentinel)

Hard-coded for development:

- Lat: 44.5520° N
- Lon: -69.6317° W
- Elev: 33 m

(Waterville / central Maine area — same reference location used in related chronosat work.)

## Bug Bounty Hunter (`bounty/`)

Local vulnerability feed monitor and high-signal research dossier generator.

```bash
cd bounty
python monitor.py --help
python monitor.py --mock                 # offline test with sample CVEs
python monitor.py --days 1 --min-cvss 8  # real recent critical+ from NVD
```

- Fetches recent high-severity CVEs from NVD (public API).
- Skips anything already in `storage/ledger.json`.
- Writes beautiful, actionable Markdown reports into `bounty/reports/`.
- Reports include: architecture overview, simulation playbook, attack surface notes, bounty hunter tips, and ready-to-customize sections.
- Fully offline capable via `--mock`.

**Example report filename:** `nvd_CVE-2025-XXXX.md`

**Storage (gitignored):**
- `bounty/storage/ledger.json` — tracks what you've already processed
- `bounty/reports/` — your personal research dossiers

**Extensibility:**
Edit `bounty/parsers.py` to add more sources (vendor security feeds, GitHub Advisories, specific bug bounty program disclosed lists, etc.). The target dict contract is simple and stable.

See `bounty/parsers.py` and `bounty/monitor.py` for implementation and CLI flags.

## Quick Start (Sentinel)

```bash
git clone https://github.com/keithdickey207/04901-sentinel.git
cd 04901-sentinel

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/sentinel_daemon.py
```

## Daemon / "Production" Install (Sentinel)

```bash
bash install.sh
```

## Project Layout

```
04901-sentinel/
├── src/
│   ├── sentinel_daemon.py   # Satellite tracker + alerting daemon
│   └── zero_vacuum.py       # Secure logger + vault stub (ntfy)
├── bounty/
│   ├── __init__.py
│   ├── parsers.py           # NVD (real) + mock vuln feed parsers
│   └── monitor.py           # Bug bounty hunter: ledger + dossier generator
├── phone/
│   ├── pixel_shipper.py     # Termux GPS telemetry shipper (Pixel → daemon)
│   └── README.md            # Termux setup + "update phone from GitHub" instructions
├── install.sh               # Sentinel daemon installer
├── requirements.txt
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
└── .gitignore
```

## How the Tracking Works (Sentinel)

1. On startup (and every 6h) fetch current TLE for the NORAD ID from Celestrak.
2. Use `ephem` to set observer + load TLE as a satellite.
3. Every 60s compute current altitude.
4. If `alt > 0` → visible ("ONLINE"). Crossing the 0° line triggers an alert print.

This is a very lightweight "is it up?" visibility predictor. It does **not** account for:
- Terrain / buildings
- Sunlight / terminator (for optical)
- Precise AOS/LOS with refraction or minimum elevation mask

For serious pass prediction use something with Skyfield + proper TLEs + masks.

## Secure Logging & Notifications (Roadmap)

`zero_vacuum.py` currently provides a no-op `SecureLogger` and a `load_vault()` that returns the ntfy endpoint `https://ntfy.sh/keith_04901_vault`.

Planned:
- Encrypt sensitive alert payloads
- POST rise/set events to ntfy (phone push)
- Optional local encrypted log append

Contributions or pairing on the crypto side welcome.

## Requirements

- Python 3.9+
- `ephem==4.1.5` (Sentinel only)
- `requests==2.32.3` (both tools)
- `cryptography==42.0.5` (reserved for zero_vacuum secure logging / future vault features)

The `bounty/` tool has no additional runtime dependencies beyond requests.

## Related Projects

- [chronosat](https://github.com/keithdickey207/chronosat) — Historical Landsat 1-3 / Skylab data tools (same observer coords)
- [dotfiles](https://github.com/keithdickey207/dotfiles) — Personal env including SDR / satellite tooling
- goodperson — Daily practice CLI

## License

MIT License

Copyright (c) 2026 Keith Dickey

See [LICENSE](LICENSE) for full text.

## Contributing

Issues and PRs welcome. Especially interested in:

- Better pass prediction / next-event table (Sentinel)
- Systemd service file + packaging (Sentinel)
- Real rotator / SDR integration hooks
- Config-driven observer + multiple NORADs
- More parsers / sources for the bounty hunter (HackerOne disclosed, vendor feeds, etc.)
- ntfy integration for the bounty hunter alerts

## Links

- **Repo**: https://github.com/keithdickey207/04901-sentinel
- **Issues**: https://github.com/keithdickey207/04901-sentinel/issues
- **Author**: https://github.com/keithdickey207

---

"04901 Sentinel standing by."
