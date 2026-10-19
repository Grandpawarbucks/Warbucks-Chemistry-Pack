# Chemistry-per-tier audit (2026-10-18)

Question: "Have we made sure that we have recipes using chemicals that make sense for the tier?"

Short answer: **mostly yes for the MI spine (LV → IV), no for three leaks.** MI's own ladder is very chemical
(rubber, silicon, aluminium, polyethylene, PVC, platinum, plutonium). The pack's own lines (Bayer/Hall-Héroult,
Haber/Ostwald/PGM) sit at the right tiers and are chemically sound. But (1) the Alchemistry route skips the
aluminium line entirely, (2) oganesson (the "complete periodic table" key for ProjectE and the Seed) comes from
dragon's breath in the T1 Dissolver, and (3) several design gates (T1 "first compound", T3 "H₂SO₄ in volume",
T6 "rocket fuel") are not actually enforced by any recipe.

Method: recipe JSONs extracted from the jars in `test/server/mods` (MI 2.5.10, Mekanism 10.7.19 + Generators,
Alchemistry 2.4.5, ChemLib 2.1.5, AE2, Ad Astra, EI, IO) plus every file in `pack/kubejs/server_scripts` and
`startup_scripts`. Tier of a machine = the circuit/hull in its crafting recipe. Design tiers are PROGRESSION.md's
T0-T6; quest chapter = design tier + 1 (t4 = T3). Not verified in-game: MI coil EU limits (cupronickel 32 / kanthal
128 EU/t) and single-block machine base EU (taken from MI docs) — check JEI.

## 1. Machine tiers that decide everything

| Machine | Crafting needs | Tier |
|---|---|---|
| MI Coke Oven, Steam Blast Furnace, bronze Mixer | fire clay / bronze | T1 steam |
| MI Mixer, Assembler, EBF (cupronickel) | `basic_machine_hull` + analog circuit | LV |
| MI Electrolyzer, Chemical Reactor, Centrifuge, Distillery | basic hull + **electronic circuit** (`…/electric_age/machine/*_asbl.json`) | **MV** (needs Al + Si) |
| MI Vacuum Freezer, Oil Drilling Rig | advanced hull | MV |
| MI Distillation Tower, Pressurizer | turbo hull + digital circuit | HV |
| MI Nuclear Reactor | highly advanced hull + processing unit | EV |
| Mek Electrolytic Separator, Gas-Burning Gen | infused alloy, electrolytic core, **no circuit** | T1/T2 (needs FE) |
| Mek Chemical Oxidizer, Infuser, Rotary Condensentrator, PRC, Enrichment, Crusher | `c:circuits/basic` = MI analog + osmium | LV |
| Mek Injection, Dissolution, Washer, Crystallizer | lowered to advanced circuit (`phase5_balance.js`) | MV |
| Mek SNA, Fission ports/control rods | elite circuit (MI digital) | HV |
| Mek Isotopic Centrifuge, SPS port, Nucleosynthesizer | ultimate circuit (MI processing unit) | EV |
| Alchemistry Dissolver / Combiner | steel plate + bronze casing (`kubejs:phase4/alchemistry/*`) | T1 |
| Alchemistry Fission / Fusion controllers | MI processing unit | EV |

## 2. First available: each gating chemical

