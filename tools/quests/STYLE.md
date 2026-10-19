# Quest writing guide (Warbucks Chemistry: The Demigod's Codex)

Each chapter is one file in `tools/quests/<key>.py` defining `CHAPTER = Chapter(...)`.
Validate with `python3 tools/build_quests.py --check` (writes nothing). The real build is run by the maintainer.

## Hard rules
1. **Never change or remove an existing quest key** (`Q("t1_steel", ...)`). Quest IDs are derived from keys, so changing one wipes player progress. Rewording titles and descriptions is fine.
2. **Only use ids that exist.** Look them up: `grep -P '^modid:item_name\t' test/ids.tsv`. Item tasks use `item("id", count)`, dimensions use `dim("id")`, tips and story use `tick()`. `--check` fails on unknown ids.
3. **Don't invent mechanics or recipes.** If unsure how something is made, read the recipe JSON in the mod jar (`unzip -p test/server/mods/<jar> data/<ns>/recipe/<path>.json`) or say "check JEI". Chemistry facts must be real and correct.
4. Only edit your assigned chapter files. Don't run the full build, don't commit, don't touch `pack/`.
5. Multiblocks: point players to where the 3D layout is shown: **JEI** (press R/U), the **MI guidebook**, or **Just Enough Mekanism Multiblocks** in JEI. No hand-drawn diagrams.

## Every quest gets
- `subtitle="..."`: one short line (≤ 60 characters) shown under the title.
- A structured `desc` of 3–7 lines, using only the sections that apply, in this order:
  - `"&6...&r"`: story line (milestones and chapter start/end only; see Story)
  - `"&eWhat:&r ..."`: what the thing is and why the player wants it
  - `"&eChemistry:&r ..."`: the real science (reaction, formula, why it works). Skip it for pure tools and QoL.
  - `"&eHow:&r ..."`: concrete steps (machine, inputs, where to find things, JEI pointers)
  - `"&eTip:&r ..."`: one practical tip (automation, common mistake, efficiency)
  Keep lines readable: 1–2 sentences each. Plain words. Use real formulas (H₂SO₄, NaCl, C₂H₄) where they help.

## Smaller steps
Split big leaps into one quest per new machine or intermediate (e.g. sulfur → SO₂ → SO₃ → H₂SO₄, each its own quest with its own machine). New quest keys use the chapter prefix (e.g. `t3_so2`). Wire `deps` so the line reads left to right. Keep existing quests as the milestones.

## Optional side quests
Bonus content off the main line: collections, challenges, fun facts, alternative routes. Mark them `optional=True` and give `tokens=1` (or 2 for hard ones). The layout places them off the main line automatically. Main-line quests never depend on optional ones.

## Story and lore
The player is a demigod who woke without their power and regains it by mastering chemistry. Each chapter should have:
- a gold `&6` line at its first quest (a memory returning, written as the demigod remembering);
- a gold `&6` payoff line at its milestone(s).
Tone: wonder and quiet confidence, a little wry; never purple prose. 1–2 lines, not paragraphs. No new characters or lore beyond "the demigod remembering what they once were".

## Layout
**Layout is automatic. Don't spend time on `x`/`y`.** `tools/layout.py` places every quest at build time from its
`deps` (the `x, y` you write in `Q(...)` are ignored; new quests can use `0, 0`). What it does:
- **Columns follow dependencies:** a quest sits one column (2 cells) right of its deepest dep in the same chapter, so
  every line points right. Deps on quests in other chapters don't count. So get `deps` right: they ARE the layout.
- **The spine is on y = 0:** the longest chain of required quests runs along the middle. Other required chains
  become rows above and below it (2 cells apart); optional quests sit 1.5 cells off their parent's row.
- Crossings are reduced automatically; groups of quests with no line to the spine are packed below it.
- **Links** (`links=[("t3_ebf", 0, 0)]`) go in a link column at x = -2 beside the rows that use them; the x/y in the
  tuple are ignored. The chapter's entry quest automatically gets a link to its deps in other chapters.
- The chapter banner goes above the topmost quest or link.
- `python3 tools/build_quests.py --layout-report` prints crossings, lines through quests, edges longer than 6 cells
  and overlaps per chapter (hand x/y vs automatic). Good chapters have few crossings and no overlaps.

Shaping the result, if a chapter reads badly:
- `Q(..., row=N)` pins a quest to y = 2N (e.g. `row=-1` puts it on the row above the spine).
- Fewer long lines: depend on the nearest quest that really unlocks this one, not on a far-away hub.
- A whole chapter can opt out with `Chapter(..., layout="manual")`: then its hand-written `x`/`y` (and link
  positions) are used as they are. Use this only for special pages (a picture, a map).

**Milestones have exactly two styles** (normalised at build time, so other sizes are converted):
- **Chapter capstone:** `size=2.0, shape="gear"` (any size of 1.75 or more becomes this).
- **Section milestone:** `size=1.5, shape="hexagon"` (sizes 1.25 to 1.5 become this).
- Everything else is size 1 in the chapter's default shape. Milestones (size >= 1.5) pay double tokens.

**Where chapters go** (`GROUPS`/`LAYOUT` in `tools/quest_data.py`; the group is set there by chapter key):
- **Top area, no group:** welcome, market, lab_notes, completionist. These are listed above the first tab (FTB
  Quests' ungrouped area, like ATM10's Welcome pages).
