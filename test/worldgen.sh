#!/usr/bin/env bash
# Worldgen check: fresh world on the fixed seed, pre-generate a radius with
# Chunky (test-only mod, not part of the pack), locate some structures and
# biomes, then scan logs for worldgen errors.
#   RADIUS=256 test/worldgen.sh
source "$(dirname "$0")/lib.sh"
RADIUS="${RADIUS:-256}"

sync_pack
prepare_server
rm -rf "$SERVER/world" "$SERVER/crash-reports" "$SERVER/logs"

# Chunky from Modrinth (official), kept only in the test server's mods folder.
if ! ls "$SERVER/mods"/Chunky*.jar >/dev/null 2>&1; then
  url=$(curl -s 'https://api.modrinth.com/v2/project/chunky/version?loaders=%5B%22neoforge%22%5D&game_versions=%5B%221.21.1%22%5D' \
        | python3 -c "import json,sys;print(json.load(sys.stdin)[0]['files'][0]['url'])")
  curl -sSL -o "$SERVER/mods/$(basename "$url")" "$url"
fi

t0=$SECONDS
start_server
wait_for 'Done \([0-9.]+s\)!' 300 || { stop_server; out=$(collect_logs worldgen); python3 "$TEST_DIR/parse_logs.py" "$out" --started 0 --elapsed $((SECONDS-t0)); exit 1; }

send "chunky world minecraft:overworld"
send "chunky center 0 0"
send "chunky radius $RADIUS"
send "chunky start"
wait_for 'Task finished for minecraft:overworld' 1200 || echo "WARN: Chunky did not report completion in 20 min"

# Spot-check that structures and biomes from vanilla and the pack resolve.
for s in minecraft:village_plains minecraft:mineshaft minecraft:ancient_city betterdungeons:skeleton_dungeon towns_and_towers:village_badlands; do send "locate structure $s"; done
for b in biomesoplenty:redwood_forest biomesoplenty:lavender_field regions_unexplored:maple_forest regions_unexplored:bamboo_forest; do send "locate biome $b"; done
sleep 30
stop_server

out="$(collect_logs worldgen)"
echo "== Locate results =="
grep -E "(The nearest|Could not find|There is no)" "$out/console.out" || echo "(no locate output)"
python3 "$TEST_DIR/parse_logs.py" "$out" --started 1 --elapsed $((SECONDS-t0))