| Chemical | Earliest route (machine, tier) | Source recipe |
|---|---|---|
| Coke (+ creosote 50%) | MI Coke Oven, T1 steam | `modern_industrialization:materials/coke_oven/coke` |
| Rubber sheet | coke dust + water → raw synthetic oil (Mixer) → synthetic oil (Blast Furnace, 2 EU) → + paper (Mixer); T1 steam. Sulfur-vulcanised route `materials/mixer/oil_to_rubber` | `materials/mixer/coke_to_raw_oil`, `oil_to_rubber_sheet` |
| Steel | Mixer 7 iron + 2 coke dust → uncooked steel → Blast Furnace; T1 | `materials/mixer/uncooked_steel_dust`, `blast_furnace/steel` |
| H₂ / O₂ | Alchemistry Dissolver items (T1); Mek Electrolytic Separator gas (T1/T2, no circuit); MI fluid only from Electrolyzer (**MV**) | `mekanism:separator/water`, `mi:…/electrolyzer/water` |
| N₂ | MI Vacuum Freezer liquid air → Centrifuge; **MV** | `materials/vacuum_freezer/liquid_air`, `centrifuge/liquid_air` |
| Cl₂ | Mek brine (Oxidizer, salt) → Separator; LV. MI: Electrolyzer salt, MV | `mekanism:separator/brine`, `mi:…/salt_electrolysis` |
| HCl | Mek Chemical Infuser (H₂ + Cl₂), LV. MI Chemical Reactor, MV | `mekanism:chemical_infusing/hydrogen_chloride`, `mi:…/chemical_reactor/hydrochloric_acid` |
| SO₂ / SO₃ / H₂SO₄ | Mek Oxidizer + Infuser + Rotary (water vapour), **LV**. MI Chemical Reactor, MV. ChemLib Combiner item (T1) | `mekanism:oxidizing/sulfur_dioxide`, `chemical_infusing/sulfur_trioxide`, `/sulfuric_acid` |
| NaOH | Combiner `chemlib:sodium_hydroxide` (T1) → lye in LV Mixer (`kubejs:aluminum/lye`); MI Chemical Reactor, MV | `alchemistry:combiner/sodium_hydroxide` |
| Sodium aluminate, Al(OH)₃, alumina | LV Mixer ×2, LV EBF calcination | `kubejs:aluminum/digestion`, `/precipitation`, `/calcination` |
| Aluminium ingot (intended) | Hall-Héroult Cell, LV | `kubejs:aluminum/electrolysis` |
| Aluminium ingot (**actual earliest**) | Dissolver obsidian → 8 `chemlib:aluminum_oxide` → cell (LV) or → Al → Compactor → furnace (**T1**) | see §4 #1 |
| Silicon | MI EBF quartz + coke, LV (32 EU). AE2 silicon: furnace (T0) or Mek Crusher on **sand** (LV) | `materials/blast_furnace/silicium_from_quartz`, `ae2:smelting/silicon_from_certus_quartz_dust`, `mekanism:compat/ae2/sand_to_silicon` |
| Fluorite (gem/dust) | Mek ore → Enrichment (6 gems) / Crusher; LV | `mekanism:processing/fluorite/*` |
| NH₃, HNO₃, NH₄Cl, aqua regia | MI Chemical Reactor; MV (N₂ needs Vacuum Freezer) | `kubejs:chem/haber_bosch`, `/ostwald`, `/ammonium_chloride`, `/pgm/aqua_regia` |
| Ethylene | MI Distillery on steam-cracked naphtha (crude from MV drilling rig), or ethanol + S; MV. Mek bio-ethene (PRC) LV | `petrochem/distillation/steam_cracked_naphtha_2`, `oil/chemical_reactor/ethanol_to_ethylene` |
| Polyethylene | MI Chemical Reactor + Cr or Pb tiny dust; MV (feeds HV board) | `petrochem/polymerization/ethylene_*` |
| Benzene / toluene | MI Distillery; MV | `steam_cracked_naphtha_5/6` |
| PVC | acetylene (EBF from methane, or Distillery) + HCl → vinyl chloride → polymerise; MV (feeds EV board) | `oil/chemical_reactor/vinyl_chloride`, `polymerization/vinyl_chloride_*` |
| SBR rubber | Vacuum Freezer 128 EU; MV+ | `oil/vacuum_freezer/styrene_butadiene_rubber` |
| Platinum | PGM line MV (`kubejs:chem/pgm/*`); MI raw platinum + H₂SO₄, MV. **Also** Dissolver andesite trace (0.074 Pt/block) → Compactor → furnace, T1 | `alchemistry:dissolver/andesite`, `chemlib:platinum_ingot_from_smelting_platinum_dust` |
| HF | Mek Dissolution Chamber (fluorite + H₂SO₄); **MV** since `phase5_balance.js` | `mekanism:processing/uranium/hydrofluoric_acid` |
| UF₆ | Infuser (UO₂ + HF), MV; fissile fuel needs Isotopic Centrifuge, EV | `processing/uranium/sulfuric_acid.json` (sic), `fissile_fuel` |
| Uraninite (UO₂) | MI Chemical Reactor U + O₂, MV | `kubejs:phase4/powah/uraninite_from_uranium_oxidation` |
| Plutonium | Mek Isotopic Centrifuge on waste, EV; MI nuclear rod recycling, EV | `processing/lategame/plutonium` |
| Polonium | Mek SNA on waste (waste needs EV fission) | `processing/lategame/polonium` |
| Antimatter | Mek SPS (EV + Pu/Po casing) | `sps_casing`, `antimatter_pellet/from_gas` |
| Oganesson (intended T5 fusion) | **Dissolver: 1 dragon's breath → 8 Og (T1 machine, after the End)** | `alchemistry:dissolver/dragon_breath` |
| Rocket fuel | `#ad_astra:fuel` includes `#c:diesel`, `#c:biodiesel` (MI Mixer, **MV**) and Ad Astra cryo fuel **from ice** | `ad_astra/tags/fluid/fuel.json`, `ad_astra:cryo_freezing/*` |
| Energy / Antimatter Core | MI Assembler 512 / 2048 EU/t (needs Highly Advanced/Quantum upgrades, EV-IV; verify) | `kubejs:chem/energy_core_charge`, `/antimatter_core` |