- Then the tabs: The Demigod's Path (start, t0 to t7, seed, creation), **Basics** (the beginner "comfort" pages:
  tools, harvest, storage, power, powah, farming, qol, building), Chemistry Lab, Industry and Automation,
  Magic and Relics, Exploration, Resources.
- A new chapter file must be added to `LAYOUT`, or it isn't built (`--check` warns about unlisted files).

## Pack facts to respect (gates set in KubeJS; see docs/PROGRESSION.md §6–7)
- Tech spine = Modern Industrialization tiers: LV analog circuit, MV electronic circuit (aluminum), HV digital circuit (polyethylene), EV processing unit (PVC), IV quantum.
- Ore processing caps at 2x per ore block before acids. Mekanism gives 3x (O₂), 4x (HCl), 5x (H₂SO₄). Byproducts come from Mekanism dirty dust in the MI Centrifuge.
- Ore deposits: scattered MI ore is reduced; rich deposits sit at metal-specific depths.
- Flight: Infusion Pylon + Potion of Flying needs hydrogen from the Alchemistry Dissolver. Iron Jetpack coils need MI LV/MV/HV/EV circuits. The Angel Ring needs an HV digital circuit.
- Gated by MI circuits: Mekanism control circuits, AE2 Inscriber (Turbo hull) and Controller (digital circuit), Powah Energizing Orb (MV), Flux Core (EV), Ad Astra NASA Workbench (EV hull), Extended Crafting tables (MV/HV/EV), HNN Simulation Chamber and Loot Fabricator (MV), Create Alternator and New Age Generator Coil (LV), New Age reactor rods (EV), Mystical Agriculture tier 3/4/5 seeds (LV/MV/HV).
- Blocked: Mystical Agriculture seeds for uranium, uraninite, osmium, fluorite, silicon, steel, aluminum, graphite, platinum, iridium, refined obsidian and refined glowstone (phase4_mysticalagriculture.js). Occultism miners for uranium, uraninite, osmium, fluorite, platinum, iridium and tungsten (phase4_occultism.js). Occultism miners still give other ores (aluminium/bauxite, titanium and more): that's ore, which still needs the chemistry lines.
- Occultism crusher spirits all give 2 dust per ore (pack/config/occultism-server.toml); higher tiers are only faster.
- Custom chemistry (MI machines): Haber-Bosch (N₂ + 3H₂ → 2NH₃), Ostwald (NH₃ → HNO₃), NH₃ + HCl → NH₄Cl, the PGM line (anode sludge from nickel/copper electrolysis → aqua regia → chloroplatinic acid + residue → ammonium hexachloroplatinate → calcine to platinum; residue centrifuged into Ir/Os/Rh/Ru), uraninite = uranium dust + O₂ (Chemical Reactor), energy cores, Seed of a New World (9x9 Ultimate Table).
- Demigod Tokens are quest rewards; shop recipes are in JEI (search "Demigod Token").

## New task types and quest options (engine v8)
Import what you need: `from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anytag, anyof`.
- `kill("minecraft:zombie", 25)`: kill 25 of that mob. Entity ids are in `test/ids.tsv` (type `entity`).
- `structure("minecraft:ancient_city")`: stand inside a structure. `biome("minecraft:cherry_grove")`: visit a biome.
  Find ids with `grep -P '\tstructure\t' test/ids.tsv` / `grep -P '\tbiome\t' test/ids.tsv`. Only use structures that actually generate in this pack.
- `anytag("minecraft:logs", 16)`: any 16 items from an item tag. `anyof(["a:x", "b:y"], 4)`: any of several items.
  Use these instead of forcing one exact variant (e.g. any wool, any sapling, any Mekanism tier).
- Quest options on `Q(...)`:
  - `hidden=True`: not shown until its dependencies are visible (spoiler-free next steps).
  - `secret=True`: invisible until completed. Secret quests are fun discoveries (a rare biome, a strange mob, a joke).
    Give them a dependency so they can't be done before the chapter opens; reward `loot="secret"`.
  - `any_dep=True`: unlocks when ANY ONE dependency is done (use for alternative routes, e.g. "any generator").
  - `loot="t3"`: one random roll from a reward table. `choice="pick_mid"`: the player picks one item.
    Tables are in `tools/quests/_tables.py`: t0..t7, hunt, boss (2 rolls), pick_early, pick_mid, pick_late, secret.
    Tier milestones in t0..t7 get their tier's loot automatically; don't add it there.
- Deep-dive pages: put the string `"{@pagebreak}"` as its own line in `desc` to start a new page in the quest
  window. Use it for long explanations (page 1 = the normal short quest, page 2+ = the deep dive).
- Quest links: `Chapter(..., links=[("t3_ebf", x, y)])` shows a quest from another chapter as a clickable shortcut.
  Use links to connect a mod page to where that mod enters the main path.

## Mod pages
Side chapters are "pages", one per mod or mod family, grouped by category (see LAYOUT in `tools/quest_data.py`).
The group is set there by key; the group argument in `Chapter(...)` is ignored, so just pass `SIDE`.
A page's first quest should depend on the main-path quest where the mod becomes available, and the page should carry a
`links=[...]` entry back to that quest.
