# Allthemodium + "the ATM family": research and fit (2026-10-19)

User request: "add all the modium and the mining dimension etc to the pack."
Sources: CurseForge (via packwiz in a scratch pack, and the CF site API), the Modrinth API, and the jars
`allthemodium-3.0.1_mc_1.21.1.jar` (ATM10 instance) and `allthemodium-3.2.1_mc_1.21.1.jar` (latest, pulled by
packwiz into a scratch pack). Everything below was read from these jars (data files and `javap` of the classes) unless it is marked *unverified*.

## 1. Availability (verified)

| Mod | Latest NeoForge 1.21.1 | Source | License | Third-party download | Required deps |
|---|---|---|---|---|---|
| **Allthemodium** | **3.2.1**, 2026-10-12 (CF file 9143638, project 364466) | **CurseForge** | All Rights Reserved | **Allowed**: `packwiz modrinth export` fetched it through the CF API, so it is not a manual download | NeoForge >= 21.1.195, **GeckoLib >= 4.7.5.1** (we ship 4.9.3). Lootr is optional (we ship it). CF also lists ATO as a dependency, but the jar's `neoforge.mods.toml` does **not** require it (see section 3). |
| AllTheOres (ATO) | 3.2.0, 2026-03-27 (CF 405593) | CurseForge | ARR | Allowed (same test) | none |
| AllTheCompressed | 4.4.0, 2025-12-21 (CF 514045) | CurseForge | MIT | Allowed (same test) | none |
| AllTheTweaks (ATM Star items) | 2.10.0 in ATM10 | not found by slug on CF/Modrinth (not checked further) | ARR | — | — |

**Modrinth warning:** `https://api.modrinth.com/v2/project/allthemodium` exists, but it is **not official**. It was
published 2026-08-19 by the user `jpaulmasonry` with no organization, its license is ARR, and it is the byte-identical
ATM10 3.0.1 jar (sha1 `1abb27a2…`) tagged with false versions (1.20.1, 26.x, Forge). It looks like an unauthorized
re-upload of an ARR mod. **Do not use it.** Use CurseForge (`packwiz curseforge add allthemodium`, answer **no** to the
ATO dependency prompt). On Modrinth, `all-the-ores` is a different MIT mod (recipes for vanilla ores), not ATO.

## 2. What Allthemodium adds (from the 3.2.1 jar)

### Ores
| Ore (block id) | Where it generates | Placement | Harvest tier (tag) |
|---|---|---|---|
| `allthemodium:allthemodium_ore` / `allthemodium_slate_ore` | Overworld **Deep Dark** biome only, Y bottom..10 on cave **ceilings**; The Other (all its biomes); Mining dim Y65-129 (1 vein/chunk, size 4) | `placed_feature/allthemodium_ore.json`, `allthemodium_mining.json` | `#neoforge:needs_netherite_tool` |
| `allthemodium:vibranium_ore` / `other_vibranium_ore` | **Nether** (all biomes) Y64-127 on ceilings, 10 tries/chunk; The Other | `vibranium_ore.json`, `other_vibranium_ore.json` | `#c:needs_allthemodium_tool` |
| `allthemodium:unobtainium_ore` | **End highlands** biome, Y0-128 on floors, 3 tries/chunk | `unobtainium_ore.json` | `#c:needs_vibranium_tool` |

The mod ships `c:incorrect_for_{allthemodium,vibranium,unobtainium,allthemodiumalloy}_tool` tags, so the ladder is
netherite pick -> ATM ore -> ATM pick -> vibranium -> vibranium pick -> unobtainium. Ancient stone bricks and the three
alloy blocks need an unobtainium tool.
Anti-automation: `events/BlockBreak` cancels the break of any ATM/vibranium/unobtainium ore by a **FakePlayer** or an
empty hand and sets the block to air. Quarries and miners destroy it, so it has to be mined by hand. Blocks in The Other's
structures (`OTHER_PROTECTION` tag) can't be broken in Other biomes.

### Dimensions and travel
| Dimension | Generator | Reached by | Contents |
|---|---|---|---|
| `allthemodium:mining` | Flat layers (`dimension/mining.json`): bedrock -64, end stone -63..0, netherrack 1..64, deepslate 65..128, stone 129..247, dirt, grass 252. Has a sky, beds work, mobs spawn at light 0 | Teleport Pad placed in the **Overworld** | Dense vanilla ores via `biome_modifier/allthemodium/dim_ores/*`: iron upper **90 tries/chunk** + 10 middle, **emerald 100**, diamond_large 6, gold 4, redstone 4, **ancient debris 4 veins x5 in the netherrack layer**, ATM ore 1. If ATO is installed, also ATO's aluminium, lead, nickel, osmium, platinum, iridium, silver, tin, uranium, zinc, ruby, sapphire and peridot (conditional modifiers). |
| `allthemodium:the_other` | Noise, Nether-like biomes (soul sand valley, crimson/warped forest, desert(s), the_other), fixed night | Teleport Pad placed in the **Nether** | ATM + vibranium ore, ancient/demonic/soul trees, structures: Ancient Pyramid (soul sand valley, with a **Piglich** that drops `piglich_heart`), Dungeon (warped forest), Piglin Village |
| `allthemodium:the_beyond` | Noise, single biome, no features | Teleport Pad placed in the **End** | Empty (a void/build world) |

