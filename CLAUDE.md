## Core requirements
- Mod loader: NeoForge. Target Minecraft 1.21.1. If a key mod isn't on NeoForge
  1.21.1, tell me and lay out the tradeoff rather than quietly substituting or
  changing versions.
- Theme: Chemistry is the center of the pack. Progression runs through real
  chemistry ideas: elements and compounds, ore processing, separation and
  refining, gases and fluids, reactions, petrochemicals, and synthesis of
  advanced materials. Most tech tiers need chemical intermediates, not just
  more metal ingots. ChemLib (elements and compounds) is the shared chemistry
  item library.
- Story: Guided by an FTB Quests storyline. The player is a demigod who spawns
  in a normal Overworld and uses chemistry to shape the world they want to
  live in. Biome mods are welcome.
- Design direction (reset 2026-10-18): Chemistry + technology, with light magic
  where it fits. Inspired by GregTech and Monifactory, but no long grinds:
  every tier should feel worth it, not padded. ProjectE: allowed only as 'lite'
  (user decision 2026-10-18): Philosopher's Stone needs oganesson; no Condensers/Collectors/Relays;
  metals/gems/dusts/Nether Star have 0 EMC via pack/config/ProjectE/custom_emc.json (verified with
  test/emc_check.sh). NOTE: ProjectE custom-conversion datapack files can't hold 0; only custom_emc.json can.
- Decisions (2026-10-18 Q&A):
  - Tech backbone: Modern Industrialization.
  - Disassembly: once a player has built the machine (Alchemistry Dissolver /
    Combiner), they can break ANY block into elements and synthesize blocks
    from elements. Goal: the player builds up the whole periodic table and
    synthesizes the game's blocks from chemicals. Modded blocks need KubeJS
    dissolver/combiner recipes (Phase 4).
  - Light magic: Relics, Artifacts and Ars Nouveau, plus story-only divine items
    (KubeJS).
  - Flight (decided 2026-10-18, "Option 2"): every flight source is a chemistry milestone
    (pack/kubejs/server_scripts/phase4_flight.js). Infusion Pylon + Potion of Flying (end of Ch. II:
    needs chemlib:hydrogen from the Dissolver plus Nether materials), Iron Jetpacks (coils need MI
    LV/MV/HV/EV circuits), Angel Ring (MI digital circuit + Elytra + Nether Stars). Flight works
    anywhere (no claim-only restriction). Pylons on 1.21.1 has NO Flight Pylon block.
- Technology: Strong automation and industrial tech supporting the chemistry
  (power, fluid/gas logistics, item transport, storage, autocrafting).
- Create (CHANGED 2026-10-18, user decision, reverses the original "No Create" rule): Create is
  allowed as an EARLY MECHANICAL TIER that feeds into MI. Addons: Crafts & Additions, Enchantment
  Industry, Create: Connected, New Age, Deco. Create ore processing obeys the same caps as everything
  else before acids (<= 2x per ore block, <= 1.5x per raw ore); its power and electric parts are gated by MI
  circuits (pack/kubejs/server_scripts/phase4_create.js). Destroy and Steam 'n' Rails have no 1.21.1 build.
- QoL: The FTB suite (Library, Teams, Quests, Chunks, Ultimine, Essentials,
  Ranks, Filter System, XMod Compat, and others that fit), plus standard QoL
  (JEI or EMI, Jade, AppleSkin, Mouse Tweaks, inventory sorting, etc.).
- Performance and libraries: All the Mods 10 (ATM10, NeoForge 1.21.1) is the
  reference. Pull its performance and shared library mods from its current mod
  list. Include them unless they conflict or only support ATM10 content we
  aren't using, and list any left out with the reason. Use ATM10's JVM argument
  recommendations as the starting point and record them in docs/README.md.

## Player setup
- macOS (Apple Silicon), 24 GB RAM. Launcher: Prism (already installed).
- Fewer than 10 players (small server).
- Mod sources: CurseForge preferred, but either is fine. Use Modrinth when a mod
  is on both, because packwiz-installer downloads from it reliably. Use CurseForge
  for CF-only mods (ChemLib, Alchemistry, AlchemyLib, ProjectE). Flag any CF mod
  that blocks third-party downloads.
- Difficulty: ATM10-like (moderate gating, not expert-mode).
- The user is comfortable editing configs and KubeJS scripts.

