# Quest book layout audit (ATM10 reference vs. the Demigod's Codex)

Read-only research, 2026-10-18. Numbers come from scripts that parse ATM10's `config/ftbquests/quests/*.snbt`
and import `tools/quest_data.py` (43 chapters, 1,617 quests). ATM10's book is All Rights Reserved, so this file
describes its **structure** only. None of its text is reused here.

---

## 1. How ATM10 organises its book

### 1.1 Groups and chapters (display order)

68 chapters, 4,808 quests. Median chapter size is **56**, mean 71. Order inside a group is mostly alphabetical.
Chapters with no group sit above the first group: Welcome, Market, Market Tiers, Bounty Board, Building Tips, Tips and Tricks.

| Group | Chapters (quests) |
|---|---|
| *(no group, top)* | welcome (6), wardaddy_market (10), market_tiers (8), bounty_board (50), building_tips (91), tips_and_tricks (23) |
| Main Questline | mainquestline_part_1 (36), allthemodium (54), the_star (128), creative (38) |
| Tools and Gear | apotheosis_gear (30), artifacts (50), **basic_armor** (128), **basic_tools** (77), mahou_tsukai (35), relics (26), silent_gear (69) |
| Storage | **storage / "Basic Storage"** (90), applied_energistics_2 (74), extended_ae (56), refined_storage (72) |
| Logistics | **basic_logistics** (40), integrated_dynamics (28), modular_router (55), pylons (13) |
| Resources | apothic_spawners (36), **food_and_farming** (35), hostile_neural_networks (50), mystical_agriculture (191), productive_bees (252), productive_trees (167) |
| Tech | create (89), draconic (140), immersive_eng (127), industrial_foregoing (78), justdirethings (154), mekanism (90), **mekanism_reactors** (94), oritech (56), xycraft (27), pneumaticcraft (127), railcraft (52) |
| Modern Industrialization | mi_steam (30), mi_electric (50), mi_digital (66), mi_endgame (25) |
| Power | **basic_power** (34), extreme_reactors (33), generators (47), powah (109) |
| Magic | 9 mod chapters, 25 to 130 quests each |
| Exploration | 9 dimension or mod chapters, 21 to 193 quests each |

### 1.2 Main line vs. mod chapters vs. basics

- **Main questline = 4 chapters, about 256 quests.** It asks for items from many mods directly, so a player can follow it alone.
  Its chapters have **zero dependencies on mod chapters**: every main and mod chapter is self-contained (cross-chapter deps were 0 in 65 of 68 chapters).
- **Mod chapters are standalone tutorials.** Each one has 1 or 2 root quests, and none of them is gated on the main line.
  ATM10 can do this because it is a kitchen-sink pack. We are a progression pack, so we should keep our gating (see §4).
- **"Basics" are not one group.** Each topic group starts with a beginner chapter: Basic Tools and Basic Armor (Tools and Gear),
  Basic Storage, Basic Logistics, Food and Farming (Resources), Basic Power. These are **catalogues**: a central hub, a handful of
  category hubs, then many optional "pick one" entries. basic_armor is 128 quests, all of them roots and 108 optional.
  basic_tools has 70 of 77 optional. They compare options rather than forcing a chain.
- Big mods are split by phase: Mekanism + Mekanism Reactors, and four MI chapters (steam, electric, digital, endgame).

### 1.3 Spatial conventions

| Convention | What ATM10 does |
|---|---|
| Flow | Main ch.1 and ch.2 read **left→right** in horizontal rows: each row is one topic (crafting, iron, diamond, nether...) and the capstones are size-2 gears at the right edge. MI chapters read **bottom→top** (y falls from 0 to -25) as a single column. |
| Hub-and-spoke | Catalogue chapters (basic_power, basic_logistics, food_and_farming, tips) put a size-2 gear root in the centre, 1.5 hexagon category hubs around it, and size-1 options in short spokes. |
| Spacing | Median nearest-neighbour distance is 1.0 to 1.5 cells, and median dependency edge is 1.5 to 2.5. Mod chapters are dense. |
| Milestone styling | Chapter capstone: **size 2.0 (sometimes 3.0) gear**. Section hubs: **1.5 hexagon**. Normal quests: 1.0 in the chapter default shape. Each chapter picks its own default shape (diamond, hexagon, gear, square). |
| Extras | `hide_dependency_lines` (480 quests) and `hide_dependent_lines` (375) cut clutter from hubs with many children. `hide_until_deps_visible` is used 199 times and `invisible` (secret) 62. 101 quests use `min_width` for wide title boxes. Images are used heavily (labels and arrows drawn as images). 10 chapters set `autofocus_id` so the book opens on the start quest. |
| Dependency fan-in | 74% of quests have exactly 1 dependency and 12% have 2. Quests with 5 or more deps are rare (25 in the whole book) and are always the big capstones. |

