#!/usr/bin/env bash
# Start the test server, run /reload so ProjectE maps EMC, wait for the result, stop.
# ProjectE only maps EMC on datapack sync (player join or /reload), so a headless server needs /reload.
# Set usePregenerated = true in test/server/config/ProjectE/mapping.toml first to get
# test/server/config/ProjectE/pregenerated_emc.json with every value (set it back afterwards).
source "$(dirname "$0")/lib.sh"
rm -f "$SERVER/config/ProjectE/pregenerated_emc.json"
start_server
wait_for 'Done \([0-9.]+s\)!' 300 || { stop_server; echo "server failed"; exit 1; }
send "reload"
wait_for 'Registered [0-9]+ EMC values' 180 && grep -h 'Registered [0-9]* EMC values' "$SERVER/console.out" | tail -1
sleep 3
stop_server
