#!/usr/bin/env bash
set -euo pipefail
practice_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
practice_url="http://127.0.0.1:8765"
if ! /usr/bin/python3 -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8765/api/problems", timeout=1)' >/dev/null 2>&1; then
  nohup /usr/bin/python3 "$practice_dir/codingbat_gui/app.py" > /tmp/physics-practice.log 2>&1 &
  for practice_attempt in {1..30}; do
    if /usr/bin/python3 -c 'import urllib.request; urllib.request.urlopen("http://127.0.0.1:8765/api/problems", timeout=1)' >/dev/null 2>&1; then
      break
    fi
    sleep 0.1
  done
fi
xdg-open "$practice_url" >/dev/null 2>&1
