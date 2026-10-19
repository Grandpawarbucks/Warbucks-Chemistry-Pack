# Changelog

All changes to the Warbucks Chemistry Pack are logged here, newest first.

## [Unreleased]

### 2026-10-19: Fast Leaf Decay, quest audit, cleaner quest lines
- **Fast Leaf Decay** (CurseForge, fastleafdecay-35) added; both sides.
- **Quest audit** `tools/quest_audit.py`: cycles, unreachable or task-less quests, required quests behind optional ones,
  unknown item/kill/dimension/structure/biome ids (cheap checks run on every `build_quests.py` and `--check`).
  `--full` also checks obtainability and tier order against a server dump (`test/audit_dump.ps1`, which uses the
  marker-gated `zz_recipe_dump.js`). Fixes: `ars_anima` asks for `sauce:anima_essence`; six nonexistent 64x Powah
  generators removed from `pw_gg_64x`; the Ars Additions chunk-loading ritual enabled (`config/ars_additions-common.toml`)
  so `ars_chunk` can be done. `test/ids.tsv` is now built from the real registry.
- **Layout** (`tools/layout.py`): lines through other quests 264 → 19, crossings 325 → 148 (937 → 264 counting the
  quest-link lines). Redundant transitive dependency lines are dropped on output only (22), with better crossing
  reduction, centred main paths, spread-out fans, quest links placed next to their dependents, and best of three
  layouts per chapter.

### 2026-10-19: Mining dimension veins for common MI metals
- All The Ores skipped (user decision: it duplicates MI/Mekanism metals everywhere and skips chemistry milestones).
- `tools/build_deposits.py` now also writes rich veins for tin, lead, nickel, silver (Mekanism ore) and bauxite into
  Allthemodium's Mining dimension only (`warbucks:mining_*`, biome tag `#allthemodium:mining_features/mining_biomes`).
  Platinum, iridium, uranium, osmium, tungsten and other milestone metals stay out. Checked on the test server: every
  generated Mining chunk with iron also has the five new ores, and none has platinum, iridium or uranium.
- `build_deposits.py` writes UTF-8/LF (it would have rewritten every deposit file with CRLF on Windows).

