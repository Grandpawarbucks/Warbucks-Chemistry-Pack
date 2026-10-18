# GTCEu Modern in four packs: research for Warbucks Chemistry

Researched 2026-10-18 from GitHub repos (file trees and raw files), the Modrinth API, the GTCEu GitHub releases, branches and issues, web search, and a `javap` check of the MI 2.5.10 jar in `test/server/mods`. No pack files were edited.

---

## 0. Compatibility check (the critical part)

### Does GTCEu Modern have a NeoForge 1.21.1 build?
Yes, but it is stale or unstable.

| Channel | Latest 1.21.1 build | Type | Date | Notes |
|---|---|---|---|---|
| Modrinth / CurseForge | **`mc1.21.1-7.0.2`** | **beta** | **2025-07-20** | Last published 1.21.1 file, about 15 months old. Built against KubeJS `2101.7.1-build.181` and Rhino `2101.2.7-build.74` (from `gradle/forge.versions.toml` at tag `v7.0.2-1.21.1`). Integrations: ae2, cctweaked, emi, jade, jei, kjs, ldlib, map, modernfix, rei, top. **No Create integration.** Required dependencies: LDLib and Configuration. |
| GitHub prerelease | **`latest-1.21` = "1.21-8.0.0 SNAPSHOT 36a6b38"** | snapshot (prerelease) | 2026-10-17 | Branch `1.21` is very active (commits daily in Oct 2026). Targets NeoForge 21.1.248, **KubeJS 2101.7.2-build.336**, Rhino 2101.2.7-build.81, **Create 6.0.10**, AE2 19.2.8, FTB Quests 2101.1.21. It has a Create integration package and **dropped LDLib for "mui" (ModularUI 3.3.1-SNAPSHOT)**. Jars are served from `maven.gtceu.com`, not Modrinth or CurseForge. |
| 1.20.1 (Forge) | 7.5.3 (beta, 2026-04-12); 8.0.0 snapshots | | | This is the main line. The default branch is still `1.20.1`. |

By comparison, the `1.21` branch is 215 commits ahead of and 831 behind `1.20.1`. The 1.21 port gets merges but lags behind.

**Stability:** the 1.21 line has never had a non-beta release. Open issues on the 1.21 line include:
- "1.21-8.0.0 SNAPSHOT not compatible with JEI" (2026-10-06)
- "JEI crash with latest 1.21 v8 snapshot" (2026-08-31)
- "[1.21.1][NeoForge] Game crashes on startup with 8.0.0-SNAPSHOT (multiple mod conflicts)" (2026-08-14)
- "1.21, KubeJS recipe id bug" (2026-05-16)
- "Custom KubeJS recipes do not retain Data Components" (2026-08-14)
- "1.21.1 NeoForge circuit settings not working"
- "Virtual programmed circuit can't be selected"
- A crash when previewing multiblock structures (missing `dimension_type` registry)

**KubeJS 7 support:** yes, in both builds. 7.0.2 was built on KubeJS 2101.7.1, and the 8.0 snapshot on 2101.7.2, the same major version as our `kubejs-neoforge-2101.7.2-build.377`. `GTCEuStartupEvents` and `GTCEuServerEvents` exist on the 1.21 branch (`integration/kjs/`). Not verified: whether 7.0.2 loads against our newer KubeJS 2101.7.2 build. It probably does, but the smoke test would tell.