## HANDOFF (2026-10-18, Mac → Windows desktop)
Development moves to the user's Windows desktop. Start there with `git pull`, then read this file and
docs/DESKTOP_SETUP.md. The user carries private memory notes (VPS rules) over in the git-ignored `handoff/` folder.
State at handoff: everything committed and pushed. 221 mods, 1,172 quests, smoke test passing; Warbucks LIVE on the VPS.
Open items / next steps, in order:
1. Test loop on Windows: smoke DONE and PASSING (test/smoke.ps1 + lib.ps1, 2026-10-18). test/known_issues.txt is now
   committed (it was git-ignored and Mac-only). Run Java and Gradle from a real terminal or the app's Terminal panel
   (they fail with "loopback connection" in Claude's shell). worldgen/emc_check/client-sync are still bash only.
2. LIVE SERVER: DONE 2026-10-18 20:17. Restarted with 0 players and the user's OK; now runs main at 33c52d1 (Warbucks Core
   loaded). For later updates: `systemctl restart warbucks` pulls the latest, but check `list` for 0 players and ask first.
3. Spectrometer: needs an in-game test (right-click near ores). The Terraformer was tested on a server.
4. GregTech decision (2026-10-18): no GTCEu for now (docs/research/gtceu.md; revisit if a stable 8.x lands on Modrinth).
   Keep MI and add GT-style chemistry lines (alumina T3, polymers T4, rare earths/PGM T5) with MI's KubeJS API
   (MIMachineEvents / MIMaterialEvents). User decisions: pacing ~100-120 h (longer, but from content, not grind);
   ONE balanced path (no packmodes); expand Warbucks Core (Periodic Table perks, reaction conditions, prospecting).
   First step DONE 2026-10-18: aluminium slice (Bayer + Hall-Héroult Cell, T4 quests, Periodic Table perks in Warbucks
   Core 1.1.0; PROGRESSION.md §7). Released (GitHub release warbuckscore-v1.1.0, packwiz points at it) and pushed.
   LIVE server restarted onto it 2026-10-18 21:10 (0 players, user OK; Done, 6,269 recipes, 0 failed). Next: the user
   playtests the line in-game; then
   polymers (design tier T4), rare earths/PGM (T5).
   Note: design tiers (PROGRESSION.md) and quest chapter keys differ by one (design T3 = quest chapter t4).
   Dissolver: no new entries needed (machines are excluded by design; ChemLib Al compounds are native Alchemistry).