### 2026-10-19: Neo Vitae and Allthemodium (224 mods, 2,524 quests)
- **Neo Vitae** 1.1.44 (Modrinth, MIT; Blood Magic's successor), gated in `phase5_neovitae.js`: Athanor ore processing
  capped at 2x per ore block / 1.5x per raw ore, fragment doubling removed; shipped `config/neovitae/materials.json`
  (no first-run ore scan, no netherite-scrap loop); Flight flask needs hydrogen, Tenebrae needs hydrogen + an MV circuit;
  the diamond → Nether Star recipe and all meteor rituals removed; the Athanor needs LV analog circuits. Quest page
  "neovitae" (31 quests). Research: `docs/research/neo_vitae.md`.
- **Allthemodium** 3.2.1 (CurseForge only, ARR with third-party download allowed; no AllTheOres), gated in
  `phase5_allthemodium.js`: no furnace smelting (MI EBF: allthemodium carbothermic at LV, vibranium by the Kroll process,
  unobtainium by sodium reduction with HF); alloys in the Mixer with a Piglich Heart, then the EBF under argon (antimatter
  for the unobtainium alloys); Teleport Pad needs MI steel plates and an analog circuit; Occultism's eldritch miners
  for the three metals removed. The Mining dimension keeps its dense ores (user decision). Quest page "Metals of
  Legend" (25 quests). Research: `docs/research/allthemodium.md`.
- Known harmless: Botany Pots' compat recipe for an Allthemodium plant that 3.2.1 no longer has.

### 2026-10-19: The Demigod's Market (token shop) and the quest editor
- **Token shop in the quest book** (`docs/research/shop_brief.md`): a new "The Demigod's Market" group with 4 chapters and
  441 repeatable shop quests: Machines (64), Materials and Chemicals (88), Tools, Armour and Gear (129), Blocks, Food and
  Wild Goods (160). Rule: whatever you've made or obtained yourself, you can buy more of. Each entry stays invisible until
  the quest where you first make it, costs Demigod Tokens (Greater Tokens from MV up), and can be bought again and again.
  Never sold: multiblocks, Alchemistry machines, flight items, finished circuits, nuclear fuel, oganesson, Nether Stars,
  Seed parts, ProjectE and creative items.
- Quest engine: `Q(repeat=..., consume=..., locked_hidden=...)` → FTB `can_repeat`, `consume_items`,
  `hide_until_deps_complete` (field names read from the FTB Quests 2101.1.36 jar).
- **Quest editor** (`tools/quest_editor.py`, http://localhost:8765): drag quests, edit titles/subtitles/descriptions,
  autosave to `tools/quest_overrides.json` (applied on top of the automatic layout), Check and Push buttons. See
  docs/DESKTOP_SETUP.md.
- Research: `docs/research/allthemodium.md` (Allthemodium 3.2.1: feasible, pending user decisions).
- 2,468 quests, 47 chapters, 9 groups.

### 2026-10-19: Quest book v11 (2,000 quests): ATM10-aligned coverage and the story arc; fresh world
- **Live world wiped** (user decision): backup `backups/world-prewipe-20261019-002252.tar.gz` on the VPS; new random seed.
- **ATM10-aligned quests** (brief: `docs/research/atm10_alignment_brief.md`): ATM10's book (All Rights Reserved) was used
  only as a checklist of items worth a quest; every quest is our own text. 378 new quests across 6 parallel writers:
  early path +14, late path +58, basics +103 (vanilla armour/tools/food/building, storage, power, Powah), tech +99
  (Mekanism, AE2 + addons, Integrated Dynamics, LaserIO, Pipez, Create, JDT), magic +60, worlds +41. Uncovered ATM10
  items dropped from 1,124 to 138, all skipped for a reason (creative, ATM-only, blocked by our gates, already covered
  by a tag task).
- **Hidden endgame chain made visible**: the Seed's Antimatter Cores need MI quantum circuits → plutonium batteries → MI
  plutonium, which only the MI Nuclear Reactor makes. Kanthal coils, titanium, tungsten, implosion compressor, nuclear
  reactor, cryofluid, superconductor, qubits, tritium and helium-3 are now required main-path quests (t6/t7).
- **Story**: one arc from first join to the end (gold lines reviewed welcome → creation), gifts numbered (Dissolver,
  Combiner, Infusion Pylon), repetition removed; t7 renamed "VIII. Beyond the Sky" (no clash with "Creation").
- Gate fix: Ars Elemental's `flight_alt` Ritual of Flight recipe removed (it skipped the hydrogen).
- `tools/quest_compare.py` counts items inside our any-of quests.

### 2026-10-19: Chemistry by tier, quest book v10 (layout, Basics, pruning), harvest tiers
Based on three audits in `docs/research/` (chem_tier_audit, quest_layout_audit, tools_harvest_plan); 7 parallel writers.
- **Chemistry gates** (`phase4_aluminum.js`, new `phase5_chem_gates.js`):
  - Aluminium only from the Hall-Héroult Cell: obsidian-dissolved alumina, ChemLib's aluminium-dust smelting and
    Alchemistry's compound→dust compacting are gone; the cell takes only Bayer alumina dust.
  - Dragon's breath dissolves to xenon + radon only; oganesson only from Fusion.
  - Redstone battery needs Combiner sulfuric acid (a lead-acid battery): the T1 "first compound" gate now exists.
  - Silicon only from carbothermic reduction (MI EBF); sand/certus/quartz-blend routes removed; MI silicon is `c:silicon`.
  - Undergarden catalyst and the Seed accept any sulfuric acid bucket (MI, Mekanism, ChemLib).
  - Seed of a New World needs 4 hydrofluoric acid buckets (polyethylene 16 → 12).
- **Harvest tiers** (`phase5_harvest_tiers.js`): MI titanium, tungsten, platinum, iridium ores need an iron pickaxe; Ad Astra
  desh iron, ostrum diamond, calorite netherite.
- **Quest book v10** (1,622 quests, 44 chapters; 801 required, 821 optional):
  - Automatic layout (`tools/layout.py`): every line points left to right, the required path on the middle row, side
    topics as rows, links in a left column. Line crossings 320 → 121, backward lines 415 → 0, overlaps 14 → 0.
    `python tools/build_quests.py --layout-report` shows the numbers.
  - New **Basics** group (tools, harvest, storage, power, Powah, farming, QoL, building); Welcome, Market, Lab Notes
    and Completionist sit above the tabs. Utilitarian merged into QoL; Mekanism split into Mekanism + Mekanism Power.
  - New **Tools, Armour and Harvest Tiers** chapter (30 quests): each pickaxe tier and what it can now mine.
  - Pruning: duplicates removed or merged (paxels, JDT intro, claim, compass, logistics, market and welcome tick
    chains), the Seed's single-item quests optional, dead ends made optional. New "Battery Acid" quest.
  - Text fixes: synthetic rubber, steel paxel mines obsidian, rocket fuel, silicon, aluminium, Undergarden acid.

### 2026-10-18: Gate fixes found while writing quests
- Powah's own Energizing recipe uranium ingot → uraninite removed: uraninite only comes from the MI Chemical Reactor
  (uranium + O₂), as designed.
- Occultism crusher spirits all give 2 dust per ore (Djinni/Afrit/Marid gave 3x/4x/6x, above the 2x cap before acids).
  Higher tiers still work faster. New `pack/config/occultism-server.toml`.
- Ars Nouveau Ritual of Flight tablet now also needs 2 hydrogen, so ritual flight arrives with the Infusion Pylon.
- Docs: STYLE.md's blocked lists corrected (Mystical Agriculture vs Occultism); CLAUDE.md no longer claims JDT flight is
  chemistry-gated (it's late by design).

### 2026-10-18: Quest book v9 (1,617 quests, 43 chapters)
- **Getting Started is a full first day** (27 → 50): logs → planks → table → sticks → wooden and stone tools → furnace →
  torches → shelter and bed → seeds and a wheat farm → cooked meat → leather → iron tools and armour → water → a first
  mining trip → Chapter I. Optional: boat, bow, campfire, glass, sugar cane, shears, smithing table, gold and chainmail.
- **New pages:** Just Dire Things (45), Powah (34), The Undergarden (34), Deeper and Darker (23), Utilitarian (20).
- **Expanded pages:** Create 35 → 81 (crushing wheels now correctly after precision mechanisms, Create 6 packages, trains),
  Mekanism 39 → 81 (factories, QIO, MekaSuit, generators, turbine, Mekanism Tools armour), Twilight Forest 29 → 79 (boss
  order fixed from the mod's own progression locks: stroganoff before the Hydra, Uncrafting Table after the Maze Map
  Focus), AE2 40 → 67 (processors, ExtendedAE, MEGA Cells, AdvancedAE), Storage 21 → 51 (Sophisticated Storage and
  Backpacks, Iron Furnaces, Logistics Network), Ars Nouveau 26 → 60, Occultism 17 → 48.
- Fix: "Undergarden Metals" no longer asks for utherium crystals right after arrival (they need the Infuser, deep in).
- `tools/quest_compare.py`: lists items another pack quests on that ours doesn't (requirements only; ATM10's book is a
  checklist, nothing copied).
- Written by 9 parallel writers (one chapter file each); smoke test passes and FTB Quests loads all 1,617 quests.

### 2026-10-18: QoL: Utilitarian, longer days, less rain, faster furnaces
- **Utilitarian** 0.19.2 (CurseForge; Modrinth's 1.21.1 build is a year older): bulk wood crafting (2 logs → 16 sticks, chests,
  ladders, bowls, slabs, stairs, doors, trapdoors), re-dyeing coloured blocks, plus Angel Block, Block Magnet, Fluid Hopper,
  Snad, Trowel, Sound Muffler, trader carpets and more. 222 mods.
- **Longer days** (`server_scripts/qol_world.js`, from the user's Wardaddy ATM10 tweak): Overworld daytime lasts 2x as long;
  night is unchanged.
- **Less rain** (same file): when the weather changes, dry spells are stretched 2x and rain is cut to half, so roughly a
  quarter as much rain. `/weather` still works; the `doWeatherCycle` gamerule turns it off.
- **4x furnace speed** (`server_scripts/qol_furnace_speed.js`, from the Wardaddy ATM10 tweak): 639 smelting, blasting and
  smoking recipes; machine recipes keep their times.
- `test/gen_modlist.py` reads and writes UTF-8/LF (it failed on Windows).

### 2026-10-18: Aluminium line (Bayer + Hall-Héroult), Periodic Table perks
- **Design decisions** (user): pacing ~100–120 h from content, not grind; one balanced path (no packmodes); no GTCEu for now,
  GT-style chemistry lines on MI instead; Warbucks Core grows (perks, reaction conditions, prospecting).
- **Aluminium is chemistry now** (`startup_scripts/aluminum_line.js`, `server_scripts/phase4_aluminum.js`): Bayer digestion and
  precipitation in the Mixer (with the lye recycled), calcination in the EBF, then the new **Hall-Héroult Cell** LV multiblock.
  MI's bauxite → EBF and bauxite → Electrolyzer shortcuts are removed. New fluid: sodium aluminate solution.
- **Quests** (T4): 6 new (Lye for the Digester, Bayer Digestion, Precipitation, Alumina, The Hall-Héroult Cell, and the optional
  Alchemist's Alumina). Bauxite, Aluminum, A Hint of Titanium, Electrolysis and Lye reworded for the new route. 1,178 quests.
- **Warbucks Core 1.1.0**: Periodic Table perks (`/warbucks elements`). Post-Transition Metals (Al, Sn, Pb, In) → +2 armor
  toughness. Groups are configurable (`perks.groups`).
- Tools: `test/build_id_index.py` reads the pack's KubeJS lang files (MI machines registered from KubeJS); `tools/build_quests.py`
  writes UTF-8/LF and keeps folders (Windows/OneDrive); `test/smoke.ps1` takes `LOCAL_MOD_JAR` to test an unreleased mod build.
- Smoke test passes with the released 1.1.0 jar (GitHub release `warbuckscore-v1.1.0`): 6,269 KubeJS recipes added (+6),
  195 removed (+3), 0 failed.

### 2026-10-18: Windows desktop setup, PowerShell smoke test
- **Fix: stale pack index.** `pack/index.toml` had old hashes for three quest files (`creation.snbt`, `t3.snbt`,
  `lang/en_us.snbt`), so packwiz-installer would reject them. Refreshed.
- **`.gitattributes`** (`* -text`): Git never converts line endings, so Windows checkouts hash the same as the Mac's.
- **`test/smoke.ps1` + `test/lib.ps1`**: PowerShell port of `smoke.sh`/`lib.sh`. The first run sets up `test\server`
  (packwiz-installer-bootstrap v0.0.3, NeoForge 21.1.262). First Windows run: server reached Done in 7.5s, no
  dependency, mixin, KubeJS or worldgen errors. It reported FAIL only on the harmless loot-table and recipe lines,
  because `test/known_issues.txt` was never committed. That file is now committed; with it the Windows smoke test
  passes (Done in 6.3s, 106 known harmless lines, 0 failures).
- `docs/DESKTOP_SETUP.md`: Windows smoke test, line endings, Claude shell loopback note.

### 2026-10-18: Warbucks Core (custom mod), dissolver coverage, formula tooltips
- **Warbucks Core 1.0.0**: the pack's own NeoForge mod. Source is in `mod/`; the jar is published as a GitHub release
  and installed by packwiz from that URL.
  - **Spectrometer** (LV: amethyst prism, steel plates, copper wire, analog circuit). Right-click to read the ore
    signal in the loaded chunks around you (radius 4 chunks). It lists each element (from `c:ores/*` tags) with
    strength, direction, distance and average depth. It reads each chunk section's block palette, so scans are cheap.
  - **Biome Capsule** (glass bottle + rubber sheet + any sapling). Sneak + right-click records the biome you stand in.
  - **Terraformer** (made from the Seed of a New World + processing units + energy cores). Give it a capsule, then
    Charged Energy Cores (`#warbuckscore:terraformer_fuel`; 1 core = 9 chunks). It rewrites the biome nearest-first out
    to 9x9 chunks, like `/fillbiome`. Tested on a server: the centre chunk and its ring of 8 converted, the next ring stayed untouched.
  - Settings: `config/warbuckscore-common.toml`. Recipes: `kubejs/server_scripts/warbuckscore.js`.
  - Quests: "The Spectrometer" (T3, optional); "A Sample of Somewhere", "The Terraformer" and "A World You Chose" (Creation).
- **Dissolver coverage** (`tools/build_dissolver.py` → `kubejs/config/dissolver_recipes.json`, loaded by
  `server_scripts/dissolver_generated.js`):
  - 6,041 new dissolver recipes for modded and missing blocks. Each copies the output of an analogous block Alchemistry
    already handles (planks, stone, glass and so on), scaled for slabs and panes.
  - Machines, metals, storage blocks, ores and ProjectE items are skipped on purpose; the rest is listed in
    `docs/dissolver-coverage.md`.
  - Also fixes Alchemistry's 1.21.1 recipes for glass and carpets, which point at empty tags.
  - One 289 KB table instead of 6,000 files, so packwiz syncs stay fast.
- **Formula tooltips** (`kubejs/client_scripts/formula_tooltips.js`): 297 chemistry items (MI, Mekanism, EI, the pack's
  own items) show their formula, e.g. "H₂SO₄ · sulfuric acid". ChemLib already shows its own.
- 221 mods. Book: 1,172 quests. Smoke test passes (6,263 KubeJS recipes added, 0 failed).

### 2026-10-18: Dedicated server kit
- New `server/` kit (see docs/SERVER.md):
  - `install.sh`: sets up the server folder.
  - `start.sh`: pulls the pack from GitHub on every start, installs or upgrades NeoForge automatically, restarts after a crash.
  - `server.properties`: whitelist on, `allow-flight=true`, Normal difficulty, 10 players.
  - `user_jvm_args.txt`: 8–12 GB.
  - `warbucks.service`: systemd unit plus tmux.
- Daily full backups, 7 kept (Simple Backups, `pack/config/simplebackups-common.toml`).
- The test server now also uses `allow-flight=true`.
- Tested on this Mac:
  - A fresh install from the GitHub URL reached Done with 203 server mods.
  - `stop` exits cleanly.
  - A second start only updates the pack.
- **Live:** Warbucks replaced ATM10 on the VPS (user decision). `warbucks.service` is enabled. ATM10 stopped with 0 players
  online and is disabled; its folder is untouched. First start: Done in 7.6s, 38 chapters / 1,168 quests,
  0 failed recipes; log check passes.

### 2026-10-18: Empty starting inventory
- New players no longer get join gifts. Switched off in pack/config:
  - Modern Industrialization guidebook (on first join and on respawn)
  - Ars Nouveau Worn Notebook
  - Silent Gear material book and starter blueprint package
  - Advanced Peripherals manual
- All of them can still be crafted. The Advanced Peripherals manual's own recipe is in the old pre-1.21 format and
  never loads, so `phase5_balance.js` adds a working one: book + wired modem.
- Client log after the v8 relaunch: world joined, 38 chapters / 1,168 quests loaded, only known harmless issues.
  Smoke test passes.

### 2026-10-18: Quest book v8: end goal, categories, hunting (1,168 quests)
- **Quest engine:** new task types: kill counts, structure, biome, and "any of" items or tags (FTB Filter System smart filters).
  Also new:
  - quest flags: hidden, secret (always optional) and alternative-route ("any one dependency");
  - quest links between chapters;
  - reward tables: random loot and choose-one;
  - `{@pagebreak}` deep-dive pages;
  - `QUEST_ONLY=` partial checks.
  Tier milestones in T0–T7 also roll that tier's loot table.
- **Book layout:** 7 category groups (The Demigod's Path, Chemistry Lab, Engineering, Magic and Relics, Exploration,
  Farming and Food, Collections) with one page per mod family. 38 chapters, 1,168 quests (up from 589); 433 optional, 26 secret, 74 kill quests.
  - Split: Divine Gifts → Ars Nouveau / Apotheosis / Relics / Occultism; Other Worlds → Worlds / Twilight Forest / Space;
    Storage → Storage / Applied Energistics; Farming → Farming and Food / Mystical Agriculture. Quest keys unchanged, so progress is kept.
  - New chapters:
    - **The end goal:** The Seed of a New World (finale around the 9x9 capstone), then Creation (post-Seed goals).
    - **Chemistry:** Lab Notebook (30 chemistry deep dives), Mekanism.
    - **Other:** ProjectE (lite), Building, Exploration (structures and biomes), Monster Hunting (kill counts, bosses), Completionist, The Demigod's Market.
- **Token shop overhaul:**
  - New Greater Demigod Token (= 9 tokens, exchanged both ways).
  - Three price bands: small (1–3), medium (4–8, raw ores and mob drops) and large (paid in Greater Tokens).
  - Convenience only: the shop never sells machines, circuits or tier skips.
  - 14 reward tables: one per tier, plus hunt, boss, three pick-one tables and secret.
- **Balance fixes** (`kubejs/server_scripts/phase5_balance.js`):
  - Mekanism Chemical Injection Chamber, Dissolution Chamber, Washer and Crystallizer need Advanced (MV) circuits instead of Elite/Ultimate. The 4x/5x ore chain now sits at MV, as designed, behind the acids.
  - Reliquary Alkahestry no longer duplicates metals, gems or Nether Stars, matching the ProjectE-lite rules.
- 220 mods. Smoke test passes (FTB Quests: 38 chapters, 1,168 quests, 14 reward tables).

### 2026-10-18: Gap-analysis mods, ProjectE "lite"
- Added (user picks):
  - Magic: ProjectE (lite), Ars Elemental, Ars Additions.
  - Endgame: Gateways to Eternity, Mekanism Extras.
  - Space chemistry: Ad Astra Giselle Addon.
  - Building and logistics: Copycats+, Entangled, Artemis' Laboratory Blocks.
  - QoL: Jade Addons, Entity Culling, Trade Cycling, Just Zoom, Chat Heads, Ping Wheel.
- Declined: Immersive Aircraft. "Building Sticks" = ATM10's Construction Sticks, already in the pack.
- **ProjectE "lite"** (`kubejs/server_scripts/phase4_projecte.js`, `config/ProjectE/custom_emc.json`):
  - The Philosopher's Stone needs oganesson.
  - Condensers, Collectors and Relays are removed.
  - Metals, gems, dusts, Nether Star, Dragon Egg and Beacon have no EMC.
  - Verified with real EMC values (new `test/emc_check.sh`): 8,159 → 3,881 items with EMC. Ingots, gems and anything made from them have none; building blocks keep theirs.
  - Lessons learned:
    - ProjectE only maps EMC on datapack sync, so a headless server needs `/reload`.
    - Custom-conversion datapack files reject 0; only `custom_emc.json` accepts it.
- Known-harmless: Mekanism Extras loot tables for unregistered factory tiers.
- 220 mods. Smoke test passes.

### 2026-10-18: Crafting On A Stick
- Added Crafting On A Stick 1.21.0.6 (portable crafting table, stonecutter, smithing table, anvil, grindstone, loom, cartography table).
- Quests: "Crafting on a Stick" (QoL) and the optional "A Whole Workshop". Book: 589 quests. 205 mods. Smoke test passes.

### 2026-10-18: Quest book v7: detailed (587 quests)
- Five parallel writers expanded every chapter following `tools/quests/STYLE.md`; each quest is now one file per chapter in `tools/quests/`.
  - Every quest has a subtitle and a structured description: What / Chemistry / How / Tip.
  - Smaller steps throughout.
  - 118 optional side quests (off the main line, 1–2 tokens).
  - Gold "memory returning" story lines at each chapter's opening and milestones.
- Quests: 213 → 587. No existing quest keys changed, so player progress is kept.
- Progression bugs found by reading the real mod recipes, and fixed:
  - Item pipes need steel gears, so they moved to Chapter II.
  - The steam cutter needs lubricant.
  - The steam boiler needs the Iron Hammer / fire-clay chain.
  - Coal dissolves into graphite, and wood into cellulose.
  - The Chapter V order was impossible (the Electrolyzer and Chemical Reactor need an electronic circuit and aluminum); dependencies re-sequenced.
  - The Nether has no sulfur (it comes from lignite or lava).
  - Boron and noble gases can't be dissolved early (Fusion Chamber only).
  - Desh is on the Moon, not Mars.
  - The Apotheosis reforging table needs netherite.
  - The Potion Filter needs 2 Extra Long potions, not 7.5.
- **Flight fix:** Apothic's Potion of Flying needs popped chorus fruit (End only), which broke "flight after the Nether". New recipe in `phase4_flight.js`: Potion of Levitation + 2 hydrogen → Potion of Flying (potion ids checked at runtime).
- TelePastries' Twilight Cake now needs an MI digital circuit (HV), matching the Twilight Forest gate.
- The capstone uses **8** Antimatter Cores (the comments and docs said 4).
- The Chapter IV/VI Electric Blast Furnace overlap is resolved (VI is now stainless steel only, after IV's EBF).
- Server: "Loaded 21 chapters, 587 quests"; KubeJS 0 failed; smoke test passes.

### 2026-10-18: Compact Machines room templates
- In-game: "No Room Templates are registered!" Compact Machines 7 ships its templates as an optional built-in datapack that's off by default.
- Copied that pack's data (8 room templates, their recipes and advancements; MIT licence) into `pack/kubejs/data/compactmachines/`, so the templates are always on, in every world and on servers. Verified on the server: all 8 templates are registered.
- Note for the future: KubeJS rejects files in `kubejs/data` with uppercase names (a README.txt there stopped the server).

### 2026-10-18: Create re-added as the early mechanical tier
- **User decision: Create is back** (reverses the original "No Create" rule; CLAUDE.md updated, mod target raised to about 210–215).
- Added Create 6.0.10, Crafts & Additions, Enchantment Industry (+ Dragons Plus), Create: Connected, Create: New Age and Create Deco. Destroy and Steam 'n' Rails have no 1.21.1 build.
- New `kubejs/server_scripts/phase4_create.js`:
  - Crushing ore yields capped at 2x.
  - The Alternator and New Age Generator Coil need an MI analog circuit (LV).
  - New Age reactor rods need an MI processing unit (EV).
- New quest side chapter "The Mechanical Age" (13 quests, Zn banner). Book: 21 chapters, 213 quests.
- Known-harmless: Create: Connected's dye-depot loot tables, the Create Deco placard recipe, and Enchantment Industry's Reliquary XP-fluid data map.
- Worldgen: Create zinc ore and New Age thorium ore generate; no errors. 204 mods. Smoke passes (3 attempts; fix: reactor-rod pattern padding).

### 2026-10-18: Suggested mods (user picks)
- Added:
  - World: Towns and Towers, Regions Unexplored, YUNG's Better Dungeons/Mineshafts/Strongholds.
  - Gameplay: Farmer's Delight, Occultism, Mekanism MoreMachine, Sophisticated Storage in Motion.
  - Map and admin: JourneyMap, Chunky.
  - Libraries: Cristel Lib, Lithostitched, YUNG's API, SmartBrainLib, Modonomicon.
- New `kubejs/server_scripts/phase4_occultism.js`: removes 17 Occultism miner recipes for chemistry-milestone resources (uranium, uraninite, osmium, fluorite, platinum, iridium, tungsten), matching the Mystical Agriculture rules.
- Known-harmless issues added: MoreMachine loot tables for unregistered variants; a Farmer's Delight compat recipe for a Silent Gear block that doesn't exist.
- Worldgen check (r=256): Better Dungeons, a Towns and Towers village, Regions Unexplored biomes and BOP biomes all generate; no worldgen errors. `test/worldgen.sh` locates the new structures and biomes too.
- 197 mods (the upper end of the 100–200 target). Smoke and worldgen pass after 3 attempts (fixes: known-issues allowlist, correct T&T structure id).
- Pending: the user wants Create plus some addons back, which reverses the original "No Create" requirement. Awaiting answers to scoping questions.

### 2026-10-18: Quest book v5 (200 quests)
- New side chapters:
  - **The Periodic Table** (11): element groups from alkali metals to actinides, each with real chemistry, ending at element 118.
  - **Power** (11): Generator Galore → Mekanism heat/gas-burning (H₂) → solar → MI diesel → Powah reactor → industrial turbine → fusion.
  - **Automation and Logic** (8): CC: Tweaked, Advanced Peripherals, Integrated Dynamics, SFM, Logistics Network, LaserIO cards, AE2 chemical autocrafting.
- **Other Worlds** expanded (+9): Otherside echo shards, Undergarden metals, the Naga and Lich, Twilight metals, Mars, Venus, alien metals.
- New banners: Og, U, Ge. Book: 20 chapters, 200 quests. Smoke test passes.

### 2026-10-18: Visual fixes from the first client launch
- The client log was clean, apart from one missing texture: the Demigod Token pointed at a texture that doesn't exist (`minecraft:item/sunflower`). It now has its own 16x16 coin texture (`kubejs/assets/kubejs/textures/item/demigod_token.png`).
- World select (and 27 other menus) now show the pack background: FancyMenu universal layout plus ATM10's menu list (minus Embeddium/KeyBind Bundles; plus Create World).
- The quest book now has a background: an FTB Quests theme (`kubejs/assets/ftbquests/ftb_quests_theme.txt`) with a seamless navy lab-grid tile, cyan borders and gold hover text.

### 2026-10-18: Pack aesthetic (title screen, loading screen, quest banners)
- Added FancyMenu 3.9.14 (+ Konkrete, Melody) and Drippy Loading Screen 3.1.5.
- New `tools/build_art.py` (Pillow) generates:
  - `config/fancymenu/assets/background.png`: a starfield over a faint periodic table, with molecule rings.
  - `logo.png`: WARBUCKS spelled in real element tiles (W, Ar, B, U, C, K, S) with CHEMISTRY in gold.
  - 17 chapter banners in `kubejs/assets/warbucks/textures/quests/`, each with a tier tile or a fitting element.
- FancyMenu layouts (format from ATM10's public config):
  - Title screen: custom background and logo; the vanilla logo, splash text and Realms are hidden.
  - Loading screen: background, logo and a cyan progress bar.
  - Window title "Warbucks Chemistry".
- Quest book: every chapter shows its banner, the Welcome chapter shows the logo, main chapters use rounded-square nodes and side chapters circles. Divine Ascent re-laid out so no lines cross the map.
- New `test/build_quest_preview.py`: a local, clickable HTML mock of the quest book, plus static chapter renders (not committed, because they contain mod textures).
- 181 mods. Smoke test passes. **The client-side look still needs checking in-game.**

### 2026-10-18: Ore deposits
- New `tools/build_deposits.py` generates vanilla-format worldgen into `pack/kubejs/data/` (no extra mod):
  - MI's scattered tin, lead, bauxite, nickel, antimony, uranium and tungsten ore cut to 35%.
  - New rare **deposits**: in 1 of every 16–30 chunks, 2–9 large ore blobs cluster in a narrow depth band.
- Measured (radius 384, 2,401 chunks): totals 66–78% of before, but concentrated. Tin: median chunk 35 ores, deposit chunks 500–700. Lead: 54 vs about 830.
- Worldgen check passes.

### 2026-10-18: GitHub, chemistry mechanics, quest book v4
- **Public GitHub repo:** https://github.com/Grandpawarbucks/Warbucks-Chemistry-Pack. Server details were scrubbed and the history restarted fresh; the full history is kept locally only.
- New `launcher/Warbucks-Chemistry-Prism.zip`, an importable Prism instance that updates itself from GitHub on every launch (tested: installs all 177 mods from the GitHub URL). New `docs/DESKTOP_SETUP.md` covers playing and developing on Windows.
- New `kubejs/startup_scripts/chemistry_items.js`: 9 items (PGM line intermediates, Demigod Token, energy cores, Seed of a New World).
- New `kubejs/server_scripts/phase4_chemistry.js` (30 recipes):
  - **Ore byproducts:** Mekanism dirty dust → MI Centrifuge gives the main dust plus a geologically real bonus (lead → silver, osmium → iridium and others).
  - **Haber-Bosch** (ammonia) and **Ostwald** (nitric acid), using ChemLib fluids (ids checked at runtime: `chemlib:*_fluid`).
  - **Platinum line** (5 steps): anode sludge → aqua regia → ammonium hexachloroplatinate → calcine; the residue centrifuges into iridium, osmium, rhodium and ruthenium.
  - **Energy cores:** empty → charged (about 3M EU in the MI Assembler) → Antimatter Core.
  - **Capstone:** Seed of a New World, a 9x9 Ultimate Table recipe with an intermediate from every tier.
  - **Demigod Token shop:** 10 convenience trades.
- **Quest book v4:** 17 chapters, 162 quests.
  - New Welcome chapter and Quality of Life side chapter.
  - New quests for byproducts, Haber-Bosch, Ostwald, the platinum line, energy cores and the Seed.
  - "A New World" now requires the Seed.
  - Generous, tier-scaled rewards: Demigod Tokens on every quest (512 total; 1/quest early up to 8 in Creation, doubled for milestones), plus milestone items (metals, circuits, free first machines, XP).
- **Ore veins (GTMOGS) not added:** its KubeJS support is broken (per its README), it turns off all vanilla ore generation, and its newest commit "breaks datagen". A safer alternative is proposed.
- 177 mods. KubeJS: 149 added, 133 removed, 0 failed. Smoke test passes.

### 2026-10-18: Flight gating (Option 2), Angel Ring, Iron Jetpacks
- Added Angel Ring (CurseForge; ⚠️ the only 1.21.1 file is 3.0.0 beta.3; deps Flight API, HaydenAPI) and Iron Jetpacks 8.0.11 (13 months old).
- New `kubejs/server_scripts/phase4_flight.js`:
  - The Infusion Pylon needs hydrogen from the Dissolver.
  - The four jetpack coils need MI LV/MV/HV/EV circuits (every jetpack tier uses a coil).
  - The Angel Ring needs an MI digital circuit.
- Quests: new "Lighter than Air" (hydrogen) step before the pylon; "Jetpacks" and "The Angel Ring" in Tools and Comfort. 141 quests.
- 177 mods. KubeJS: 119 added, 133 removed, 0 failed. Smoke test passes.

### 2026-10-18: Monifactory-inspired mods
- Added Hostile Neural Networks, Extended Crafting, PackagedAuto + PackagedExCrafting, Compact Machines (CurseForge), Cable Facades and TelePastries.
- New `kubejs/server_scripts/phase4_monifactory.js`: HNN simulation needs MV; Extended Crafting's big tables need MV/HV/EV circuits.
- New quest side chapter "Mob Data and Big Crafting" (11 quests). Book: 15 chapters, 138 quests.
- Declined: Lost Cities and William Wythers' Overhauled Overworld (user). Skipped: Ender IO and Bountiful (betas), plus GregTech, MoniLabs and MAE2 (not on 1.21.1).
- 173 mods. KubeJS: 113 added, 127 removed, 0 failed. Smoke test passes.

### 2026-10-18: Quest book v2 (step-by-step), Silent Gear, Mekanism Tools
- Added Silent Gear (+ Silent Lib) and Mekanism Tools (paxels). Tinkers' Construct has no 1.21.1 build (newest is 1.20.1 Forge), so Silent Gear replaces it. Comforts (sleeping bags, hammocks) was already in.
- NeoForge version checking turned off (`config/fml.toml`): update-check timeouts were cluttering the logs.
- Quest book rewritten to walk players through every step: 14 chapters, 127 quests (was 11 and 69).
  - New "Getting Started": JEI and Ultimine tips, tools, food, sleeping bag, iron, water, backpack, claiming land, paxel, first Silent Gear tool.
  - Every MI steam machine in order, the electronic components inside an analog circuit, each LV machine, and the Mekanism entry (infuser → circuits → enrichment).
  - New chapter "IV. The Electric Age". Added stainless steel/EBF, salt, cracking, PVC, semiconductor silicon and space-suit steps.
  - New side chapter "Tools and Comfort": Silent Gear grader and salvager, paxels from bronze to refined obsidian, hammock, waystones.
  - Every quest has a "How:" line.
- Generator split into `tools/questlib.py` (helpers, id checks), `tools/quest_data.py` (content: edit this one) and `tools/build_quests.py` (writes the SNBT files and `docs/QUESTS.md`).
- New `docs/QUESTS.md`: a readable overview of every chapter and quest.
- 166 mods. Server log: "Loaded 3 chapter groups, 14 chapters, 127 quests". Smoke test passes.

### 2026-10-18: Phase 5 (FTB Quests)
- New quest book, "Warbucks Chemistry: The Demigod's Codex": 11 chapters, 69 quests, generated by `tools/build_quests.py`.
  - The Demigod's Path (T0–T6): Awakening, Steam and Steel, Divine Ascent, Electrochemistry and Acids, Petrochemistry, Materials and Nuclear, Creation.
  - Divine Workshop (side chapters): Storage and Logistics, Divine Gifts, Other Worlds, Farming.
- Every quest teaches the chemistry behind its step (pyrolysis, reduction, alloys, destructive distillation, electrolysis, the contact process, hydrometallurgy, fractional distillation, polymerisation, chlor-alkali/PVC, isotope separation, transmutation, antimatter).
- Format checked against the FTB Quests v2101.1.36 source; text lives in `lang/en_us.snbt`.
- New `test/build_id_index.py`: indexes every item, block and dimension id (vanilla + all mods). The quest build fails on any unknown id.
- Server log: "Loaded 3 chapter groups, 11 chapters, 69 quests", no warnings. Smoke test passes.

### 2026-10-18: AE2 addons, Mystical Agriculture (gated)
- Added AE2 addons: Applied Flux, Advanced AE, AE Infinity Booster, ME Requester, AE2 Import Export Card. These join MEGA Cells, ExtendedAE, AE2WTLib, Applied Mekanistics and AE2 JEI Integration.
- Added Mystical Agriculture (+ Cucumber), gated by the new `kubejs/server_scripts/phase4_mysticalagriculture.js`:
  - 12 chemistry-milestone crops blocked.
  - 46 tier 3–5 seed recipes now need an MI LV/MV/HV circuit.
- Known-harmless log line added: AE2 Import Export Card has a client-only mixin that the server skips.
- 163 mods. KubeJS: 108 added, 122 removed, 0 failed. Smoke test passes.

### 2026-10-18: Generator Galore, Botany Pots
- Added Generator Galore 1.7.0 (CurseForge; the Modrinth build is 19 months old) and Botany Pots (Hopper Botany Pots are built in). Iron Furnaces was already in the pack.
- 156 mods; smoke test passes. Mystical Agriculture is pending a design decision.

### 2026-10-18: Phase 4 (integration)
- New `kubejs/server_scripts/phase4_integration.js` (commented): 15 recipes replaced or added that tie Alchemistry, Mekanism circuits, Powah, AE2, Flux Networks, the Undergarden and Ad Astra to MI's chemistry-gated tiers. Full table in PROGRESSION.md §7.
- Uraninite is now made by oxidising uranium in MI's Chemical Reactor (closes the Phase 3 gap).
- KubeJS: 62 recipes added, 65 removed, 0 failed. Smoke test passes.
- Known: the Iron Furnaces vibranium and unobtainium upgrades fail to parse because they need ATM10-only metals. They were already broken before this change, are harmless and can't be crafted.

### 2026-10-18: Building mods
- Added: Construction Sticks, Effortless Building, FramedBlocks, Rechiseled, Supplementaries, Handcrafted (19 months old), and the Macaw's set (Doors, Windows, Roofs, Fences and Walls, Bridges, Trapdoors, Lights and Lamps, Paths and Pavings, Furniture, Stairs). Building Gadgets 2 was already in.
- New libraries: Moonlight, Fusion, SuperMartijn642 Core/Config.
- Left out: Copycats+ (Create addon), Chipped (stale), LittleTiles (pre-release), Decorative Blocks (no 1.21.1 build).
- 154 mods; smoke test passes.

### 2026-10-18: Phase 3 (compatibility pass)
- **Almost Unified:** MI is the top-priority mod (then Mekanism, AE2, Ad Astra, ChemLib, Alchemistry, Powah, Just Dire Things, Extended Industrialization). 723 recipes unified, 121 duplicates merged. Debug dumps are off again.
- **Ore generation:** Mekanism tin/lead/uranium off (`config/Mekanism/world.toml`). Powah uraninite ore off (`kubejs/data/powah/neoforge/biome_modifier/`). Verified with `test/ore_scan.py` over 1,089 chunks: Mekanism now generates only osmium and fluorite, there's no Powah ore, and MI supplies tin, lead and uranium.
- **Ore processing:** `kubejs/server_scripts/phase3_compat.js` caps pre-acid routes at 2× per ore block: MI Macerator (11 recipes), MI Forge Hammer with tool (8), Integrated Dynamics squeezer (14) and mechanical squeezer (14).
- **Petrochemistry:** removed `ad_astra:refining/fuel_from_refining_oil` (rockets use MI diesel). MI ethylene is tagged `c:ethene` so it feeds Mekanism HDPE.
- Decisions recorded in PROGRESSION.md §6. Smoke test and worldgen check pass.
- Known gap until Phase 4: Powah uraninite has no source yet.

### 2026-10-18: Phase 2: client test and ore check
- Client (Prism "Warbucks Chemistry (Dev)"): launched and joined a world. No crashes or real errors.
  - 5 harmless errors (SFM/ExtendedAE loot tables, FTB entity icons, a GeckoLib animation).
  - About 5,000 cosmetic "Unknown recipe category" warnings from Alchemistry recipes in the vanilla recipe book.
- `test/parse_logs.py`: new loot-table check, a catch-all "Other ERROR lines" section, a `--client` mode, and `test/known_issues.txt` (an allowlist of harmless lines, each with a reason).
- New `test/ore_scan.py`: reads region files and counts ore blocks by mod (decoder sanity-checked).
  - In 49 spawn chunks, MI, Mekanism and Powah ores all generate.
  - Duplicates for Phase 3: **tin** (MI + Mekanism), **lead** (MI + Mekanism), **uranium** (MI + Mekanism + Powah uraninite).

### 2026-10-18: Phase 2: worldgen check
- `test/worldgen.sh` (radius 256, seed 20261018): 1,089 chunks generated in 10s with no worldgen errors.
  - Found: Plains village, mineshaft, Ancient City, BOP Redwood Forest (at spawn), BOP Lavender Field.
  - Not yet checked: that modded ores (MI, Mekanism) appear in the generated chunks. A block-scan check is planned.
- ATM10 left-out list with reasons added to MODLIST.md. Added Invasive Optimizations (optional Create integration, flagged), Borderless Window, Simple Backups, AttributeFix. 134 mods.

### 2026-10-18: Phase 2: tech, logic and AE2 addons
- Added (user-approved):
  - Power: Powah, Flux Networks, Extended Industrialization, Industrialization Overdrive.
  - Logistics: Pipez, LaserIO, Super Factory Manager, Logistics Network.
  - Logic: CC: Tweaked + Advanced Peripherals, Integrated Dynamics/Tunnels/Terminals/Crafting.
  - Automation: Just Dire Things.
  - AE2 addons: AE2WTLib, ExtendedAE, MEGA Cells, Applied Mekanistics, AE2 JEI Integration.
- New libraries: Cloth Config, Tesseract API, Cyclops Core, Common Capabilities, Glodium.
- Fixed: ExtendedAE's dependency step added a second AE2 entry from CurseForge, which deleted the AE2 jar on sync. Removed the duplicate. `sync_pack` now fails on duplicate jar filenames.
- 130 mods; smoke test passes.

### 2026-10-18: Tooling, test loop, Phase 2 (mod list, in progress)
- Tools: Temurin 21, Go and packwiz installed. The NeoForge 21.1.262 test server and packwiz-installer-bootstrap are in `test/`.
- Test loop: `test/smoke.sh`, `test/worldgen.sh`, `test/parse_logs.py`, `test/mrcheck.py`, `test/client-sync.sh` (Prism hook). Prism instance "Warbucks Chemistry (Dev)" created.
- Pack: 105 mods. Smoke test passes (server start about 16s wall clock).
  - Core: MI, Mekanism + Generators, Alchemistry/ChemLib/AlchemyLib, AE2.
  - Magic: Ars Nouveau, Relics, Artifacts, Reliquary Reincarnations, Apotheosis suite.
  - Flight: Pylons + Apothic Attributes.
  - World: Biomes O' Plenty, Undergarden, Twilight Forest, Deeper and Darker, Ad Astra.
  - Storage: Sophisticated Storage/Backpacks + Item Actions + Storage Plus + Backpack Plus, Functional Storage, Tom's Simple Storage. Iron Furnaces.
  - FTB suite (Library, Teams, Quests, Chunks, Ultimine, Essentials, Ranks, Filter System, XMod Compat, JEI Extras).
  - QoL and performance mods taken from ATM10 8.3's mod list.
- Smoke-test fixes: added GeckoLib (Ars Nouveau) and Architectury (OctoLib), which the mod metadata doesn't declare. Made the test script survive a server that dies early.
- JVM args: ATM's official Java 21 server args, recorded in docs/README.md.
- New: `docs/README.md`, generated `docs/MODLIST.md` (from `docs/modlist-meta.tsv`).

### 2026-10-18: Phase 1 v2 (Design pitch after reset)
- New `docs/PROGRESSION.md`: demigod identity, 6 design pillars, 7 tiers (T0–T6), grind controls, open items.
- Decisions: MI backbone; Alchemistry/ChemLib for full disassembly and synthesis; Mekanism for gases and nuclear; AE2; Ars Nouveau + Relics + Artifacts + Reliquary Reincarnations; Apotheosis suite; Biomes O' Plenty; dimensions (Undergarden, Twilight Forest, space).
- Flight: Pylons Infusion Pylon + Apothic Attributes Potion of Flying (Pylons on 1.21.1 has no Flight Pylon block).
- Dropped: Immersive Engineering, Immersive Petroleum, PneumaticCraft, ProjectE.
- Verified NeoForge 1.21.1 builds for every mod named in PROGRESSION.md §2 (Modrinth API / CurseForge files pages).

### 2026-10-18: Design reset
- Reset at the user's request. The earlier 8-tier design (in git history, commit 2f97494) has been dropped.
- New direction: chemistry and technology, light magic, no ProjectE, GregTech/Monifactory-inspired but without long grinds, item disassembly into chemicals, normal Overworld start, demigod story, and creative flight from a crafted item (Pylons-style).
- Next step: clarifying questions, then a new design pitch.
