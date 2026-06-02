# Contributing to 04901-sentinel

Thank you for your interest in 04901-sentinel — the personal satellite visibility daemon and ground station toolkit.

We welcome contributions of all sizes: bug reports, improvements to tracking accuracy, notification integrations, documentation, and new features.

## Code of Conduct

Be respectful, constructive, and inclusive. This is a small personal systems / creative / radio-adjacent project.

## How to Contribute

### Reporting Issues

- Use the [GitHub Issues](https://github.com/keithdickey207/04901-sentinel/issues) page.
- For bugs, please include:
  - Python version and OS
  - Exact command/output
  - Whether running interactively or via install.sh
  - Any TLE or network related symptoms

### Suggesting Features / Roadmap Items

High-value areas:

- Next-pass prediction (AOS/LOS times, duration)
- Systemd unit file + proper daemon packaging (deb/rpm, pipx, etc.)
- ntfy / push notification integration via zero_vacuum + cryptography
- Config file (YAML/JSON) + support for multiple observer locations / NORAD IDs
- Elevation mask / terrain awareness (simple)
- Integration with local SDR tools or rotator control (hamlib, etc.)
- Better logging + log rotation

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/pass-prediction`)
3. Make focused changes
4. Test manually (the daemon is easy to run in foreground)
5. Update README or add comments as needed
6. Submit a Pull Request

We prefer small, focused PRs.

### Development Setup

```bash
git clone https://github.com/keithdickey207/04901-sentinel.git
cd 04901-sentinel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/sentinel_daemon.py
```

### Coding Style

- Keep it simple and readable. This is a lightweight tool, not an enterprise framework.
- Prefer working code + clear comments over clever abstractions.
- Satellite math accuracy matters — cite sources (Celestrak, ephem docs, etc.) when changing propagation logic.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Open an issue or reach the maintainer on GitHub.

---

"04901 Sentinel standing by for your patches."
