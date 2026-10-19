# Tools, Armour and Harvest Tiers: research and chapter plan

Status: research only (2026-10-18). Nothing in `tools/quests/` or `pack/` was changed.
Sources: block/item tags read from the vanilla 1.21.1 client jar, NeoForge 21.1.262 universal jar and all 205 jars in
`test/server/mods` (tags resolved recursively, decor mods ignored); tool tiers read from the mod classes with `javap`;
our book in `tools/quests/*.py`; ATM10's book (structure and item ids only, it is All Rights Reserved).
The pack has **no** KubeJS or datapack tag overrides for harvest levels (`pack/kubejs/data/*/tags` has no `needs_*` or `incorrect_for_*`).

---

## 1. How harvest tiers work in this pack

In 1.21.1 a block asks for a tier with a `needs_*` block tag, and a tool refuses blocks listed in its `incorrect_for_*` tag.
The tags in play:

| Tier | Block tag (blocks that need it) | Notes |
|---|---|---|
| 0 Any pickaxe | (no tag) | coal, nether quartz, nether gold, amethyst, AE2 certus, JDT goo ores, **all Ad Astra planet metal ores** |
| 0* Wood | `neoforge:needs_wood_tool` | only Twilight nagastone / mazestone trim, AP peripheral casing |
| 1 Stone | `minecraft:needs_stone_tool` | iron, copper, lapis, **every MI ore**, every Mekanism ore |
| 2 Iron | `minecraft:needs_iron_tool` | gold, redstone, diamond, emerald, zinc, thorium, uraninite, sky stone, crimson iron, bort |
| 3 Diamond | `minecraft:needs_diamond_tool` | obsidian, crying obsidian, ancient debris, refined obsidian block, cobalt obsidian, Twilight mazestone/deadrock |
| 4 Netherite | `neoforge:needs_netherite_tool` | Silent Gear **azure silver ore** (End), Mekanism Extras **naquadah ore** |
| Side branch | `undergarden:needs_forgotten_tool` | dreadrock + **dreadrock utherium / rogdorium ore**. Vanilla netherite cannot mine it (it sits in `incorrect_for_netherite_tool`) |
| Side branch | `projecte:needs_dark_matter_tool` / `needs_red_matter_tool` | DM / RM blocks only (ProjectE lite, oganesson-gated) |

`silentgear:needs_copper_tool` exists (gold, redstone, silver ores) but has no effect: SG copper tools use the stone tier list.

### 1a. Ores and key blocks by tier

| Ore / block | Tier | Where it matters in our path |
|---|---|---|
| Coal, nether quartz, nether gold, amethyst, certus, JDT goo ores | 0 | any pickaxe |
| Ad Astra desh, ostrum, calorite, ice shard, cheese, planet iron/copper/coal | 0 | **gap**: rocket-age metals mine with a wooden pickaxe |
| Ad Astra glacio lapis, Mars diamond, Venus gold | 2 | vanilla parity only |
| Iron, copper, lapis (also Deeper and Darker, Undergarden iron, cloggrum) | 1 | start.py stone pickaxe |
| MI tin, lead, nickel, antimony, bauxite, salt, lignite, monazite, quartz ore | 1 | |
| **MI titanium, tungsten, platinum, iridium, uranium** | 1 | **gap**: endgame metals need only a stone pickaxe (chemistry gates them, harvest does not) |
| Mekanism osmium, fluorite (tin/lead/uranium gen is off) | 1 | |
| Gold, redstone, diamond, emerald (all dims), Occultism/MekMM silver | 2 | start.py iron pickaxe |
| Create zinc, New Age thorium, Powah uraninite (gen off), AE2 sky stone | 2 | |
| SG crimson iron (Nether), bort; Undergarden regalium, utherium (depthrock), froststeel | 2 | |
| MA prosperity ore (inferium ore is 1) | 2 | |
| Obsidian, crying obsidian, ancient debris, respawn anchor, netherite block | 3 | t1_combiner_parts (2 obsidian), t2_obsidian (portal), t2_debris |
| Mekanism refined obsidian block, Regions Unexplored cobalt obsidian | 3 | |
| SG azure silver ore (End), Mekanism Extras naquadah ore | 4 | tc_azure (azure electrum) |
| Undergarden dreadrock utherium / rogdorium | Forgotten | ug_* (only forgotten tools or "mine-anything" tools) |

### 1b. Which tools reach which tier

"All" = the tool's `incorrect_for` tag is empty, so it harvests everything, including the forgotten and netherite-only blocks.

