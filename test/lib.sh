#!/usr/bin/env bash
# Shared helpers for the test scripts. Source this file; don't run it.
set -euo pipefail
trap "" PIPE   # a dead server must not kill the script when we write to its FIFO

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$TEST_DIR")"
SERVER="$TEST_DIR/server"
PACK="$ROOT/pack"
PORT="${PACKWIZ_PORT:-8099}"
SEED="${SEED:-20261018}"
PACKWIZ="${PACKWIZ:-$(command -v packwiz || echo "$HOME/go/bin/packwiz")}"

# Java 21: $JAVA_HOME if set, then the system Temurin, then the user-level JDK.
find_java() {
  for c in "${JAVA_HOME:-}" \
           /Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home \
           "$HOME"/.local/java/jdk-21*/Contents/Home; do
    [[ -n "$c" && -x "$c/bin/java" ]] && { echo "$c/bin/java"; return; }
  done
  echo "Java 21 not found" >&2; exit 1
}
JAVA="$(find_java)"

# Serve the packwiz pack over HTTP and install it into the test server.
sync_pack() {
  # packwiz cf/mr add can pull in a dependency that is already in the pack from the
  # other site. Two entries for one jar confuse packwiz-installer, so fail early.
  local dupes; dupes=$(grep -h '^filename' "$PACK"/mods/*.pw.toml | sort | uniq -d)
  [[ -z "$dupes" ]] || { echo "Duplicate mod files in pack: $dupes" >&2; exit 1; }
  (cd "$PACK" && "$PACKWIZ" refresh >/dev/null)
  (cd "$PACK" && "$PACKWIZ" serve --port "$PORT" >/dev/null 2>&1) &
  local serve_pid=$!
  trap "kill $serve_pid 2>/dev/null || true" RETURN
  for _ in $(seq 1 20); do curl -sf "http://localhost:$PORT/pack.toml" >/dev/null && break; sleep 0.5; done
  (cd "$SERVER" && "$JAVA" -jar "$TEST_DIR/packwiz-installer-bootstrap.jar" -g -s server \
      "http://localhost:$PORT/pack.toml")
}

# Write server settings: EULA (test folder only), fixed seed, offline local server.
prepare_server() {
  echo "eula=true" > "$SERVER/eula.txt"
  local props="$SERVER/server.properties"
  [[ -f "$props" ]] || touch "$props"
  set_prop() { grep -q "^$1=" "$props" && sed -i '' "s|^$1=.*|$1=$2|" "$props" || echo "$1=$2" >> "$props"; }
  set_prop level-seed "$SEED"
  set_prop level-name "world"
  set_prop online-mode false
  set_prop server-ip 127.0.0.1
  set_prop spawn-protection 0
  set_prop view-distance 6
  # Use the pack's JVM args (from docs/README.md) for the test server too.
  cp "$TEST_DIR/jvm_args.txt" "$SERVER/user_jvm_args.txt"
}

# Start the server with stdin on a FIFO. Sets SERVER_PID and writes to the server via `send`.
start_server() {
  rm -f "$SERVER/console.in"; mkfifo "$SERVER/console.in"
  (cd "$SERVER" && exec ./run.sh --nogui < console.in > console.out 2>&1) &
  SERVER_PID=$!
  exec 7>"$SERVER/console.in"   # keep the FIFO open
}
send() { echo "$*" >&7 2>/dev/null || true; }

# Wait until a regex shows up in console output. Returns 1 on timeout or server exit.
wait_for() {
  local pattern="$1" timeout="$2" start=$SECONDS
  while (( SECONDS - start < timeout )); do
    grep -Eq "$pattern" "$SERVER/console.out" 2>/dev/null && return 0
    kill -0 "$SERVER_PID" 2>/dev/null || return 1
    sleep 2
  done
  return 1
}

stop_server() {
  send stop || true
  for _ in $(seq 1 60); do kill -0 "$SERVER_PID" 2>/dev/null || break; sleep 1; done
  kill "$SERVER_PID" 2>/dev/null || true
  exec 7>&- || true
  rm -f "$SERVER/console.in"
}

# Copy logs and crash reports into test/results/<label>-<timestamp>.
collect_logs() {
  local out="$TEST_DIR/results/$1-$(date +%Y%m%d-%H%M%S)"
  mkdir -p "$out"
  cp "$SERVER/console.out" "$out/" 2>/dev/null || true
  cp "$SERVER/logs/latest.log" "$SERVER/logs/debug.log" "$out/" 2>/dev/null || true
  [[ -d "$SERVER/logs/kubejs" ]] && cp -R "$SERVER/logs/kubejs" "$out/" || true
  [[ -d "$SERVER/crash-reports" ]] && cp -R "$SERVER/crash-reports" "$out/" || true
  echo "$out"
}
