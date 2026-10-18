# Warbucks Chemistry Pack: Progression Design

**Loader:** NeoForge · **Minecraft:** 1.21.1 · **Status:** Phase 1 design pitch v2, after the reset (2026-10-18)

---

## 1. Identity

> *You woke up in a world that wasn't made for you. You have a god's patience and a chemist's hands. Take it apart, element by element, and build the world you want to live in.*

You're a **demigod** who spawns in an ordinary Overworld with your power gone. Your divinity comes back through **understanding matter**. Every block can be taken apart into its elements, and every element can be put back together into something new. The quest book follows you as you rebuild the periodic table, reclaim your gifts (flight first), and open new realms to shape.

### Design pillars

1. **Everything is chemistry.** Once you've built the machine, you can break **any** block into elements (Alchemistry Dissolver) and synthesize blocks from elements (Combiner). The long-term goal is a complete periodic table and the ability to synthesize the game's blocks from chemicals.
2. **Intermediates over ingots.** Tier gates are chemical products (coke, acids, chlorine, plastics, pure silicon, isotopes), not bigger piles of metal.
3. **GregTech's structure, not GregTech's grind.** Modern Industrialization gives the voltage-tier skeleton, with short recipe chains, no 64-step circuits and quest rewards that skip busywork. The test for every recipe: *is this a decision or a chore?* Chores get cut.
4. **Divinity comes back early.** Creative flight arrives right after the Nether and brewing. You're a demigod, not a peasant.
5. **Light magic, chemistry-flavored.** Ars Nouveau, relics and artifacts are the "divine" side, and their key recipes use chemical intermediates.
6. **One backbone per system.** MI covers machines and power, Mekanism covers gases and nuclear, Alchemistry covers elements, and AE2 covers storage. Other mods feed into these systems rather than bypass them (enforced in Phase 3).

---

## 2. Core roster (all checked for NeoForge 1.21.1 on 2026-10-18)

| Role | Mod | Latest 1.21.1 build | Source |
|---|---|---|---|
| Tech backbone (steam → LV → … → EV+) | Modern Industrialization | 2.5.10 (2026-10-07) | Modrinth |
| Elements, disassembly, synthesis | Alchemistry + ChemLib + AlchemyLib | 2.4.5 / 2.1.5 / 1.1.6 (2026-06-12) | CurseForge only |
| Gas chemistry, ore processing, nuclear | Mekanism + Generators | 10.7.19 (2026-04-10) | Modrinth |
| Storage and autocrafting | Applied Energistics 2 | 19.2.18 (2026-09-27) | Modrinth |
| Light magic | Ars Nouveau | 5.13.3 (2026-10-03) | Modrinth |
| Relics | Relics | 0.12.8 (2026-05-28) | Modrinth |
| Relics | Artifacts | 13.2.5 (2026-09-02) | Modrinth |
| Relics | Reliquary Reincarnations | 2.0.81 (2026-10-17) | Modrinth |
| Enchanting and loot | Apotheosis + Apothic Attributes / Enchanting / Spawners + Placebo | 8.9.0 / 2.11.0 / 1.6.4 / 1.4.0 / 9.9.4 | Modrinth |
| **Flight** | Pylons (Infusion Pylon) + Apothic Attributes (Potion of Flying) | 5.4.2 (2026-02-07) | Modrinth |
| Biomes | Biomes O' Plenty (+ TerraBlender, GlitchCore) | 21.1.0.14 (2026-06-20) | Modrinth |

Apotheosis addons: there are lots of them, but most are compatibility bridges for mods we aren't using, and several need Create (Create: Apokinetics, Apotheotic Creation are excluded). Candidates that fit us: **Apotheosis Addon Compat**, **Apothic Tooltip Cleanup**, **Apotheosis Bags**, **Apothic Renaming**, **Ancient Reforging**, and **Apothic Category Compat** (adds Twilight Forest loot categories). I'll make the final picks and verify them in Phase 2.

### Dimensions (all confirmed to have NeoForge 1.21.1 builds)

