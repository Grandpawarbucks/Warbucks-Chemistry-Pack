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
- A chapter with one section gets no header (the chapter banner is enough). Every other auto-layout page, main path
  and mod pages alike, shows its sections as headers (one chapter per mod; see "Where chapters go").

**Shape motifs** (`STYLES` in `tools/quest_data.py`, by chapter key; default `"comb"`). Every page keeps progression
readable: only straight lines, no line through a quest, no overlaps, and FTB's real geometry (a quest of size s is
about s cells wide). Pick a motif by looking at `test/build_quest_preview.py --gallery` (and ATM10's "The Beginning"
on the `test/build_quest_map.py --compare` page); try one without editing the file:
`$env:LAYOUT_STYLE="t6=winding,qol=radial"` before a build (`QUEST_OUT=<folder>` keeps it out of pack/).
- `"comb"` (v13, 2026-10-19; every auto page but building): the grammar of ATM10's hand-made main questline, as an
  algorithm (never its coordinates).
  - **One straight spine** on y = 0: the longest chain of required quests, left to right, on the 2-cell grid. The
    chapter's way in (a link to the quest it follows on from) leads the row. A spine of more than 16 quests (18 when
    one row reads better) wraps into 2 or 3 stacked rows that run back and forth, joined by one straight vertical step
    at the end of each row; the cut is chosen so the rows come out about as long as each other.
  - **Teeth.** Everything else hangs off its spine quest (through each quest's deepest dependency here) as a tooth:
    a small tree that grows straight down or up. Each quest goes on the free grid spot next to the quest it hangs from
    where its lines are horizontal or vertical (45 degrees only when nothing straight is free), so a chain runs
    straight down and side branches leave it at right angles; a tooth deeper than 8 cells turns sideways instead.
    A spine quest's branches are split over its two sides, and each tooth goes up or down so the page stays
    balanced. Spine quests spread apart only as far as their teeth need (teeth interlock without touching), and a
    quest with lines into other teeth leans towards them.
  - **Nothing floats.** A quest whose deps are all in other chapters gets a quest link to its first dep, one cell
    away. Links (yours and these) sit next to the quest they feed. A small group with no line to the spine joins the
    tooth of the quest it feeds (else it sits by the chapter's way in). A quest or link that needs two quests far
    apart moves to the free spot where both lines are shortest and straightest.
  - **Section headers** label the spine from outside: just past the teeth of their section, on the side most of
    its quests hang, clear of every quest and line. A section of only one or two quests gets no header unless the
    writer named it (`section=`).
  - **Hidden lines** on comb pages are settled by a small search over the flags (FTB can only hide ALL of a quest's
    lines, or all lines from a dependency): a line through a quest or a header is never drawn; after that it avoids,
    in order, a quest with no line at all, lines over 10 cells, crossings, lines over 6 cells and slanted lines.
- `"radial"` (building): hub pages. The hub (the quest most of the page hangs from) sits in the middle with its own
  section as a radial tree around it; the other sections are spokes in compass slots, each a short tree pointing
  outward with its header at the far end. Kept where a page is a set of independent hubs (the comb tangles there).
- Older motifs, kept for comparison and `LAYOUT_STYLE`: `"winding"` (the spine snakes in rows of 4 to 7 with
  sections hanging above and below each row), `"molecule"` (sections as rings of 5 or 6 quests joined by bonds;
  `BLOCKS` in quest_data.py can ask for them on a winding/radial page), `"tree"` (sections as top-down trees in
  columns or rows), `"grid"` (tighter rows for collections) and `"spine"` (v11: one straight row, sections above and
  below).
- The shop chapters (and welcome, tips) stay `Chapter(..., layout="manual")`: hand-written `x`/`y` and link positions
  are used as they are. A page the comb can't draw cleanly can be hand-placed the same way (use the comb grammar).
- No "periodic" element grid: the periodic chapter is family by family (alkali metals, halogens, ...), not one quest
  per element, so a period/group grid wouldn't fit it.

**Hidden lines (other motifs).** The layout sets FTB's `hide_dependency_lines` on a quest (and `hide_dependent_lines`
on a dependency) where a line is clutter: a hub with 6 or more dependents here (4 on grid pages; never on radial
pages, whose spokes are short), a line that runs through a quest or header, a long line between two sections, or
(every page but `"spine"`) a line that crosses two or more others. It only hides a line when the dependency stays
readable without it: same section, a neighbouring section (within 2 in reading order, or touching), the spine, or
shown as a quest link; on motif, tree and grid pages any line between two sections counts as readable, since sections
sit by shape rather than in reading order. Spine steps are never hidden, and a radial page's hub keeps its own lines.
FTB still draws hidden lines on mouse-over. Quests shown as a link on another page never get these flags (FTB applies
a quest's flags to every button of it).

**Links.** `links=[("t3_ebf", 0, 0)]` (x/y ignored) sit beside the quests that depend on them (comb: one cell from the
first one; other motifs: inside their section; links nothing here depends on go next to the quest they follow on
from, or in rows above the page). The chapter's entry quest automatically gets links to its deps in other chapters.
On non-comb pages, when all of a quest's dependents here are in one far section, the layout adds a link to that quest
inside that section: FTB draws a dependency line from the LAST button of a quest on the page (links come after
quests), so the lines then start at the link. That quest's own dependency lines are hidden (FTB would draw them at
the link too).

- Redundant lines are dropped on output: if A -> B -> C and C also lists A, the A -> C line isn't drawn (what the
  player must do doesn't change).
- The chapter banner goes at the top left, above the topmost quest, link or section header.
- `python tools/build_quests.py --layout-report` prints, per chapter, the v10 layout vs now: size (with headers),
  sections, crossings, lines through quests, edges longer than 6 cells, hidden lines, overlaps, line directions,
  the **orthogonal %** (drawn lines that are horizontal or vertical) and the median line length.
  `tools/layout_lint.py` (on the built book) has the same orthogonal % per chapter (`orth%`) and in the medians, plus
  `lone` (quests with no visible line); `--compare` puts ATM10 beside it. Targets for a comb page: orthogonal 85% or
  more, no lone quests, no crossings.

Shaping the result, if a chapter reads badly:
- Fewer long lines: depend on the nearest quest that really unlocks this one, not on a far-away hub.
- `section="..."` to regroup; `Q(..., row=N)` still pins a quest's row inside its section's tree.
- `Q(..., icon="mod:item")` sets the quest's icon (handy for checkmark tips).

**Milestones have exactly two styles** (normalised at build time, so other sizes are converted):
- **Chapter capstone:** `size=2.0, shape="gear"` (any size of 1.75 or more becomes this).
- **Section milestone:** `size=1.5, shape="hexagon"` (sizes 1.25 to 1.5 become this).
- Everything else is size 1 in the chapter's default shape. Milestones (size >= 1.5) pay double tokens.

**Where chapters go** (`GROUPS`/`LAYOUT` in `tools/quest_data.py`; the group is set there by chapter key). The
sidebar follows All the Mods 10's book (user decision 2026-10-19; its structure only, never its text): **one chapter
per mod**, grouped by category. A mod's sections are section headers on its page.
- **Top area, no group** (FTB's ungrouped area, like ATM10's Welcome/Market/Bounty Board/Tips pages), in order:
  welcome, market (the token shop's entry), tips ("Tips and Tricks"), building ("Building Tips"), hunting
  ("Bounty Board"), lab_notes, completionist.
- **The Demigod's Path (Main Questline):** start, t0 to t7, seed, creation (our story replaces ATM10's main questline).
- **The Demigod's Market:** shop_materials, shop_gear, shop_world (manual grids).
- **Tools and Gear:** tools, harvest, apotheosis, relics, qol. **Storage:** storage, ae2. **Logistics:** logic.
- **Resources:** farming, mystical, factory (mob data and big crafting; ATM10 files Hostile Neural Networks here).
- **Tech:** create, mekanism, mekanism_power ("Mekanism: Power", like ATM10's Mekanism Reactors), justdirethings.
- **Chemistry:** periodic (the pack's own group, where ATM10 has Modern Industrialization).
- **Energy:** power, powah. **Magic:** ars, occultism, neovitae, projecte.
- **Exploration:** worlds, explore, undergarden, twilight, deeperdarker, allthemodium, space.
- `TITLES` in quest_data.py renames a chapter in the sidebar (and on its banner) without touching its file.
- A new chapter file must be added to `LAYOUT`, or it isn't built (`--check` warns about unlisted files). A key in
  `LAYOUT` whose file doesn't exist yet is skipped quietly.
- Progression is `flexible`; the shop pages (market and the Market group) are `linear`. Tokens per quest come from
  `TOKENS` by chapter key (default 1).
- Banners: the build writes every chapter's banner outside the Demigod's Path (`<key>.png`: the page's element tile,
  the chapter's sidebar title) and deletes stale ones (such as old split-chapter banners).
- The v12 "Mod = category" split (each mod its own group, its sections as chapters) is switched off but kept in
  quest_data.py: list group keys in `SPLIT_TABS` to split those groups' pages again (`CHAPTER_TITLES` names the parts).

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
Side chapters are "pages", one file per mod or mod family (see LAYOUT in `tools/quest_data.py`); each page is one
chapter in its category's group ("Where chapters go", above). The group is set in quest_data.py; the group argument
in `Chapter(...)` is ignored, so just pass `SIDE`. Write deps as usual: they decide the page's sections.
A page's first quest should depend on the main-path quest where the mod becomes available, and the page should carry a
`links=[...]` entry back to that quest.
