#!/usr/bin/env bash
# Smoke test: sync the pack, start the server on a fixed seed, wait for "Done"
# (5-minute timeout), stop it, collect logs, and print a pass/fail summary.
#   test/smoke.sh            fresh world each run
#   KEEP_WORLD=1 test/smoke.sh   reuse the existing world
source "$(dirname "$0")/lib.sh"

echo "== Syncing pack =="
sync_pack
prepare_server
[[ "${KEEP_WORLD:-0}" == 1 ]] || rm -rf "$SERVER/world"
rm -rf "$SERVER/crash-reports" "$SERVER/logs"

echo "== Starting server (seed $SEED) =="
t0=$SECONDS
start_server
if wait_for 'Done \([0-9.]+s\)!' 300; then started=1; else started=0; fi
elapsed=$((SECONDS - t0))
[[ $started == 1 ]] && sleep 5
stop_server

out="$(collect_logs smoke)"
echo "== Logs: $out =="
python3 "$TEST_DIR/parse_logs.py" "$out" --started "$started" --elapsed "$elapsed"