| Dimension | Mod | Build | Fit |
|---|---|---|---|
| Twilight Forest | The Twilight Forest | 4.8.3345 (2026-03-22, CurseForge) | Adventure realm, boss progression |
| The Undergarden | The Undergarden | 0.9.6 (2026-04-02) | Dark underground realm, new ores and minerals |
| Space / other planets | Ad Astra | 1.16.26 (2026-09-13) | Late-game: rocket fuel from our refinery, new planets to terraform. Heavy, with about 6 library deps (Botarium, Resourceful Lib/Config, etc.). |
| (alt) Space | Stellaris | 1.4.25 (2026-07-09) | Lighter alternative to Ad Astra |
| (optional) The Aether | The Aether | 1.5.10 (2025-09-28) | ⚠️ Last update 13 months ago |
| (optional) Bumblezone | The Bumblezone | 7.17.0 (2026-10-18) | Lighthearted bee dimension |
| (optional) Deeper and Darker | Deeper and Darker | 1.4.1 (2026-06-05) | Otherside realm past the Ancient City |

**Dropped from the old design:** Immersive Engineering (15 months without an update; MI already has coke and steel), Immersive Petroleum (depends on IE), PneumaticCraft (overlaps MI), ProjectE (excluded by the user), Botania (no 1.21.1 build), and Create plus all its addons.

---

## 3. Tier progression

Seven tiers. Each one lists the chemistry concept, the divine milestone (the story beat), and the gate. *(verify)* marks a mechanic I need to confirm in-game or in source before scripting it. KubeJS enforces the gates in Phase 4.

### T0: Awakening (fire and ore)
- **Chemistry:** combustion and reduction. Charcoal, smelting, the first alloy (**bronze** = Cu + Sn).
- **Story:** You wake up mortal. A worn journal (quest book) holds fragments of what you once knew.
- **Play:** vanilla start, Biomes O' Plenty exploration, and MI bronze tools and steam machines.
- **Gate → T1:** bronze + **charcoal/coke supply** → MI steam boiler.

### T1: Steam and Steel (carbon chemistry) + *the periodic table opens*
- **Chemistry:** destructive distillation (coal → **coke** + creosote *(verify MI coke oven outputs)*) and carburization (iron + coke → **steel**).
- **Divine milestone:** build the **Alchemistry Dissolver and Combiner** out of steam-age parts. From then on, any block can be broken into elements and rebuilt. The first quest chapter on the periodic table starts collecting elements (H through Fe).
- **Gate → T2:** **steel** + **first synthesized compound** (from the Combiner) → LV machine hull.

### T2: Divine Ascent (Nether and brewing) + *flight*
- **Chemistry:** the Nether as a chemistry lab: sulfur sources, quartz (SiO₂) and blaze powder, and brewing as applied chemistry.
- **Divine milestone, flight:** brew **Potion of Flying** (Apothic Attributes, effect `apothic_attributes:flying`). Load 1 hour of it onto a **Potion Filter** and put the filter in an **Infusion Pylon** (Pylons). That gives permanent creative flight at any distance (it may need chunkloading). *(verify that the Infusion Pylon accepts the modded effect, and the brewing recipe for Potion of Flying)*
- **Magic begins:** Ars Nouveau (Source, the first spells). Relics and Artifacts drop in Nether structures.
- **Gate → T3:** flight + **LV power online**.

### T3: Electrochemistry and Acids (LV → MV)
- **Chemistry:** electrolysis (water → **H₂ + O₂**, brine → **Cl₂** *(verify outputs)*), then **HCl** and the contact process for **H₂SO₄** (sulfur → SO₂ → SO₃ → H₂SO₄, all in Mekanism).
- **Play:** Mekanism multi-stage ore processing (O₂ purification → HCl injection → H₂SO₄ dissolution). Each ore multiplier comes from a chemistry step.
- **Realm unlocked: The Undergarden** (portal catalyst needs a chemical component *(design: KubeJS)*).
- **Gate → T4:** **sulfuric acid** in volume → MV hulls and the first circuits.

### T4: Petrochemistry (HV) + *the god's archive*
- **Chemistry:** crude oil → **fractional distillation** (MI distillation tower) → fuels and ethylene → **polyethylene / plastic** *(verify MI oil source and fraction names)*.
- **Divine milestone:** **AE2** comes online, gated by silicon and plastic. Your memory, rebuilt as an ME network.
- **Realm unlocked: The Twilight Forest** (the portal is a vanilla-style ritual; quest-gated, possibly needing a refined catalyst).
- **Gate → T5:** **plastic** + **refined fuel** → HV/EV hulls and AE2 processors.

