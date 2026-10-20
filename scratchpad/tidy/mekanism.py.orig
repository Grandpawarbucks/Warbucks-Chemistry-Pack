"""Quest chapter: mekanism (mod page: Mekanism and Mekanism Tools). Reactors, Mekanism: More Machine and Mekanism Extras
are on the second page, mekanism_power.py (split 2026-10-18; keys moved unchanged).
See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Main-path Mekanism quests live in t3..t7, power.py and tools.py; this page LINKS to them (columns x = -4 / -6)
instead of duplicating them. Mekanism control circuits need the same-tier MI circuit (phase4_integration.js):
basic = LV analog (t3_mekcircuit), advanced = MV electronic (t4_mv), elite = HV digital (t5_hv),
ultimate = EV processing unit (t6_pu). phase5_balance.js lowers the Chemical Injection Chamber, Dissolution
Chamber, Washer and Crystallizer to Advanced (MV) circuits, so the 4x/5x ore line sits at MV behind the acids.

Already covered elsewhere (not repeated here): Metallurgic Infuser, Enrichment Chamber, Crusher (t3); separator,
tubes, oxidizer, infuser, condensentrator, Purification / Injection / Dissolution / Washer / Crystallizer, MI
Centrifuge byproducts, Thermal Evaporation (t4); HDPE (t5); yellowcake to fission, plutonium, polonium, Solar Neutron
Activator, hazmat (t6); SPS, antimatter, Nucleosynthesizer (t7); every Mekanism generator, energy cubes, induction
matrix, turbine casing, D-T fuel, fusion (power); paxels, Atomic Disassembler, scuba, free runners, jetpack, MekaSuit
helmet + chest (tools); electric pump + heavy water (periodic).
"""
from questlib import Q, Chapter, item, dim, tick, anyof, anytag, MAIN, SIDE  # noqa: F401

MEK = "mekanism:"
GEN = "mekanismgenerators:"
TOOLS = "mekanismtools:"
MM = "mekmm:"
EX = "mekanism_extras:"


def factories(tier, kinds=("smelting", "enriching", "crushing", "compressing", "combining", "purifying", "injecting", "infusing", "sawing")):
    return [f"{MEK}{tier}_{k}_factory" for k in kinds]


def ex_factories(tier):
    kinds = ("smelting", "enriching", "crushing", "compressing", "combining", "purifying", "injecting", "infusing", "sawing",
             "oxidizing", "dissolving", "washing", "crystallizing", "centrifuging")
    return [f"{EX}{tier}_{k}_factory" for k in kinds]


def armour(metal):
    return [item(f"{TOOLS}{metal}_{p}") for p in ("helmet", "chestplate", "leggings", "boots")]


def fac(machine, kind):
    """A machine or any tier of its factory (the ore-line quests accept either)."""
    return anyof([MEK + machine] + [f"{MEK}{t}_{kind}_factory" for t in ("basic", "advanced", "elite", "ultimate")])


