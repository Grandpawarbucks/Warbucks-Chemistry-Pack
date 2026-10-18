#!/usr/bin/env bash
# Set up a Warbucks Chemistry server folder.   Usage: server/install.sh /opt/warbucks
# Copies the start script, JVM args and server.properties (only if missing, so your edits are kept)
# and downloads packwiz-installer-bootstrap. The first ./start.sh installs NeoForge and all mods.
# The Minecraft EULA (https://aka.ms/MinecraftEULA) must be accepted by the server owner:
#   echo eula=true > <dir>/eula.txt
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dir="${1:?usage: install.sh <server folder>}"
mkdir -p "$dir"
install -m 755 "$here/start.sh" "$dir/start.sh"
for f in user_jvm_args.txt server.properties; do
  [ -f "$dir/$f" ] || cp "$here/$f" "$dir/$f"
done
[ -f "$dir/packwiz-installer-bootstrap.jar" ] || curl -fsSL -o "$dir/packwiz-installer-bootstrap.jar" \
  https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar
echo "Installed to $dir. Next: accept the EULA (eula.txt), then run $dir/start.sh"