### T5: Materials and Nuclear (EV)
- **Chemistry:** semiconductor-grade **silicon**, **hydrofluoric acid** (fluorite + H₂SO₄ *(verify)*), **UF₆** enrichment (Isotopic Centrifuge), fission, and waste → **plutonium / polonium**.
- **Divine milestone:** **Alchemistry fission and fusion chambers** let you transmute between elements, which **completes the periodic table**. Now every block is buildable from chemicals.
- **Gate → T6:** HF + plutonium/polonium + a **complete periodic table** quest.

### T6: Creation (endgame)
- **Chemistry:** antimatter (Mekanism SPS) and rocket fuel from your refinery.
- **Divine milestone:** leave the planet (**Ad Astra** or Stellaris). Other worlds are blank canvases to shape. The capstone item, the **Seed of a New World**, needs an intermediate from every tier (coke, synthesized compound, H₂SO₄, plastic, HF, antimatter).

---

## 4. Tier summary

| Tier | Name | Chemistry gate | Divine milestone | Power | Unlocks |
|---|---|---|---|---|---|
| T0 | Awakening | Bronze, charcoal/coke | Journal | Manual | — |
| T1 | Steam and Steel | Steel, first compound | **Dissolver + Combiner** | Steam | Periodic table H–Fe |
| T2 | Divine Ascent | Nether chemistry, brewing | **Creative flight** (pylon) | Steam/LV | Ars Nouveau, relics |
| T3 | Electrochemistry and Acids | H₂SO₄, HCl | Ore processing ×3–5 | LV→MV | **Undergarden** |
| T4 | Petrochemistry | Plastic, refined fuel | **AE2** | HV | **Twilight Forest** |
| T5 | Materials and Nuclear | HF, Pu/Po | **Full periodic table** | EV, fission | Transmutation |
| T6 | Creation | Antimatter, rocket fuel | **Seed of a New World** | Endgame | **Space** |

---

## 5. Grind controls (how "not a time sink" gets enforced)

- MI config and KubeJS: fewer crafting steps for hulls and circuits, and no recipes that need more than about 3 nested intermediates for a single machine.
- Quest rewards include a few of each tier's first machines, so you only build the first one of a type by hand.
- FTB Ultimine, and Mekanism processing that pays off quickly.
- Pacing target: about 50–80 hours to finish, and flight within the first 2–4 hours (right after the Nether and brewing).

---

## 6. Phase 3 decisions (compatibility pass, 2026-10-18)