| Tier reached | Tools in this pack (source of tier) | First available (our chapter) |
|---|---|---|
| 0 Wood | vanilla wood/gold, Mek wood paxel, SG wood/bamboo/netherwood, TF glass/ice sword | start |
| 1 Stone | vanilla stone, Mek stone + **lapis** paxel/tools, SG flint/stone/copper/bone/basalt/obsidian heads, TF **giant** pickaxe | start |
| 2 Iron | vanilla iron, Mek **bronze**, **osmium**, iron paxel; SG iron/bronze/blaze gold/emerald/high-carbon steel/quartz; **JDT ferricore**; TF **ironwood**; UG **cloggrum, froststeel**; MA **soulium** dagger | start (iron), t0 (bronze), t3 (osmium) |
| 3 Diamond | vanilla diamond, Mek **steel** and **refined glowstone** paxels/tools, Mek diamond paxel; SG diamond/crimson iron/azure silver/dimerald heads; **JDT blazegold, celestigem**; TF **steeleaf, knightmetal**; UG **utherium**; Occultism infused (spirit attuned) pickaxe; **MI Steam Mining Drill** (hard-coded diamond tier) | **t1 (steel paxel)**, t0 opt (steam drill) |
| 4 Netherite | vanilla netherite, Mek **refined obsidian**, Mek netherite paxel; SG crimson steel/azure electrum/tyrian steel; **JDT eclipse alloy**; TF **fiery**; **MI Diesel Mining Drill** (hard-coded netherite tier) | t2 Nether onward; t3+ (refined obsidian); t5 (diesel drill) |
| All | **UG forgotten**; **Deeper and Darker resonarium + warden**; **every Mystical Agriculture tool (inferium to awakened supremium)**; Mekanism **Atomic Disassembler**, **Meka-Tool**; ProjectE DM/RM (DM cannot do RM blocks) | UG (t4), Otherside, MA inferium pickaxe needs a diamond pickaxe + inferium |
| (hardness only) | Mining Gadgets laser breaks by hardness, no tier check found (verify in game); EI electric/laser drills not checked (verify) | t3+ |

Not mining tools: MI forge hammers (crafting tools), AE2 quartz tools (vanilla-like, treat as iron; verify), Create (no pickaxe).

### 1c. Surprises worth knowing
1. **Diamond tier arrives at T1 without diamonds.** Mekanism steel tools are diamond tier, so `t1_steel_paxel` already mines obsidian for `t1_combiner_parts`. Neither quest says so.
2. **No quest ever asks for a diamond pickaxe**, yet obsidian is needed in t1 and t2. The text of t2_obsidian says "diamond pickaxe" (fine), but the book never shows one.
3. **Vanilla diamond and netherite gear (tools and armour) is not quested anywhere.** The netherite smithing template is not quested either.
4. **Netherite cannot mine dreadrock.** In the Undergarden only forgotten tools (or the "All" tools) work. That is a nice, real "new tier" moment the Undergarden chapter already uses (ug_forgotten_tools).
5. **Mystical Agriculture tools skip the ladder.** An inferium pickaxe (diamond pickaxe + inferium) harvests everything, including azure silver, naquadah and dreadrock ores. Not a gate break (ore still needs chemistry), but it flattens any tier quest. Worth a decision.
6. **Ad Astra ores have no tier at all** and **MI's late metals (Ti, W, Pt, Ir, U) are stone tier.** Harvest tiers stop meaning anything after the Nether unless we add tags (see section 5).
7. MI gravichestplate (flight) needs superconductor parts, so it is late; not chemistry-gated by script, but effectively gated. Not quested.

---

## 2. What our book already covers (overlaps)

