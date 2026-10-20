# Quest writing guide (Warbucks Chemistry: The Demigod's Codex)

Each chapter is one file in `tools/quests/<key>.py` defining `CHAPTER = Chapter(...)`.
Validate with `python3 tools/build_quests.py --check` (writes nothing). The real build is run by the maintainer.

## Hard rules
1. **Never change or remove an existing quest key** (`Q("t1_steel", ...)`). Quest IDs are derived from keys, so changing one wipes player progress. Rewording titles and descriptions is fine.
2. **Only use ids that exist.** Look them up: `grep -P '^modid:item_name\t' test/ids.tsv`. Item tasks use `item("id", count)`, dimensions use `dim("id")`, tips and story use `tick()`. `--check` fails on unknown ids.
3. **Don't invent mechanics or recipes.** If unsure how something is made, read the recipe JSON in the mod jar (`unzip -p test/server/mods/<jar> data/<ns>/recipe/<path>.json`) or say "check JEI". Chemistry facts must be real and correct.
4. Only edit your assigned chapter files. Don't run the full build, don't commit, don't touch `pack/`.
   The full workflow (checks, layout, audit, build) is the `quest-book` skill: `.claude/skills/quest-book/SKILL.md`.
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
`deps` (the `x, y` you write in `Q(...)` are ignored; new quests can use `0, 0`). Get `deps` right: they ARE the
layout. Order of the build: `normalize_milestones`, then `tools/quest_style.py` (shapes and sizes by role), then the
layout (it spaces quests by size), then the quest editor's overrides.

**Sections.** Every auto-layout chapter is split into visual sections: small trees of about 4 to 14 quests, each under
a labelled header image (`pack/kubejs/assets/warbucks/textures/quests/sections/<chapter>_<slug>.png`, made by the
build; stale ones are deleted). Sections are found automatically: the branches hanging off the chapter's spine (the
longest chain of required quests), split along their own subtrees when too big (a hub keeps its small leaves) and
merged with their neighbours when too small. A prerequisite that only feeds one section joins it. Auto titles come
from the section's root quest (a loose group of unrelated quests is named "From <chapter>" after where it starts).
- `Q(..., section="Title")` puts a quest in a named section. Its descendants (through each quest's deepest
  dependency here) without a section of their own follow it. Use it when an auto title or grouping reads badly.
- A chapter with one section gets no header (the chapter banner is enough).
- Mod pages are split into chapters by these same sections (see "Mod = category" below), so on a mod page a section
  becomes a sidebar chapter, not a header. Headers are only drawn on the Demigod's Path and the top-area pages.

**Shape motifs** (`STYLES` in `tools/quest_data.py`, by chapter key; default `"tree"`). Every page is a shape, not a
long row. All of them keep progression readable: only straight lines, no line through a quest, no overlaps, and
FTB's real geometry (a quest of size s is about s cells wide). A motif that doesn't fit a section falls back to a
plain tree for that section. Pick them by looking at `testuild_quest_preview.py --gallery`; try one without editing
the file: `$env:LAYOUT_STYLE="t6=radial,t4=winding+molecule"` before a build (`QUEST_OUT=<folder>` keeps it out of pack/).
- `"winding"` (start, t0 to t7, seed, creation, occultism): the main path snakes like an S. Rows of 4 to 7 spine
  quests alternate direction (left to right, then right to left) and are joined by a vertical step at each bend; when
  two rows are far apart, up to 2 spine quests sit on the bend as a rounded corner. Sections hang off their spine quest
  as small trees: below a row (pointing down, header beside the root, or sideways with the row's flow) or above it
  (pointing up, header on top), in the lane between two rows; a section hanging from a bend quest sits outside the
  bend. The row length and pitch are chosen per page so it comes out compact (close to square).
- `"radial"` (qol, building, storage, harvest, undergarden, deeperdarker): hub pages. The hub (the quest most of the
  page hangs from) sits in the middle with its own section as a radial tree around it: its children share the circle
  (a crowded first ring alternates two radii), deeper quests fan out one ring further. The other sections are spokes
  in compass slots (sideways first, then down, up and the diagonals), each a short tree pointing outward with its
  header at the far end; the core leaves a gap in the ring where each spoke's line goes out. Sections hanging from a
  spoke sit beyond it. Small leaf branches of a hub stay in the hub's own section here, so they ring the hub.
- `"molecule"` (periodic, mekanism, mekanism_power, power, factory): a section whose quests form a tree is drawn as
  rings of 5 or 6 quests (benzene-like hexagons) joined by bonds, with short side chains pointing outward. Ring order
  follows the dependency order (depth first, biggest branch first, so a chain closes into a hexagon); the ring's
  closing side is not a dependency, so FTB draws no line there. `BLOCKS` in quest_data.py asks for molecule sections
  on another motif's page (t4 uses it on its winding page).
- `"tree"` (other mod pages): sections are top-down trees (root on top, children fanning below), laid out in columns
  or rows in reading order, whichever fits the 26 x 18 target page better.
- `"grid"` (hunting, completionist, lab_notes, explore): like tree, with tighter, wider rows for collections.
- `"spine"`: the v11 main-path style (one straight row with sections above and below), kept for comparison.
- The shop chapters stay `Chapter(..., layout="manual")`: hand-written `x`/`y` and link positions are used as they are.
- No "periodic" element grid: the periodic chapter is family by family (alkali metals, halogens, ...), not one quest
  per element, so a period/group grid wouldn't fit it.

**Hidden lines.** The layout sets FTB's `hide_dependency_lines` on a quest (and `hide_dependent_lines` on a
dependency) where a line is clutter: a hub with 6 or more dependents here (4 on grid pages; never on radial pages,
whose spokes are short), a line that runs through a quest or header, a long line between two sections, or (every
page but `"spine"`) a line that crosses two or more others. It only hides a line when the dependency stays readable
without it: same section, a neighbouring section (within 2 in reading order, or touching), the spine, or shown as a
quest link; on motif, tree and grid pages any line between two sections counts as readable, since sections sit by
shape rather than in reading order. Spine steps on spine and winding pages are never hidden, and a radial page's hub
keeps its own lines. FTB still draws hidden lines on mouse-over.