**Teleport Pad** (`allthemodium:teleport_pad`): recipe = 1 ender pearl + 4 `#c:nuggets/allthemodium` (plus shape).
Use it with sneak + right-click and both hands empty. Partners are hard-coded in `blocks/TeleportPad` (`DEFAULT_PARTNERS`):
Overworld<->Mining, Nether<->The Other, End<->The Beyond. The return pad is spawned automatically and doesn't drop.
There is **no portal** and **no config file** (the jar has no config class). The only override hooks are AllTheTweaks
packmode entries for AoA dimensions.
**The Mining dimension does not reset itself.** ATM servers reset it by deleting the dimension folder, which the mod
does nothing to support.

### Gear, alloys, misc (ids)
- Metals: `allthemodium:{allthemodium,vibranium,unobtainium}_{ingot,nugget,dust,plate,gear,rod,block}`, `raw_*`,
  `crushed_*`, plus Mekanism-chain items (`*_clump/shard/crystal/dirty_dust`, slurries). The mod's own recipes give
  Mekanism **2x (enriching) up to 5x (slurry)**, but the **furnace and blast furnace also smelt raw ore/ore/dust directly**
  (`*_ingot_from_{raw,ore,dust}_{smelting,blasting}.json`).
- Alloys: `vibranium_allthemodium_alloy_*`, `unobtainium_allthemodium_alloy_*`, `unobtainium_vibranium_alloy_*`
  (ingot, dust, block). **Without Tinkers there is no recipe that makes them.** The only recipes are `tconstruct:alloy`
  and casting with a piglich heart. ATM10 makes them with its own (ARR) KubeJS Powah energizing recipes
  (`kubejs/server_scripts/modpack/atm_alloys.js`; don't copy). The alloy tools (`alloy_pick/axe/shovel/sword/paxel`,
  `alloy_trident`) have no recipe either.