**Why it is easy to navigate:** you can tell a chapter's purpose from its group. Every topic group starts with a beginner chapter.
Big mods are split by phase. Each chapter has one obvious entry point and one obvious capstone. Optional catalogue entries are
visibly separate from the required line. Long cross-chapter lines don't exist.

---

## 2. Our book: measurements

### 2.1 Group and chapter order (LAYOUT)

| Group | Chapters | Quests |
|---|---|---|
| The Demigod's Path | welcome, start, t0 … t7, seed, creation (12) | 390 |
| Chemistry Lab | periodic, lab_notes, mekanism | 157 |
| Engineering | power, powah, factory, logic, create, tools, justdirethings, storage, ae2, building (10) | 457 |
| Magic and Relics | ars, apotheosis, relics, occultism, projecte (`magic` is listed but has no file) | 163 |
| Exploration | worlds, undergarden, twilight, deeperdarker, space, explore, hunting | 281 |
| Farming and Food | farming, mystical | 50 |
| Collections | qol, utilitarian, market, completionist | 119 |

Median chapter size is **34**, smaller than ATM10's 56. Every chapter has 0 roots: every chapter's first quest depends on a main-line quest.

### 2.2 Per-chapter metrics

*flow +x%* is the share of in-chapter edges that point right. *>8* counts edges longer than 8 cells. *crossings* counts pairs of
dependency lines that intersect. *line-thru* counts lines that pass within 0.45 cells of an unrelated quest. *dead ends* counts
non-optional, non-milestone quests that nothing depends on. In *milestones*, `1.5def` means size 1.5 with no shape.

