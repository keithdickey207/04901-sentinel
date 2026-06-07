#!/data/data/com.termux/files/usr/bin/bash
#
# 04901-sentinel Termux Bootstrap for Pixel 10
# Run this on your phone after cloning the repo (or let it guide you).
#
# Usage (in Termux):
#   chmod +x phone/termux_setup.sh
#   ./phone/termux_setup.sh
#
# This sets up everything needed for:
#   - pixel_shipper.py  (location telemetry to your daemon)
#   - monitor.py / bounty hunter (run vuln research from your phone)
#

set -e

echo "========================================"
echo "  04901-sentinel Pixel 10 / Termux Setup"
echo "========================================"

echo "[1/4] Updating packages and installing essentials..."
pkg update -y
pkg install -y git python termux-api

echo "[2/4] Upgrading pip and installing Python deps (for bounty hunter + future tools)..."
pip install --upgrade pip
pip install requests

echo "[3/4] Checking for Termux:API app..."
if command -v termux-location >/dev/null 2>&1; then
    echo "    ✓ termux-location available"
else
    echo "    [!] termux-location not found yet."
    echo "        Install the 'Termux:API' app from F-Droid or GitHub Releases,"
    echo "        then grant it Location permission (and any other perms it asks)."
fi

echo "[4/4] Optional but recommended for background running:"
echo "    termux-wake-lock     # prevent CPU sleep while shipper runs"
    # You can put this in a small wrapper script or run it manually."

echo ""
echo "✓ Base setup complete."

# Detect if we're inside the repo
if [ -d "phone" ] && [ -d "bounty" ]; then
    echo ""
    echo "✓ You are inside the 04901-sentinel repo root."
    echo ""
    echo "Next steps / usage:"
    echo ""
    echo "  # Update everything from your GitHub (the main way to 'incorporate latest'):" 
    echo "  git pull"
    echo ""
    echo "  # Location shipper (the Pixel 10 part):"
    echo "  #   Set your daemon IP once (this Debian box IP when reachable):"
    echo "  export DAEMON_IP=10.64.40.230"
    echo "  python phone/pixel_shipper.py"
    echo "  # or with flags:"
    echo "  python phone/pixel_shipper.py --ip 10.64.40.230 --port 9876 --interval 60"
    echo ""
    echo "  # Bounty hunter / research (works great on phone too):"
    echo "  python monitor.py --mock"
    echo "  python monitor.py --days 1 --min-cvss 8"
    echo "  # or the module form:"
    echo "  python -m bounty.monitor --help"
    echo ""
    echo "  # The old-school root monitor.py also works because we added one in the repo:"
    echo "  python monitor.py --mock"
    echo ""
    echo "Tips:"
    echo "  - Run 'termux-wake-lock' before long-running shipper."
    echo "  - For autostart / always-on, look into termux-services or a simple script + crond."
    echo "  - To keep 'it all' fresh on your Pixel: just git pull from this directory."
    echo ""
else
    echo ""
    echo "[!] Not inside the repo yet. Do this first:"
    echo "    git clone https://github.com/keithdickey207/04901-sentinel.git"
    echo "    cd 04901-sentinel"
    echo "    ./phone/termux_setup.sh"
fi

echo ""
echo "All set. Your Pixel 10 now has the full 04901 toolkit + phone shipper."
echo "========================================"