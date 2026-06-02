# Changelog

All notable changes to 04901-sentinel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release of the 04901 Sentinel tracker daemon
- Real-time horizon visibility (alt > 0°) monitoring with state-change alerts
- Automatic TLE refresh from Celestrak (every 6h)
- `install.sh` for quick venv + backgrounded daemon setup
- `zero_vacuum.py` stub for future secure logging / ntfy push notifications
- Professional README, MIT license, Python .gitignore, CONTRIBUTING.md

### Changed
- N/A (first release)

## [0.1.0] - 2026-06-02

### Added
- Core `sentinel_daemon.py` Tracker class using pyephem + live Celestrak TLEs
- Console telemetry + ALERT logging
- Observer constants for Maine ground station (44.5520, -69.6317)
- Hardened signal handling (SIGINT/SIGTERM)
- Network error resilience loop
