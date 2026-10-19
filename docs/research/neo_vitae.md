# Neo Vitae (added 2026-10-19)

Blood magic for NeoForge 1.21.1: a ground-up successor of Blood Magic by WayofTime and Saereth (breakinblocks).

## Source and distribution (verified 2026-10-19)
- Modrinth project `neovitae` (id `rvaW4C93`), team of author Saereth; source https://github.com/breakinblocks/NeoVitae.
- License: MIT (Modrinth project page and `license="MIT"` in the jar's neoforge.mods.toml). Redistributable.
- Pack file: `neovitae-1.21.1-1.1.44.jar` (Modrinth version `nt0gFkED`, released 2026-10-17, game version 1.21.1,
  loader neoforge, client + server). Added with `packwiz mr add neovitae` (pack/mods/neovitae.pw.toml).
- Official file check: ATM10's jar (`neovitae-1.21.1-1.1.26.jar`) has SHA-1 5403fcf0... which Modrinth resolves to the
  same project's version 1.21.1-1.1.26, so ATM10 uses this official project. The 1.1.44 jar downloaded from the
  Modrinth CDN matches the sha512 in the packwiz metafile.
- Required dependencies: NeoForge 21.1+, GeckoLib, Modonomicon. Both libraries were already in the pack.
  Optional: JEI, EMI, Jade, Curios (not needed by us beyond what's already there).

## What it adds
- **Ara Vitae** (blood altar, 6 tiers built from runes) fills with Essentia Vitae (EV) from self-sacrifice or mob kills
  and transmutes items placed on it. Six **Orbs of Vitae** (Novicius → Divinus) hold the player's EV network.
- **Tabula Vitae** (alchemy table: reagents, catalysts, cutting fluids, anointments, Alchemy Flask potions),
  **Alchemy Arrays** (sigils: water, lava, void, holding, magnetism, air dash, phantom bridge...),
  **Hellfire Forge** (Spiritus-fuelled crafting: Spiritus gems, Sentient tools, explosive charges, dungeon keys),
  **Athanor** (reaction chamber with tool slots: ore processing, hydration, resonator; Spiritus-boosted).
- **Rituals** (~45, Master Ritual Stone + inscribed stones; elemental, Tenebrae and Deus tiers): crops, mob farming
  (Well of Suffering, Torment Nexus spawner simulation), Magnetism (ore quarry, Fortune III or Silk Touch), Felling,
  Placer, Sphere, Condor (area flight), Meteo (meteors), Enchanted Vitae (book enchanting), dungeon gates.
- **Sentient Armour** (upgrades trained by activity, tomes from dungeons; Elytra upgrade = elytra-style gliding).
- **Demon Realm** dimension (`neovitae:dungeon`) with procedural dungeons, bosses, Tau fruit and demonite ore
  (Hellforged metal), routing nodes (item logistics), teleposers, potion flasks with a Flight effect.
- **Material system**: `config/neovitae/materials.json` registers fragment/gravel/dust items and generates Athanor and
  Tabula Vitae ore recipes at load time (in-memory datapack). On a first run without the file it also auto-discovers
  modded ores on first player login and appends them, which needs a restart and would desync client and server items.

## Progression (altar tier → key unlock)
| Tier | Orb (altar input) | Unlocks |
|---|---|---|
| I | Novicius (diamond) | Tabula Vitae, arrays, Hellfire Forge, blank runes |
| II | Discipulus (redstone block) | Sacrifice/Speed runes, Tabula Robur, potion flasks |
| III | Veneficus (gold block) | rituals, Tabula Animata, Athanor, Sentient Armour |
| IV | Magus (Weak Blood Shard: Saturated Tau from the Demon Realm, refined in the Athanor) | Tenebrae rituals |
| V | Dominus (Hellforged block from demonite) | reinforced runes |
| VI | Divinus (Crystal Cluster: needs a Nether Star) | Deus rituals |

## Problems found and what we did (pack/kubejs/server_scripts/phase5_neovitae.js)
| Issue | Default | Pack rule | Change |
|---|---|---|---|
| Athanor ore processing | ore → 5 fragments → 5 dust (6 with Spiritus); raw → 3 (4) | ≤ 2x per ore, ≤ 1.5x per raw before acids | ore → 2 fragments, no Spiritus bonus; raw → fragments removed (raw → 1 dust + 25%, ≤ 1.5x with the best fluid doubling the bonus); dust-only ore (coal 6, gems 3) → max 2; Tabula "fragment + corrupted dust → 2 gravel" removed. Demonite/hellforged (mod-own Demon Realm metal) left as designed. |
| Netherite scrap material | ancient debris → 5 scrap; scrap → 3 fragments → 3 scrap (infinite loop) | no duplication | `netherite_scrap` dropped from the shipped materials.json (and the cap above would catch it anyway) |
| Flight | Flight flask effect (Suspended + Levitation + Combinational Catalyst); Ritual of the Condor (Tenebrae runes) | every flight source is a chemistry milestone | flask fusion needs 2 `chemlib:hydrogen`; the Tenebrae scribe tool moves from the altar to the Tabula Vitae: coal block + 2 hydrogen + MI electronic circuit (MV) |
| Free milestone resources | Athanor: diamond + hellforged ingot + EV → Nether Star | Nether Stars gate the Angel Ring and ProjectE lite | recipe removed |
| Meteors | Ritual of Meteo: iron block → ~r14 sphere of iron/copper/gold ore; diamond → diamond/emerald ore; Nether Star → ancient debris; glowstone → nether ores; certus → fluix block core; deepslate → r32 of coal/iron ore | ore comes from deposits and chemistry | all 6 meteor recipes removed (the ritual exists but has no catalysts) |
| Tier fit | Athanor is a Tier III magic block | key machines take that tier's MI part | Athanor's 2 iron blocks → 2 MI analog circuits (LV). Since Weak Blood Shards come from the Athanor, Tier IV (Magus) also sits after LV, and Tenebrae after MV. |

Shipped config: `pack/config/neovitae/materials.json` = the mod's 12 default materials minus netherite scrap
(iron, gold, copper, coal, demonite, hellforged, diamond, emerald, lapis, quartz, amethyst), so the first-run
auto-discovery never runs and client/server register identical items.

## Left as is (judgement calls, flag for the user)
- Ritual of Magnetism / Deus Endless Quarry: pulls ore blocks from below with Fortune III or Silk Touch, the same yield
  as a Fortune III pickaxe. Late-ish (Tier III+, EV upkeep).
- Torment Nexus (simulated spawner kills, Deus = 3x loot) and Well of Suffering: mob-farm equivalents.
- Sulfur from lava + cobblestone (Tabula Vitae, 4 sulfur; with the Lava Sigil it's unlimited) and 2 sulfur per
  netherrack (Athanor). Sulfur is cheap in this pack already (Nether, Mekanism); not a milestone.
- Gilded blackstone → 9 gold nuggets (Tabula Vitae): about vanilla silk-touch value.
- Sentient Armour Elytra upgrade: elytra-style gliding (not creative flight), dungeon loot only.
- Spawner capture with a Spiritus Gem (movable spawners), Teleposers.
- Deus tier (altar VI, Nether Star) is not MI-gated beyond the Athanor; it is very late anyway.

## Not verified
- In-game behaviour of the KubeJS changes (no smoke test run in this session): `event.findRecipes({type:'neovitae:athanor'})`
  must see the in-memory generated recipes; the console logs `[phase5] neovitae ...` lines for each change.
- That the Tabula Vitae accepts the moved Tenebrae recipe with `upgradeLevel: 3`, and that the flask fusion accepts
  extra items in its `input` list (both formats copied from the mod's own recipes).
- ProjectE EMC of the new neovitae dust/fragment items (custom_emc.json may need entries; run test/emc_check.sh).
- Almost Unified may want neovitae dusts added to its unification (they share c:dusts/* tags).