**Known or likely incompatibilities with our stack**
- **Modern Industrialization overlap:** this is the big one. Both mods register full material sets (copper, tin, bronze, steel, aluminium, titanium, tungsten, platinum and so on, as dusts, plates, rods, wires and gears), both run their own EU voltage ladders (MI LV/MV/HV/EV versus GT ULV to MAX), and both have cables, ore processing, EBF, distillation, chemical reactors and oil chains. There's no GT–MI integration code. Almost Unified could unify the item tags (both use `c:` tags on 1.21), but recipe duplication, two parallel tier ladders and the separate energy networks remain. GT has a `nativeEUToFE` option, so GT machines can accept FE (every pack below enables it with ratio 4). MI's own energy uses a separate API, and I couldn't verify MI↔GT cable interop. Expect power bridging to need FE as the common currency.
- **Almost Unified:** GTCEu 1.21 has no built-in AU integration (code search found none), but AU works on tags. GT generates huge numbers of material items, so the unify config needs GT added to the priority list. Not tested.
- **Create:** 7.0.2 has no Create compat, while 8.0-SNAPSHOT targets Create 6.0.10 (our exact version). Greate (the Create↔GT bridge TFG uses) is **1.20.1 only** (0.0.82 alpha lists forge and neoforge loaders, but only for 1.20.1).
- **Mekanism:** no integration in either GTCEu build. Gas and chemical systems stay separate.
- **ChemLib/Alchemistry:** GT has its own element registry (`gtceu:<element>_dust` and so on) that would duplicate ChemLib's elements. Almost Unified can't unify those because ChemLib doesn't use `c:` material tags the same way. Not verified in detail.
- CLAUDE.md already notes that the standalone GT ore-gen mod (GTMOGS) was rejected for broken KubeJS.

### Pack versions: which ones can be adopted directly?
| Pack | MC / loader | GTCEu | Mods | Activity | Direct adoption into NeoForge 1.21.1? |
|---|---|---|---|---|---|
| TerraFirmaGreg-Modern | 1.20.1 Forge 47.4.13 | 7.5.3 (plus TFG-Core and GT addons) | ~279 projects in `pakku-lock.json` | Very active (0.13.13 released 2026-10-18; 530 stars) | No. Inspiration only (no 1.21 branch). |
| GTCP Modern | 1.20.1 Forge 47.4.10 (main); **1.21 branch: NeoForge 21.1.249** | main: 8.0.0-SNAPSHOT (1.20.1); 1.21 branch: `gtceu-1.21.1-8.0.0-…-80.jar` | 86 | Main released v1.14.5 (2026-02); **1.21 port in progress, last commit 2026-10-13 ("Fix up quests to work on 1.21", "make KJS work")** | Partly. The 1.21 branch scripts and quests are the only GT-on-1.21 reference, but the port is unreleased. |
| Star Technology | 1.20.1 Forge 47.4.20 | Own fork, `StarT-Dev-Team/GTM-StarT-Fork` (mod_version 1.7.1c) | 182 | Active (theta-2-hotfix-4, 2026-10-06) | No. 1.20.1 only, and it uses a fork. |
| Monifactory | 1.20.1 Forge 47.4.13 | 7.5.x (MoniLabs builds against 7.5.2) plus the MoniLabs core mod | 222 | Active (0.13.8, 2026-08-27; main pushed 2026-10-17; 475 stars) | No. Inspiration only (no 1.21 branch). |

**Three of the four packs are 1.20.1-only. Only GTCP has a 1.21.1 port, and it isn't released.** Their KubeJS also targets KubeJS 6 (2001.x), so even "copy the script" means porting: `forge:` tags become `c:`, and NBT becomes data components.

---

## 1. TerraFirmaGreg-Modern (TFG)
Repo: https://github.com/TerraFirmaGreg-Team/Modpack-Modern (branch `dev`). Built with pakku.

