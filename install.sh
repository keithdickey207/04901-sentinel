#!/bin/bash
set -e
mkdir -p /var/log/04901-sentinel
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup venv/bin/python src/sentinel_daemon.py > /var/log/04901-sentinel/daemon.log 2>&1 &
echo $! > /tmp/04901-sentinel.pid
echo "✅ Sentinel running! PID: $(cat /tmp/04901-sentinel.pid)"
echo "Logs: tail -f /var/log/04901-sentinel/daemon.log"
