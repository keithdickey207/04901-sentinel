# 04901 Bounty Hunter

Bug bounty research companion tool.

See the main [README](../README.md) for usage and the overall 04901 toolkit description.

## Quick commands

```bash
# From repo root
python -m bounty.monitor --mock
python -m bounty.monitor --days 2 --min-cvss 7.5
```

Reports land in `reports/`. Your personal tracking state is in `storage/ledger.json` (gitignored).

Extend `parsers.py` with more sources as needed.