- **Concept:** TerraFirmaCraft survival (knapping, primitive metallurgy, food) leads into GregTech. It also ships Create, Greate, AE2, Ad Astra (Moon, Mars, Venus, Europa), Firmalife, CC:Tweaked and TACZ.
- **KubeJS structure:** one folder per mod for both `startup_scripts/<mod>/` and `server_scripts/<mod>/`, plus a large `tfg/` namespace. On the startup side, `tfg/materials/materials.alumina.js`, `materials.bakelite.js` and `material_modification.{colors,components,flags,ores,tools}.js` split material edits by concern, alongside `gtceu/{machines,recipe_types,tag_prefixes,modifications}.js`. On the server side are `tfg/mv_rework/`, `tfg/hv_rework/` (tier reworks), `tfg/ores_and_materials/recipes.{bromine,chromium,tungsten,zirconium,mo_si_b,gem_slurries}.js` and `tfg/powergen/{nuclear,biodiesel,early_gas,gas_burner,solar}`. Files are named `recipes.*`, `tags.*` and `data.*`.
- **gtceu.yaml:** the hardest of the four. `hardWood/Redstone/ToolArmor/Iron/Glass/AdvancedIron/Dye/harderBrick` are all true, plus `disableManualCompression: true`, `steelSteamMultiblocks: true` and `doBedrockOres: true`. EU↔FE is native at a 4:1 ratio.
- **Ore generation:** GT's vein generator is effectively replaced by **TFC `tfc:cluster_vein` datapack features filled with GT ore blocks**, with 77 Overworld veins plus per-planet folders (`kubejs/data/tfg/worldgen/configured_feature/{earth,mars,moon,venus,nether}/vein/*.json`). They're generated by a tool ("OresToFieldGuide"). Each vein is stone-type specific, for example a granite-only `deep_apatite` vein mixing apatite, tricalcium phosphate and so on. There are also fluid veins.
- **Chemistry:** real industrial chemistry. The **Bayer-style alumina line** (aluminium sulfate, aluminium hydroxide, sodium sulfate, alumina), chromium(III) oxide to ferrochrome, bromine, zirconium, tungsten, Mo-Si-B, bakelite and silicon carbide. Snippet (`kubejs/server_scripts/tfg/mv_rework/material.recipes.js`):
  ```js
  event.remove({ id: 'gtceu:electric_blast_furnace/blast_rough_silicon_carbide' })
  event.recipes.gtceu.electric_blast_furnace('tfg:rough_sic_gem')
    .itemInputs(Item.of('gtceu:quartzite_gem', 9), Item.of('gtceu:graphite_dust', 27))
    .itemOutputs(Item.of('tfg:hot_rough_silicon_carbide_ingot', 1))
    .outputFluids(Fluid.of('gtceu:carbon_monoxide', 18000))
    .blastFurnaceTemp(1760).duration(20 * 180).EUt(GTValues.VA[GTValues.MV])
  ```
  The recipe is chemically correct: SiO2 + 3C gives SiC + 2CO, and CO comes out as a byproduct.
- **Quests:** 17 FTB chapters, translated through `kubejs/assets/ftbquests/lang/*.json`. One chapter is **`chemical_elements.snbt`: about 88 item tasks, one per element** (a periodic-table collection chapter), which matches Warbucks' "build the whole periodic table" goal. TFC's own field guide covers the mechanics.
- **Other tech mods:** Create plus Greate (Create machines tiered by GT material). AE2 recipes are rewritten (`server_scripts/ae2/recipes.js`, and AE2 materials are registered as GT materials in `startup_scripts/ae2/materials.js`).
- **Pain points:** the slow TFC start (knapping, food decay) is deliberately demanding. Reviewers call it TFC plus GT, "two notoriously grindy mods", but the sentiment is mostly positive. I found no Reddit threads, so treat this as a thin signal.

## 2. GregTech Community Pack Modern (GTCP)
Repo: https://github.com/GregTechCEu/GregTech-Modern-Community-Pack (packwiz, like ours). It's the official introductory pack from the GTCEu org.