| Chapter | Grp | n | req/opt | ticks | extent WxH | flow +x% | edge mean/max | >8 | crossings | line-thru | ext deps | links | max deps | dead ends | milestones |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| welcome | main | 11 | 9/2 | 11 | 10x6 | 100 | 2.3/4 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2.0gea 1.5hex |
| start | main | 50 | 37/13 | 7 | 48x8 | 56 | 2.1/3 | 0 | 0 | 0 | 1 | 0 | 2 | 4 | 2.0gea 1.5hex |
| t0 | main | 34 | 29/5 | 0 | 26x6 | 87 | 2.4/4 | 0 | 1 | 0 | 3 | 0 | 3 | 2 | 1.5def x2 |
| t1 | main | 33 | 28/5 | 1 | 31x6 | 83 | 2.8/5 | 0 | 1 | 0 | 1 | 0 | 3 | 4 | 1.5def, 1.75hex x2, 1.5hex |
| t2 | main | 25 | 19/6 | 4 | 26x6 | 85 | 4.1/14 | 5 | 8 | 8 | 2 | 0 | 4 | 1 | 2.0hex |
| t3 | main | 41 | 34/7 | 0 | 16x13 | 85 | 3.8/14 | 6 | **41** | 12 | 6 | 0 | 4 | 6 | 1.5def, 1.5gea |
| t4 | main | 47 | 38/9 | 6 | 26x17 | 79 | 3.8/14 | 4 | **33** | 7 | 13 | 0 | 3 | 0 | 1.5def x2, 1.5hex, 1.75hex |
| t5 | main | 30 | 25/5 | 0 | 22x8 | 61 | 2.2/4 | 0 | 0 | 0 | 4 | 0 | 2 | 1 | 1.5def x2, 1.75hex |
| t6 | main | 34 | 30/4 | 0 | 24x15 | 97 | 2.6/5 | 0 | 0 | 0 | 6 | 0 | 2 | 1 | 1.5def x4, 2.0gea |
| t7 | main | 21 | 15/6 | 0 | 18x7 | 85 | 3.2/6 | 0 | 0 | 1 | 6 | 1 | 3 | 1 | 1.5def x2, 1.75hex |
| seed | main | 31 | 27/4 | 2 | 18x18 | 52 | 5.6/16 | 10 | 23 | 3 | 11 | 3 | **10** | 0 | 1.5hex, 1.25def, 2.0hex |
| creation | main | 33 | 28/5 | 3 | 22x13 | 56 | 4.0/14 | 5 | 7 | 9 | 1 | 2 | 6 | 1 | 2.5gea, 1.5gea, 1.5hex, 2.0gea |
| periodic | chem | 44 | 21/23 | 1 | 18x12 | 65 | 3.7/10 | 5 | **40** | 18 | 6 | 0 | 3 | 1 | 2.0gea, 1.5def |
| lab_notes | chem | 32 | 0/32 | 30 | 10x10 | n/a | n/a | 0 | 0 | 0 | 32 | 5 | 1 | 0 | 1.5hex |
| mekanism | chem | **81** | 54/27 | 2 | **12x34** | 79 | 2.5/9 | 2 | 9 | 4 | **44** | **17** | 3 | 11 | 1.5hex x3, 1.5gea |
| power | eng | 40 | 29/11 | 0 | 16x10 | 91 | 2.6/7 | 0 | 1 | 4 | 17 | 4 | 2 | 3 | 1.5hex, 1.75hex |
| powah | eng | 34 | 26/8 | 0 | 34x10 | 81 | 3.2/12 | 1 | 0 | 7 | 9 | 13 | 2 | 4 | 1.5hex, 1.5gea |
| factory | eng | 29 | 16/13 | 1 | 11x13.5 | 79 | 2.2/3 | 0 | 2 | 0 | 15 | 4 | 2 | 1 | 1.5def x2, 1.5hex |
| logic | eng | 34 | 22/12 | 4 | 16x11 | 81 | 2.7/6 | 0 | 0 | 2 | 5 | 3 | 2 | 0 | 2.0gea |
| create | eng | 81 | 55/26 | 0 | 34x15 | 56 | 2.9/18 | 4 | 14 | 9 | 4 | 4 | 2 | 9 | 1.5def x2, 1.5gea |
| tools | eng | 40 | 24/16 | 0 | 10x23 | 93 | 3.2/18 | 2 | 6 | 9 | 25 | 4 | 3 | 5 | 1.5hex x3 |
| justdirethings | eng | 45 | 20/25 | 0 | 12x16 | 61 | 4.3/15 | 10 | **65** | 20 | 4 | 5 | 2 | 1 | 1.5hex, 1.5gea |
| storage | eng | 51 | 38/13 | 1 | 10x23 | 91 | 2.5/9 | 2 | 3 | 4 | 16 | 7 | 3 | 10 | *(none)* |
| ae2 | eng | 67 | 40/27 | 0 | 10x29.5 | 75 | 4.1/18 | 11 | **89** | **37** | 13 | 7 | 3 | 10 | *(none)* |
| building | eng | 36 | 4/32 | 2 | 10x17 | 100 | 3.6/8 | 0 | 0 | 20 | 14 | 4 | 4 | 1 | 1.5hex |
| ars | magic | 60 | 31/29 | 5 | 20x12 | 51 | 4.5/16 | 11 | **125** | **35** | 2 | 2 | **8** | 1 | 1.5hex x2 |
| apotheosis | magic | 21 | 10/11 | 1 | 11x8.5 | 88 | 2.4/4 | 0 | 0 | 2 | 8 | 1 | 2 | 4 | 1.5def |
| relics | magic | **15** | 7/8 | 2 | 9x3 | 100 | 2.8/5 | 0 | 0 | 3 | 5 | 1 | 2 | 2 | *(none)* |
| occultism | magic | 48 | 36/12 | 0 | 28x9 | 75 | 3.2/16 | 5 | 22 | 13 | 3 | 2 | 3 | 0 | 1.5def x3, 1.5hex x3 |
| projecte | magic | 19 | 13/6 | 3 | 12x5 | 89 | 3.1/8 | 0 | 2 | 8 | 1 | 1 | 2 | 5 | 1.5hex, 1.5gea |
| worlds | world | 21 | 14/7 | 1 | 8x12 | 80 | 2.5/4 | 0 | 0 | 0 | 3 | 2 | 2 | 0 | 1.5def |
| undergarden | world | 34 | 16/18 | 0 | 16x10 | 70 | 3.4/11 | 1 | 1 | 5 | 1 | 2 | 2 | 2 | 1.5hex, 1.5gea |
| twilight | world | 79 | 30/49 | 0 | **48x24** | **29** | 3.2/16 | 4 | 0 | 1 | 3 | 1 | 2 | 1 | 1.5hex x2, 2.0gea |
| deeperdarker | world | 23 | 11/12 | 0 | 8x8 | 90 | 3.9/9 | 1 | 6 | 6 | 3 | 3 | 1 | 2 | 1.5hex, 1.5gea |
| space | world | 28 | 10/18 | 0 | 17.5x10 | 50 | 2.3/4 | 0 | 1 | 0 | 6 | 2 | 2 | 0 | 1.75hex |
| explore | world | 45 | 18/27 | 3 | 14x19.5 | 78 | 2.0/2 | 0 | 0 | 0 | 13 | 2 | 1 | 3 | *(none)* |
| hunting | world | 51 | 34/17 | 0 | 18x15.5 | 86 | 2.0/3 | 0 | 0 | 0 | 28 | 13 | 1 | 17 | 1.5hex |
| farming | life | 22 | 13/9 | 0 | 8x9 | 89 | 2.6/6 | 0 | 4 | 2 | 8 | 4 | 3 | 3 | *(none)* |
| mystical | life | 28 | 20/8 | 1 | 14x9.5 | 70 | 2.9/10 | 1 | 5 | 6 | 6 | 5 | 3 | 5 | 1.5hex |
| qol | extra | 37 | 15/22 | **14** | 16x10 | 75 | 2.2/5 | 0 | 0 | 0 | 19 | 4 | 2 | 7 | *(none)* |
| utilitarian | extra | 20 | 14/6 | 0 | 8x8 | 73 | 2.6/4 | 0 | 0 | 2 | 5 | 1 | 2 | 4 | *(none)* |
| market | extra | **12** | 11/1 | 6 | 6x4 | 61 | 2.6/6 | 0 | 0 | 2 | 4 | 1 | 3 | 1 | *(none)* |
| completionist | extra | 50 | 0/50 | 1 | 18x13.5 | 97 | 3.9/16 | 3 | 0 | 37 | 35 | 4 | 4 | 0 | 1.5gea, 1.5def |