## 3. Every pack recipe that consumes a chemical

| Recipe id (file) | Chemical in | Runs at | Output used at | Verdict |
|---|---|---|---|---|
| `kubejs:phase4/pylons/infusion_pylon` (`phase4_flight.js`) | `chemlib:hydrogen` | T1 Dissolver | T2 flight | OK, real ("lighter than air") |
| `kubejs:phase4/flight/potion_of_flying_from_hydrogen` | 2 H | T1 | T2 | OK |
| `kubejs:phase4/ars_nouveau/ritual_flight` | 2 H | T1 | T2 | OK |
| `kubejs:phase4/undergarden/catalyst` (`phase4_integration.js`) | MI `sulfuric_acid_bucket` | **MV** (MI reactor) | T3 realm | (a) forced detour: Mek H₂SO₄ (LV) not accepted |
| `kubejs:phase4/powah/uraninite_from_uranium_oxidation` | O₂ 500 mB | MV | T3/MV Powah | OK |
| `kubejs:aluminum/lye` | NaOH crystal/dust | LV Mixer | T3 | OK |
| `kubejs:aluminum/digestion`, `/precipitation`, `/calcination` | NaOH, aluminate | LV | T3 → MV gate | OK, real Bayer (precipitation is really cooling + seeding; fine) |
| `kubejs:aluminum/electrolysis` | alumina, coke dust 50%, `mekanism:dust_fluorite` 5% | LV cell | MV gate | OK chemistry (fluorite is a real bath additive; real flux is cryolite). **Bypass**: see §4 #1 |
| `kubejs:chem/byproduct/*` | Mek dirty dust (O₂/HCl chain) | MV Centrifuge | T3-T4 | OK, all pairings real |
| `kubejs:chem/haber_bosch` | N₂ + 3 H₂ | MV | T5 PGM | OK (no Fe catalyst; optional flavour) |
| `kubejs:chem/ostwald` | NH₃ + 2 O₂ | MV | T5 | OK (net equation correct) |
| `kubejs:chem/ammonium_chloride` | NH₃ + HCl | MV | T5 | OK |
| `kubejs:chem/pgm/sludge_from_{nickel,copper}` | — (electrorefining) | MV Electrolyzer | T5 | OK (anode slime is real) |
| `kubejs:chem/pgm/aqua_regia` | 3 HCl : 1 HNO₃ | MV | T5 EV board (Pt) | OK, correct ratio and Ir/Os/Rh/Ru insolubility |
| `kubejs:chem/pgm/precipitate`, `/calcine`, `/residue` | NH₄Cl | MV (calcine 64 EU: kanthal EBF) | T5 | OK, real (NH₄)₂PtCl₆ route |
| `kubejs:chem/energy_core_empty` | Po pellets | EV | T6 | OK |
| `kubejs:chem/antimatter_core` | antimatter pellets | EV-IV | T6 | OK |
| `kubejs:chem/seed_of_a_new_world` | coke, `chemlib:water`, H, MI H₂SO₄ + PE buckets, Og, Pu, Po, antimatter cores | — | finale | Missing **HF** and PVC that PROGRESSION §3 promises; Og leaks (§4 #2) |
| `kubejs:phase4/projecte/philosophers_stone` | `chemlib:oganesson` | "T5" | ProjectE lite | **Leak**: Og from dragon's breath at T1 Dissolver |
| `kubejs:warbuckscore/biome_capsule` | rubber sheet | T1 | QoL | OK |
| `kubejs:shop/rubber`, `/coke`, `/salt`, `/osmium`, `/bauxite` (`phase4_chemistry.js` §5) | tokens | any | — | (b) rubber 16/2 tokens skips the LV rubber chemistry; osmium 8/3 tokens contradicts "osmium is a milestone" (blocked in MA/Occultism) |
| Every circuit swap (Mek circuits, AE2, Flux, Jetpacks, Angel Ring, EC tables, HNN, MA seeds, Create, TelePastries) | none directly | matching MI tier | matching tier | OK: chemistry arrives through the MI circuit (Al/Si, PE, PVC/Pt). No chemical intermediate of their own |

## 4. Mismatches found (by impact)

1. **(a/b) Aluminium gate bypassed by Alchemistry (HIGH).** Native `alchemistry:dissolver/obsidian` gives
   8 `chemlib:aluminum_oxide` per obsidian (renewable). `warbucks:alumina` (`phase4_aluminum.js`) accepts the
   *item* `chemlib:aluminum_oxide`, so 1 obsidian = **8 Al ingots** in the cell vs 4 bauxite = 2 ingots via Bayer.
   Worse, no cell is needed at all: Dissolver Al₂O₃ → 2 `chemlib:aluminum`; 16 → `alchemistry:compactor/aluminum_dust`;
   `chemlib:aluminum_ingot_from_smelting_aluminum_dust` / `_blasting_` turn it into a `c:ingots/aluminum` ingot in a
   vanilla furnace (AU unifies to MI), and MI's compressor (`materials/aluminum/compressor/main`) makes plates. The
   dust also fits MI's EBF `materials/aluminum/blast_furnace/dust`. Net: MV's aluminium gate is reachable at **T1**.
2. **(b) Oganesson at T1 (HIGH).** `alchemistry:dissolver/dragon_breath` → 8 Xe + 8 Rn + **8 Og**. The ProjectE lite
   gate ("opens only after the complete periodic table, T5") and the Seed's 8 Og are therefore satisfied after one
   dragon fight with a T1 Dissolver. Also chemically absurd (Og has a sub-ms half-life; it can't be in anything).
3. **(c) T3 gate "H₂SO₄ in volume → MV hulls" isn't real.** MV hull = electronic circuit + silicon battery
   (`assembler_generated/electric_age/hull/advanced_machine_hull`); no MV-entry recipe takes sulfuric acid. H₂SO₄ is
   only needed by the Undergarden catalyst, Mekanism 5x, HF and the Seed. The real LV → MV chemistry is NaOH/Bayer
   + carbothermic silicon (good, but not what the doc says).
4. **(c) T1 gate "first synthesized compound → LV hull" isn't real.** No LV part needs a Combiner product
   (LV hull = analog circuit + tin cable + redstone battery + steel casing). The Combiner's first forced use is the
   NaOH lye bootstrap at T3.
5. **(a) Undergarden catalyst forces MI's MV acid.** The pack's own design puts the contact process in Mekanism
   (LV), but `kubejs:phase4/undergarden/catalyst` only takes `modern_industrialization:sulfuric_acid_bucket`
   (Chemical Reactor = MV). `mekanism:sulfuric_acid_bucket` and `chemlib:sulfuric_acid_bucket` exist.
6. **(b/d) Rocket fuel is MV diesel (and "cryo fuel from ice").** `#ad_astra:fuel` accepts `#c:diesel`/`#c:biodiesel`
   for every rocket tier; Ad Astra's `cryo_freezing/*` makes cryo fuel from ice. T6's "rocket fuel from your refinery"
   is an MV product, and diesel with no oxidiser contradicts quest `t7_parts`' own chemistry line.
7. **(d) Silicon from crushed sand / smelted certus.** `mekanism:compat/ae2/sand_to_silicon` (Crusher: sand → Si) and
   `ae2:smelting|blasting/silicon_from_certus_quartz_dust` skip the reduction step (SiO₂ + 2C → Si + 2CO) that MI uses.
   AE2 is HV-gated so balance impact is small; it's a correctness/theme issue ("AE2 gated by silicon").
8. **(b) Dissolver stone traces give gate metals at T1** (CLAUDE.md open item 5): andesite 0.074 Pt/block, diorite
   0.07 Os, deepslate 0.053 Os, amethyst block 0.19 U. Pt is the EV board metal (`processing_unit_board` needs
   `c:plates/platinum`); ~216 andesite → 1 Pt dust → furnace. Only matters if andesite is mass-generated (verify).
9. **(c) Seed lacks HF and PVC** that PROGRESSION §3 lists; hydrogen and water both represent T1.
10. **(d) Quest text:** `t3_rubber` says rubber is plant polyisoprene "from plant matter"; in this pack rubber is coal-
    derived (coke → synthetic oil, optionally sulfur-vulcanised). Minor, quest-only.
11. **(b) HF arrives at MV** (Dissolution Chamber lowered in `phase5_balance.js`) though design T5. Harmless: its only
    consumer (UF₆ → fissile fuel) needs the EV Isotopic Centrifuge. Just note it in the quest book.

## 5. Chemistry the player actually does, per design tier

| Tier | What the player really does | Matches "intermediates over ingots"? |
|---|---|---|
| T0 | Smelting, bronze alloy, charcoal | Fine for a start tier |
| T1 steam | Coke oven (coke, creosote), carburised steel, coal-derived synthetic rubber; Dissolver/Combiner open | Yes for coke/steel/rubber. Combiner not required for anything (gap #4) |
| T2 Nether | Dissolver hydrogen → Pylon/Potion of Flying; Mek electrolysis possible (no circuit) | Yes, light but real. Sulfur/quartz flavour not used in a recipe |
| T3 LV→MV | Bayer process + Hall-Héroult, carbothermic silicon, Mek H₂/O₂/Cl₂/HCl/SO₂→H₂SO₄ (all LV), Mek 3x-5x ore at MV, uraninite | Strongest tier, **but** Alchemistry alumina/Al leaks (#1) and H₂SO₄ gates nothing core (#3) |
| T4 HV | Crude → hydrotreat with H₂ → steam crack → ethylene → polyethylene (done with MV machines to reach HV); AE2, Twilight | Yes (PE is in the HV board) |
| T5 EV | PVC (acetylene + HCl), PGM line (Haber, Ostwald, aqua regia, NH₄Cl), monocrystalline Si (Ar, Ir), Cd battery (monazite), HF → UF₆ → fission → Pu/Po | Yes, very good. Og leak (#2) undercuts "full periodic table" |
| T6 | SPS antimatter, energy cores, Seed; rockets | Antimatter yes; rocket fuel is MV diesel (#6) |

## 6. Recommended fixes (ordered by impact)

| # | Fix | Why / real chemistry | Type |
|---|---|---|---|
| 1 | In `phase4_aluminum.js`: remove `chemlib:aluminum_ingot_from_smelting_aluminum_dust`, `chemlib:aluminum_ingot_from_blasting_aluminum_dust`, and `alchemistry:compactor/aluminum_dust`; set tag `warbucks:alumina` to `chemlib:aluminum_oxide_dust` only (8 Combiner items = 1 dust, so 1 obsidian = 1 ingot). | Aluminium must be won by electrolysis (Hall-Héroult); no furnace can reduce Al₂O₃. Keeps the alchemical route but at Bayer-like cost | Safe KubeJS (check ids in JEI; AU may hide chemlib ids) |
| 2 | Re-add `alchemistry:dissolver/dragon_breath` without oganesson (keep Xe, Rn), so Og comes only from Fusion (T5, `alchemistry:fusion/*_to_118oganesson`). | Og is synthetic only; restores the ProjectE and Seed gates | Safe KubeJS (`event.remove` + `event.custom`) |
| 3 | Undergarden catalyst: `A: ['modern_industrialization:sulfuric_acid_bucket', 'mekanism:sulfuric_acid_bucket', 'chemlib:sulfuric_acid_bucket']`. | Contact process is already a Mekanism LV chain; removes the MV detour | Safe KubeJS |
| 4 | T1 → LV compound gate: add 1 `chemlib:sulfuric_acid` (Combiner: 2H + S + 4O) to MI's redstone battery (`modern_industrialization:electric_age/battery/lv_battery_asbl` and `…:assembler_generated/electric_age/battery/lv_battery`). | MI battery alloy is Pb-Sb, the real lead-acid grid alloy; H₂SO₄ is its electrolyte. Makes the Combiner a real T1 milestone | Safe KubeJS, small design call (2 per LV hull) |
| 5 | Silicon: remove `mekanism:compat/ae2/sand_to_silicon`, `mekanism:compat/ae2/certus_quartz_dust_to_silicon`, `ae2:smelting/…` and `ae2:blasting/silicon_from_certus_quartz_dust`; add `modern_industrialization:silicon_ingot` to item tag `c:silicon`. | Silicon needs carbothermic reduction (EBF quartz + coke), which MI already does | Safe KubeJS |
| 6 | Seed: replace the 4 `H` (hydrogen) slots with `mekanism:hydrofluoric_acid_bucket` (optionally 2 `P` → `modern_industrialization:polyvinyl_chloride_bucket`). | Matches PROGRESSION §3 ("… HF, antimatter"); water already stands for T1 | Safe KubeJS |
| 7 | Rocket fuel: drop `#c:diesel`/`#c:biodiesel` from `ad_astra:fuel`; add an MI Mixer/Chemical Reactor recipe light fuel (kerosene) + O₂ → `ad_astra:fuel` (RP-1/LOX), and replace `ad_astra:cryo_freezing/*` with Vacuum Freezer H₂ → `ad_astra:cryo_fuel` (liquid hydrogen). Update quests `t5_diesel`, `t7_fuel`. | Rockets carry their oxidiser; LH₂/LOX is the real cryogenic fuel. Reverses the Phase 3 "rockets run on diesel" choice | **Design call** |
| 8 | Make H₂SO₄ an MV gate as the doc says: MI assembler `electronic_circuit_board` + 250 mB `#c:sulfuric_acid` (fluid tag holds MI and Mek acid), remove the crafting-table variant `electric_age/circuit/craft/electronic_circuit_board_asbl`. | H₂SO₄/H₂O₂ micro-etch is a real PCB step; Mek's LV acid avoids a circular MV dependency | **Design call** (adds a step at the busiest gate) |
| 9 | Shop: drop or reprice `kubejs:shop/osmium` and `kubejs:shop/rubber`. | Osmium is listed as a milestone elsewhere; rubber is the LV chemistry | Design call (convenience) |
| 10 | Dissolver stone traces: remove Pt/Os/U from stone outputs in `tools/build_dissolver.py` overrides (native andesite/diorite/deepslate/amethyst recipes need KubeJS re-adds). | Gate metals at T1 from cobble automation | Design call (CLAUDE.md item 5) |
| 11 | Flavour (optional): Haber gets `{tag:'c:dusts/iron', amount:1, probability:0}` as catalyst; fix `t3_rubber` text to "coal-derived synthetic rubber, vulcanised with sulfur". | Fe catalyst is the real Haber catalyst | Safe |

Not changed / fine as is: MI circuit chain (Al, Si, PE, PVC, Pt, Cd, Pu), Mekanism ore chain at MV, Haber/Ostwald/PGM
chemistry, Bayer chemistry, byproduct pairings, uraninite, energy cores. After any change: smoke test, then check JEI.