- **Concept:** a normal Overworld with GT as the only tech mod (plus AE2, storage drawers, backpacks). It's the "vanilla GTCEu" experience. 86 mods.
- **KubeJS:** small. The server side has per-mod folders (`appliedenergistics2/*.js`, which gates AE2 behind GT parts, plus `gregtech/{components,machines,greenhouse,wood_unification,void_air}.js`, `tags/`, `vanilla/`). The startup side is tiny (`components/hsla-steel.js`, `dimension_markers.js`).
- **gtceu.yaml:** mostly defaults with `harderRods`, `hardIron` and `hardGlass` turned on. GT ore veins (`oreVeinGridSize: 3`, `removeVanillaOreGen: true`, `oreIndicators: true`), `enableFEConverters: false` (native EU↔FE at 4:1 instead), and cleanroom, research and maintenance all on.
- **Quests:** one chapter per voltage tier (`steam_age`, `lv__low_voltage` through `zpm__zero_point_module`) plus topic chapters (`ore_generation`, `ore_processing`, `heating_coils`, `multiblock_dilemma`, `renewability_and_you`, `tips_and_tricks_2`). Reward tables are tied to chemistry milestones: `polyethylene`, `gallium_arsenide`, `platinum_group_processing`, `titanium`, `distillation_tower`.
- **1.21 branch:** NeoForge 21.1.249 with the GTCEu 1.21.1 8.0.0 snapshot. The commit "make KJS work" mostly migrates tags from `#forge:` to `#c:` and renames ids (`expatternprovider` to `extendedae`). It's the best public reference for GTCEu-on-1.21 KubeJS.
- **Code pattern** (AE2 or another mod gated by GT tier parts, `kubejs/server_scripts/gregtech/machines.js`):
  ```js
  event.shaped("gtceu:greenhouse", ["GGG", "CHC", "PUP"], {
    G: "gtceu:tempered_glass", C: "#gtceu:circuits/mv",
    H: "gtceu:mv_machine_hull", P: "gtceu:mv_electric_piston", U: "gtceu:mv_electric_pump" });
  ```

## 3. Star Technology (StarT)
Repo: https://github.com/StarT-Dev-Team/Star-Technology. Wiki: https://StarT-Dev-Team.github.io/StarT-Wiki/

- **Concept:** a GT skyblock. You start with Ex Nihilo, move to void miners and oil rigs, and the end goal is stargates. It's playable to mid-UIV. "Not beginner-friendly." Two packmodes (Hardmode, Abydos Start). 182 mods. It uses a **GTCEu fork** (`GTM-StarT-Fork`).
- **KubeJS structure:** the most organized of the four, with a README in each folder.
  - `startup_scripts/elements_materials/elements/{abydos,end,nether,nuclear,…}.js` add custom elements.
  - `material/lines/*.js` holds about 30 chemistry lines, one file per line: bromine, crown ethers, deionized water, xenotime (rare earths), zirconium, PEEK, polyimide, polycarbonate, PEDOT:PSS, perfluoroelastomer, aerogel and others.
  - `machines/multiblocks/…` registers multiblocks.
  - The server side has `systems/` (fission, fusion, research, ore_factory_processing, resource_gen/{seawater, hydrocarbons, latex, exotic_gas_siphon, void_drill_line}), `additions/progression/{early_game, circuitry, components, lines}`, `modifications/<mod>.js` (AE2, Create, Thermal, LaserIO and others re-gated) and `mass_removals.js`.
- **gtceu.yaml:** `hardIron` and `hardGlass` on, GT veins, FE converters on, world accelerators off.
- **Code pattern worth copying:** a helper DSL that reduces each material to one line. `startup_scripts/elements_materials/material/helpers.js` defines `ICONSETS` and `FLAGS` maps plus a `global.materialHelpers(event)`, so each line file reads like this (`lines/xenotime_line.js`):
  ```js
  GTCEuStartupEvents.registry('gtceu:material', (event) => {
    const MH = global.materialHelpers(event);
    const { noDecomp } = FLAGS;
    MH.compLiquid('rare_earth_sulfate_solution', ['2x mystery', '3x sulfate'], 0xc6c2a8, [noDecomp]);
    MH.compDust('rich_rare_earth', ['1x mystery'], 0xb5ac90, [noDecomp]);
  });
  ```
- **Quests:** 24 chapters, staged by age (`early_game`, `industrial_revolution`, `automation_age`, `draconic_age_part_1`) with a `line_of_progression`, `pl1`–`pl5` and a `shop`.
- **Pain points:** deep post-UHV content, a skyblock start, and a reputation for heavy grind. I found only one 5-star review, so the signal is thin.