| Chapter | Tool / armour quests today |
|---|---|
| start (main) | gs_woodpick, gs_stone, gs_stonetools, gs_leather, gs_shield, gs_ironpick, gs_irontools, gs_armor (iron set), gs_paxel (iron paxel), gs_silent (SG pickaxe), opt: gs_opt_gold, gs_opt_chain, gs_opt_smithing, gs_opt_paxels (wood/stone/gold/diamond paxel) |
| t0 | t0_iron_hammer (MI), opt: t0_opt_paxel (bronze), t0_opt_drill (steam drill, diamond tier) |
| t1 | t1_steel_paxel (diamond tier, main line, not optional) |
| t2 | t2_obsidian, opt t2_debris (no netherite follow-up) |
| t5 / t6 / t7 | t5_opt_tools (diesel drill + jetpack), t6_opt_hazmat, t7_suit / t7_suit_full / t7_opt_hot_suit |
| tools (side, 40 quests, `tc_`) | Silent Gear line (repair, blaze gold, grader, salvager, crimson iron/steel, alloy forge, azure electrum, tyrian), paxels (bronze, osmium, diamond, refined obsidian, steel), Atomic Disassembler, Mek gear (scuba, free runners, MekaSuit, hazmat, jetpack), Iron Jetpacks, Angel Ring, toolbelt, Mining Gadget, SG parts/coating/curios/armour, JDT goo summary, comfort items |
| mekanism | mk2_mekatool, mk2_mekasuit_full, mk2_armor_osmium, mk2_armor_obsidian, opt mk2_armor_glowstone |
| justdirethings | jdt_tools_t1..t4, jdt_oreminer, jdt_bows, jdt_upgrades, jdt_armor, jdt_elytra, jdt_flight |
| undergarden | ug_cloggrum_tools/armor, ug_forgotten_tools, ug_utherium_gear, ug_froststeel, battleaxes |
| twilight | tf_ironwood/steeleaf/naga/fiery/knight gear, tf_mazebreaker, tf_giants, arctic/yeti armour |
| deeperdarker / worlds | dd_res_gear, dd_warden_tools, dd_warden_set; w_warden_armor, w_elytra, w_soul_elytra |
| apotheosis | m_gems, reforging, salvage, gem cutting, sockets, augmenting (gear upgrading, not tiers) |
| projecte / ae2 / creation | pe_dm_tools, pe_dm_armor; ae_quantum_armor; cn_quantum_armor |
| completionist | armour trims (5 quests) |

Overlap to watch: the paxel line is split between start (iron, opt set), t0 (bronze), t1 (steel), tools (bronze, osmium, diamond, steel, refined obsidian). `tc_bronze_paxel` duplicates `t0_opt_paxel`, `tc_steel_paxel` duplicates `t1_steel_paxel`, `tc_diamond_paxel` overlaps `gs_opt_paxels`.

---

## 3. ATM10's approach (patterns only, described in our own words)

- **basic_tools (~77 quests):** one short "tier spine" of raw materials, each step being the thing the previous tier lets you mine (cobblestone, raw iron, diamond, ancient debris, then their two custom ores). Beside it, a column of the vanilla pickaxe for each tier (plus refined obsidian), and a big fan of optional "any pickaxe of this mod/tier" collection quests built with FTB Filter System `or(item(...))` filters. A second fan does the same for swords. Almost all quests optional, one dependency each, no text.
- **basic_armor (~80 quests):** no dependencies at all. A horizontal row of vanilla sets (iron, diamond, netherite mandatory; leather, chain, gold optional) ordered by strength left to right, then their custom ores; modded sets (Mekanism Tools, MA, Undergarden, JDT, Ars robes, etc.) sit as optional satellites near the vanilla set of equal strength; a grid of armour trims below.
- **apotheosis_gear (30) / silent_gear (69):** mod mechanics pages: tables, sigils, rarity materials, then gateways; SG via their foundry addon casts, blueprints, grader/salvager, alloy forge and the three top alloys as blocks.
- Takeaways for us: (a) a visible "material you can now mine" spine is the core idea; (b) group tools by **tier**, not by mod, with any-of tasks; (c) armour placed by strength; (d) heavy use of optional collection quests. What we do differently: every step carries text and real material science, and the spine hangs off our main path instead of floating.

---

## 4. Proposal: chapter `harvest`, "Tools, Armour and Harvest Tiers"

- **Key / prefix:** `harvest`, quest keys `hv_*` (prefix unused). Group `eng`, placed before `tools` in LAYOUT
  (`"eng": [..., "create", "harvest", "tools", "justdirethings", ...]`). Icon `minecraft:diamond_pickaxe`.
- **Shape:** three horizontal rows. Row y=0: the **harvest spine** (milestone hexagons, one per tier, task = the ore you can now
  mine). Row y=-2: **tools** that reach the tier (any-of tasks across mods). Row y=+2: **armour** of matching strength.
  Optional material-science side quests at y=+4.
- **Entry:** first quest depends on `gs_woodpick`; the chapter carries `links` to gs_stone, gs_ironpick, t1_steel_paxel,
  t2_nether, t3_infuser, t4_undergarden, t5_twilight, w_dragon. Each tier quest also depends on the main-path quest where that
  tier becomes reachable, so the page never runs ahead of the story.
