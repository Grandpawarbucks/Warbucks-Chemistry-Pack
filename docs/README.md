# Warbucks Chemistry Pack

A chemistry and technology modpack for **NeoForge 21.1.262 / Minecraft 1.21.1**. You're a demigod who rebuilds the world from its elements. See [PROGRESSION.md](PROGRESSION.md) for the design, [MODLIST.md](MODLIST.md) for the mods and [CHANGELOG.md](CHANGELOG.md) for history.

## Get the pack
- **Play:** import [`launcher/Warbucks-Chemistry-Prism.zip`](../launcher/Warbucks-Chemistry-Prism.zip) into Prism Launcher. It updates itself from this repo on every launch.
- **Develop on another PC:** see [DESKTOP_SETUP.md](DESKTOP_SETUP.md).
- Pack URL (packwiz): `https://raw.githubusercontent.com/Grandpawarbucks/Warbucks-Chemistry-Pack/main/pack/pack.toml`

## Layout
| Path | What |
|---|---|
| `pack/` | packwiz pack, the source of truth for mods (`pack.toml`, `index.toml`, `mods/*.pw.toml`) |
| `pack/kubejs/`, `pack/config/` | Pack overrides (KubeJS scripts, configs). Inside `pack/` so packwiz ships them. |
| `test/` | Test scripts. Server files and results are git-ignored. |
| `docs/` | Design and docs. `MODLIST.md` is generated from `modlist-meta.tsv`. |

## Tools (macOS)
- **Java 21:** Eclipse Temurin (`brew install --cask temurin@21`)
- **packwiz:** `go install github.com/packwiz/packwiz@latest` (installs to `~/go/bin/packwiz`)
- **packwiz-installer-bootstrap v0.0.3** and the **NeoForge 21.1.262 server**, both in `test/`

## Test loop
```bash
test/smoke.sh                 # sync pack → start server (seed 20261018) → wait for Done (5 min max) → stop → pass/fail summary
RADIUS=256 test/worldgen.sh   # fresh world, Chunky pre-gen, locate structures/biomes, scan for worldgen errors
test/mrcheck.py <slug>...     # check Modrinth for NeoForge 1.21.1 builds
test/ore_scan.py              # count ore blocks by mod in test/server/world
python3 test/parse_logs.py <dir> --client   # summarize a client log folder
python3 test/gen_modlist.py   # regenerate docs/MODLIST.md
python3 test/build_id_index.py   # index all item/block/dimension ids (run after a smoke test)
python3 tools/build_deposits.py  # regenerate ore-deposit worldgen (pack/kubejs/data)
<pillow-python> tools/build_art.py # regenerate title/loading art + quest banners (needs Pillow + macOS Avenir font)
python3 test/build_quest_preview.py # browsable quest book mock -> test/preview/index.html (local only)
python3 tools/build_quests.py    # regenerate the FTB Quests book from tools/build_quests.py (fails on unknown ids)
```
Results go to `test/results/<run>-<timestamp>/`. The smoke test fails on missing dependencies, mixin errors, KubeJS errors, recipe errors, duplicate registrations, worldgen errors or crash reports.

### Client test instance (Prism)
Instance: `~/Library/Application Support/PrismLauncher/instances/Warbucks-Chemistry-Dev`.
Its pre-launch command runs `test/client-sync.sh`, which serves `pack/` locally and installs the client side with packwiz-installer. Logs: `.../Warbucks-Chemistry-Dev/minecraft/logs/latest.log`.

## JVM arguments
Starting point: AllTheMods' official Java guide ([alltheguides `docs/help/java.md`](https://raw.githubusercontent.com/AllTheMods/alltheguides/HEAD/docs/help/java.md)). ATM10's own `memorysettings.json` warns below 6 GB on the client and 4 GB on the server, and recommends 8 GB (16 GB systems) to 12 GB (32 GB+ systems).

**Server (`user_jvm_args.txt`), used by the test server (`test/jvm_args.txt`):**
```
-Xms4G -Xmx6G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M
```
For a server with 8–12 GB and a fast CPU with 4+ cores, ATM's ZGC option is:
```
-Xms8G -Xmx12G -XX:+UseZGC -XX:+ZGenerational -XX:SoftMaxHeapSize=10g -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:+UseDynamicNumberOfGCThreads
```
**Client (Prism → instance settings → Java arguments), with 8–10 GB allocated:**
```
-XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M
```
With 12 GB or more allocated, ATM suggests ZGC: `-XX:+UseZGC -XX:+ZGenerational -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:+UseDynamicNumberOfGCThreads`

## Quests
The quest book is generated. Edit the content in `tools/quest_data.py` (see `docs/QUESTS.md` for a readable overview), not the files in `pack/config/ftbquests/quests/` (they're overwritten on every build). If you edit quests in-game with FTB Quests' editor, copy the changes back into `build_quests.py` before the next build.