## 4. Monifactory
Repo: https://github.com/Omicron-Industries/Monifactory. Core mod: https://github.com/Omicron-Industries/MoniLabs

- **Concept:** a remaster of Nomifactory CEu on GTCEu Modern. Three packmodes (Normal, Hard, Expert). Ores come from processing and miners rather than worldgen (Nomi heritage: no structures, see `fixes_tweaks/no_structures.js`), with GT ore veins defined for Ad Astra planets. 222 mods. Mods like AE2, EnderIO, Thermal, Extended Crafting, HNN and PackagedAuto are all re-gated with GT parts. **CLAUDE.md says Warbucks already borrowed HNN, Extended Crafting, PackagedAuto and others from Moni.**
- **KubeJS structure:**
  - `startup_scripts/gregtech_material_registry/chemline_*.js` holds one file per chemistry line: `chemline_harder_platinum_group`, `chemline_harder_naquadah`, `chemline_rare_earth`, `chemline_germanium`, `chemline_peek`, `chemline_kapton_k`, `chemline_naqfuel`.
  - Elsewhere on the startup side: `registry/{multiblock,singleblock,item,fluid,block}_registry.js`, `worldgen/oreVeins.js` and `oreVeinsRemoval.js`, `gregtech_crafting_components.js`, and `nukeLists/` (mass item hiding and removal).
  - The server side has `gregtech/*.js` (rare_earth, germanium, circuits, solder, energy_cores, …), `mods/*.js` (per-mod gating), `mods/optionalCompats/*.js` (guarded by `Platform.isLoaded`) and `_hardmode/platline.js`.
- **Packmode pattern** (`startup_scripts/_packmode.js`): it reads `config/packmode.json` with `JsonIO` and exposes feature booleans instead of mode checks:
  ```js
  global.doHarderProcessing = packMode == "Hard" || packMode == "Expert";
  global.doConverters = packMode == "Normal" || packMode == "Hard";
  global.doHNN = packMode == "Normal";
  ...
  const doHarderProcessing = !!global.doHarderProcessing;
  ```
  Each chemistry line is then wrapped in `if (doHarderProcessing) { ... }`. Normal mode keeps GT's short default platinum line, and Hard mode swaps in "an abbreviated version of NH's platline". **This maps directly onto Warbucks' "no long grinds" goal: one config file, with an optional harder line for players who want it.**
- **Chemistry snippet** (`server_scripts/gregtech/rare_earth.js`, "Line for rare earths with actual chemistry"):
  ```js
  event.recipes.gtceu.mixer("re_digestion_mixer")
    .itemInputs("1x gtceu:rare_earth_dust").inputFluids("gtceu:sulfuric_acid 250")
    .outputFluids("gtceu:rare_earth_sulfate_solution 1000")
    .duration(120).EUt(GTValues.VA[GTValues.EV])
  event.recipes.gtceu.centrifuge("rare_earth_mass_separation")
    .itemInputs("4x gtceu:oxidized_re_sludge_dust").inputFluids("gtceu:nitric_acid 1000")
    .outputFluids("gtceu:light_rare_earths 600", "gtceu:heavy_rare_earths 500", "gtceu:oxalic_acid_solution 750")
  ```
  The sulfuric acid digestion step, oxalate precipitation and nitric acid split, with oxalic acid returned as a recycled reagent, make a short, real chemistry loop. Moni's PGM materials also carry real formulas (`.formula("(NH4)2PtCl6")`).
- **Create** (`mods/optionalCompats/create.js`): it **removes Create's processing** (milling, crushing, mixer, press, deploying recipes and the hand crank) so Create is only "for fun, not functionality". That's the opposite of Warbucks' choice to make Create the early tier.
- **gtceu.yaml:** only `hardIron` on (plus `hardGlass` in Hard mode), so it's the lightest. FE converters are on in Normal and Hard, and Expert disables RF→EU.
- **Quests:** 17 chapters (genesis, groundwork, feeding_the_machine, dependency_chain, some_assembly_required, scaling_up, into_the_microverse, …), with lang in `kubejs/assets/ftbquests/lang`. Monicoins act as a quest currency in Normal mode, like Warbucks' Demigod Token shop.
- **Complaints:** a ModDex reviewer said every inconvenience you overcome is "just replaced with a new one". Nomi-lineage packs are generally rated less grindy than GT:NH or TFG.