5. Review items: AdvancedAE Flight Card and Ars Ritual of Flight aren't chemistry-gated; More Machine UU-Matter is
   ungated; dissolver stone recipes give trace metals (copied from Alchemistry's own stone recipe), so decide whether to keep them.
6. Phase 6 final test pass (client launch, worldgen, JEI sanity, quest completion).

## Current state (update every session)
- Phase 1 design: approved (docs/PROGRESSION.md v2). Space = Ad Astra; extra dimension = Deeper and Darker.
- Phase 2 mod list: IN PROGRESS. 134 mods; smoke + worldgen (r=256) passing; ATM10 left-out list done.
  Phase 2: COMPLETE (client launch, smoke, worldgen, ore scan all pass).
- Phase 3 compatibility: DONE pending user review. Decisions are in PROGRESSION.md §6.
  Files: pack/config/almostunified/, pack/config/Mekanism/world.toml, pack/kubejs/server_scripts/phase3_compat.js,
  pack/kubejs/data/powah/neoforge/biome_modifier/. Phase 4: DONE (phase4_integration.js, phase4_mysticalagriculture.js; PROGRESSION.md §7). User confirmed the recipes in JEI. 163 mods. 
- Monifactory review (2026-10-18): added HNN, Extended Crafting, PackagedAuto(+ExCrafting), Compact Machines,
  Cable Facades, TelePastries (gated in phase4_monifactory.js). Flight gating done (Angel Ring + Iron Jetpacks added). 177 mods.
- Chemistry mechanics (2026-10-18): phase4_chemistry.js + startup_scripts/chemistry_items.js (byproducts,
  Haber/Ostwald, PGM line, energy cores, capstone Seed of a New World, Demigod Token shop).
  ChemLib fluid ids are <name>_fluid (verified at runtime). GTMOGS ore veins rejected (broken KubeJS).
- Aesthetic (2026-10-18): FancyMenu + Drippy layouts in pack/config/fancymenu; art from tools/build_art.py
  (needs Pillow: use a venv). Banners in pack/kubejs/assets/warbucks/textures/quests. Ore deposits from
  tools/build_deposits.py (calibrated with test/ore_scan.py). 181 mods.
- 2026-10-18 later: 197 mods (Towns&Towers, Regions Unexplored, YUNG's, Farmer's Delight, Occultism [gated:
  phase4_occultism.js], MoreMachine, SS in Motion, JourneyMap, Chunky). Quest book v5 = 200 quests, 20 chapters.
  Create re-added (early mechanical tier, phase4_create.js) -> 220 mods; quest book v6 = 213 quests, 21 chapters.
- Quest book v8 (1,172 quests, 38 chapters, 7 category groups set by LAYOUT in tools/quest_data.py): one file per
  chapter in tools/quests/, style in tools/quests/STYLE.md (engine v8: kill/structure/biome/anytag/anyof tasks, hidden/
  secret/any_dep, loot=/choice= reward tables in tools/quests/_tables.py, links, {@pagebreak}). Validate with
  `python3 tools/build_quests.py --check` (or `QUEST_ONLY=a,b ...--check` for a few chapters). End goal = Seed chapter,
  then Creation. Tokens: Demigod Token + Greater (=9); shop in phase4_chemistry.js §5 (convenience only).
  Empty starting inventory: join-gift books are off in pack/config (MI, Ars, Silent Gear, Advanced Peripherals).
  Balance fixes in phase5_balance.js (Mekanism 4x/5x machines at MV circuits; no Reliquary metal duplication).
  Open review items: AdvancedAE Flight Card and Ars Ritual of Flight aren't chemistry-gated (both late or area-limited);
  Mekanism More Machine UU-Matter replicator is ungated (late game); Entangled/Integrated Tunnels/Rechiseled ids are
  missing from test/ids.tsv (their quests use checkmarks). Flying potion = levitation + 2 chemlib:hydrogen (phase4_flight.js).
- Phase 5 quests (history): v4 (162 quests, 17 chapters incl. Welcome + QoL; tokens on every quest, step-by-step per user request) pending user review.
  QUESTS ARE GENERATED: edit tools/quest_data.py (content; helpers in tools/questlib.py), then run `python3 test/build_id_index.py` (after a smoke test) and
  `python3 tools/build_quests.py`. Never hand-edit pack/config/ftbquests/quests (it gets overwritten).
  If the user edits quests in-game, copy those changes back into tools/quests/<chapter>.py first.
  Next: Phase 6 final test pass (launch, worldgen, JEI sanity, quest completion, dedicated server on VPS with user OK).
- KubeJS 7 (2101.7.x) API confirmed via javap: event.findRecipes/remove/custom; recipe.json; recipe.getId().
  Editing pattern: parse JSON, remove the original, re-add under kubejs:phase3/... (see phase3_compat.js).
- Warbucks Core (custom mod, 2026-10-18): source in mod/ (NeoForge 21.1.262 ModDevGradle; build with mod/gradlew build;
  textures from mod/tools/textures.py). Spectrometer, Biome Capsule, Terraformer. Released as GitHub release
  warbuckscore-vX.Y.Z; packwiz entry pack/mods/warbucks-core.pw.toml (`packwiz url add`). To ship a change: bump
  mod_version, build, `gh release create`, then re-add the URL with packwiz. The Terraformer was tested on a
  server; the Spectrometer still needs an in-game test (it needs a player).
- Dissolver coverage: tools/build_dissolver.py -> pack/kubejs/config/dissolver_recipes.json (one table, loaded by
  server_scripts/dissolver_generated.js); 6,041 recipes, uncovered list in docs/dissolver-coverage.md. Rerun after mod changes.
- Formula tooltips: pack/kubejs/client_scripts/formula_tooltips.js (ItemEvents.modifyTooltips).
- Dedicated server kit: server/ (install.sh, start.sh auto-updates from GitHub, warbucks.service), docs/SERVER.md.
  User decision 2026-10-18: Warbucks REPLACES ATM10 as the live server on the VPS (/opt/warbucks); whitelist on,
  auto-update, daily backups (7 kept), Normal difficulty. LIVE since 2026-10-18 19:08: warbucks.service enabled on
  port 25565; atm10.service stopped + disabled (folder untouched, re-enable to switch back).
- Remote test server: the user's VPS (connection details are kept in local Claude memory, NOT in this public repo).
  Live ATM10 runs there; stopping it needs explicit user OK + 0 players. Default: test locally.
- Phase 4 gates: Powah's Energizing Orb (MI electronic circuit). Just Dire Things flight is NOT chemistry-gated, by
  decision: it is late anyway (eclipse alloy chestplate = tier 4 goo from an Ancient City + a netherite block).
- Tooling: Temurin 21 (system), packwiz at ~/go/bin/packwiz, Prism instance "Warbucks-Chemistry-Dev".
  Windows desktop (2026-10-18): Temurin 21 (JAVA_HOME; an old Java 8 shim is also on PATH), Go, packwiz in
  %USERPROFILE%\go\bin, Python 3.12 with repo .venv (Pillow), Prism instance "Warbucks-Chemistry-Prism".
- Market + editor (2026-10-19): 2,468 quests. "shop" group (market, shop_materials, shop_gear, shop_world): 441 repeatable
  token-shop quests, rule "buy more of what you've made yourself" (docs/research/shop_brief.md); shop chapters use
  layout="manual" grids. Quest editor: tools/quest_editor.py (localhost:8765), user edits land in
  tools/quest_overrides.json (applied after the auto layout; never change keys/deps/tasks).
- Neo Vitae + Allthemodium added 2026-10-19 (224 mods). Allthemodium: Mining dimension KEPT WITH its dense ores (user
  decision); metals T3-T6. Open: alloy tools have no recipe (hide in JEI or add smithing), argon cost may need tuning,
  test/emc_check.sh not ported to Windows (EMC for the new metals relies on the broad c: tags in custom_emc.json).
  Neo Vitae open choices: Magnetism quarry, Torment Nexus, lava+cobble sulfur, meteors removed entirely.
- Quest book v11 (2026-10-19): 2,000 quests (848 required, 320 on the main path). ATM10-aligned coverage (138 ATM10 items
  left, all skipped on purpose), story arc reviewed end to end, the MI nuclear/quantum chain before the Seed is now
  required on the main path (adds endgame hours; watch pacing vs the 100-120 h target). LIVE WORLD WIPED 2026-10-19 00:22
  (backup on the VPS: /opt/warbucks/backups/world-prewipe-20261019-002252.tar.gz). Quest preview for review:
  `python test/build_quest_preview.py`, then serve test/preview (the session's quest-preview launch config).
- Quest book v10 (2026-10-19): 1,622 quests (801 required), 44 chapters. AUTOMATIC LAYOUT (tools/layout.py): writers no
  longer place x/y (Chapter(layout="manual") opts out; Q(row=N) pins). `build_quests.py --layout-report` for metrics.
  Groups: top (welcome, market, lab_notes, completionist), main, basics, chem, eng, magic, world, life; new chapters
  harvest and mekanism_power; utilitarian merged into qol. Audits in docs/research/ (chem_tier_audit, quest_layout_audit,
  tools_harvest_plan, build_round_brief). Chemistry gate fixes in phase5_chem_gates.js; ore tiers in
  phase5_harvest_tiers.js. Not yet done: in-game visual check of the auto layout (tall hub chapters: qol, twilight,
  mekanism, seed; FTB hide_dependent_lines for hubs is the next engine step). Still open user decisions: real rocket fuel,
  sulfuric acid in the MV board, token shop prices, stone trace metals, Occultism crystallizer multipliers.
- Quest book v9 (2026-10-18): 1,617 quests, 43 chapters. Getting Started is a full first day; new pages powah,
  justdirethings, undergarden, deeperdarker, utilitarian; create/mekanism/twilight/ae2/storage/ars/occultism expanded.
  Use tools/quest_compare.py (ATM10 book at C:\Users\Grandpawarbucks\curseforge\minecraft\Instances\All the Mods 10 - ATM10
  \config\ftbquests\quests, requirements only, ARR: never copy text). Parallel writers work well: one chapter file each,
  QUEST_ONLY=<keys> --check; the integrator rebuilds ids.tsv, runs the real build, smoke tests and commits.
  NEXT ROUND: densify the MI tier chapters t0-t7 (MI gaps: ~112 items) one at a time (cross-chapter deps).
  Gate gaps the writers found, FIXED 2026-10-18 (user decision): Powah's energizing uraninite_from_uranium removed
  (phase4_integration.js); Occultism crusher spirits capped at 2x via pack/config/occultism-server.toml (outputMultiplier
  1.0 for all tiers; speed bonus kept); Ars Ritual of Flight tablet needs 2 chemlib:hydrogen (phase4_flight.js); STYLE.md
  blocked lists corrected. Left as is by decision: Occultism miners for non-milestone ores (aluminium/bauxite, titanium,
  thorium, monazite give ore only) and JDT flight (late, not chemistry-gated). Still open: Occultism CRYSTALLIZER spirits
  multiply output 1.5x/2x/3x (not yet reviewed); no Ars recipe uses a chemical intermediate besides the flight tablet.
- QoL (user request 2026-10-18): Utilitarian mod (222 mods, above the ~210-215 target by user choice); longer days + less rain
  (server_scripts/qol_world.js); 4x vanilla cooking (qol_furnace_speed.js). Day and rain length still need an in-game check.
- Python tools on Windows: pass encoding="utf-8" (and newline="\n" when writing). build_quests, build_id_index and
  gen_modlist are fixed; build_dissolver/build_deposits/build_prism_instance are not yet (run them with PYTHONUTF8=1).
- Line endings: .gitattributes `* -text` (no conversion). packwiz hashes files on disk, so CRLF checkouts on Windows
  would break the pushed index. If packwiz refresh changes hashes of files you didn't edit, check line endings first.
- MODLIST.md is GENERATED: add a row to docs/modlist-meta.tsv for every new mod, then run
  `python3 test/gen_modlist.py` (it fails if a mod has no row).
- KubeJS rejects any file under pack/kubejs/data or assets with UPPERCASE in its name (server won't start).
- Compact Machines room templates are shipped in pack/kubejs/data/compactmachines (built-in pack is off by default).
- Modrinth API rate-limits (HTTP 429): use test/mrcheck.py, which retries.
- Some mods don't declare all their dependencies in metadata (Ars Nouveau→GeckoLib, OctoLib→Architectury).
  The smoke test catches these.

## Project layout
- `pack/`: packwiz pack (source of truth for the mod list)
- `pack/kubejs/`, `pack/config/` (incl. `pack/config/ftbquests/`): pack overrides. They must live
  inside `pack/` so packwiz indexes and ships them.
- `test/`: headless server, smoke test and worldgen scripts. Only the scripts
  are committed.
- `docs/`: README.md, MODLIST.md, PROGRESSION.md, CHANGELOG.md

## Workflow
- Phases: 1 Design pitch → 2 Mod list → 3 Compatibility pass → 4 KubeJS
  integration → 5 FTB Quests → 6 Final test pass.
- Run the smoke test after every change to the mod list, configs or KubeJS
  scripts. Don't move to the next phase until it passes. After 3 failed fix
  attempts, stop and show the user what you found.
- After each phase: run the smoke test, update docs/CHANGELOG.md, commit to Git,
  summarize, and wait for the user's go-ahead.
- GitHub (PUBLIC): https://github.com/Grandpawarbucks/Warbucks-Chemistry-Pack (branch main).
  After a passing smoke test, commit AND `git push` so Prism instances auto-update. Never commit
  secrets or server connection details (repo is public). The user also develops from a Windows
  desktop: always `git pull` before starting work (see docs/DESKTOP_SETUP.md).
- Player/desktop instance: launcher/Warbucks-Chemistry-Prism.zip (rebuild with
  `python3 tools/build_prism_instance.py` if MC/NeoForge version or pack URL changes).

## Rules
- Verify every mod exists for NeoForge 1.21.1 before adding it by checking its
  page or files list, not memory. Flag anything you couldn't verify.
- Don't invent mods, recipes, item IDs, or config options. If you're unsure,
  check.
- Prefer actively maintained mods. Note when a mod's last update is old.
- Aim for ~210–215 mods (raised from 100–200 on 2026-10-18 for Create) and justify anything heavy.
- Keep docs/MODLIST.md and docs/CHANGELOG.md current with every change.
- Ask up to 3 clarifying questions when something is ambiguous.
- Before ending any session, update CLAUDE.md and /docs so the next session
  can pick up cleanly.
