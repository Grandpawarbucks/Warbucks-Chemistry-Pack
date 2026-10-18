#!/usr/bin/env bash
# Warbucks Chemistry dedicated server - start script (Linux/macOS). Java 21; RAM in user_jvm_args.txt.
# Every start: pull the latest pack from GitHub (packwiz), install/upgrade NeoForge if the pack needs
# a new version, then run the server. Restarts after a crash; "stop" in the console shuts down for good.
cd "$(dirname "$0")"
PACK_URL="${PACK_URL:-https://raw.githubusercontent.com/Grandpawarbucks/Warbucks-Chemistry-Pack/main/pack/pack.toml}"
JAVA="${JAVA:-java}"
ver=$("$JAVA" -version 2>&1 | head -1 | sed -E 's/.*version "([0-9]+).*/\1/')
[ "$ver" != "21" ] && { echo "Java 21 is required (found: $("$JAVA" -version 2>&1 | head -1))."; exit 1; }
[ -f eula.txt ] && grep -q 'eula=true' eula.txt || { echo "Accept the Minecraft EULA first: echo eula=true > eula.txt"; exit 1; }

update() {
  # NeoForge version the pack wants (falls back to the installed one if GitHub is unreachable).
  want=$(curl -fsSL --max-time 20 "$PACK_URL" | sed -nE 's/^neoforge = "([^"]+)"/\1/p')
  if [ -n "$want" ] && [ ! -f "libraries/net/neoforged/neoforge/$want/unix_args.txt" ]; then
    echo "== Installing NeoForge $want =="
    curl -fsSL -o neoforge-installer.jar \
      "https://maven.neoforged.net/releases/net/neoforged/neoforge/$want/neoforge-$want-installer.jar" &&
      "$JAVA" -jar neoforge-installer.jar --installServer >neoforge-install.log 2>&1 &&
      rm -f neoforge-installer.jar run.sh run.bat || echo "NeoForge install failed (see neoforge-install.log)"
  fi
  echo "== Updating pack from $PACK_URL =="
  "$JAVA" -jar packwiz-installer-bootstrap.jar -g -s server "$PACK_URL" || echo "Pack update failed - starting with the files already here."
}

while true; do
  update
  args=$(ls -d libraries/net/neoforged/neoforge/*/unix_args.txt 2>/dev/null | sort -V | tail -1)
  [ -z "$args" ] && { echo "NeoForge is not installed (no network?)."; exit 1; }
  "$JAVA" @user_jvm_args.txt @"$args" nogui "$@"
  code=$?
  [ "$code" -eq 0 ] && break
  echo "Server stopped with code $code - restarting in 10 seconds (Ctrl+C to cancel)..."
  sleep 10
done