| System | Backbone | How it's enforced |
|---|---|---|
| Metals and materials (ingots, dusts, plates, nuggets, blocks) | **MI** items are canonical, then Mekanism, AE2, Ad Astra, ChemLib | Almost Unified `mod_priorities` (`pack/config/almostunified/unification/materials.json`): 723 recipes unified, 121 duplicate recipes merged |
| Ore generation | **MI** for tin, lead, uranium. Mekanism keeps only osmium and fluorite. | `pack/config/Mekanism/world.toml` turns off Mekanism tin/lead/uranium. Powah uraninite ore is turned off via `pack/kubejs/data/powah/neoforge/biome_modifier/*` (uraninite gets a chemistry recipe in Phase 4). |
| Ore processing | **Mekanism** from T2/T3: 3× O₂, 4× HCl, 5× H₂SO₄ | Pre-acid routes capped at **2× per ore block**: MI Macerator (was 3×), MI Forge Hammer with tool (was 3–4×), Integrated Dynamics squeezers (was about 2.75–4×). Raw-ore routes are unchanged (≤1.5×). Alchemistry Dissolver ore → 32 elements = 2× (already in line). |
| Petrochemistry | **MI** distillation tower | Ad Astra's Fuel Refinery recipe removed; rockets run on MI diesel (`#c:diesel` is already in `#ad_astra:fuel`). MI ethylene added to `#c:ethene` so it feeds Mekanism HDPE. Mekanism's bio-ethene route stays as an alternative (real-world bio-ethylene). |
| Storage network | **AE2** (Tom's Simple Storage as the early network) | Refined Storage not included |
| Reactors | **Mekanism** fission (primary), MI nuclear as an alternative | To be balanced in Phase 4 |

### Ore deposits (2026-10-18)
Scattered MI ore is reduced to 35%, and rich deposits (500–900 ores in one chunk) appear in about 1 of every 16–30 chunks, at a metal-specific depth (`tools/build_deposits.py`). Prospecting with Jade, Ultimine and exploration pays off; byproducts and 3–5x processing make up the difference.

## 7. Phase 4 integration (KubeJS, 2026-10-18)

MI's tier ladder is the spine. Its hulls already need chemical intermediates: LV analog circuit + steel (coke); MV electronic circuit (aluminum) + silicon battery; HV digital circuit (**polyethylene**) + sodium battery; EV processing unit (**PVC**) + cadmium battery; IV quantum circuit + plutonium battery. `pack/kubejs/server_scripts/phase4_integration.js` hooks the other mods onto it:

| Tier | Item | Now needs |
|---|---|---|
| T1 steam | Alchemistry Dissolver, Combiner | Steel plates + MI Bronze Machine Casing |
| LV | Mekanism Basic Control Circuit | MI Analog Circuit + osmium (infuser recipe removed) |
| MV | Mekanism Advanced Control Circuit | + MI Electronic Circuit (infuser shortcut removed) |
| T3 | Undergarden Catalyst | + Sulfuric Acid Bucket |
| T3 / MV | Powah Energizing Orb | + MI Electronic Circuit |
| T3 | Powah Uraninite | **New:** MI Chemical Reactor, uranium dust + 500 mB O₂ → UO₂ |
| HV | Mekanism Elite Control Circuit | + MI Digital Circuit |
| T4 / HV | AE2 Inscriber / ME Controller | MI Turbo Machine Hull / MI Digital Circuit |
| EV | Mekanism Ultimate Control Circuit | + MI Processing Unit |
| T5 / EV | Flux Core; Alchemistry Fission and Fusion controllers | MI Processing Unit |
| T5→T6 | Ad Astra NASA Workbench | MI Highly Advanced Machine Hull |

**Mystical Agriculture** (`phase4_mysticalagriculture.js`):
- Seeds for chemistry-milestone resources are removed: uranium, uraninite, osmium, fluorite, silicon, steel, aluminum, graphite, platinum, iridium, refined obsidian, refined glowstone.
- Tier 3/4/5 seeds swap one altar essence for an MI Analog/Electronic/Digital circuit (LV/MV/HV). That's 46 recipes, a one-time cost per seed type.

**Monifactory-inspired mods** (`phase4_monifactory.js`):
- Hostile Neural Networks: the Simulation Chamber and Loot Fabricator need an MI Electronic Circuit (MV).
- Extended Crafting: the Advanced, Elite and Ultimate tables need MI MV, HV and EV circuits.

**Flight** (`phase4_flight.js`, Option 2: every flight source is a chemistry milestone):
| Source | When | Gate |
|---|---|---|
| Infusion Pylon + Potion of Flying | End of Ch. II | Needs `chemlib:hydrogen` (Dissolver only) + Nether quartz and blackstone |
| Iron Jetpacks | LV → EV | Basic/Advanced/Elite/Ultimate coils need MI analog/electronic/digital circuits / processing unit |
| Angel Ring | HV+ | MI digital circuit + Elytra + Nether Stars |
| Just Dire Things flight upgrade | After the End | End Crystals (unchanged) |
| Ars Nouveau Ritual of Flight | T2+ | Source, area-limited (unchanged) |

Previously left as-is: the Infusion Pylon (already needs Nether quartz and blackstone, so flight comes after the Nether), the Just Dire Things flight upgrade (needs End Crystals), and the Twilight Forest portal (no recipe; gated by quests in Phase 5).

## 8. Open items

1. Verify in-game (JEI) that the Potion of Flying brewing recipe exists and that the Infusion Pylon accepts it.
2. How to gate portals to the chemistry tiers (KubeJS catalyst items, or quest-only).
5. Alchemistry coverage: write KubeJS dissolver/combiner rules for modded blocks (BOP woods and stones, MI materials, dimension blocks). List anything left uncovered.