# Layout (bands, top to bottom; optional quests sit 1.5 rows off their band's main line):
#   y -4.5..1   alloys, circuits, teleportation, Robit / Digital Miner, QIO
#   y  3..7.5   machines, factories, upgrades, ore line, brine and salt
#   y  9..10.5  pressurized reactions, substrate and HDPE, MekaSuit / Meka-Tool
#   y 12..13.5  transmitters and logistics
#   y 19.5..21  Mekanism Tools armour
# (Generators, reactors, More Machine and Extras moved to mekanism_power.py.)
# Links to main-path quests at x = -4 / -6.
CHAPTER = Chapter("mekanism", "Mekanism", "mekanism:metallurgic_infuser",
        ["Osmium, infusion and gases: Mekanism's machines, factories, circuits and logistics. Reactors and add-ons are on the next page."], SIDE, [
    # --- Alloys and circuits (y = -1 / 1) -------------------------------------------------------
    Q("mk2_intro", 0, 0, [tick()], "The Mekanism Way", subtitle="Infuse, tier up, process", deps=["t3_infuser"], xp=50, desc=[
        "&6Osmium hums in your hand. You remember metals that drank other substances and grew stronger.&r",
        "&eWhat:&r Mekanism is a machine mod built on infusion and gases: soak a metal in carbon, redstone, diamond or refined obsidian and it becomes an alloy; pipe gases between machines and they become chemistry.",
        "&eHow:&r every machine comes in tiers (basic, advanced, elite, ultimate). In this pack each tier's control circuit needs the matching &eMI circuit&r.",
        "&eTip:&r this page is a side path. The main-path Mekanism quests are linked on the left; click one to jump there. Reactors, More Machine and Mekanism Extras are on the next page, &ePower and Beyond&r."], mirror="58B125BD4876054C", section="Osmium and Steel", size=2.0, shape="gear"),
    Q("mk2_configurator", 0, -2, [item(MEK + "configurator")], "Configurator", subtitle="Every side of every machine, your choice", deps=["mk2_steel"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r the Configurator sets which side of a Mekanism block takes input and gives output, ejects contents, and rotates blocks.",
        "&eHow:&r iron, an osmium ingot and steel. Sneak + right-click to change its mode; the side colours match the machine's GUI.",
        "&eTip:&r most \"my machine won't take gas\" problems are a side set to the wrong colour."], mirror="5E116409DC7D30BB", section="Pipes and Storage", size=2.0, shape="gear", loot="t3"),
    Q("mk2_tablet", 2, -3, [item(MEK + "energy_tablet")], "Energy Tablet", subtitle="A battery you can hold", deps=["mk2_infused_alloy"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r a portable FE store. It is also a crafting part in the Robit, the Wind Generator, lasers, Free Runners and the Portable Teleporter.",
        "&eHow:&r gold ingots, redstone and Infused Alloy (check JEI).",
        "&eTip:&r make a few at once; you'll keep needing them."], mirror="4935209D870E25F2", section="Energy", size=2.0, shape="gear", loot="t3"),
    Q("mk2_reinforced", 2, -1, [item(MEK + "alloy_reinforced", 4)], "Reinforced Alloy", subtitle="Infused alloy plus diamond", deps=["mk2_intro", "t3_infused"], xp=60, desc=[
        "&eWhat:&r the second Mekanism alloy, used in elite circuits, lasers and the Solar Neutron Activator.",
        "&eChemistry:&r real alloys work the same way: a few percent of a second element (carbon in steel, chromium in stainless) changes the metal's properties.",
        "&eHow:&r Metallurgic Infuser: Infused Alloy + diamond infusion (from diamonds or diamond dust; check JEI)."]),
    Q("mk2_atomic", 4, -1, [item(MEK + "alloy_atomic", 4)], "Atomic Alloy", subtitle="Reinforced alloy plus refined obsidian", deps=["mk2_reinforced"], xp=80, desc=[
        "&eWhat:&r the top Mekanism alloy, needed for ultimate circuits, teleportation cores and the Robit.",
        "&eHow:&r first infuse obsidian dust with diamond to get refined obsidian dust, then infuse Reinforced Alloy with refined obsidian.",
        "&eTip:&r crush obsidian in the Crusher or an MI macerator for obsidian dust."]),
    Q("mk2_refined_obsidian", 6, -1, [item(MEK + "ingot_refined_obsidian")], "Refined Obsidian", subtitle="The Osmium Compressor's speciality", deps=["mk2_compressor", "mk2_obsidian_dust"], xp=100, desc=[
        "&eWhat:&r refined obsidian ingots: very hard, blast-proof metal for teleporters, the Robit and endgame tools.",
        "&eHow:&r the Osmium Compressor presses refined obsidian dust with liquid osmium into ingots. It needs an Advanced Control Circuit (MV).",
        "&eTip:&r refined glowstone ingots come from the same machine: glowstone dust plus osmium."], mirror="31B73D16C0199785", section="Machines"),
    Q("mk2_adv_circuit", 2, 1, [item(MEK + "advanced_control_circuit")], "Advanced Control Circuit", subtitle="Mekanism's MV tier", deps=["mk2_steel_casing", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the circuit for every advanced-tier Mekanism block: factories, cubes, tanks, the Purification Chamber, and in this pack the whole 4x/5x ore line (injection, dissolution, washer, crystallizer).",
        "&eHow:&r an &eMI electronic circuit&r above two Infused Alloys and a Basic Control Circuit (check JEI).",
        "&eTip:&r the old infuser shortcut for circuits is removed in this pack. Circuits follow MI's voltage tiers."], mirror="6263A27182B2CE3D", section="Machines"),
    Q("mk2_elite_circuit", 4, 1, [item(MEK + "elite_control_circuit")], "Elite Control Circuit", subtitle="Mekanism's HV tier", deps=["mk2_adv_circuit", "t5_hv"], xp=150, desc=[
        "&eWhat:&r the circuit for elite-tier blocks, the Combiner, the Security Desk and the Solar Neutron Activator.",
        "&eHow:&r an &eMI digital circuit&r above two Reinforced Alloys and an Advanced Control Circuit (check JEI).",
        "&eTip:&r HV comes with polyethylene on the main path. Make a stack of these before upgrading factories."], mirror="71CF9E59F8F0B4A6", section="Machines"),
    Q("mk2_ult_circuit", 6, 1, [item(MEK + "ultimate_control_circuit")], "Ultimate Control Circuit", subtitle="Mekanism's EV tier", deps=["mk2_elite_circuit", "t6_pu"], xp=250, desc=[
        "&eWhat:&r the circuit behind Mekanism's best blocks: the Isotopic Centrifuge, QIO, the Quantum Entangloporter, the Dimensional Stabilizer, the MekaSuit and the Meka-Tool.",
        "&eHow:&r an &eMI processing unit&r above two Atomic Alloys and an Elite Control Circuit (check JEI).",
        "&eTip:&r this unlocks the rest of the page: ultimate factories, QIO, More Machine's big machines and Mekanism Extras."], mirror="1ABD22AA58E093A6", section="Machines"),

    # --- Teleportation, Robit, Digital Miner, QIO (y = -4.5 .. 2.5) ----------------------------
    Q("mk2_teleport_core", 6, -3, [item(MEK + "teleportation_core", 2)], "Teleportation Core", subtitle="The heart of everything that moves far", deps=["mk2_refined_obsidian", "mk2_atomic"], xp=120, desc=[
        "&eWhat:&r the part inside teleporters, the Digital Miner, QIO drive arrays and the Quantum Entangloporter.",
        "&eHow:&r Atomic Alloy, gold ingots, a diamond and ender pearls (check JEI).",
        "&eTip:&r you'll need at least four of these for this page alone. Automate Atomic Alloy early."]),
    Q("mk2_teleporter", 5, -4.5, [item(MEK + "teleporter"), item(MEK + "teleporter_frame", 9)], "Teleporter", subtitle="Step through a frame, arrive elsewhere", deps=["mk2_infuser", "mk2_teleport_core"], xp=150, optional=False, tokens=None, desc=[
        "&eWhat:&r a frame-and-controller portal that links to other teleporters, even across dimensions.",
        "&eHow:&r the controller is a Teleportation Core in steel casings with basic circuits. Frames are refined obsidian around refined glowstone. Build a 3x4 frame with the controller in it (check JEI).",
        "&eTip:&r set both ends to the same frequency, and give the sending end plenty of power."], mirror="7B0DFA55B4D8B16D", section="Big Builds"),
    Q("mk2_portable_tp", 7, -4.5, [item(MEK + "portable_teleporter")], "Portable Teleporter", subtitle="A teleporter in your pocket", deps=["mk2_chargepad", "mk2_teleport_core"], xp=100, optional=False, tokens=None, desc=[
        "&eWhat:&r a hand-held teleporter that jumps you to any teleporter frequency you own.",
        "&eHow:&r a Teleportation Core between two Energy Tablets and two basic circuits (check JEI). Charge it first.",
        "&eTip:&r the further the jump, the more energy it costs."], mirror="2EA0C74AE7366656", section="Gadgets"),
    Q("mk2_stabilizer", 4, -3, [item(MEK + "dimensional_stabilizer")], "Dimensional Stabilizer", subtitle="Keep the chunks loaded", deps=["mk2_refined_obsidian", "t6_pu"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r Mekanism's chunk loader. It keeps chunks around it running while you're away, so your factories never pause.",
        "&eHow:&r refined obsidian, Atomic Alloy, Ultimate Control Circuits (EV) and a diamond block (check JEI). Pick the chunks in its GUI.",
        "&eTip:&r load only what you need. Every loaded chunk costs server time."]),
    Q("mk2_entangloporter", 8, -3, [item(MEK + "quantum_entangloporter", 2)], "Quantum Entangloporter", subtitle="One frequency, two places, everything shared", deps=["mk2_teleport_core", "t6_pu"], xp=200, optional=False, tokens=None, desc=[
        "&eWhat:&r two Entangloporters on the same frequency act as one block: energy, items, fluids, chemicals and heat go in one and out the other, across any distance or dimension.",
        "&eChemistry:&r real quantum entanglement can't carry information or matter faster than light (the no-communication theorem). Mekanism takes a little artistic licence.",
        "&eHow:&r refined obsidian, Atomic Alloy, Ultimate Control Circuits (EV) and a Teleportation Core (check JEI).",
        "&eTip:&r a pair is the easiest way to pipe uranium hexafluoride or D-T fuel from a remote plant to your base."], mirror="7CC49360D07086B8", section="Big Builds"),

    # --- Machines and factories (y = 3 / 4.5) ---------------------------------------------------
    Q("mk2_smelter", 0, 3, [item(MEK + "energized_smelter")], "Energized Smelter", subtitle="A furnace that runs on FE", deps=["mk2_steel_casing"], xp=50, desc=[
        "&eWhat:&r Mekanism's electric furnace. It smelts anything a furnace can, takes upgrades, and is the base of the smelting factory.",
        "&eChemistry:&r electric heating is Joule heating: current through a resistance makes heat (P = I²R). No fuel, no smoke.",
        "&eHow:&r Basic Alloy, glass, a Basic Control Circuit and a steel casing (check JEI)."], mirror="488DBE69595F38F8", section="Machines"),
    Q("mk2_basic_factory", 2, 3, [anyof(factories("basic"))], "Basic Factory", subtitle="Three jobs at once", deps=["mk2_smelter"], xp=80, desc=[
        "&eWhat:&r a factory is a machine with several slots that work in parallel. A basic factory runs 3 operations at once.",
        "&eHow:&r craft any single machine (Energized Smelter, Enrichment Chamber, Crusher...) with Basic Control Circuits and Basic Alloy. Any factory type counts.",
        "&eTip:&r factories sort their own inputs with auto-sort in the GUI, so one input pipe is enough."]),
    Q("mk2_adv_factory", 4, 3, [anyof(factories("advanced"))], "Advanced Factory", subtitle="Five jobs at once", deps=["mk2_basic_factory"], xp=120, desc=[
        "&eWhat:&r 5 parallel slots, and faster with upgrades.",
        "&eHow:&r upgrade a basic factory in the crafting grid with Advanced Control Circuits, Infused Alloy and osmium, or use a Tier Installer on a placed one.",
        "&eTip:&r upgrading keeps the factory's type, so plan which machines you want at five slots."]),
    Q("mk2_elite_factory", 6, 3, [anyof(factories("elite"))], "Elite Factory", subtitle="Seven jobs at once", deps=["mk2_adv_factory"], xp=180, desc=[
        "&eWhat:&r 7 parallel slots. Pair an Elite Purifying or Injecting Factory with your ore line and the bottleneck moves elsewhere.",
        "&eHow:&r upgrade an advanced factory with Elite Control Circuits and Reinforced Alloy (check JEI).",
        "&eTip:&r the factory GUI shows each slot's progress; idle slots mean the input line is too slow."]),
    Q("mk2_ult_factory", 8, 3, [anyof(factories("ultimate"))], "Ultimate Factory", subtitle="Nine jobs at once", deps=["mk2_elite_factory"], xp=300, size=1.5, shape="hexagon", desc=[
        "&6Nine tasks in one box, all at once. You remember doing many things at once without effort.&r",
        "&eWhat:&r 9 parallel slots, the top of base Mekanism. Mekanism Extras goes further (see the bottom band).",
        "&eHow:&r upgrade an elite factory with Ultimate Control Circuits and Atomic Alloy (check JEI).",
        "&eTip:&r add Speed and Energy upgrades: speed raises power use, energy upgrades bring it back down."]),
    Q("mk2_installer", 1, 4.5, [anyof([MEK + t + "_tier_installer" for t in ("basic", "advanced", "elite", "ultimate")])], "Tier Installers", subtitle="Upgrade without breaking", deps=["mk2_tier_basic"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r right-click a placed machine with a Tier Installer to turn it into the next tier, keeping its contents and settings.",
        "&eHow:&r the basic installer needs a Basic Control Circuit; the advanced one needs an Advanced Control Circuit (MV).",
        "&eTip:&r a plain machine plus a basic installer becomes a basic factory."], mirror="090B564935D7A8F5", section="Upgrades"),
    Q("mk2_sawmill", 3, 4.5, [item(MEK + "precision_sawmill")], "Precision Sawmill", subtitle="More planks, plus sawdust", deps=["mk2_steel_casing"], xp=50, desc=[
        "&eWhat:&r cuts logs into more planks than hand crafting, often with a bonus of sawdust, and breaks wooden items back down.",
        "&eChemistry:&r wood is about 40-50% cellulose (chains of glucose), with hemicellulose and lignin gluing the fibres together. Sawdust is the same polymers, finely divided.",
        "&eHow:&r iron, Infused Alloy, a Basic Control Circuit and a steel casing (check JEI).",
        "&eTip:&r sawdust feeds wood gasification in the PRC and the Cardboard Box."], mirror="7ECA0633AF1AEC19", section="Machines"),
    Q("mk2_ore_factory", 5, 4.5, [anyof(factories("basic", ("purifying", "injecting")) + factories("advanced", ("purifying", "injecting")) +
                                         factories("elite", ("purifying", "injecting")) + factories("ultimate", ("purifying", "injecting")))],
      "Factories for the Ore Line", subtitle="Purifying and injecting in parallel", deps=["mk2_adv_factory", "t4_ore4"], xp=150, desc=[
        "&eWhat:&r a Purifying (O₂, 3x) or Injecting (HCl, 4x) Factory runs several ores at once. Ore processing is where factories pay off most.",
        "&eChemistry:&r the gas is consumed per operation: oxygen oxidises the ore surface into clumps, hydrogen chloride attacks it into shards. More slots means more gas, so size the separator to match.",
        "&eHow:&r build the factory from a Purification Chamber or Chemical Injection Chamber (both MV in this pack). Any tier and either type counts.",
        "&eTip:&r feed the gas into the factory's gas side with pressurized tubes, the same as the single machine."]),
    Q("mk2_combiner", 7, 4.5, [item(MEK + "combiner")], "Combiner", subtitle="Two inputs pressed into one block", deps=["mk2_elite_circuit"], xp=80, optional=False, tokens=None, desc=[
        "&eWhat:&r the Combiner presses a main input together with a second block, for example flint + cobblestone into gravel, or 4 obsidian dust + cobbled deepslate back into obsidian.",
        "&eChemistry:&r pressing powders into a solid below their melting point is sintering; it's how ceramics and many metal parts are made.",
        "&eHow:&r Reinforced Alloy, &eElite Control Circuits&r (HV) and a steel casing (check JEI). Press U on it in JEI for every recipe."], mirror="566C1DBA9829E328", section="Machines"),
    Q("mk2_upgrades", 2, 6, [item(MEK + "upgrade_speed")], "Speed Upgrade", subtitle="Faster machines, bigger bills", deps=["mk2_steel_casing", "mk2_glass"], xp=80, desc=[
        "&eWhat:&r slot them into any Mekanism machine. Speed upgrades make it work faster; energy upgrades cut its power use and enlarge its buffer.",
        "&eHow:&r Infused Alloy and glass around osmium dust (speed) or gold dust (energy). A machine takes up to 8 of each.",
        "&eTip:&r speed upgrades raise power use faster than they raise speed. Balance every speed upgrade with an energy upgrade."], mirror="3C8D9278B81BB37A", section="Upgrades"),
    Q("mk2_upgrade_set", 2, 7.5, [item(MEK + "upgrade_filter")],
      "Filter Upgrade", subtitle="Choose what the pump pulls up", deps=["mk2_steel_casing", "mk2_glass"], xp=150, optional=False, tokens=None, desc=[
        "&eWhat:&r the Filter upgrade goes in an Electric Pump. With it the pump pulls heavy water out of ordinary water blocks instead of plain water.",
        "&eChemistry:&r heavy water is D₂O: water whose hydrogen atoms carry an extra neutron. About 1 molecule in 6,400 in seawater has a deuterium atom in it.",
        "&eHow:&r Infused Alloy and glass around tin dust (check JEI). One per pump.",
        "&eTip:&r heavy water is the start of deuterium, and later of fusion fuel."], mirror="763FB27929E053BE", section="Upgrades"),
    Q("mk2_cardboard", 4, 6, [item(MEK + "cardboard_box")], "Moving Day", subtitle="Secret: pack a block in a box", deps=["mk2_sawmill"], xp=50, secret=True, loot="secret", desc=[
        "&eWhat:&r a Cardboard Box made from sawdust. Right-click almost any block (even a full chest or a spawner) to pack it up and carry it.",
        "&eChemistry:&r cardboard is pressed cellulose fibre, the same polymer that makes up most of the sawdust.",
        "&eTip:&r boxes can't pick up everything; blocks on the mod's blacklist won't pack."], mirror="24BA664B60E49461", section="Gadgets"),
    Q("mk2_ore_states", 6, 6, [item(MEK + "crystal_iron"), item(MEK + "shard_iron"), item(MEK + "clump_iron"), item(MEK + "dirty_dust_iron")],
      "Challenge: Every Stage of Iron", subtitle="Crystal, shard, clump, dirty dust", deps=["mk2_ore_factory", "t4_ore5"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the full 5x chain, one stage of each: crystal (5x) → shard (4x) → clump (3x) → dirty dust → dust.",
        "&eChemistry:&r sulfuric acid dissolves the iron oxide into iron sulfate (Fe₂O₃ + 3H₂SO₄ → Fe₂(SO₄)₃ + 3H₂O). Washing rinses out insoluble rock, and crystallising pulls pure salt back out of solution.",
        "&eHow:&r dissolve, wash and crystallise, then inject crystals with HCl, purify shards with O₂, crush clumps. Dirty dust goes to the MI Centrifuge for byproducts.",
        "&eTip:&r each stage can also be fed raw ore directly, so a half-built line still gives 3x or 4x."]),
    Q("mk2_heaters", 8, 6, [item(MEK + "resistive_heater")], "Resistive Heater", subtitle="Electricity in, heat out", deps=["mk2_conductors", "pw_brine"], xp=120, desc=[
        "&eWhat:&r the Resistive Heater turns FE into heat; the Fuelwood Heater burns furnace fuel. Thermodynamic Conductors carry the heat to where it's needed, such as a Thermal Evaporation Plant.",
        "&eChemistry:&r evaporation speeds up with temperature because more water molecules have enough energy to escape the surface. The conductors are copper in steel: copper conducts heat about 8 times better than steel.",
        "&eHow:&r heaters need a steel casing and a circuit or Energy Tablet; conductors are steel and copper (check JEI). Watch the plant's temperature in its GUI.",
        "&eTip:&r a hot plant in a desert biome runs much faster than a cold one in the snow."], mirror="21F3379C904BFD50", section="Pipes and Storage"),
    Q("mk2_salt", 10, 6, [item(MEK + "salt", 16)], "Salt and Sodium", subtitle="What brine leaves behind", deps=["mk2_heaters", "t4_separator"], xp=120, desc=[
        "&eWhat:&r brine from the evaporation plant crystallises into salt, and splits into sodium and chlorine in the Electrolytic Separator.",
        "&eChemistry:&r real sodium is made by electrolysing molten NaCl (2NaCl → 2Na + Cl₂, the Downs cell). Salt is also a classic HCl source: NaCl + H₂SO₄ → NaHSO₄ + HCl.",
        "&eHow:&r Chemical Crystallizer: 15 mB brine → 1 salt. Electrolytic Separator: brine → sodium + chlorine. Salt also counts as a hydrogen chloride source in an HCl machine's chemical item slot (press U on Salt in JEI).",
        "&eTip:&r sodium is the coolant for the best fission setups (see Sodium Coolant on the Power and Beyond page)."]),

    # --- Pressurized reactions, substrate, HDPE and Meka-gear (y = 9 / 10.5) -------------------
    Q("mk2_dynamic_tank", 0, 9, [item(MEK + "dynamic_tank", 24), item(MEK + "dynamic_valve", 2)], "Dynamic Tank", subtitle="Your first Mekanism multiblock", deps=["mk2_chem_tanks", "mk2_fluid_tanks", "t3_mekcircuit"], xp=100, desc=[
        "&eWhat:&r a hollow multiblock tank of any size from 3x3x3 up, for huge amounts of a fluid or a chemical.",
        "&eHow:&r dynamic tank blocks (steel and a bucket) for the frame, structural glass for walls, and valves to pipe in and out. The layout is in &eJust Enough Mekanism Multiblocks&r in JEI.",
        "&eTip:&r one dynamic tank block is also a part in the PRC and the Chemical Oxidizer."], mirror="1796E08BBDC09B84", section="Pipes and Storage"),
    Q("mk2_prc", 2, 9, [item(MEK + "pressurized_reaction_chamber")], "Pressurized Reaction Chamber", subtitle="Solid, liquid and gas in, products out", deps=["mk2_steel_casing", "t4_separator"], xp=120, desc=[
        "&eWhat:&r the PRC reacts an item, a fluid and a gas together under pressure. It makes substrate, HDPE, plutonium and polonium pellets, and gasifies coal and wood.",
        "&eChemistry:&r pressure pushes gas molecules closer together so they collide with the other reactants more often. Le Chatelier: a reaction that shrinks gas volume is favoured by high pressure.",
        "&eHow:&r Basic Control Circuits, Infused Alloy, steel, an Enrichment Chamber, a Dynamic Tank and chemical tanks (check JEI). Press &eU&r on it in JEI for every recipe.",
        "&eTip:&r it often makes two products at once (an item and a gas). Give each output side its own pipe."], mirror="71869B1D81D6A7EF", section="Chemical Machines"),
    Q("mk2_substrate", 4, 9, [item(MEK + "substrate", 16)], "Substrate", subtitle="Bio fuel and hydrogen into ethene", deps=["mk2_prc"], xp=120, desc=[
        "&eWhat:&r substrate is Mekanism's polymer seed: a little of it, with ethene and oxygen, becomes HDPE.",
        "&eChemistry:&r plant matter can become ethylene: real bio-ethylene is made by dehydrating bioethanol (C₂H₅OH → C₂H₄ + H₂O). Polyethylene is then thousands of C₂H₄ units joined on a catalyst.",
        "&eHow:&r PRC: 2 bio fuel + water + hydrogen → substrate + ethene. Then substrate + water + ethene → 8 substrate (plus a little O₂). Check JEI for amounts.",
        "&eTip:&r MI ethylene is tagged as ethene in this pack, so your distillation tower can feed this line too."]),
    Q("mk2_hdpe_parts", 6, 9, [item(MEK + "hdpe_sheet", 8), item(MEK + "hdpe_rod", 2), item(MEK + "hdpe_stick", 4)], "HDPE Parts", subtitle="Sheets, rods and sticks of plastic", deps=["mk2_substrate", "t5_hdpe"], xp=150, desc=[
        "&eWhat:&r HDPE pellets shaped into sheets, rods and sticks: parts for the Solar Neutron Activator, module bases, the MekaSuit and the Meka-Tool.",
        "&eChemistry:&r high-density polyethylene has straight chains with few branches, so they pack tightly. That makes it stiffer and stronger than the bendy LDPE in plastic bags.",
        "&eHow:&r PRC: substrate + ethene + oxygen → HDPE pellet (or use your MI line from the main path). Then shape pellets in the crafting grid (check JEI).",
        "&eTip:&r the MekaSuit alone eats dozens of sheets. Automate the pellets."]),
    Q("mk2_pigment", 1, 10.5, [item(MEK + "pigment_extractor"), item(MEK + "pigment_mixer"), item(MEK + "painting_machine")], "Pigments", subtitle="Colour as a chemical", deps=["mk2_steel_casing", "t4_mv", "t5_hv"], xp=80, optional=False, tokens=None, desc=[
        "&eWhat:&r the Pigment Extractor pulls coloured pigment out of dyes; the Painting Machine applies it to blocks and items.",
        "&eChemistry:&r a pigment's colour comes from the light its molecules absorb: indigo absorbs orange-red light, so it looks blue.",
        "&eHow:&r the extractor needs Basic Circuits; the Painting Machine needs an Advanced Control Circuit (MV)."], mirror="07084582F9562740", section="Big Builds"),
    Q("mk2_coal_gas", 3, 10.5, [item(MEK + "dust_sulfur")], "Sulfur, the Key Element", subtitle="Every chemical machine, one yellow dust", deps=["mk2_chem_infuser", "mk2_oxidizer", "mk2_dissolution", "mk2_enrich", "mk2_condensentrator", "mk2_prc"], xp=100, optional=False, tokens=None, desc=[
        "&6Yellow dust, and every acid you will ever need. You remember sulfur as the first gift of volcanoes.&r",
        "&eWhat:&r sulfur dust: the start of sulfur dioxide, sulfur trioxide and sulfuric acid, the gas behind Mekanism's 5x ore line.",
        "&eChemistry:&r the PRC can gasify coal (C + H₂O → CO + H₂, with a little O₂ burning to keep it hot) and leaves the coal's sulfur behind. The Oxidizer then burns S + O₂ → SO₂.",
        "&eHow:&r PRC with coal or coal dust, water and O₂ (check JEI), or crush sulfur from other sources. Every machine before this quest has a job in the acid line.",
        "&eTip:&r more sulfur is the usual bottleneck of a 5x line. Automate a source early."], mirror="7276892E129A739B", section="Chemical Machines", size=2.0, shape="gear", loot="t4"),
    Q("mk2_chem_plant", 5, 10.5, [item(MEK + "chemical_infuser"), item(MEK + "chemical_oxidizer"), item(MEK + "electrolytic_separator"), item(MEK + "pressurized_reaction_chamber"),
                                  item(MEK + "chemical_washer"), item(MEK + "chemical_crystallizer"), item(MEK + "chemical_dissolution_chamber"),
                                  item(MEK + "isotopic_centrifuge"), item(MEK + "solar_neutron_activator"), item(MEK + "sps_port")],
      "Challenge: The Full Chemical Plant", subtitle="One of every Mekanism chemical machine", deps=["mk2_prc", "t7_sps"], xp=500, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each of Mekanism's ten chemical machines, from the Chemical Infuser to an SPS port.",
        "&eChemistry:&r together they cover the unit operations of a real chemical plant: reaction, oxidation, electrolysis, washing, crystallisation, dissolution and isotope separation.",
        "&eHow:&r most are on the main path (see the links on the left). The washer, crystallizer and dissolution chamber are MV in this pack; the centrifuge needs Ultimate Control Circuits (EV).",
        "&eTip:&r an optional collection. Keep spares in a chest as you build each one."]),

    # --- Transmitters and logistics (y = 12 / 13.5) ---------------------------------------------
    Q("mk2_cables", 0, 12, [anyof([MEK + t + "_universal_cable" for t in ("basic", "advanced", "elite", "ultimate")])], "Universal Cable", subtitle="Energy, Mekanism style", deps=["mk2_tablet"], xp=50, desc=[
        "&eWhat:&r Universal Cable carries FE between generators, cubes and machines. Any tier counts here.",
        "&eChemistry:&r a cable is a conductor: electrons drift through the metal, and its resistance turns a little of the power into heat (P = I²R).",
        "&eHow:&r steel with redstone, 8 per craft. Higher tiers wrap 8 of the tier below around an alloy (check JEI).",
        "&eTip:&r cables of one type join into one network. Colour them with a Configurator to keep two networks apart."], mirror="62827AA1AD29A222", section="Energy"),
    Q("mk2_transporter", 2, 12, [anyof([MEK + t + "_logistical_transporter" for t in ("basic", "advanced", "elite", "ultimate")])], "Logistical Transporters", subtitle="Item pipes you can see", deps=["mk2_configurator"], xp=60, desc=[
        "&eWhat:&r item pipes that carry stacks to the nearest inventory that will take them, and show the items moving.",
        "&eHow:&r steel around a Basic Control Circuit, 8 per craft.",
        "&eTip:&r a transporter's colour (set with the Configurator) only delivers into sides of the same colour."], mirror="60ECCCAB66AAC05D", section="Pipes and Storage"),
    Q("mk2_sorter", 4, 12, [item(MEK + "logistical_sorter")], "Logistical Sorter", subtitle="Pull, filter, send", deps=["mk2_transporter"], xp=80, desc=[
        "&eWhat:&r pulls items out of the inventory behind it and sends them down transporters by filter: item, tag, mod or material.",
        "&eHow:&r iron, a piston and a Basic Control Circuit. It is also a part of the Digital Miner.",
        "&eTip:&r give each filter a colour, and the items arrive only at inventories with that colour."]),
    Q("mk2_transporter_types", 1, 13.5, [item(MEK + "diversion_transporter", 2), item(MEK + "restrictive_transporter", 2)], "Diversion and Restriction", subtitle="Redstone-switched and last-resort routes", deps=["mk2_transporter"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r a Diversion Transporter opens or closes with redstone; a Restrictive Transporter is only used when no other path works.",
        "&eHow:&r steel and iron bars, plus redstone for the diversion type (check JEI).",
        "&eTip:&r a restrictive segment in front of an overflow chest makes it fill last."]),
    Q("mk2_transporter_tiers", 3, 13.5, [item(MEK + "elite_logistical_transporter", 8), item(MEK + "ultimate_logistical_transporter", 8)], "Faster Transporters", subtitle="Elite and ultimate item pipes", deps=["mk2_transporter"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r higher tiers move bigger stacks, faster.",
        "&eHow:&r 8 transporters of the tier below around Reinforced Alloy (elite) or Atomic Alloy (ultimate).",
        "&eTip:&r the line only needs to be as fast as its slowest machine. Upgrade the trunk, not every branch."]),
    Q("mk2_seismic", 5, 13.5, [item(MEK + "seismic_vibrator"), item(MEK + "seismic_reader")], "Seismic Survey", subtitle="Listen to the ground", deps=["mk2_cables"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r the Seismic Vibrator shakes the ground beneath it; the Seismic Reader then shows every block straight down to bedrock.",
        "&eChemistry:&r real prospectors use reflection seismology: sound waves bounce off layers of different density, and the echo times map oil and ore bodies.",
        "&eHow:&r vibrator: tin, lapis, Basic Control Circuits and a steel casing; reader: steel, lapis and an Energy Tablet (check JEI).",
        "&eTip:&r rich ore deposits sit at metal-specific depths. Survey before you dig."]),
    Q("mk2_assemblicator", 7, 13.5, [item(MEK + "formulaic_assemblicator")], "Formulaic Assemblicator", subtitle="An autocrafter with a memory", deps=["mk2_transporter"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r saves a crafting recipe on a Crafting Formula and crafts it whenever ingredients arrive.",
        "&eHow:&r steel, a crafter, a chest, Basic Control Circuits and a steel casing (check JEI). Encode the recipe on a formula in its GUI.",
        "&eTip:&r handy for alloy blocks or circuits until your AE2 autocrafting is up."]),
    Q("mk2_nutrition", 9, 13.5, [item(MEK + "nutritional_liquifier"), item(MEK + "canteen")], "Nutritional Paste", subtitle="Dinner, liquefied", deps=["mk2_cables"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r the Nutritional Liquifier turns food into nutritional paste; a Canteen carries it and feeds you when you drink.",
        "&eChemistry:&r food energy is chemical energy in carbohydrates, fats and proteins. Mashing food changes its form, not its calories.",
        "&eHow:&r liquifier: redstone, bowls, Basic Control Circuits and a steel casing. Canteen: tin and a bowl (check JEI). The MekaSuit has a module that drinks paste for you."]),
    Q("mk2_security", 11, 13.5, [anyof([MEK + "personal_barrel", MEK + "personal_chest"])], "Mine, Not Yours", subtitle="Storage that only opens for you", deps=["mk2_transporter"], xp=80, optional=False, tokens=None, desc=[
        "&eWhat:&r a Personal Chest only opens for its owner. The Security Desk sets who may use your Mekanism blocks: you, a trusted list, or everyone.",
        "&eHow:&r personal chest: steel, glass, chests and a Basic Control Circuit. Security desk: steel, glass, a Network Reader and &eElite Control Circuits&r (HV) (check JEI).",
        "&eTip:&r on a shared server, lock your reactor controls."], mirror="1F8B4F648EB5A0DC", section="Pipes and Storage"),

    # --- ATM10-alignment round (2026-10-19): items worth a quest that the page didn't ask for yet ---
    Q("mk2_enriched", 0, 0, [anytag("mekanism:enriched")], "Enriched Infusion",
      subtitle="Concentrate the infuse before you use it", deps=["mk2_enrich"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r the Enrichment Chamber turns coal, charcoal and redstone into enriched forms. One enriched item gives the Metallurgic Infuser far more infuse than the raw material.",
        "&eChemistry:&r charcoal is nearly pure carbon left after heating wood without air (pyrolysis). Enriching it is like refining coal into coke: less ash, more carbon per gram.",
        "&eHow:&r crush charcoal into Charcoal Dust in the Crusher, then put coal, charcoal or redstone through the Enrichment Chamber (check JEI).",
        "&eTip:&r feed enriched items into the infuser's left slot: one stack lasts a long time."], mirror="0F326EEEC2EBE4E5", section="Machines"),
    Q("mk2_obsidian_dust", 0, 0, [item(MEK + "dust_refined_obsidian"), item(MEK + "dust_obsidian", 4)], "Obsidian Dusts",
      subtitle="The road to refined obsidian", deps=["mk2_infuser", "mk2_crusher"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r obsidian dust, and refined obsidian dust made by infusing it with diamond. Refined obsidian dust becomes Atomic Alloy and refined obsidian ingots.",
        "&eChemistry:&r obsidian is volcanic glass, mostly SiO₂ (about 70%) with aluminium, iron and alkali oxides, frozen before it could crystallise.",
        "&eHow:&r crush obsidian in the Crusher, then Metallurgic Infuser: obsidian dust + diamond infusion → refined obsidian dust (check JEI).",
        "&eTip:&r a Combiner can turn spare obsidian dust back into obsidian later."], mirror="5B556192F060F3F1", section="Machines"),
    Q("mk2_bio_fuel", 0, 0, [item(MEK + "bio_fuel")], "Bio Fuel",
      subtitle="Crush plants into fuel", deps=["mk2_crusher"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r bio fuel is crushed plant matter. It burns in the Bio-Generator and is the start of the substrate line in the PRC.",
        "&eChemistry:&r plants store sunlight as sugars and cellulose: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Burning or digesting them gives that energy back.",
        "&eHow:&r put seeds, saplings, crops or other plant items into the Crusher (press U on Bio Fuel in JEI to see what counts).",
        "&eTip:&r a Mystical Agriculture or Farmer's Delight farm feeding a Crusher makes it renewable."], mirror="081DC030A0546549", section="Machines"),
    Q("mk2_lab_tools", 0, 0, [item(MEK + "dictionary")], "Dictionary",
      subtitle="Read any item's tags", deps=["mk2_chargepad"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r the Dictionary shows the tags of any item or block you click. The Gauge Dropper sucks a little fluid or gas out of a tank, or dumps a tank you don't want.",
        "&eHow:&r Dictionary: a book under a Basic Control Circuit. Gauge Dropper: osmium over glass panes (check JEI).",
        "&eTip:&r the Dictionary is the fastest way to find out which tag a filter needs (c:dusts/iron, c:ores and so on)."], mirror="041365A540BF5A03", section="Gadgets"),
    Q("mk2_chargepad", 0, 0, [item(MEK + "chargepad")], "Chargepad",
      subtitle="Stand on it, charge everything", deps=["mk2_tablet"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r the Chargepad charges the FE items in your inventory (and a Robit) while you stand on it.",
        "&eHow:&r polished blackstone pressure plates over steel and an Energy Tablet (check JEI). Feed it power from below.",
        "&eTip:&r put one in front of your storage. Every visit tops up your tools."], mirror="4274E777FB60BA28", section="Energy"),
    Q("mk2_fluid_tanks", 0, 0, [anyof([MEK + t + "_fluid_tank" for t in ("basic", "advanced", "elite", "ultimate")])], "Portable Fluid Tanks",
      subtitle="Tanks that keep their contents", deps=["mk2_pipes"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r Mekanism fluid tanks keep their fluid when broken, so you can carry a tank of acid to another machine. Each tier holds more and moves it faster.",
        "&eHow:&r basic: iron and Basic Alloy. Advanced: a basic tank ringed with iron and Infused Alloy (check JEI). They stack on top of each other and pass fluid down.",
        "&eTip:&r right-click a tank with a bucket to fill or empty it; tanks also fill buckets placed in their GUI."], mirror="7952DA35B4F5C598", section="Pipes and Storage"),
    Q("mk2_elite_tanks", 0, 0, [item(MEK + "elite_fluid_tank"), item(MEK + "elite_chemical_tank")], "Elite Tanks",
      subtitle="Bigger tanks for fluids and gases", deps=["mk2_fluid_tanks"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r elite tanks hold far more than basic ones. The chemical tank is the gas version, for H₂, O₂, Cl₂ or SO₂.",
        "&eHow:&r the advanced tank ringed with Reinforced Alloy and iron (fluid) or osmium (chemical). Check JEI.",
        "&eTip:&r a chemical tank under an Electrolytic Separator smooths out its output while the rest of the line catches up."]),
    Q("mk2_liquid_gases", 0, 0, [item(MEK + "hydrogen_bucket"), item(MEK + "oxygen_bucket")], "Liquefied Gases",
      subtitle="Hydrogen and oxygen, cold enough to pour", deps=["t4_vapor", "mk2_fluid_tanks"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r the Rotary Condensentrator turns gases into liquids and back. Liquid hydrogen and oxygen fit in buckets and ordinary fluid tanks.",
        "&eChemistry:&r hydrogen boils at -253 °C and oxygen at -183 °C. Liquid oxygen is pale blue and is attracted to a magnet, because O₂ has two unpaired electrons.",
        "&eHow:&r set the condensentrator to condensing, feed it H₂ or O₂ from a separator, and pipe the liquid into a fluid tank. Fill buckets from the tank.",
        "&eTip:&r rockets in this pack burn fuel and oxygen; liquids are how big amounts travel."]),
    Q("mk2_liquid_acids", 0, 0, [item(MEK + "hydrogen_chloride_bucket"), item(MEK + "sulfuric_acid_bucket")], "Acids by the Bucket",
      subtitle="HCl and H₂SO₄ as liquids", deps=["mk2_liquid_gases", "t4_mek_acid", "t4_hcl"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r the same machine liquefies hydrogen chloride and sulfuric acid, so other mods' machines (and the Undergarden catalyst) can use Mekanism's acids.",
        "&eChemistry:&r hydrogen chloride dissolved in water is hydrochloric acid; sulfuric acid is already a liquid at room temperature and boils at 337 °C.",
        "&eHow:&r Rotary Condensentrator on condensing mode, fed from your contact process or HCl line (check JEI).",
        "&eTip:&r one bucket is 1,000 mB, the same as 1,000 mB of the gas form."]),
    Q("mk2_adv_transmitters", 0, 0, [item(MEK + "advanced_universal_cable", 8), item(MEK + "advanced_mechanical_pipe", 8), item(MEK + "advanced_pressurized_tube", 8),
                                     item(MEK + "advanced_logistical_transporter", 8), item(MEK + "advanced_thermodynamic_conductor", 8)],
      "Advanced Transmitters", subtitle="The second tier of all five", deps=["mk2_transporter", "t3_infused"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r every Mekanism transmitter has four tiers. Advanced ones carry several times more energy, fluid, gas, items or heat than basic.",
        "&eHow:&r eight basic transmitters around Infused Alloy make eight advanced ones (check JEI).",
        "&eChemistry:&r gas flow through a pipe rises with its cross-section and the pressure difference; Mekanism just lets you buy the bigger pipe.",
        "&eTip:&r upgrade the trunk line from the separator first; the branches can stay basic."]),
    Q("mk2_ult_cable", 0, 0, [item(MEK + "ultimate_universal_cable", 8)], "Ultimate Universal Cable",
      subtitle="Enough power for a reactor hall", deps=["mk2_adv_transmitters"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r the top tier of power cable: tens of thousands of times what a basic cable carries.",
        "&eHow:&r elite cables around Atomic Alloy (elite cables use Reinforced Alloy). Check JEI.",
        "&eChemistry:&r real cables lose power as heat (P = I²R); fusion plants send power at high voltage so the current, and the loss, stays low."]),
    Q("mk2_electric_bow", 0, 0, [item(MEK + "electric_bow")], "Electric Bow",
      subtitle="A bow that never needs repairs", deps=["mk2_chargepad"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r an FE-powered bow. Its fire mode sets arrows alight.",
        "&eHow:&r string, Infused Alloy and an Energy Tablet (check JEI). Charge it on a Chargepad.",
        "&eTip:&r it has no durability, only charge."], mirror="4E7823C2FCEBE4DC", section="Gadgets"),
    Q("mk2_flamethrower", 0, 0, [item(MEK + "flamethrower")], "Flamethrower",
      subtitle="Hydrogen, lit", deps=["mk2_chargepad", "t4_separator", "t4_mv"], xp=80, optional=False, tokens=None, desc=[
        "&eWhat:&r a hand-held flamethrower that burns hydrogen gas. One mode smelts the blocks it hits.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O, about 286 kJ per mole of hydrogen. The flame is nearly invisible in daylight and leaves only water vapour.",
        "&eHow:&r tin, bronze, a basic chemical tank, flint and steel and an &eAdvanced Control Circuit&r (MV). Fill it with H₂ from the separator's output or a chemical tank.",
        "&eTip:&r never point it at your storage."], mirror="109310AF19AAC482", section="Gadgets"),
    Q("mk2_pigment_mixer", 0, 0, [item(MEK + "pigment_mixer")], "Pigment Mixer",
      subtitle="Two colours in, one colour out", deps=["mk2_pigment"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r mixes two pigments into a new one, for colours no single dye gives.",
        "&eChemistry:&r pigments mix subtractively: each absorbs part of the spectrum, so yellow + cyan leaves only green to reflect.",
        "&eHow:&r Reinforced Alloy, HDPE rods, a steel casing and &eElite Control Circuits&r (HV). Check JEI."]),

    # --- Mekanism Tools armour (y = 19.5 / 21) --------------------------------------------------
    Q("mk2_armor_osmium", 0, 19.5, armour("osmium"), "Osmium Armour", optional=True, subtitle="The densest metal, worn", deps=["mk2_intro"], xp=100, desc=[
        "&eWhat:&r Mekanism Tools adds a full armour set for each of its metals. Osmium is the first, and tougher than iron.",
        "&eChemistry:&r osmium is the densest natural element (22.6 g/cm³). Real osmium is brittle and its oxide, OsO₄, is volatile and very toxic, so nobody actually wears it.",
        "&eHow:&r osmium ingots in the usual armour shapes (check JEI).",
        "&eTip:&r bronze, steel and lapis sets exist too; see JEI for their stats."]),
    Q("mk2_armor_obsidian", 2, 19.5, armour("refined_obsidian"), "Refined Obsidian Armour", optional=True, subtitle="The best of Mekanism Tools", deps=["mk2_armor_osmium", "tc_obsidian_paxel"], xp=250, desc=[
        "&eWhat:&r the strongest Mekanism Tools armour: high protection and toughness, good until the MekaSuit.",
        "&eChemistry:&r obsidian is volcanic glass: lava cooled too fast for crystals to form. Infusing it with diamond and pressing it with osmium makes Mekanism's refined form.",
        "&eHow:&r refined obsidian ingots from the Osmium Compressor, in armour shapes (check JEI)."]),
    Q("mk2_armor_glowstone", 4, 21, armour("refined_glowstone"), "Refined Glowstone Armour", subtitle="Light, pressed into metal", deps=["mk2_armor_obsidian"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the other Osmium Compressor metal as an armour set. Check JEI for how it compares with refined obsidian.",
        "&eChemistry:&r real glow-in-the-dark materials store energy in their crystal and release it as light (phosphorescence); glowstone is Minecraft's version.",
        "&eHow:&r Osmium Compressor: glowstone dust + osmium → refined glowstone ingots, then armour shapes."]),


    # --- ATM10 mirror round (2026-10-20): one quest per ATM10 Mekanism quest we have the items for -------------
    # Osmium and steel
    Q("mk2_osmium", 0, 0, [item(MEK + "ingot_osmium")], "Osmium", subtitle="Mekanism's own metal", deps=["mk2_intro"], xp=30,
      mirror="6F62B5510FA881CD", section="Osmium and Steel", desc=[
        "&eWhat:&r osmium is the metal in almost every Mekanism machine, cable and upgrade.",
        "&eChemistry:&r osmium (Os, element 76) is a platinum-group metal and the densest element known, about 22.6 g/cm³.",
        "&eHow:&r mine osmium ore underground and smelt it, or run it through your ore line for more per ore.",
        "&eTip:&r you will want stacks of it. Put osmium at the top of your ore processing list."]),
    Q("mk2_tips", 0, 0, [tick()], "Reading a Machine", subtitle="Colours, sides and multiblocks", deps=["mk2_intro"], xp=10,
      optional=True, tokens=1, mirror="4A1C8125896F7F1A", section="Osmium and Steel", icon=MEK + "configurator", desc=[
        "&eWhat:&r every Mekanism machine has a side configuration tab. Each colour is a slot or tank, and each side of the block can be set to one of them.",
        "&eHow:&r open a machine and click the side tab on its GUI, or use the Configurator in the world. Multiblock layouts are in &eJust Enough Mekanism Multiblocks&r in JEI.",
        "&eTip:&r auto-eject on the output side saves you a pump or a transporter."]),
    Q("mk2_infuser", 0, 0, [item(MEK + "metallurgic_infuser")], "Metallurgic Infuser", subtitle="Soak a metal, make an alloy", deps=["mk2_osmium"],
      xp=60, size=1.5, shape="hexagon", mirror="162CE44400A63575", section="Osmium and Steel", desc=[
        "&6A furnace that adds rather than burns. Your hands remember this kind of patience.&r",
        "&eWhat:&r the Metallurgic Infuser pushes carbon, redstone, diamond or refined obsidian into a metal. It is how every Mekanism alloy and steel starts.",
        "&eChemistry:&r carburising is real: hot iron soaks up carbon from its surroundings and becomes steel. Mekanism uses the same idea for every alloy.",
        "&eHow:&r iron, osmium, redstone and a furnace (check JEI). Put the infuse material in the left slot and the metal in the middle."]),
    Q("mk2_infused_alloy", 0, 0, [item(MEK + "alloy_infused")], "Infused Alloy", subtitle="Iron and redstone, fused", deps=["mk2_infuser"],
      xp=40, mirror="166971866A9234C7", section="Osmium and Steel", desc=[
        "&eWhat:&r the first Mekanism alloy. It goes into energy tablets, advanced circuits, upgrades and the second tier of everything.",
        "&eHow:&r Metallurgic Infuser: iron ingot + redstone infusion.",
        "&eTip:&r enriched redstone from the Enrichment Chamber gives far more infuse per item."]),
    Q("mk2_basic_circuit", 0, 0, [item(MEK + "basic_control_circuit")], "Basic Control Circuit", subtitle="Mekanism's LV tier",
      deps=["mk2_infuser", "t3_mekcircuit"], xp=40, mirror="0498A578D0EC3254", section="Osmium and Steel", desc=[
        "&eWhat:&r the circuit inside every basic Mekanism machine.",
        "&eHow:&r in this pack it needs an &eMI analog circuit&r (LV) with osmium and Basic Alloy (check JEI). The infuser shortcut is removed.",
        "&eTip:&r make a stack. Almost every quest on this page eats a few."]),
    Q("mk2_steel", 0, 0, [anytag("c:ingots/steel")], "Steel", subtitle="Iron plus carbon", deps=["mk2_infuser"], xp=40,
      mirror="4B35C01F5D0AAC58", section="Osmium and Steel", desc=[
        "&eWhat:&r steel ingots: the frame of every Mekanism casing, cable and tank.",
        "&eChemistry:&r steel is iron with about 0.2-2% carbon. The carbon atoms sit between the iron atoms and stop the layers from sliding, which makes it harder.",
        "&eHow:&r infuse iron with carbon to get enriched iron, infuse that again into steel dust and smelt it. Steel from your MI line works too.",
        "&eTip:&r any steel ingot counts: the pack unifies them."]),
    Q("mk2_steel_casing", 0, 0, [item(MEK + "steel_casing")], "Steel Casing", subtitle="The shell of every machine", deps=["mk2_steel", "t3_mekcircuit"],
      xp=80, size=2.0, shape="gear", loot="t3", mirror="21D8B88155648EA6", section="Machines", desc=[
        "&6A steel shell, ready for a purpose. You remember building with intent.&r",
        "&eWhat:&r the Steel Casing is the body of every Mekanism machine on this page.",
        "&eHow:&r steel ingots, glass and an osmium ingot (check JEI).",
        "&eTip:&r every machine below starts from one casing. Make several at once."]),
    # Circuit tiers
    Q("mk2_tier_basic", 0, 0, [item("minecraft:redstone"), item(MEK + "basic_control_circuit")], "The Basic Tier", subtitle="Redstone and a basic circuit",
      deps=["mk2_basic_circuit", "mk2_infused_alloy"], xp=60, size=1.5, shape="hexagon", mirror="19341B01E048ACAB", section="Circuit Tiers", desc=[
        "&eWhat:&r every Mekanism block comes in four tiers: basic, advanced, elite and ultimate. Each tier pairs an alloy with a control circuit.",
        "&eHow:&r the basic tier runs on redstone and Basic Control Circuits.",
        "&eTip:&r the tier of a factory, cube or tank shows in its name and its colour stripe."]),
    Q("mk2_tier_adv", 0, 0, [item(MEK + "alloy_infused"), item(MEK + "advanced_control_circuit")], "The Advanced Tier", subtitle="Infused alloy, MV circuits",
      deps=["mk2_tier_basic", "t4_mv"], xp=100, size=1.5, shape="hexagon", mirror="7C687DCF71D77761", section="Circuit Tiers", desc=[
        "&eWhat:&r the advanced tier pairs Infused Alloy with the Advanced Control Circuit.",
        "&eHow:&r the circuit needs an &eMI electronic circuit&r (MV) in this pack.",
        "&eTip:&r advanced cables, tanks and factories all use this pair."]),
    Q("mk2_tier_elite", 0, 0, [item(MEK + "alloy_reinforced"), item(MEK + "elite_control_circuit")], "The Elite Tier", subtitle="Reinforced alloy, HV circuits",
      deps=["mk2_tier_adv", "t5_hv"], xp=150, size=1.5, shape="hexagon", mirror="1AEFF93A398B8BBF", section="Circuit Tiers", desc=[
        "&eWhat:&r the elite tier pairs Reinforced Alloy (diamond infusion) with the Elite Control Circuit.",
        "&eHow:&r the circuit needs an &eMI digital circuit&r (HV) in this pack.",
        "&eTip:&r diamond infuse comes from diamonds or diamond dust; enrich it first for more per diamond."]),
    Q("mk2_tier_ult", 0, 0, [item(MEK + "alloy_atomic"), item(MEK + "ultimate_control_circuit")], "The Ultimate Tier", subtitle="Atomic alloy, EV circuits",
      deps=["mk2_tier_elite", "t6_pu"], xp=250, size=1.5, shape="hexagon", loot="t5", mirror="06210B6FD0F9989B", section="Circuit Tiers", desc=[
        "&6The top of the ladder. You remember when four steps felt like a long climb.&r",
        "&eWhat:&r the ultimate tier pairs Atomic Alloy (refined obsidian infusion) with the Ultimate Control Circuit.",
        "&eHow:&r the circuit needs an &eMI processing unit&r (EV) in this pack."]),
    # Machines
    Q("mk2_enrich", 0, 0, [item(MEK + "enrichment_chamber")], "Enrichment Chamber", subtitle="Ore into two dusts", deps=["mk2_steel_casing"], xp=50,
      mirror="08DDE018A804BFE7", section="Machines", desc=[
        "&eWhat:&r the Enrichment Chamber turns one ore into two dusts, and enriches coal, redstone and diamonds for the infuser.",
        "&eHow:&r redstone, a Basic Control Circuit and a steel casing (check JEI).",
        "&eTip:&r 2x is the cap before acids in this pack. The 3x, 4x and 5x lines are below."]),
    Q("mk2_crusher", 0, 0, [item(MEK + "crusher")], "Crusher", subtitle="Ingots and blocks into dust", deps=["mk2_steel_casing"], xp=50,
      mirror="7AE502EDB73BD57A", section="Machines", desc=[
        "&eWhat:&r the Crusher grinds ingots into dust, stone into gravel and plants into bio fuel.",
        "&eHow:&r redstone, a Basic Control Circuit, lava buckets and a steel casing (check JEI).",
        "&eTip:&r it is the last step of the 3x line: clumps go in, dirty dust comes out."]),
    Q("mk2_compressor", 0, 0, [item(MEK + "osmium_compressor")], "Osmium Compressor", subtitle="Dust pressed with liquid osmium", deps=["mk2_adv_circuit"],
      xp=80, mirror="195729280394ABFB", section="Machines", desc=[
        "&eWhat:&r the Osmium Compressor presses a dust together with osmium into a refined ingot: refined obsidian or refined glowstone.",
        "&eHow:&r an Advanced Control Circuit, alloys and a steel casing (check JEI). Osmium ingots go in its fuel slot.",
        "&eTip:&r one osmium ingot feeds many operations."]),
    Q("mk2_purifier", 0, 0, [item(MEK + "purification_chamber")], "Purification Chamber", subtitle="Oxygen for 3x ore", deps=["mk2_adv_circuit", "mk2_enrich"],
      xp=80, mirror="33415CB421F7620A", section="Machines", desc=[
        "&eWhat:&r the Purification Chamber uses oxygen to turn ore into clumps, three per ore.",
        "&eChemistry:&r oxygen attacks the ore's surface and loosens the metal-bearing grains from the rock around them.",
        "&eHow:&r an Advanced Control Circuit (MV), an Enrichment Chamber and osmium (check JEI). Feed it O₂ from an Electrolytic Separator."]),
    Q("mk2_injector", 0, 0, [item(MEK + "chemical_injection_chamber")], "Chemical Injection Chamber", subtitle="Hydrogen chloride for 4x ore",
      deps=["mk2_adv_circuit", "mk2_purifier"], xp=100, mirror="27512B0434531195", section="Machines", desc=[
        "&eWhat:&r the Injection Chamber uses hydrogen chloride to turn ore into shards, four per ore.",
        "&eChemistry:&r HCl dissolves metal oxides into chlorides (for example FeO + 2HCl → FeCl₂ + H₂O), which frees more metal from each ore.",
        "&eHow:&r a Purification Chamber, gold and circuits (check JEI; MV in this pack). Feed it HCl from a Chemical Infuser."]),
    Q("mk2_washer", 0, 0, [item(MEK + "chemical_washer")], "Chemical Washer", subtitle="Rinse the ore slurry", deps=["mk2_dissolution"], xp=100,
      mirror="60B52705049D1BA5", section="Machines", desc=[
        "&eWhat:&r the Washer cleans dirty ore slurry into clean slurry with water.",
        "&eChemistry:&r washing removes the insoluble rock and gangue that the acid left behind.",
        "&eHow:&r an Advanced Control Circuit in this pack, a steel casing and a bucket (check JEI). Feed it water with an Electric Pump.",
        "&eTip:&r it is part of the 5x line, together with the Dissolution Chamber and Crystallizer."]),
    Q("mk2_dissolution", 0, 0, [item(MEK + "chemical_dissolution_chamber")], "Chemical Dissolution Chamber", subtitle="Sulfuric acid eats the ore",
      deps=["mk2_adv_circuit"], xp=100, mirror="6B8040401B512E50", section="Machines", desc=[
        "&eWhat:&r the Dissolution Chamber dissolves ore in sulfuric acid into a dirty slurry, the first step of the 5x line.",
        "&eChemistry:&r H₂SO₄ turns metal oxides into soluble sulfates, so the metal leaves the rock as a solution.",
        "&eHow:&r an Advanced Control Circuit in this pack, a steel casing and chemical tanks (check JEI)."]),
    Q("mk2_crystallizer", 0, 0, [item(MEK + "chemical_crystallizer")], "Chemical Crystallizer", subtitle="Clean slurry back into solids",
      deps=["mk2_washer"], xp=100, mirror="602A6CF9D5B66AD3", section="Machines", desc=[
        "&eWhat:&r the Crystallizer turns clean slurry into crystals, five per ore, and brine into salt.",
        "&eChemistry:&r crystallisation pulls a pure solid out of a saturated solution: as the solvent goes, the ions arrange into a lattice and leave impurities behind.",
        "&eHow:&r an Advanced Control Circuit in this pack, a steel casing and chemical tanks (check JEI)."]),
    Q("mk2_dusts", 0, 0, [anytag("c:dusts")], "A Pile of Dust", subtitle="Anything crushed counts", deps=["mk2_crusher", "mk2_enrich"], xp=20,
      mirror="47F38E606AD3FF53", section="Machines", desc=[
        "&eWhat:&r any dust. Dust is the common middle step: ore and ingots become dust, and dust smelts into ingots.",
        "&eChemistry:&r grinding raises surface area, and reactions happen at surfaces, so powders react and melt faster than lumps.",
        "&eHow:&r put an ingot in the Crusher or an ore in the Enrichment Chamber."]),
    # Chemical machines
    Q("mk2_separator", 0, 0, [item(MEK + "electrolytic_separator")], "Electrolytic Separator", subtitle="Split water into H₂ and O₂",
      deps=["mk2_steel_casing"], xp=60, mirror="18783C62009934DB", section="Chemical Machines", desc=[
        "&eWhat:&r the Separator splits fluids with electricity: water into hydrogen and oxygen, brine into sodium and chlorine.",
        "&eChemistry:&r electrolysis of water: 2H₂O → 2H₂ + O₂. Twice as much hydrogen as oxygen comes out, by volume.",
        "&eHow:&r redstone, iron, osmium and a Basic Control Circuit (check JEI). Pump water in, take each gas out on its own side."]),
    Q("mk2_oxidizer", 0, 0, [item(MEK + "chemical_oxidizer")], "Chemical Oxidizer", subtitle="Solids into gases", deps=["mk2_steel_casing"], xp=60,
      mirror="2A793B35FE25003C", section="Chemical Machines", desc=[
        "&eWhat:&r the Oxidizer burns a solid into a gas: sulfur into sulfur dioxide, and later uranium compounds for fission fuel.",
        "&eChemistry:&r S + O₂ → SO₂. Sulfur burns with a pale blue flame.",
        "&eHow:&r a Dynamic Tank block, a chemical tank and a circuit (check JEI)."]),
    Q("mk2_chem_infuser", 0, 0, [item(MEK + "chemical_infuser")], "Chemical Infuser", subtitle="Two gases in, one out", deps=["mk2_steel_casing"], xp=60,
      mirror="376532CD98D39781", section="Chemical Machines", desc=[
        "&eWhat:&r the Chemical Infuser reacts two gases: H₂ + Cl₂ into HCl, SO₂ + O₂ into SO₃, SO₃ + water vapour into sulfuric acid.",
        "&eChemistry:&r the contact process: 2SO₂ + O₂ → 2SO₃, then SO₃ + H₂O → H₂SO₄. Sulfuric acid is the most produced chemical in the world.",
        "&eHow:&r a Basic Control Circuit, chemical tanks and a steel casing (check JEI)."]),
    Q("mk2_condensentrator", 0, 0, [item(MEK + "rotary_condensentrator")], "Rotary Condensentrator", subtitle="Gas to liquid and back",
      deps=["mk2_steel_casing"], xp=60, mirror="603BEDD49070ECAD", section="Chemical Machines", desc=[
        "&eWhat:&r turns a gas into its liquid form and back. It also boils water into vapour for the acid line.",
        "&eChemistry:&r every gas liquefies when cooled below its boiling point; water vapour is just water above 100 °C.",
        "&eHow:&r glass, a chemical tank, a fluid tank and a circuit (check JEI). Toggle the mode in its GUI."]),
    Q("mk2_hdpe_pellet", 0, 0, [item(MEK + "hdpe_pellet")], "HDPE Pellet", subtitle="Polyethylene from the PRC",
      deps=["mk2_bio_fuel", "mk2_prc", "mk2_condensentrator", "t5_hdpe"], xp=100, mirror="78DD2A3DFF6D1613", section="Chemical Machines", desc=[
        "&eWhat:&r high-density polyethylene pellets, the plastic for sheets, rods and the late Mekanism gear.",
        "&eChemistry:&r n C₂H₄ → (C₂H₄)ₙ: thousands of ethene units join into long, straight chains.",
        "&eHow:&r PRC: substrate + ethene + oxygen → HDPE pellet (check JEI). Your MI polyethylene line from the main path is the other route."]),
    # Upgrades
    Q("mk2_glass", 0, 0, [item(MEK + "structural_glass", 4)], "Structural Glass", subtitle="Windows for multiblocks", deps=["mk2_steel_casing"], xp=30,
      mirror="01A90E2541C91DB2", section="Upgrades", desc=[
        "&eWhat:&r Structural Glass is the wall block of dynamic tanks, evaporation plants, boilers, turbines and the SPS.",
        "&eChemistry:&r glass is mostly SiO₂ cooled too fast to crystallise, so it stays clear.",
        "&eHow:&r glass and steel (check JEI)."]),
    Q("mk2_upg_energy", 0, 0, [item(MEK + "upgrade_energy")], "Energy Upgrade", subtitle="Lower bills, bigger buffer", deps=["mk2_steel_casing", "mk2_glass"],
      xp=40, mirror="0ACE573560A19309", section="Upgrades", desc=[
        "&eWhat:&r cuts a machine's energy use and enlarges its internal buffer.",
        "&eHow:&r Infused Alloy and glass around gold dust (check JEI). Up to 8 per machine.",
        "&eTip:&r pair every speed upgrade with an energy upgrade."]),
    Q("mk2_upg_muffling", 0, 0, [item(MEK + "upgrade_muffling")], "Muffling Upgrade", subtitle="Quiet machines", deps=["mk2_steel_casing", "mk2_glass"],
      xp=30, mirror="001DE8028CAF0A08", section="Upgrades", desc=[
        "&eWhat:&r makes a machine quieter. Four make it silent.",
        "&eHow:&r Infused Alloy and glass around wool (check JEI).",
        "&eTip:&r your ears will thank you in a room of 20 crushers."]),
    Q("mk2_upg_chemical", 0, 0, [item(MEK + "upgrade_chemical")], "Chemical Upgrade", subtitle="Use less gas per job", deps=["mk2_steel_casing", "mk2_glass"],
      xp=40, mirror="09830BB2A23E94B4", section="Upgrades", desc=[
        "&eWhat:&r cuts the gas a machine uses per operation, in machines that take a secondary gas (purification, injection).",
        "&eHow:&r Infused Alloy and glass around a gas ingredient (check JEI).",
        "&eTip:&r on an injection line it saves a lot of HCl."]),
    Q("mk2_upg_stone", 0, 0, [item(MEK + "upgrade_stone_generator")], "Stone Generator Upgrade", subtitle="Cobble on demand",
      deps=["mk2_steel_casing", "mk2_glass"], xp=30, mirror="515A60B89ED5440D", section="Upgrades", desc=[
        "&eWhat:&r lets an Electric Pump make stone from the water and lava next to it.",
        "&eChemistry:&r lava is molten rock; water cools its surface below the melting point and it sets as stone.",
        "&eHow:&r Infused Alloy and glass around water and lava (check JEI)."]),
    Q("mk2_upg_anchor", 0, 0, [item(MEK + "upgrade_anchor")], "Anchor Upgrade", subtitle="Keep one machine's chunk loaded", deps=["mk2_upgrades"], xp=40,
      optional=True, tokens=1, section="Upgrades", desc=[
        "&eWhat:&r a machine with an Anchor upgrade keeps its own chunk loaded.",
        "&eHow:&r Infused Alloy and glass around diamond dust (check JEI).",
        "&eTip:&r cheaper than a Dimensional Stabilizer for one remote machine."]),
    # Pipes and storage
    Q("mk2_pipes", 0, 0, [anyof([MEK + t + "_mechanical_pipe" for t in ("basic", "advanced", "elite", "ultimate")])], "Mechanical Pipes",
      subtitle="Fluids, Mekanism style", deps=["mk2_configurator"], xp=40, mirror="33C69B5934BE4D64", section="Pipes and Storage", desc=[
        "&eWhat:&r Mechanical Pipes carry fluids. Any tier counts.",
        "&eHow:&r steel and a bucket, 8 per craft (check JEI).",
        "&eTip:&r pipes pull only from blocks that push; set the source's side to output."]),
    Q("mk2_tubes", 0, 0, [anyof([MEK + t + "_pressurized_tube" for t in ("basic", "advanced", "elite", "ultimate")])], "Pressurized Tubes",
      subtitle="Gases need their own pipe", deps=["mk2_configurator"], xp=40, mirror="3AF1DC02E9A0010C", section="Pipes and Storage", desc=[
        "&eWhat:&r Pressurized Tubes carry Mekanism chemicals: gases, slurries and infuse types.",
        "&eChemistry:&r gases spread to fill any space, so a gas line must be sealed. Pressure drives the flow from the full end to the empty end.",
        "&eHow:&r steel and glass, 8 per craft (check JEI)."]),
    Q("mk2_conductors", 0, 0, [anyof([MEK + t + "_thermodynamic_conductor" for t in ("basic", "advanced", "elite", "ultimate")])], "Thermodynamic Conductors",
      subtitle="Pipes for heat", deps=["mk2_configurator"], xp=40, mirror="66A450CAC07232E1", section="Pipes and Storage", desc=[
        "&eWhat:&r conductors carry heat between heaters, the evaporation plant and the boiler.",
        "&eChemistry:&r heat flows from hot to cold. Copper conducts heat about eight times better than steel.",
        "&eHow:&r steel and copper (check JEI)."]),
    Q("mk2_chem_tanks", 0, 0, [anyof([MEK + t + "_chemical_tank" for t in ("basic", "advanced", "elite", "ultimate")])], "Chemical Tanks",
      subtitle="A bottle for any gas", deps=["mk2_tubes"], xp=50, mirror="1922623A26E08078", section="Pipes and Storage", desc=[
        "&eWhat:&r Chemical Tanks store gases and keep them when broken. Any tier counts.",
        "&eHow:&r osmium and redstone (check JEI). Higher tiers ring the tank below with alloy.",
        "&eTip:&r one under each separator output keeps the line steady."]),
    Q("mk2_bins", 0, 0, [anyof([MEK + t + "_bin" for t in ("basic", "advanced", "elite", "ultimate")])], "Bins", subtitle="Lots of one item",
      deps=["mk2_transporter"], xp=40, mirror="73E6878553BA6908", section="Pipes and Storage", desc=[
        "&eWhat:&r a Bin holds a large amount of one item type and keeps it when broken.",
        "&eHow:&r a chest, Basic Alloy and a circuit (check JEI). Left-click to take a stack, right-click to put one in.",
        "&eTip:&r good for cobblestone, dusts or anything you hoard by the thousand."]),
    Q("mk2_fuelwood", 0, 0, [item(MEK + "fuelwood_heater")], "Fuelwood Heater", subtitle="Burn fuel for heat", deps=["mk2_conductors"], xp=40,
      mirror="2D1CBCEC82F1B37D", section="Pipes and Storage", desc=[
        "&eWhat:&r burns any furnace fuel and gives heat to the conductors around it.",
        "&eChemistry:&r burning is fast oxidation: C + O₂ → CO₂ releases about 394 kJ per mole of carbon.",
        "&eHow:&r a steel casing, a furnace and a circuit (check JEI)."]),
    Q("mk2_security_desk", 0, 0, [item(MEK + "security_desk")], "Security Desk", subtitle="Who may use your machines", deps=["mk2_security", "mk2_elite_circuit"],
      xp=60, optional=True, tokens=1, section="Pipes and Storage", desc=[
        "&eWhat:&r sets who may use your Mekanism blocks: you, a trusted list, or everyone.",
        "&eHow:&r steel, glass and &eElite Control Circuits&r (HV) (check JEI).",
        "&eTip:&r on a shared server, lock your reactor controls."]),
    # Big builds
    Q("mk2_evaporation", 0, 0, [item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"), item(MEK + "thermal_evaporation_valve")],
      "Thermal Evaporation Plant", subtitle="Sun and heat turn water into brine", deps=["mk2_steel_casing"], xp=120, mirror="120572510F525930", section="Big Builds", desc=[
        "&eWhat:&r a tall multiblock that boils water down into brine, and brine into lithium.",
        "&eChemistry:&r salt pans work the same way: water evaporates and the dissolved salts stay behind at higher and higher concentration.",
        "&eHow:&r a 4x4 base of evaporation blocks, up to 18 high, with a controller and valves (layout in JEI). Heat makes it faster."]),
    # Energy
    Q("mk2_solar", 0, 0, [item(GEN + "solar_generator")], "Solar Generator", subtitle="Free power by day", deps=["mk2_tablet"], xp=40,
      mirror="74200A48498DD7F8", section="Energy", desc=[
        "&eWhat:&r a small generator that makes FE in daylight under open sky.",
        "&eChemistry:&r a photovoltaic cell is a silicon junction: light knocks electrons loose and the junction pushes them one way, making a current.",
        "&eHow:&r solar panels, an Energy Tablet and osmium (check JEI)."]),
    Q("mk2_adv_solar", 0, 0, [item(GEN + "advanced_solar_generator")], "Advanced Solar Generator", subtitle="Four panels, one block",
      deps=["mk2_solar"], xp=60, mirror="4EDD96EB60EF5814", section="Energy", desc=[
        "&eWhat:&r four solar generators on a frame, with much more output.",
        "&eHow:&r solar generators, Infused Alloy and iron (check JEI).",
        "&eTip:&r it works in the rain too, just slower."]),
    Q("mk2_heat_gen", 0, 0, [item(GEN + "heat_generator")], "Heat Generator", subtitle="Lava and fuel into power", deps=["mk2_tablet"], xp=40,
      mirror="0650996C7818ADB5", section="Energy", desc=[
        "&eWhat:&r burns fuel or sits by lava and turns heat into FE.",
        "&eChemistry:&r a heat engine needs a hot side and a cold side; the bigger the difference, the more work it can do.",
        "&eHow:&r iron, wood, copper and a furnace (check JEI)."]),
    Q("mk2_bio_gen", 0, 0, [item(GEN + "bio_generator")], "Bio-Generator", subtitle="Burn bio fuel", deps=["mk2_tablet"], xp=40,
      mirror="6CD1720B76F47806", section="Energy", desc=[
        "&eWhat:&r burns bio fuel (crushed plants) for FE.",
        "&eChemistry:&r plants store sunlight as sugars: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Burning them gives that energy back.",
        "&eHow:&r redstone, bio fuel and an Energy Tablet (check JEI)."]),
    Q("mk2_wind", 0, 0, [item(GEN + "wind_generator")], "Wind Generator", subtitle="Higher is windier", deps=["mk2_tablet"], xp=50,
      mirror="7778937DF377C1B4", section="Energy", desc=[
        "&eWhat:&r a turbine that makes more FE the higher you build it.",
        "&eChemistry:&r a turbine's power grows with the cube of wind speed, so a little more wind gives a lot more power.",
        "&eHow:&r an Energy Tablet, osmium and circuits (check JEI). Put it on a tall tower."]),
    Q("mk2_cubes", 0, 0, [anyof([MEK + t + "_energy_cube" for t in ("basic", "advanced", "elite", "ultimate")])], "Energy Cube",
      subtitle="Store the surplus", deps=["mk2_tablet"], xp=50, mirror="0AA9EF3981E9BA37", section="Energy", desc=[
        "&eWhat:&r a block battery that stores FE and keeps it when broken. Any tier counts.",
        "&eHow:&r redstone, iron, Energy Tablets and a steel casing (check JEI).",
        "&eTip:&r set its sides in the GUI: one input, the rest output."]),
    # Gadgets
    Q("mk2_jetpack", 0, 0, [item(MEK + "jetpack")], "Jetpack", subtitle="Hydrogen-powered hops", deps=["mk2_chargepad"], xp=60,
      mirror="37D4E5ACB35D8BF1", section="Gadgets", desc=[
        "&eWhat:&r a chest-slot jetpack that burns hydrogen.",
        "&eChemistry:&r hydrogen burns with oxygen into water: 2H₂ + O₂ → 2H₂O, with a lot of energy per gram.",
        "&eHow:&r steel, a basic chemical tank and circuits (check JEI). Fill it with H₂ from a separator.",
        "&eTip:&r hover mode is the safe one for building."]),
    Q("mk2_gauge_dropper", 0, 0, [item(MEK + "gauge_dropper")], "Gauge Dropper", subtitle="Sample or empty a tank", deps=["mk2_chargepad"], xp=20,
      mirror="424B3E3B299D3999", section="Gadgets", desc=[
        "&eWhat:&r sucks a little fluid or gas out of a tank, or dumps a tank you don't want.",
        "&eHow:&r osmium over glass panes (check JEI).",
        "&eTip:&r sneak + right-click empties the dropper itself."]),
    Q("mk2_free_runners", 0, 0, [item(MEK + "free_runners")], "Free Runners", subtitle="No fall damage, taller steps", deps=["mk2_chargepad"], xp=50,
      mirror="227E9783382527CA", section="Gadgets", desc=[
        "&eWhat:&r powered boots that stop fall damage and let you walk up full blocks.",
        "&eHow:&r string, Infused Alloy and an Energy Tablet (check JEI). Charge them on the Chargepad."]),
    Q("mk2_scuba", 0, 0, [item(MEK + "scuba_tank"), item(MEK + "scuba_mask")], "Scuba Gear", subtitle="Breathe from a tank", deps=["mk2_chargepad"], xp=50,
      mirror="47E79DFD123BF617", section="Gadgets", desc=[
        "&eWhat:&r a tank of oxygen on your back and a mask on your face: breathe underwater for a long time.",
        "&eChemistry:&r we need O₂ for respiration; a scuba tank just carries it with you.",
        "&eHow:&r tank: a basic chemical tank and alloy; mask: glass and alloy (check JEI). Fill the tank with O₂ from a separator."]),
    # Ore line: 2x, 3x, 4x, 5x (each machine counts as its factory too)
    Q("mk2_ore2", 0, 0, [fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")], "2x: Enrich and Smelt",
      subtitle="Two ingots per ore", deps=["mk2_steel_casing"], xp=60, mirror="119BED334E331C25", section="Ore Line: 2x", desc=[
        "&eWhat:&r the first ore line: ore into the Enrichment Chamber (2 dusts), dusts into the smelter.",
        "&eHow:&r an Enrichment Chamber and an Energized Smelter, or any factory of either. Join them with a transporter.",
        "&eTip:&r this is the pack's cap before acids. Every step up needs a gas."]),
    Q("mk2_ore3", 0, 0, [item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"), fac("purification_chamber", "purifying")], "3x: Oxygen",
      subtitle="Water, split, feeds the purifier", deps=["mk2_steel_casing", "t4_ore3"], xp=80, mirror="445CC9AAA6F8AAB6", section="Ore Line: 3x", desc=[
        "&eWhat:&r the 3x line starts with oxygen: pump water, split it, and feed the O₂ into a Purification Chamber.",
        "&eChemistry:&r 2H₂O → 2H₂ + O₂. Keep the hydrogen: it's fuel and a reagent later.",
        "&eHow:&r an Electric Pump, an Electrolytic Separator and a Purification Chamber or Purifying Factory."]),
    Q("mk2_ore3b", 0, 0, [fac("crusher", "crushing"), fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")], "3x: The Rest of the Line",
      subtitle="Clumps to dust to ingots", deps=["mk2_ore3"], xp=80, mirror="67E7A9A65B14C933", section="Ore Line: 3x", desc=[
        "&eWhat:&r clumps go through the Crusher into dirty dust, the Enrichment Chamber cleans it, and the smelter finishes the ingots.",
        "&eHow:&r a Crusher, an Enrichment Chamber and an Energized Smelter (or their factories), all on one transporter line.",
        "&eTip:&r dirty dust can go to the MI Centrifuge instead for byproducts."]),
    Q("mk2_ore4", 0, 0, [item(MEK + "electric_pump"), item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"),
                         item(MEK + "thermal_evaporation_valve", 2), item(MEK + "electrolytic_separator")], "4x: Brine and Chlorine",
      subtitle="Sea salt becomes a reagent", deps=["mk2_steel_casing", "t4_ore4"], xp=120, mirror="7485BCBE366501DF", section="Ore Line: 4x", desc=[
        "&eWhat:&r the 4x line needs chlorine: an evaporation plant makes brine, and a separator splits it.",
        "&eChemistry:&r electrolysis of brine (the chlor-alkali process): 2NaCl + 2H₂O → Cl₂ + H₂ + 2NaOH. Mekanism gives you Cl₂ and sodium.",
        "&eHow:&r a pump into the evaporation plant, its brine into a separator. Keep the chlorine."]),
    Q("mk2_ore4b", 0, 0, [item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"), item(MEK + "chemical_infuser"), item(MEK + "chemical_injection_chamber")],
      "4x: Hydrogen Chloride", subtitle="H₂ + Cl₂ → 2HCl", deps=["mk2_ore4"], xp=120, mirror="0E175356D43E6A10", section="Ore Line: 4x", desc=[
        "&eWhat:&r hydrogen from a water separator and chlorine from the brine separator meet in the Chemical Infuser to make HCl for the Injection Chamber.",
        "&eChemistry:&r H₂ + Cl₂ → 2HCl. In daylight the mix can react explosively; Mekanism keeps it tame.",
        "&eHow:&r a second pump and separator for H₂, a Chemical Infuser, and the Injection Chamber."]),
    Q("mk2_ore4c", 0, 0, [fac("purification_chamber", "purifying"), fac("crusher", "crushing"), fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")],
      "4x: Shards to Ingots", subtitle="Finish with the 3x line", deps=["mk2_ore4b"], xp=120, mirror="0095422BC87AA135", section="Ore Line: 4x", desc=[
        "&eWhat:&r shards go into the Purification Chamber and then down the 3x line: crush, enrich, smelt.",
        "&eHow:&r one of each machine (or its factory) on a transporter line.",
        "&eTip:&r one factory of each type keeps up with a basic injection chamber."]),
    Q("mk2_ore5", 0, 0, [item(MEK + "dust_sulfur"), item(MEK + "chemical_oxidizer"), item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"),
                         item(MEK + "chemical_infuser"), item(MEK + "rotary_condensentrator")], "5x: Sulfuric Acid",
      subtitle="The contact process", deps=["mk2_steel_casing", "t4_ore5"], xp=150, mirror="75E4751F7A802A44", section="Ore Line: 5x", desc=[
        "&eWhat:&r the 5x line runs on sulfuric acid: burn sulfur, oxidise it again, then add water vapour.",
        "&eChemistry:&r S + O₂ → SO₂; 2SO₂ + O₂ → 2SO₃; SO₃ + H₂O → H₂SO₄.",
        "&eHow:&r Oxidizer (sulfur → SO₂), separator (O₂), Chemical Infuser (SO₃, then acid) and a Rotary Condensentrator for water vapour."]),
    Q("mk2_ore5b", 0, 0, [item(MEK + "chemical_infuser"), item(MEK + "chemical_dissolution_chamber"), item(MEK + "chemical_washer"), item(MEK + "chemical_crystallizer")],
      "5x: Dissolve, Wash, Crystallise", subtitle="Ore into slurry and back", deps=["mk2_ore5"], xp=150, mirror="77FB313845779AED", section="Ore Line: 5x", desc=[
        "&eWhat:&r the acid dissolves ore into dirty slurry, the washer cleans it, and the crystallizer turns it into crystals.",
        "&eChemistry:&r leach, purify, crystallise: the same three steps real hydrometallurgy uses for copper, zinc and uranium.",
        "&eHow:&r one of each machine, joined by pressurized tubes. The washer needs water."]),
    Q("mk2_ore5c", 0, 0, [item(MEK + "electric_pump", 2), item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"),
                          item(MEK + "thermal_evaporation_valve", 2), item(MEK + "electrolytic_separator", 2), item(MEK + "chemical_infuser"),
                          item(MEK + "chemical_injection_chamber")], "5x: The HCl Stage", subtitle="Crystals into shards",
      deps=["mk2_ore5b"], xp=150, mirror="6DC1E08D019FD543", section="Ore Line: 5x", desc=[
        "&eWhat:&r crystals go into the Injection Chamber, so the 5x line needs the whole HCl setup from the 4x line as well.",
        "&eHow:&r two pumps, the evaporation plant, two separators, a Chemical Infuser and an Injection Chamber.",
        "&eTip:&r if you built the 4x line, reuse it: just send the crystals in front of it."]),
    Q("mk2_ore5d", 0, 0, [item(MEK + "electric_pump"), item(MEK + "electrolytic_separator"), fac("purification_chamber", "purifying"), fac("crusher", "crushing"),
                          fac("enrichment_chamber", "enriching"), fac("energized_smelter", "smelting")], "5x: The Full Line",
      subtitle="Five ingots per ore", deps=["mk2_ore5c"], xp=200, mirror="7934873E784C4B3C", section="Ore Line: 5x", desc=[
        "&6Five from one. You remember when the world gave freely; now you make it give.&r",
        "&eWhat:&r the last stage is the 3x line again: oxygen, purifier, crusher, enrichment, smelter.",
        "&eHow:&r a pump and separator for O₂, then one of each machine (or factory).",
        "&eTip:&r dirty dust can also go to the MI Centrifuge for byproducts."]),
], links=[("t3_infuser", -4, 0), ("t3_mekcircuit", -4, 2), ("t4_mv", -6, 1), ("t4_ore4", -4, 4), ("t4_ore5", -4, 6), ("pw_brine", -6, 6),
          ("t4_separator", -4, 8), ("t5_hdpe", -6, 9), ("tc_mekasuit", -4, 10), ("t7_sps", -6, 11), ("t6_centrifuge", -4, 12),
          ("tc_obsidian_paxel", -4, 20)], mirror="mekanism")