### 2.3 What the numbers say

**Good already:** no overlapping quests anywhere. No spacing under 1 cell (nearest neighbour is 1.5 to 2.0, roomier than ATM10).
Flow is left→right in almost every chapter. start, t5, t6 and t7 are clean (0 crossings).

**Problems:**
1. **Two chapter shapes compete.** The main tiers and big mod chapters are *wide*: x 0→30, spine near y=0. Most side chapters are
   *tall, narrow stacks of rows*: x 0→10 and y down to 20 or 30 (mekanism 12x34, ae2 10x29.5, tools 10x23, storage 10x23,
   explore 14x19.5, building 10x17). The tall ones make you scroll down through unrelated rows: storage has 7 unrelated rows,
   including iron furnaces and logistics nodes.
2. **The spine isn't on y=0 in the heaviest tiers.** Only 3 of 34 required t3 quests and 1 of 38 required t4 quests sit on y=0.
   Both read as a web: 41 and 33 line crossings.
3. **Tangled chapters:** ars (125 crossings, 35 lines through quests), ae2 (89/37), justdirethings (65/20), t3 (41), periodic (40/18),
   t4 (33), seed (23), occultism (22). The cause is hub quests feeding children spread over many rows (`m_apparatus` 16 children,
   `ars_source_gem` 9, `jdt_blazegold` 8) and edges of 10 to 18 cells.
