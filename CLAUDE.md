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
  every tier should feel worth it, not padded. NO ProjectE.
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
  Create re-added (early mechanical tier, phase4_create.js) -> 204 mods; quest book v6 = 213 quests, 21 chapters.
- Quest book v7 (587 quests, 118 optional): one file per chapter in tools/quests/, style in tools/quests/STYLE.md;
  validate with `python3 tools/build_quests.py --check`. Flying potion = levitation + 2 chemlib:hydrogen (phase4_flight.js).
- Phase 5 quests (history): v4 (162 quests, 17 chapters incl. Welcome + QoL; tokens on every quest, step-by-step per user request) pending user review.
  QUESTS ARE GENERATED: edit tools/quest_data.py (content; helpers in tools/questlib.py), then run `python3 test/build_id_index.py` (after a smoke test) and
  `python3 tools/build_quests.py`. Never hand-edit pack/config/ftbquests/quests (it gets overwritten).
  If the user edits quests in-game, copy those changes back into tools/quests/<chapter>.py first.
  Next: Phase 6 final test pass (launch, worldgen, JEI sanity, quest completion, dedicated server on VPS with user OK).
- KubeJS 7 (2101.7.x) API confirmed via javap: event.findRecipes/remove/custom; recipe.json; recipe.getId().
  Editing pattern: parse JSON, remove the original, re-add under kubejs:phase3/... (see phase3_compat.js).
- Remote test server: the user's VPS (connection details are kept in local Claude memory, NOT in this public repo).
  Live ATM10 runs there; stopping it needs explicit user OK + 0 players. Default: test locally.
- Gate in Phase 4: Just Dire Things flight items and Powah parts (chemical intermediates).
- Tooling: Temurin 21 (system), packwiz at ~/go/bin/packwiz, Prism instance "Warbucks-Chemistry-Dev".
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