---

## 5. Cross-pack observations

**Shared integration recipe**
1. Startup: register GT materials (`GTCEuStartupEvents.registry('gtceu:material')`), with one file per chemistry line and `DISABLE_DECOMPOSITION` on intermediates.
2. Startup: register custom recipe types and multiblocks (`'gtceu:recipe_type'` and `'gtceu:machine'`, using `FactoryBlockPattern`).
3. Startup: register world-gen layers and tag prefixes for new dimensions.
4. Server: `event.remove({id})` the default GT recipe, then rebuild it with `event.recipes.gtceu.<type>(id)`.
5. Server: per-mod gating files that replace other mods' key recipes with GT hulls, circuits and plates.
6. Bulk hide and remove lists.

**Common gtceu.yaml choices**
All four use native EU↔FE at 4:1, remove vanilla ores in favor of GT veins (TFG uses TFC veins instead), leave cleanroom, research and maintenance on, enable `hardIronRecipes`, and enable `removeSmeltingForEBFMetals`.

**GT pain points to avoid** (general GT community knowledge plus the reviews above; not separately sourced)
- Circuit and component chains: each tier needs new circuit boards, SMDs and wafers.
- Maintenance hatches and cleanroom chores.
- EBF coil temperature gates combined with long blast times.
- Hunting for ore veins.
- Assembly-line research.
- Huge material item counts, which bloat JEI.
- The "every solution creates a new problem" loop.

