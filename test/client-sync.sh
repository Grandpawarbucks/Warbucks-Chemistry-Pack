#!/usr/bin/env bash
# Prism pre-launch hook: install the local packwiz pack into the client instance.
# Prism runs this with INST_MC_DIR set to the instance's minecraft folder.
#   PreLaunchCommand=/bin/bash "/path/to/test/client-sync.sh"
source "$(dirname "$0")/lib.sh"
PORT="${PACKWIZ_CLIENT_PORT:-8098}"
MC_DIR="${INST_MC_DIR:?INST_MC_DIR not set (run from Prism)}"

(cd "$PACK" && "$PACKWIZ" refresh >/dev/null)
(cd "$PACK" && "$PACKWIZ" serve --port "$PORT" >/dev/null 2>&1) &
serve_pid=$!
trap 'kill $serve_pid 2>/dev/null || true' EXIT
for _ in $(seq 1 20); do curl -sf "http://localhost:$PORT/pack.toml" >/dev/null && break; sleep 0.5; done

cd "$MC_DIR"
"$JAVA" -jar "$TEST_DIR/packwiz-installer-bootstrap.jar" -g -s client "http://localhost:$PORT/pack.toml"