4. **Long edges (>8 cells):** 112 in total. The worst are `cr_tube→cr_clockwork` (18.1), `s_ae_cell` fan-out (up to 18),
   `tc_crimson_steel→tc_sg_armor` (17.6), `ars_wings→m_ritual` (16.3), `oc_attuned_gem→oc_infused_pick` (16.1), `sd_intro→*` (8 to 13.5),
   and `cn_*→cn_demigod` (8.6 to 14.2).
5. **Milestone styling is inconsistent.** Sizes in use: 1.25, 1.5, 1.75, 2.0 and 2.5. 1.5 quests come with no shape, hexagon or
   gear more or less at random: t0/t3/t6 use bare 1.5 squares, t1/t4/t5/t7 use 1.75 hexagons. Seven chapters
   (storage, ae2, explore, farming, qol, utilitarian, market, relics) have **no milestone at all**.
6. **Many deps on one quest:** `t7_seed` 10, `ars_mastery` 8, `cn_demigod` 6, `t7_seed_nuclear` 5. Plus 4-dep collectors
   (`t2_pylon`, `t3_analog`, `bd_lab_done`, `cp_el_all`). Fine for capstones, but they need to sit at the right edge, centred on their inputs.
7. **Hub quests with huge fan-out across the book:** `gs_iron` has 45 dependents, `t2_nether` 36, `t6_pu` 23, `t5_hv` 19, `gs_table` 17.
   That's fine, because those are chapter entry points, but it means link icons are the only way to see where a chapter starts.
   Links are used inconsistently: 0 in all main tiers, 17 in mekanism, 13 in powah and hunting.
8. **Link placement:** the `t2_pylon` link in ars sits within 1 cell of a quest. Hunting's links at y=-3 sit under the auto-placed chapter banner.
9. **Quest keys don't match their chapter** in 11 chapters (`s_*` in ae2, `m_*` in ars/apotheosis/relics/occultism, `w_*` in twilight/space/explore,
   `q_*` in building, `t7_seed*` in seed). That's harmless, because keys are frozen, but it shows chapters were split by hand. A layout pass must not assume the prefix gives the chapter.
10. **Chapter sizes:** six chapters have 21 or fewer quests (welcome 11, market 12, relics 15, projecte 19, utilitarian 20, worlds 21, apotheosis 21).
    Mekanism and create have 81 each. Twilight is the widest at 48 cells and flows mostly right→left (only 29% of its edges point right).

---

## 3. Prune candidates ("un-needed" quests)

Rules: keys are never renamed. "Remove" loses only that quest's completion. "Merge into X" means delete the key, move its
task or text into X, and re-point its dependents to X's key. "Make optional" loses nothing, but STYLE.md says a main-line quest
can never depend on an optional one, so any dependents have to be re-pointed first.

### 3.1 True duplicates (same task twice)