**Ideas that fit a chemistry-first, low-grind pack**
- A **periodic-table quest chapter** (TFG `chemical_elements.snbt`). Warbucks has Alchemistry, so this suits it naturally.
- **Byproduct and reagent recycling loops** (Moni rare earth returns oxalic acid; TFG's SiC recipe outputs CO). Warbucks' `phase4_chemistry.js` already has byproducts, Haber/Ostwald and a PGM line.
- **One file per chemistry line** with a header comment explaining the real chemistry (Moni `chemline_*.js`, StarT `material/lines/*.js`).
- **Feature-flag packmode** (Moni `_packmode.js`): a normal short line plus an opt-in "expert" line, all from one JSON config.
- **Material helper DSL** (StarT `helpers.js`) to keep registration terse.
- **Reward tables tied to chemistry milestones** (GTCP: polyethylene, GaAs, PGM, titanium).
- **Gate other mods with tier components** (all four). Warbucks already does this with MI circuits.
- **Planet-specific ores and resources** (Moni `oreVeins.js` world-gen layers for Ad Astra; TFG per-planet veins). Warbucks has Ad Astra.

---

## 6. Recommendation

### Option A (recommended): keep MI, borrow GT design through KubeJS
MI 2.5.10 already ships a full KubeJS 7 API, confirmed with `javap` on our jar:
- `MIMachineEvents.{registerRecipeTypes, registerCasings, registerMachines, registerHatches, addMultiblockSlots, addEbfTiers}`
- `MIMaterialEvents.{addMaterials, modifyMaterial}`
- `MIRecipeEvents.customCondition`
- `MIRegistrationEvents.{registerCableTiers, registerFluids, registerFluidNeutronInteractions}`

`RegisterMachinesEventJS` exposes `craftingSingleBlock`, `simpleElectricCraftingMultiBlock`, `simpleSteamCraftingMultiBlock`, `simpleGeneratorSingleBlock` and `simpleGeneratorMultiBlock`. That covers the GT-style building blocks: custom chemical multiblocks such as a "Leaching Vat" or "Solvent Extraction Column", custom recipe types, new EBF coil tiers and new fluids.

- **What to port as ideas:**
  - Moni's rare-earth and PGM lines as short MI and Mekanism chemical-reactor chains with recycled reagents.
  - TFG's Bayer alumina and SiC.
  - StarT's polymer lines (PEEK, polyimide, polycarbonate) as advanced-material gates.
  - A periodic-table chapter.
  - A packmode flag for optional harder lines.
  - A helper DSL for ChemLib, MI and KubeJS registration.
- **Effort:** low to medium, done incrementally inside the existing Phase 4 pattern.
- **Risk:** low. No new mod, and no MC or loader change.
- **Tradeoff:** no GT machine tiers, covers, EU cables or ULV→UHV ladder. You get GT's ideas, not its look.

### Option B: add GTCEu Modern on 1.21.1
- **B1 (alongside MI):** not recommended. You'd get two full material systems, two EU ladders, duplicate EBFs, chemical reactors, distillation and ore processing, plus Mekanism, Create and Alchemistry on top. That breaks the "one backbone per system" pillar and adds thousands of items. Expect Almost Unified pain, ChemLib element duplication and power-bridging problems.
- **B2 (replacing MI):** coherent in principle, but it means a near-total redo of Phases 3–5: MI circuit gates in flight, Create and Monifactory scripts, about 1,168 quests, and the MI-based progression in PROGRESSION.md.
- **Version risk:** the only releases are 7.0.2 beta (July 2025, stale, no Create compat, LDLib UI) or unreleased 8.0.0 snapshots from `maven.gtceu.com` (not on Modrinth or CurseForge, so packwiz would need a URL-type entry; JEI-crash issues open; the API is still changing with the move to ModularUI).
- **Effort:** very high. **Risk:** high.
- **Revisit if** a stable GTCEu 8.x for 1.21.1 lands on Modrinth or CurseForge and GTCP's 1.21 branch ships, which would prove the stack.

### Option C: middle grounds
- **C1:** prototype GTCEu 8.0-SNAPSHOT in a throwaway Prism instance with only our core mods, to measure the overlap with MI and Mekanism before deciding anything. It takes about half a day and the results are informative.
- **C2:** keep MI and use the GTCP 1.21 branch and the Moni and StarT repos purely as a recipe and quest-structure reference library (this is Option A plus a reading list).
- **C3:** GT-style ore veins for Warbucks: already handled by `tools/build_deposits.py`. GTMOGS was rejected, so don't revisit it.

### Couldn't verify
- Whether GTCEu 7.0.2 loads against KubeJS 2101.7.2-build.377 (built on 2101.7.1).
- Whether MI and GT energy and cables interoperate on 1.21.1.
- Almost Unified behavior with GTCEu 1.21.
- Monifactory's exact GTCEu file version (CurseForge file ID 7917773 is in the manifest; MoniLabs builds against 7.5.2).
- Monifactory's void or skyblock start (inferred from its Nomi heritage and `no_structures.js`).
- Player grind sentiment: there are few reviews and no Reddit threads came up in search. The GT pain-points list is general community knowledge.
- CurseForge mod counts or download stats; the counts above come from repo manifests and lockfiles.

### Sources
- https://github.com/GregTechCEu/GregTech-Modern (branches `1.21` and `1.20.1`, releases `latest-1.21` and `v7.0.2-1.21.1`, `gradle/forge.versions.toml`, issues)
- https://modrinth.com/mod/gregtechceu-modern (API: version list)
- https://github.com/TerraFirmaGreg-Team/Modpack-Modern
- https://github.com/GregTechCEu/GregTech-Modern-Community-Pack (`main` and `1.21` branches)
- https://github.com/StarT-Dev-Team/Star-Technology and https://github.com/StarT-Dev-Team/GTM-StarT-Fork
- https://github.com/Omicron-Industries/Monifactory and https://github.com/Omicron-Industries/MoniLabs
- https://moddex.gg/modpack/monifactory, https://mmcreviews.com/all/modpacks/terrafirmagreg, https://moddex.gg/modpack/star-technology
- `test/server/mods/Modern-Industrialization-2.5.10.jar` (`javap` of `aztech.modern_industrialization.compat.kubejs.*`)
