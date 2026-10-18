# Changelog

All changes to the Warbucks Chemistry Pack are logged here, newest first.

## [Unreleased]

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