- Tools/armour: `{allthemodium,vibranium,unobtainium}_{pickaxe,axe,shovel,hoe,sword,mace,helmet,chestplate,leggings,boots}`
  by **smithing**: netherite -> ATM -> vibranium -> unobtainium. Each step needs `*_upgrade_smithing_template`. Templates
  come from archaeology loot (`loot_table/arch*.json`, `chest/template.json`, in The Other's structures) and are duplicated
  vanilla-style. 3.2.1 adds `*_brush`. Also `allthemodium_apple`/`carrot` (8 nuggets + food).
- **Armour effects** (`events/ArmorEvents`): boots cancel fall damage; chestplate multiplies **magic** damage by
  0.5/0.25/0.1; helmet refills air; it also clears fire. **No flight, no step-assist, no creative abilities**, so it is
  safe for our flight gating.

## 3. The "etc": ATM family

| Mod | What it adds | Fit | Verdict |
|---|---|---|---|
| **AllTheOres** | ~20 metals/gems (Al, Pb, Ni, Os, Pt, Ir, Ag, Sn, U, Zn, ruby, sapphire, peridot, cinnabar, fluorite, salt, sulfur) with ore gen in the Overworld, Nether, End and The Other (`biome_modifier/*_{overworld,nether,end}.json`), plus ore hammers and alloy recipes | Duplicates MI/Mekanism ores, **breaks the ore-deposit design** (scattered ore everywhere), adds hundreds of items for Almost Unified, and every overworld modifier would need a datapack override | **Skip.** Allthemodium only uses it through conditional `dim_ores` modifiers and 5 hammer recipes (dead without it, harmless) |
| AllTheCompressed | 1x-9x compressed blocks (stone, logs, metals, ATM blocks) | Pure storage/grind convenience; AE2 covers storage; it would add dissolver coverage work | Skip (optional later) |
| AllTheTweaks | ATM Star / shards / GregStar / Patrick Star items, mini portals, packmode, Discord RPC. The **recipes for the Star chain live in ATM10's ARR KubeJS** | Its endgame competes with our **Seed of a New World**; we couldn't reuse ATM10's recipes anyway | **Skip** |
| ATM gear (Arcanist/Wizard gear), ATM: Compat | Armour for Ars/Iron's; compat recipes | Not needed | Skip |

## 4. Fit with our design

### Where the metals sit (proposal)
| Metal | Found | Tier slot | Why |
|---|---|---|---|
| Allthemodium | Deep Dark ceilings (Y<10), The Other | **T3 (LV->MV)**, next to the Undergarden | Needs a netherite pick (T2) and exploring the Deep Dark/Ancient City. Refining goes through the T3 acid line |
| Vibranium | Nether ceilings Y64-127, The Other | **T4/T5** | Needs ATM tools. Its alloy with ATM is a T5 refractory alloy |
| Unobtainium | End highlands | **T5/T6** | Needs vibranium tools + End access. Its alloys are T6 gear, **not** part of the Seed |

These are fictional metals: ChemLib has no element for them, so the Combiner can't synthesize them and they stay
exploration-locked. Leave them out of the dissolver (`tools/build_dissolver.py` will just list them as uncovered).

### Conflicts and checks
| Area | Finding | Action |
|---|---|---|
| Ore deposits (`tools/build_deposits.py`) | Our MI deposit modifiers target `#minecraft:is_overworld`; `allthemodium:mining` is not in it, so no MI ore spawns there. But the Mining dim's own vanilla ores are **far richer than our overworld** (iron 100 tries/chunk, emerald 100, **ancient debris 4 veins/chunk**). That would trivialize iron, diamonds and **netherite** | Override `data/allthemodium/neoforge/biome_modifier/allthemodium/dim_ores/{iron,emerald,netherite,diamond,gold,redstone,lapis,coal,copper,quartz}.json` with `{"type":"neoforge:none"}` (KubeJS data folder; file names are lowercase). Optionally add our own scattered-ore modifiers at overworld density (35%) for `allthemodium:mining` |
| Harvest tiers (`phase5_harvest_tiers.js`) | ATM tags itself; netherite tier for ATM ore is consistent (Calorite is also netherite). No edits needed | Nothing, unless the quest wants ATM tools to gate Venus |
| Almost Unified | ATM metals are unique (no MI/Mek duplicates). Without ATO there's nothing to unify | Nothing |
| ProjectE lite | `custom_emc.json` already zeros `c:ingots`, `c:ores`, `c:raw_materials`, `c:nuggets`, `c:dusts`, `c:storage_blocks` | Re-run `test/emc_check.sh`, and add `allthemodium:piglich_heart` and the alloy ingots by id if they show EMC |
| Flight | ATM armour has no flight (bytecode checked) | Nothing |
| Direct smelting | Raw/ore/dust -> ingot in a furnace skips chemistry | Remove the 18 `*_ingot_from_{raw,ore,dust}_{smelting,blasting}` recipes; allow MI EBF and the Mekanism chain |
| Automation | Ores vanish when a FakePlayer breaks them (by design) | Mention it in the quest text; Ultimine works (real player) |
| Iron Furnaces (in pack) | Has allthemodium/vibranium/unobtainium furnaces that may unlock once the tags exist (*unverified*) | Check in JEI. They're fine as late-tier smelting speed |
| Mining dim as an ore farm | No reset mechanism | Optional: a VPS script that deletes `world/dimensions/allthemodium/mining` on a monthly restart (players must be warned) |

### Proposed KubeJS gates (new `phase5_allthemodium.js`)
1. **Refining is chemistry.** Remove direct smelting/blasting. Allthemodium: raw -> MI **Electric Blast Furnace**
   (cupronickel coil tier) 1:1, or the Mekanism chain (2-5x, already in the mod, so it rewards the T3 acids).
   Vibranium: EBF at the kanthal coil tier, and its MI Chemical Reactor leach uses **HF** (T5 intermediate). Unobtainium: EBF at the top coil.
2. **Alloys are reactions** (they don't exist without our recipes): MI Mixer `atm dust + vibranium dust + piglich_heart`
   -> `vibranium_allthemodium_alloy_dust` -> EBF -> ingot (T5). UA/UV alloys: the same pattern plus an **antimatter**
   or plutonium input (T6). The alloy tools/paxel can either get recipes or be hidden in JEI.
3. **Teleport pad**: replace the recipe with ender pearl + 2 `allthemodium_plate` + MI **analog circuit** (T3), so
   The Other opens with the Undergarden. Decide on the Overworld->Mining use (block it or keep it) based on section 4's neutered ores.
4. **Templates**: keep them as loot (exploration). No change.

### Quests
A side chapter "Metals of Legend" (about 15 quests, `world` group): Deep Dark ATM ore -> EBF ingot -> teleport pad ->
The Other (pyramid, Piglich) -> vibranium (Nether ceilings) -> ATM/vibranium armour -> unobtainium (End) -> alloys.
None of it is required for the Seed, so it adds content, not grind.

### Mod count
**+1** (Allthemodium; GeckoLib and Lootr are already in) -> **223**. It would be +2 with ATO, +3 with AllTheCompressed.

## 5. Recommendation
Add **Allthemodium 3.2.1 from CurseForge only**: decline ATO, and skip AllTheCompressed, AllTheTweaks and the ATM Star.
Use it as an optional exploration-and-gear side line (T3->T6). Gate refining, alloys and the teleport pad through
chemistry with the KubeJS above. Ship the Mining dimension **with its dense vanilla ore modifiers turned off**, so it is
a flat, safe quarry/build world with 1 ATM vein per chunk, not an ore farm that bypasses deposits and netherite.
After adding it: run a smoke test (the mods.toml says ATO isn't needed, but it needs a runtime check), the worldgen
scan, `emc_check`, JEI checks (Iron Furnaces ATM furnaces, alloy recipes), `build_dissolver.py`, and a modlist-meta row.