- **Story beat:** the demigod remembering that their old power was "the hardness of things": each tier is a memory of a
  harder substance.

### 4a. The line (≈34 quests: 9 spine, 9 tools, 8 armour, 8 optional)

| # | Key | Spine step (task) | "Now you can mine" | Tool row (any-of) | Armour row | Material science angle | Hangs off |
|---|---|---|---|---|---|---|---|
| 0 | hv_intro | tick() | how tiers work (Jade shows the needed tool) | | | hardness vs toughness; Mohs scale is a scratch test | gs_woodpick |
| 1 | hv_stone | any 16 cobblestone + raw iron | iron, copper, lapis, every MI and Mekanism ore | stone pickaxe / stone or lapis paxel / SG flint head / TF giant | leather set (opt) | flint and chert are microcrystalline SiO₂ (Mohs ~7), conchoidal fracture makes an edge | gs_stone |
| 2 | hv_bronze | raw tin + bronze ingot | (same tier, more durability) | bronze paxel / SG bronze / MI bronze tools | Mek bronze armour | solid-solution strengthening: Sn atoms in the Cu lattice pin dislocations; Cu ~Mohs 3, bronze clearly harder | t0_bronze |
| 3 | hv_iron | raw gold + redstone + diamond | gold, redstone, diamond, emerald, zinc, thorium, sky stone, crimson iron | iron pickaxe / iron, bronze or osmium paxel / JDT ferricore / TF ironwood / UG cloggrum | iron set (link gs_armor), chainmail (opt) | iron is soft when pure; bloomery vs blast furnace; why pig iron is brittle (≈4% C) | gs_ironpick |
| 4 | hv_steel | 2 obsidian | **obsidian, crying obsidian, ancient debris** | steel paxel (link t1_steel_paxel) / diamond pickaxe / Steam Mining Drill / JDT blazegold / SG diamond or crimson iron | Mek steel armour | 0.2-2% carbon; quench to martensite, then temper; heat treatment trades hardness for toughness | t1_steel |
| 5 | hv_diamond | hv_diamond_pick: a diamond pickaxe | (vanilla route to the same tier) | diamond pickaxe / diamond paxel | diamond set | sp³ carbon network, Mohs 10, but cleaves: hard is not tough | gs_ironpick |
| 6 | hv_netherite | ancient debris + netherite scrap + smithing template | azure silver ore, naquadah ore | netherite pickaxe / refined obsidian paxel / SG crimson steel / JDT eclipse alloy / TF fiery / diesel drill | netherite set (template from a bastion: `structure("minecraft:bastion_remnant")` opt) | netherite is fictional; compare real super-hard composites: tungsten carbide (WC, Mohs ~9) cemented with cobalt | t2_debris (make dep, not optional) / t2_nether |
| 7 | hv_refined | refined obsidian ingot | (netherite tier, Mekanism route) | refined obsidian pickaxe/paxel (link tc_obsidian_paxel) | Mek refined obsidian armour (link mk2_armor_obsidian) | infusing osmium into obsidian dust: a made-up cermet; real ceramic-metal composites are why drill bits last | t3_infuser |
| 8 | hv_forgotten | dreadrock utherium ore | dreadrock ores (netherite fails here) | forgotten pickaxe (link ug_forgotten_tools) / resonarium / warden | UG utherium armour (link ug_utherium_gear) | why "harder" is not one number: a tool must out-scratch the mineral it cuts | t4_undergarden |
| 9 | hv_all | tick() milestone | everything | any of: Atomic Disassembler, Meka-Tool, warden pickaxe | MekaSuit (link mk2_mekasuit_full) | energy instead of edge: FE tools break bonds, not scratch | t3_infuser / t4_mv |