| Key | Chapter | Reason | Recommendation |
|---|---|---|---|
| `q_claim` | qol | Same title and tick as `gs_claim` (start) | **Remove** (dead end), or make optional |
| `ex_compass` | explore | Identical tasks to `q_compass` (both compasses); both are dead ends | **Remove**, add a link to `q_compass` |
| `tc_waystone` | tools | Same item as `ql_warpstone` (qol); dead end | **Remove** (keep the qol one) |
| `tc_toolbelt` | tools | Same item as `ql_belt` (qol); dead end | **Remove** |
| `tc_jdt_goo`, `tc_jdt_ferricore`, `tc_jdt_blazegold`, `tc_jdt_celestigem`, `tc_jdt_eclipse`, `tc_jdt_pocket`, `tc_jdt_portal` | tools | A copy of the first JDT tiers; the justdirethings chapter has its own `jdt_goo`/`jdt_blazegold` line | **Make all optional** (nothing outside the row depends on them), or remove and add a link to `jdt_goo` |
| `t1_steel_paxel` | t1 | Same as `tc_steel_paxel`; a *required* dead end on the main tier | **Make optional** |
| `t0_opt_paxel` | t0 | Same as `tc_bronze_paxel` (tools) | **Remove** or leave optional |
| `t0_opt_wrench` / `t3_wrench` | t0 / t3 | Same MI wrench asked twice, both optional | **Remove `t3_wrench`** |
| `pw_iron_gen` | power | Same item as main `t1_power` | Change its task to the next generator, or swap it for a link to `t1_power` (rewire `pw_gold_gen`, `pw_heat`) |
| `t5_cells` | t5 | 1k cell is also `s_ae_cell` (ae2); required dead end | **Make optional** |
| `t5_inscriber` / `t5_ae2` | t5 | Both ask for the inscriber | Drop the inscriber task from `t5_ae2` |
| `t6_pgm` | t6 | Re-asks the sludge and chloroplatinic acid already done in `t6_sludge` and `t6_aqua` | Keep only the final product in its tasks |
| `t7_cores` / `t7_core_charge` | t7 | Both ask for `energy_core` | Merge the tasks; keep both keys |
| `t4_ore5` | t4 | Re-asks the dissolution chamber and washer (`t4_dissolution`, `t4_washer`) | Keep only the crystallizer task |
| `sto_ln_node` (+ `sto_ln_upgrade`, `sto_ln_chem`, `sto_ln_computer`) | storage | Logistics Networks is also taught in logic (`lg_logistics`) | **Move the row into logic** beside `lg_logistics` (keys unchanged) |
| `ma_pots` | mystical | Hopper botany pot is already `f_pot` (farming); dead end | **Make optional** |
| `w_desh` / `t7_desh` | space / t7 | Both ask for raw desh | Turn `w_desh` into a link to `t7_desh` (rewire its 4 dependents) |
| `ut_sticks`, `ut_chests` | utilitarian | Repeat `gs_sticks` and `gs_chest` (vanilla crafting) | Change the tasks to Utilitarian items, or move the row's dependents onto `gs_table` and **remove** them |
| `cn_atomic`, `cn_shining`, `cn_pocket` | creation | Repeat `mk2_atomic`, `mk2_ex_cosmic` and `mf_cm_*` | OK as a capstone recap; or replace with links |
| `sd_wither`, `sd_dragon` | seed | Same kills as `hn_wither` / `wd_dragon` | Keep (the seed needs them), but place them as links |

### 3.2 Intermediate re-asks and over-long chains

