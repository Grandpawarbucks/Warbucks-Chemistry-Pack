#!/usr/bin/env python3
"""Check Modrinth for NeoForge 1.21.1 builds.

Usage: test/mrcheck.py slug [slug ...]
Prints: slug | builds | latest version | date | days since update
"""
import datetime
import json
import sys
import urllib.parse
import subprocess
import time

API = "https://api.modrinth.com/v2/project/{}/version?" + urllib.parse.urlencode(
    {"loaders": '["neoforge"]', "game_versions": '["1.21.1"]'})
HEADERS = {"User-Agent": "warbucks-chemistry-pack/0.1 (modpack verification)"}


def check(slug):
    # curl uses the system trust store; python.org builds may lack certificates.
    for attempt in range(6):
        out = subprocess.run(["curl", "-s", "-w", "\n%{http_code}", "-A", HEADERS["User-Agent"],
                              API.format(slug)], capture_output=True, text=True).stdout
        body, _, code = out.rpartition("\n")
        if code != "429":
            break
        time.sleep(10 * (attempt + 1))  # Modrinth rate limit: back off and retry
    if code != "200":
        return f"{slug:30} | not on Modrinth (HTTP {code})"
    data = json.loads(body)
    if not data:
        return f"{slug:30} | NO NeoForge 1.21.1 build"
    v = data[0]
    date = v["date_published"][:10]
    age = (datetime.date.today() - datetime.date.fromisoformat(date)).days
    stale = "  STALE >12mo" if age > 365 else ""
    return f"{slug:30} | {len(data):3} builds | {v['version_number'][:40]:40} | {date} | {age}d{stale}"


if __name__ == "__main__":
    for s in sys.argv[1:]:
        print(check(s))