**Links.** `links=[("t3_ebf", 0, 0)]` (x/y ignored) sit above or beside the quests that depend on them, inside their
section; links nothing here depends on go in rows above the page. The chapter's entry quest automatically gets links
to its deps in other chapters. When all of a quest's dependents here are in one far section, the layout adds a link
to that quest inside that section: FTB draws a dependency line from the LAST button of a quest on the page (links
come after quests), so the lines then start at the link. That quest's own dependency lines are hidden (FTB would
draw them at the link too).

- Redundant lines are dropped on output: if A -> B -> C and C also lists A, the A -> C line isn't drawn (what the
  player must do doesn't change).
- The chapter banner goes at the top left, above the topmost quest, link or section header.
- `python tools/build_quests.py --layout-report` prints, per chapter, the v10 layout vs now: size (with headers),
  sections, crossings, lines through quests, edges longer than 6 cells, hidden lines, overlaps, line directions and
  the median line length. `tools/layout_lint.py` (on the built book) compares with ATM10.

Shaping the result, if a chapter reads badly:
- Fewer long lines: depend on the nearest quest that really unlocks this one, not on a far-away hub.
- `section="..."` to regroup; `Q(..., row=N)` still pins a quest's row inside its section's tree.
- `Q(..., icon="mod:item")` sets the quest's icon (handy for checkmark tips).

**Milestones have exactly two styles** (normalised at build time, so other sizes are converted):
- **Chapter capstone:** `size=2.0, shape="gear"` (any size of 1.75 or more becomes this).
- **Section milestone:** `size=1.5, shape="hexagon"` (sizes 1.25 to 1.5 become this).
- Everything else is size 1 in the chapter's default shape. Milestones (size >= 1.5) pay double tokens.

**Where chapters go** (`GROUPS`/`LAYOUT` in `tools/quest_data.py`; the group is set there by chapter key):
- **Top area, no group:** welcome, lab_notes, completionist. These are listed above the first category (FTB
  Quests' ungrouped area, like ATM10's Welcome pages).
- Then The Demigod's Path (start, t0 to t7, seed, creation: one chapter per tier, sections with headers) and The
  Demigod's Market (market, shop_*: manual grids, linear progression). Neither is split.
- **Mod = category** (user decision 2026-10-19). Every other chapter file (a "page") becomes its own category (an
  FTB chapter group titled after the page) and its layout sections become the chapters inside it, so the sidebar
  reads "Mekanism > Factories and Upgrades, Alloys and Teleporters, ...". FTB has one level of groups only.
  - The split runs at load time in `tools/quest_data.py` (`_split`): the page's sections (`layout.page_sections`, as
    trees; grid pages as grids) are merged so each chapter has about 5 to 25 quests (a section under `SPLIT_MIN`
    joins the neighbour it shares the most deps with), then ordered by progression (a chapter after the chapters it
    needs; the page's first quest opens the first chapter).
  - Chapter keys: the FIRST chapter keeps the page's key (links and docs still resolve); the others are
    `<page>_<slug of the title>`. Quest keys never change; only which chapter shows a quest.
  - Titles, one-line subtitles and optional icons: `CHAPTER_TITLES` in quest_data.py, keyed by the chapter's root
    quest (the quest the layout would name the section after). Unlisted chapters keep the auto title, so check new
    or regrouped ones in `docs/QUESTS.md` (its "Sidebar" list) and add a title. Never use "From <chapter>".
    Icons default to the root quest's item (another member's if a sibling chapter already shows it).
  - `JOIN` puts a page's chapters into another page's category (mekanism_power joins Mekanism); `PAGE_TITLES`
    renames a category. Category order follows the old tabs: Basics pages, Chemistry Lab, Industry and Automation,
    Magic and Relics, Exploration, Resources (`SPLIT_TABS` and `LAYOUT`).
  - A page that comes out as a single chapter stays in its old tab's group ("Basics", "Exploration", ...).
  - Tokens: a split chapter pays its page's `TOKENS` rate. Each chapter gets its own banner (`<key>.png`, the
    page's element tile with the chapter title), written by the build; stale split-chapter banners are deleted.
  - Links: the page's writer links go to the chapters whose quests depend on them (loose ones stay in the first
    chapter), and every quest a chapter needs from another chapter of its category is shown there as a quest link.
  - Layout: split chapters have no section headers. Their style is the page's motif (molecule, grid), except that
    only the hub chapter of a radial page stays radial and winding pages become trees. On these small chapters a
    hub's fan lines stay drawn unless a fan line crosses another line.
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
Side chapters are "pages", one file per mod or mod family (see LAYOUT in `tools/quest_data.py`); each page becomes a
category of small chapters in the book ("Mod = category", above). The group is set in quest_data.py; the group
argument in `Chapter(...)` is ignored, so just pass `SIDE`. Write deps as usual: they decide how the page splits.
A page's first quest should depend on the main-path quest where the mod becomes available, and the page should carry a
`links=[...]` entry back to that quest.