| Key(s) | Chapter | Reason | Recommendation |
|---|---|---|---|
| `sd_coke`, `sd_water`, `sd_hydrogen`, `sd_sulfur`, `sd_acid`, `sd_ethylene`, `sd_pe`, `sd_stainless`, `sd_unit`, `sd_oganesson`, `sd_plutonium`, `sd_polonium` (12) | seed | Each asks for 1 item that the `t7_seed_*` bundle right after it asks for again in bulk. The player made all of these in t1 to t6. This is the main source of seed's 23 crossings and its 10-dep capstone. | Point the `t7_seed_*` bundles straight at `sd_intro`, then make the 12 `sd_*` quests **optional** (a hidden "bill of materials" checklist). This loses no progress. |
| `sd_cores2` → `sd_cores4` → `t7_seed_cores` | seed | A count ladder (2, 4, 8 of the same core) | Make `sd_cores2` and `sd_cores4` optional; `t7_seed_cores` depends on `sd_pellets` and `sd_quantum` |
| `t2_awkward`, `t2_flying`, `t2_filter_full` | t2 | Tick-only steps between item steps of the flight potion line | **Merge** each into its neighbour (`t2_brewing`, `t2_chorus`, `t2_filter`) as a "How:" line |
| `t2_chunkload` | t2 | Tick tip after the milestone; required dead end | **Make optional** |
| `gs_planks`, `gs_sticks`, `gs_cobble`, `gs_seeds` | start | Vanilla micro-steps on a 25-quest spine (ATM10's chapter 1 skips them) | **Merge** into the next quest (`gs_table`, `gs_woodpick`, `gs_stone`, `gs_farm`), or keep them as cheap onboarding (author's call) |
| `gs_jade`, `gs_daylight` | start | Tick tips that are dead ends | Merge into `gs_jei` / `gs_shelter`, or make optional |
| `wel_book`, `wel_team`, `wel_perf` | welcome | 11 tick quests in a row (ATM10's welcome has 6) | **Merge** into `wel_progress` and `wel_keys` → a 6 to 8 quest welcome |
| `mk_jei`, `mk_rules`, `mk_medium`, `mk_large` | market | Chain of 6 ticks explaining the shop | **Merge** `mk_jei`+`mk_rules` into `mk_intro`, and `mk_medium`+`mk_large` into `mk_small` (rewire `mk_day_mid`/`mk_day_late`) |
| `ex_desert_village` → … → `ex_tt_swamp` → `w_town` | explore | A chain of 6 optional village visits; order has no meaning | Give all of them `ex_village` as the only dep (siblings, not a chain); make `w_town` (tick) part of `ex_village`'s text |
| `t3_ecompressor`, `t3_ewiremill`, `t3_efurnace`, `t3_cutting`, `t3_packer` | t3 | Required dead ends: electric copies of steam machines; nothing needs them | **Make optional** and put them on one "electrify the workshop" row |
| `t4_brine`, `t4_chlorine`, `t4_hcl` | t4 | Tick-only chemistry steps | **Keep** (teaching value); just place them in a row |
| `pw_gas`, `pw_large_diesel`, `pw_large_turbine`, `pw_photo`, `pw_cell_hardened`, `pw_cable_hardened`, `pw_ender_gate` | power / powah | Required dead ends inside side chapters | Make optional (they are alternatives, not steps) |

### 3.3 Side quests with little gameplay value (keep optional, low priority)

`lab_notes` (30 hidden optional ticks) is lore-only. Keep it, but consider moving each note into its main quest as a
`{@pagebreak}` deep-dive page and leaving the chapter as an index. Kill-count ladders in hunting (`*_2`, `*_3`) are already optional.
`bd_*` decor quests are already optional.

### 3.4 Chapters that are too small or too big

| Chapter | Size | Recommendation |
|---|---|---|
| mekanism | 81, 34 tall, 17 links | **Split** (as ATM10 does): keep `mekanism` for machines, factories, circuits, alloys, teleport, QIO and logistics (about 50 quests, rows y ≤ 13.5). Make a new `mekanism_power` chapter for the boiler, turbine, fusion, armour, MM and Mekanism Extras rows (about 31). |
| storage | 51 with 7 unrelated rows | Move the Iron Furnaces row (`s_furnace`, `sto_if_*`, 12 quests) to a Basics "Machines and Furnaces" chapter, and Logistics Nodes plus `s_pipes`/`s_laser` to logic. That leaves about 32 quests of storage: barrels, drawers, Tom's, backpacks. |
| ae2 | 67, 29.5 tall, 89 crossings | Keep it, but re-lay it out as a wide chapter: 5 rows (network, cells, autocrafting, add-ons, Extended AE). |
| utilitarian (20) | small | **Merge into qol** or building (both are "comfort" pages). |
| market (12), welcome (11) | small | Shrink (§3.2) and move to the ungrouped top area like ATM10. |
| relics (15), apotheosis (21), projecte (19) | small | Fine as mod pages (ATM10 has 13 to 26 quest pages). Optionally group them as "Gear and Loot". |
| twilight | 79, 48 wide, flows right→left | Re-lay out left→right: one row per boss tier. |

Rough net effect: about 25 quests removed or merged and about 45 made optional. The required count drops by about 70.

---

## 4. Proposal: the reformatted book

### 4.1 Groups and order

We keep progression gating (side chapters open from main quests). That is what makes this a progression pack, unlike ATM10.
From ATM10 we take the "Basics first" idea, standalone-looking chapters and the phase splits.

| # | Group (tab) | Chapters, in order | Change |
|---|---|---|---|
| top | *(ungrouped)* | welcome, market, lab_notes (Codex), completionist | welcome and market move out of main/extra |
| 1 | The Demigod's Path | start, t0, t1, t2, t3, t4, t5, t6, t7, seed, creation | welcome moves out |
| 2 | **Basics** | tools, storage, power, farming, qol (+utilitarian merged), building | new group; these are the beginner "comfort" pages |
| 3 | Chemistry Lab | periodic, mekanism, **mekanism_power** (new) | split |
| 4 | Industry and Automation | factory, logic, create, powah, justdirethings, ae2 | power moves to Basics |
| 5 | Magic and Relics | ars, occultism, apotheosis, relics, projecte | remove the dead `magic` entry |
| 6 | Exploration | worlds, explore, undergarden, twilight, deeperdarker, space, hunting | none |
| 7 | Resources | mystical (+ farming, if it stays out of Basics) | rename "Farming and Food" |

All of this is a `GROUPS`/`LAYOUT` edit plus moving `Q(...)` blocks between chapter files. Quest keys are untouched.
A chapter key is only used for the chapter id, so new chapter keys like `mekanism_power` are safe.
`build_quests.py` currently gives every chapter a group (`next(...)` in quest_data.py). An ungrouped top section needs a tiny engine
change: give the empty group `""` an `"ungrouped"` key and leave the `group` field out for those chapters.

### 4.2 Layout rules for an automatic pass

Make it opt-in per chapter: `Chapter(..., layout="auto")`, with optional `Q(..., row=N)`. Coordinates that are already written by hand stay as overrides.

| Rule | Spec |
|---|---|
| L1 Grid | Column pitch **2.0**, row pitch **2.0**, optional sub-row pitch **1.5**. All coordinates are multiples of 0.5. |
| L2 Column = depth | x = 2 × (longest in-chapter dependency path from the entry quest). Deps on other chapters count as depth 0. Every edge then points right. |
| L3 Spine on y=0 | The required critical path (entry → capstone, longest chain of non-optional quests) sits on **y=0**. |
| L4 Rows = sub-topics | Other required branches become rows at y = −2, +2, −4, +4 … (closest to the spine first, by attachment column). Each row is one sub-topic (e.g. t4: acids row, aluminium row, sodium row). Use `row=` to pin one. Max 6 rows. |
| L5 Optional placement | An optional quest sits half a row outward (±1.5) from its parent's row, in the next column. It never sits on y=0 (STYLE.md already says this). |
| L6 Crossing reduction | Inside each column, order quests by the mean y of their parents (one or two barycentre sweeps, as in Sugiyama-style graph drawing). Target: under 5 crossings per chapter. |
| L7 Max edge | An in-chapter edge longer than **6 cells** (3 columns) is flagged. Either move the child closer, or swap the dep for a quest link placed next to the child. |
| L8 Links | Cross-chapter entry deps become a **link column at x = −2**, sorted by target row. Every chapter gets one (main tiers currently have none). There must be at least 1.2 cells of clearance from quests and banners. |
| L9 Milestones | Exactly two styles. **Chapter capstone: size 2.0 gear**, at the rightmost column, y=0. **Section milestone: size 1.5 hexagon**. No 1.25, 1.75 or 2.5 sizes, and no shapeless 1.5. Every chapter needs a capstone (8 chapters currently lack one). |
| L10 Fan-in | A quest with 4 or more deps goes one column right of its deepest dep, at the mean y of its deps. A hub with 6 or more in-chapter children gets `hide_dependent_lines` (needs a small engine flag; ATM10 uses this on 375 quests). |
| L11 Chapter size | 15 to 60 quests and at most 36 cells wide. Over 60 means split by phase; under 15 means merge. `--check` warns. |
| L12 Banner | Placed above the topmost row and the link column, not just above the top-left quest (fixes the hunting overlap). |

Add a `--layout-report` to `build_quests.py` (the metric script used for §2.2) so that crossings, long edges and size are checked on every build.

### 4.3 Effort

| Task | Effort |
|---|---|
| Group restructure (LAYOUT, ungrouped top, remove `magic`) | 1 to 2 h |
| Metric/lint script into `tools/` (`--layout-report`, warnings for L7/L9/L11) | 2 to 3 h |
| Auto-layout engine (L1 to L8, L10, L12) in questlib/build, opt-in per chapter | 1 to 1.5 days |
| Apply it chapter by chapter and hand-tune `row=` pins (43 chapters; main tiers t3, t4, seed and ars/ae2/jdt/periodic first) | 1.5 to 2 days |
| Prune pass (§3: about 25 removals or merges, about 45 made optional, rewiring deps, rewriting merged text) | 0.5 to 1 day |
| Splits and moves (mekanism → 2, storage rows → logic/Basics, utilitarian → qol) | 0.5 day |
| In-game review pass (open every chapter, fix outliers) | 0.5 to 1 day |
| **Total** | **about 5 to 7 working days**; the main tiers alone are about 2 days |