Optional side quests (y=+4, `optional=True`, 1-2 tokens):
- `hv_opt_mohs`: "The Scratch Test": calcite or chemlib:calcium_carbonate (3), chemlib:calcium_sulfate (gypsum, 2), mekanism:fluorite_gem (4, a Mohs reference mineral), chemlib:hydroxylapatite (5), minecraft:quartz (7), chemlib:aluminum_oxide or MI ruby dust (corundum, 9), minecraft:diamond (10). 7 of the 10 reference minerals exist (no talc, orthoclase, topaz).
- `hv_opt_ore_hardness`: tick/info page: real Mohs of the ores the player mines (galena 2.5, bauxite 1-3, fluorite 4, wolframite ~4.5, ilmenite 5-6, uraninite 5-6, cassiterite 6-7, sperrylite 6-7) and why the game's tiers don't follow it.
- `hv_opt_gold`: golden tools are the fastest and the weakest (gold is Mohs 2.5-3; real gold is too soft to cut stone).
- `hv_opt_ma`: any MA pickaxe (note it ignores tiers) if we keep that behaviour.
- `hv_opt_twilight`: steeleaf or knightmetal pickaxe (link tf_knight_gear).
- `hv_opt_sg_tier`: an SG pickaxe with a netherite-tier head (crimson steel, azure electrum or tyrian steel): one tool, tier set by its head material.
- `hv_opt_trims`: link to completionist trims instead of duplicating.
- `hv_secret_debris` (secret): mine ancient debris with a stone pickaxe and get nothing (a tick() joke, or skip).

### 4b. Moves and links (keys stay unchanged; IDs come from the key, so moving a Q between files keeps progress)

| Existing quest | Action |
|---|---|
| tc_bronze_paxel, tc_steel_paxel, tc_diamond_paxel | duplicates of t0_opt_paxel / t1_steel_paxel / gs_opt_paxels: move them into `harvest` as the tool-row quests for tiers 2-4, or delete the tc_ copies (deleting loses progress on a few optional quests; moving is cleaner) |
| tc_osmium_paxel, tc_obsidian_paxel | move into `harvest` (tool row tiers 3 and 7) and keep a link in `tools` |
| mk2_armor_osmium, mk2_armor_obsidian, mk2_armor_glowstone | keep in mekanism, link from the armour row |
| gs_ironpick, gs_armor, gs_opt_paxels, t1_steel_paxel, t0_opt_drill, t5_opt_tools | stay on the main path; link from the spine |
| ug_forgotten_tools, ug_utherium_gear, tf_*_gear, dd_warden_tools, jdt_tools_t1..t4 | stay on their pages; link from the matching tier |
| `tools` chapter | becomes the mod-depth page (Silent Gear, Mek gear, jetpacks, comfort); rename to "Gear and Comfort" (title only) |
| t1_combiner_parts, t1_steel_paxel text | add one line each: "steel tools are diamond tier, so the steel paxel mines obsidian" |
| t2_debris | give the netherite step somewhere to go (hv_netherite depends on it) |

Token note: `harvest` is not in the TOKENS map, so it pays 1 token per quest like other side pages.

---

## 5. Gaps and decisions for the user

| Gap | Effect | Option (needs a KubeJS tag script; user call) |
|---|---|---|
| Ad Astra desh/ostrum/calorite have no tier | rocket metals mine with wood | tag desh → `needs_iron_tool`, ostrum → `needs_diamond_tool`, calorite → `neoforge:needs_netherite_tool` (common pack convention, verify ids in ids.tsv) |
| MI Ti/W/Pt/Ir/U ores are stone tier | the spine has nothing to say after iron | optional: tungsten/titanium/platinum/iridium ores → `needs_iron_tool` or `needs_diamond_tool`. Real Mohs supports "harder than iron ores" for cassiterite/sperrylite. Low risk: steel paxel (t1) is diamond tier, so this only blocks bronze-age players |
| MA tools mine everything | flattens tiers late (needs diamond pickaxe + inferium, so not early) | leave (late enough) or add `#minecraft:incorrect_for_diamond_tool` to MA inferium/prudentium tags |
| Resonarium / warden / forgotten mine everything | fine: all are post-Ancient-City or Undergarden | leave |
| No diamond pickaxe / diamond or netherite gear quests | ATM10's spine items missing from our book | covered by hv_diamond, hv_netherite |
| Silent Gear azure silver ore needs netherite tier | tc_azure players need a netherite-tier tool first | make tc_azure depend on hv_netherite, or say so in its text |
| Steel = diamond tier at T1 | obsidian before diamonds; good, but undocumented | explain it in hv_steel and t1 text |
| Gravichestplate (MI flight) not quested | late (superconductors) so effectively gated | quest it near t6/t7, or list as a flight-gate review item |

Respecting the pack's gates: the chapter grants no flight (jetpacks, Angel Ring, JDT flight stay in `tools` / `justdirethings`),
uses no ProjectE beyond a link to pe_dm_tools at the far right (oganesson-gated), and Mystical Agriculture appears only as an
optional quest.

Rough size: **~34 quests** (9 spine milestones, 9 tool-row, 8 armour-row, 8 optional), plus 5 moved tc_ paxel quests.
