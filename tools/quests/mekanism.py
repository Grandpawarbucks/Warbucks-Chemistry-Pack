"""Quest chapter: mekanism (mod page: Mekanism, Mekanism Generators, Mekanism Tools, Mekanism: More Machine, Mekanism Extras).
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
from questlib import Q, Chapter, item, dim, tick, anyof, MAIN, SIDE  # noqa: F401

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


# Layout (bands, top to bottom; optional quests sit 1.5 rows off their band's main line):
#   y -4.5..1   alloys, circuits, teleportation, Robit / Digital Miner, QIO
#   y  3..7.5   machines, factories, upgrades, ore line, brine and salt
#   y  9..10.5  pressurized reactions, substrate and HDPE, MekaSuit / Meka-Tool
#   y 12..13.5  transmitters and logistics
#   y 16..17.5  generators and reactor multiblocks
#   y 19.5..21  Mekanism Tools armour
#   y 22.5..25.5 Mekanism: More Machine
#   y 28..29.5  Mekanism Extras
# Links to main-path quests at x = -4 / -6.
CHAPTER = Chapter("mekanism", "Mekanism", "mekanism:metallurgic_infuser",
        ["Osmium, infusion and gases: Mekanism's machines, generators and its two big add-ons."], SIDE, [
    # --- Alloys and circuits (y = -1 / 1) -------------------------------------------------------
    Q("mk2_intro", 0, 0, [tick()], "The Mekanism Way", subtitle="Infuse, tier up, process", deps=["t3_infuser"], xp=50, desc=[
        "&6Osmium hums in your hand. You remember metals that drank other substances and grew stronger.&r",
        "&eWhat:&r Mekanism is a machine mod built on infusion and gases: soak a metal in carbon, redstone, diamond or refined obsidian and it becomes an alloy; pipe gases between machines and they become chemistry.",
        "&eHow:&r every machine comes in tiers (basic, advanced, elite, ultimate). In this pack each tier's control circuit needs the matching &eMI circuit&r.",
        "&eTip:&r this page is a side path. The main-path Mekanism quests are linked on the left; click one to jump there."]),
    Q("mk2_configurator", 0, -2, [item(MEK + "configurator")], "Configurator", subtitle="Every side of every machine, your choice", deps=["mk2_intro"], xp=40, desc=[
        "&eWhat:&r the Configurator sets which side of a Mekanism block takes input and gives output, ejects contents, and rotates blocks.",
        "&eHow:&r iron, an osmium ingot and steel. Sneak + right-click to change its mode; the side colours match the machine's GUI.",
        "&eTip:&r most \"my machine won't take gas\" problems are a side set to the wrong colour."]),
    Q("mk2_tablet", 2, -3, [item(MEK + "energy_tablet")], "Energy Tablet", subtitle="A battery you can hold", deps=["mk2_intro", "t3_infused"], xp=40, desc=[
        "&eWhat:&r a portable FE store. It is also a crafting part in the Robit, the Wind Generator, lasers, Free Runners and the Portable Teleporter.",
        "&eHow:&r gold ingots, redstone and Infused Alloy (check JEI).",
        "&eTip:&r make a few at once; you'll keep needing them."]),
    Q("mk2_reinforced", 2, -1, [item(MEK + "alloy_reinforced", 4)], "Reinforced Alloy", subtitle="Infused alloy plus diamond", deps=["mk2_intro", "t3_infused"], xp=60, desc=[
        "&eWhat:&r the second Mekanism alloy, used in elite circuits, lasers and the Solar Neutron Activator.",
        "&eChemistry:&r real alloys work the same way: a few percent of a second element (carbon in steel, chromium in stainless) changes the metal's properties.",
        "&eHow:&r Metallurgic Infuser: Infused Alloy + diamond infusion (from diamonds or diamond dust; check JEI)."]),
    Q("mk2_atomic", 4, -1, [item(MEK + "alloy_atomic", 4)], "Atomic Alloy", subtitle="Reinforced alloy plus refined obsidian", deps=["mk2_reinforced"], xp=80, desc=[
        "&eWhat:&r the top Mekanism alloy, needed for ultimate circuits, teleportation cores and the Robit.",
        "&eHow:&r first infuse obsidian dust with diamond to get refined obsidian dust, then infuse Reinforced Alloy with refined obsidian.",
        "&eTip:&r crush obsidian in the Crusher or an MI macerator for obsidian dust."]),
    Q("mk2_refined_obsidian", 6, -1, [item(MEK + "osmium_compressor"), item(MEK + "ingot_refined_obsidian", 4)], "Refined Obsidian", subtitle="The Osmium Compressor's speciality", deps=["mk2_atomic", "mk2_adv_circuit"], xp=100, desc=[
        "&eWhat:&r refined obsidian ingots: very hard, blast-proof metal for teleporters, the Robit and endgame tools.",
        "&eHow:&r the Osmium Compressor presses refined obsidian dust with liquid osmium into ingots. It needs an Advanced Control Circuit (MV).",
        "&eTip:&r refined glowstone ingots come from the same machine: glowstone dust plus osmium."]),
    Q("mk2_adv_circuit", 2, 1, [item(MEK + "advanced_control_circuit", 2)], "Advanced Control Circuit", subtitle="Mekanism's MV tier", deps=["t3_mekcircuit", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the circuit for every advanced-tier Mekanism block: factories, cubes, tanks, the Purification Chamber, and in this pack the whole 4x/5x ore line (injection, dissolution, washer, crystallizer).",
        "&eHow:&r an &eMI electronic circuit&r above two Infused Alloys and a Basic Control Circuit (check JEI).",
        "&eTip:&r the old infuser shortcut for circuits is removed in this pack. Circuits follow MI's voltage tiers."]),
    Q("mk2_elite_circuit", 4, 1, [item(MEK + "elite_control_circuit", 2)], "Elite Control Circuit", subtitle="Mekanism's HV tier", deps=["mk2_adv_circuit", "mk2_reinforced", "t5_hv"], xp=150, desc=[
        "&eWhat:&r the circuit for elite-tier blocks, the Combiner, the Security Desk and the Solar Neutron Activator.",
        "&eHow:&r an &eMI digital circuit&r above two Reinforced Alloys and an Advanced Control Circuit (check JEI).",
        "&eTip:&r HV comes with polyethylene on the main path. Make a stack of these before upgrading factories."]),
    Q("mk2_ult_circuit", 6, 1, [item(MEK + "ultimate_control_circuit", 2)], "Ultimate Control Circuit", subtitle="Mekanism's EV tier", deps=["mk2_elite_circuit", "mk2_atomic", "t6_pu"], xp=250, desc=[
        "&eWhat:&r the circuit behind Mekanism's best blocks: the Isotopic Centrifuge, QIO, the Quantum Entangloporter, the Dimensional Stabilizer, the MekaSuit and the Meka-Tool.",
        "&eHow:&r an &eMI processing unit&r above two Atomic Alloys and an Elite Control Circuit (check JEI).",
        "&eTip:&r this unlocks the rest of the page: ultimate factories, QIO, More Machine's big machines and Mekanism Extras."]),

    # --- Teleportation, Robit, Digital Miner, QIO (y = -4.5 .. 2.5) ----------------------------
    Q("mk2_teleport_core", 6, -3, [item(MEK + "teleportation_core", 2)], "Teleportation Core", subtitle="The heart of everything that moves far", deps=["mk2_refined_obsidian"], xp=120, desc=[
        "&eWhat:&r the part inside teleporters, the Digital Miner, QIO drive arrays and the Quantum Entangloporter.",
        "&eHow:&r Atomic Alloy, gold ingots, a diamond and ender pearls (check JEI).",
        "&eTip:&r you'll need at least four of these for this page alone. Automate Atomic Alloy early."]),
    Q("mk2_teleporter", 5, -4.5, [item(MEK + "teleporter"), item(MEK + "teleporter_frame", 9)], "Teleporter", subtitle="Step through a frame, arrive elsewhere", deps=["mk2_teleport_core"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r a frame-and-controller portal that links to other teleporters, even across dimensions.",
        "&eHow:&r the controller is a Teleportation Core in steel casings with basic circuits. Frames are refined obsidian around refined glowstone. Build a 3x4 frame with the controller in it (check JEI).",
        "&eTip:&r set both ends to the same frequency, and give the sending end plenty of power."]),
    Q("mk2_portable_tp", 7, -4.5, [item(MEK + "portable_teleporter")], "Portable Teleporter", subtitle="A teleporter in your pocket", deps=["mk2_teleport_core", "mk2_tablet"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r a hand-held teleporter that jumps you to any teleporter frequency you own.",
        "&eHow:&r a Teleportation Core between two Energy Tablets and two basic circuits (check JEI). Charge it first.",
        "&eTip:&r the further the jump, the more energy it costs."]),
    Q("mk2_stabilizer", 4, -3, [item(MEK + "dimensional_stabilizer")], "Dimensional Stabilizer", subtitle="Keep the chunks loaded", deps=["mk2_refined_obsidian", "t6_pu"], xp=150, desc=[
        "&eWhat:&r Mekanism's chunk loader. It keeps chunks around it running while you're away, so your factories never pause.",
        "&eHow:&r refined obsidian, Atomic Alloy, Ultimate Control Circuits (EV) and a diamond block (check JEI). Pick the chunks in its GUI.",
        "&eTip:&r load only what you need. Every loaded chunk costs server time."]),
    Q("mk2_entangloporter", 8, -3, [item(MEK + "quantum_entangloporter", 2)], "Quantum Entangloporter", subtitle="One frequency, two places, everything shared", deps=["mk2_teleport_core", "t6_pu"], xp=200, desc=[
        "&eWhat:&r two Entangloporters on the same frequency act as one block: energy, items, fluids, chemicals and heat go in one and out the other, across any distance or dimension.",
        "&eChemistry:&r real quantum entanglement can't carry information or matter faster than light (the no-communication theorem). Mekanism takes a little artistic licence.",
        "&eHow:&r refined obsidian, Atomic Alloy, Ultimate Control Circuits (EV) and a Teleportation Core (check JEI).",
        "&eTip:&r a pair is the easiest way to pipe uranium hexafluoride or D-T fuel from a remote plant to your base."]),
    Q("mk2_robit", 8, -1, [item(MEK + "robit")], "Robit", subtitle="A small robot friend", deps=["mk2_refined_obsidian"], xp=100, desc=[
        "&eWhat:&r the Robit follows you, picks up items, smelts and crafts. It is also a crafting part for the Digital Miner and several More Machine blocks.",
        "&eHow:&r Atomic Alloy, refined obsidian, steel, an Energy Tablet and a personal chest (check JEI). Place it on a Chargepad to recharge.",
        "&eTip:&r rename it with a name tag. It won't mind."]),
    Q("mk2_miner", 10, -1, [item(MEK + "digital_miner")], "Digital Miner", subtitle="Mine a whole area by filter", deps=["mk2_robit", "mk2_teleport_core"], xp=200, desc=[
        "&eWhat:&r a machine that mines out a large radius below it, taking only the blocks you filter for.",
        "&eHow:&r Atomic Alloy, a Logistical Sorter, a Robit, a Teleportation Core and a steel casing (check JEI). Set filters (tags like c:ores work), radius and height, then start it.",
        "&eTip:&r it uses a lot of power. Speed upgrades help, but bring Energy upgrades too. Rich deposits sit at metal-specific depths: set its height range to match."]),
    Q("mk2_qio", 8, 1, [item(MEK + "qio_drive_array"), item(MEK + "qio_dashboard"), item(MEK + "qio_drive_base")], "QIO", subtitle="Mekanism's digital storage", deps=["mk2_ult_circuit"], xp=250, desc=[
        "&eWhat:&r Quantum Item Orchestration: drives in a drive array hold items, and dashboards, importers and exporters reach them wirelessly through a frequency.",
        "&eHow:&r the drive array needs a Teleportation Core and Ultimate Control Circuits (EV); the base drive needs an ultimate circuit too. Give every QIO block the same frequency.",
        "&eTip:&r AE2 is the pack's main storage. QIO is a good wireless add-on for a remote outpost."]),
    Q("mk2_qio_io", 10, 1, [item(MEK + "qio_importer"), item(MEK + "qio_exporter"), item(MEK + "portable_qio_dashboard")], "QIO In and Out", subtitle="Importers, exporters and a dashboard to carry", deps=["mk2_qio", "t6_polonium"], xp=200, desc=[
        "&eWhat:&r importers pull items from the inventory they face into QIO; exporters push chosen items out. The Portable Dashboard opens your QIO from anywhere.",
        "&eHow:&r importer and exporter: lead, ender pearls, a Teleportation Core, an ultimate circuit and a (sticky) piston. The portable dashboard wraps a dashboard and a core in seven polonium pellets (check JEI).",
        "&eTip:&r an exporter with a filter on a machine's input is a tiny autocrafting line."]),
    Q("mk2_qio_drives", 12, 2.5, [item(MEK + "qio_drive_hyper_dense")], "Challenge: Denser Drives", subtitle="More items per drive", deps=["mk2_qio_io"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r the Hyper-Dense QIO Drive holds far more than a base drive. Time-Dilating and Supermassive drives go further still.",
        "&eHow:&r each tier wraps the one below with a Teleportation Core and rarer materials (check JEI for each).",
        "&eTip:&r drive count matters as much as size: an array holds 12 drives."]),

    # --- Machines and factories (y = 3 / 4.5) ---------------------------------------------------
    Q("mk2_smelter", 0, 3, [item(MEK + "energized_smelter")], "Energized Smelter", subtitle="A furnace that runs on FE", deps=["t3_mekcircuit"], xp=50, desc=[
        "&eWhat:&r Mekanism's electric furnace. It smelts anything a furnace can, takes upgrades, and is the base of the smelting factory.",
        "&eChemistry:&r electric heating is Joule heating: current through a resistance makes heat (P = I²R). No fuel, no smoke.",
        "&eHow:&r Basic Alloy, glass, a Basic Control Circuit and a steel casing (check JEI)."]),
    Q("mk2_basic_factory", 2, 3, [anyof(factories("basic"))], "Basic Factory", subtitle="Three jobs at once", deps=["t3_mekcircuit", "mk2_smelter"], xp=80, desc=[
        "&eWhat:&r a factory is a machine with several slots that work in parallel. A basic factory runs 3 operations at once.",
        "&eHow:&r craft any single machine (Energized Smelter, Enrichment Chamber, Crusher...) with Basic Control Circuits and Basic Alloy. Any factory type counts.",
        "&eTip:&r factories sort their own inputs with auto-sort in the GUI, so one input pipe is enough."]),
    Q("mk2_adv_factory", 4, 3, [anyof(factories("advanced"))], "Advanced Factory", subtitle="Five jobs at once", deps=["mk2_basic_factory", "mk2_adv_circuit"], xp=120, desc=[
        "&eWhat:&r 5 parallel slots, and faster with upgrades.",
        "&eHow:&r upgrade a basic factory in the crafting grid with Advanced Control Circuits, Infused Alloy and osmium, or use a Tier Installer on a placed one.",
        "&eTip:&r upgrading keeps the factory's type, so plan which machines you want at five slots."]),
    Q("mk2_elite_factory", 6, 3, [anyof(factories("elite"))], "Elite Factory", subtitle="Seven jobs at once", deps=["mk2_adv_factory", "mk2_elite_circuit"], xp=180, desc=[
        "&eWhat:&r 7 parallel slots. Pair an Elite Purifying or Injecting Factory with your ore line and the bottleneck moves elsewhere.",
        "&eHow:&r upgrade an advanced factory with Elite Control Circuits and Reinforced Alloy (check JEI).",
        "&eTip:&r the factory GUI shows each slot's progress; idle slots mean the input line is too slow."]),
    Q("mk2_ult_factory", 8, 3, [anyof(factories("ultimate"))], "Ultimate Factory", subtitle="Nine jobs at once", deps=["mk2_elite_factory", "mk2_ult_circuit"], xp=300, size=1.5, shape="hexagon", desc=[
        "&6Nine tasks in one box, all at once. You remember doing many things at once without effort.&r",
        "&eWhat:&r 9 parallel slots, the top of base Mekanism. Mekanism Extras goes further (see the bottom band).",
        "&eHow:&r upgrade an elite factory with Ultimate Control Circuits and Atomic Alloy (check JEI).",
        "&eTip:&r add Speed and Energy upgrades: speed raises power use, energy upgrades bring it back down."]),
    Q("mk2_installer", 1, 4.5, [item(MEK + "basic_tier_installer"), item(MEK + "advanced_tier_installer")], "Tier Installers", subtitle="Upgrade without breaking", deps=["mk2_basic_factory"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r right-click a placed machine with a Tier Installer to turn it into the next tier, keeping its contents and settings.",
        "&eHow:&r the basic installer needs a Basic Control Circuit; the advanced one needs an Advanced Control Circuit (MV).",
        "&eTip:&r a plain machine plus a basic installer becomes a basic factory."]),
    Q("mk2_sawmill", 3, 4.5, [item(MEK + "precision_sawmill")], "Precision Sawmill", subtitle="More planks, plus sawdust", deps=["t3_mekcircuit"], xp=50, desc=[
        "&eWhat:&r cuts logs into more planks than hand crafting, often with a bonus of sawdust, and breaks wooden items back down.",
        "&eChemistry:&r wood is about 40-50% cellulose (chains of glucose), with hemicellulose and lignin gluing the fibres together. Sawdust is the same polymers, finely divided.",
        "&eHow:&r iron, Infused Alloy, a Basic Control Circuit and a steel casing (check JEI).",
        "&eTip:&r sawdust feeds wood gasification in the PRC and the Cardboard Box."]),
    Q("mk2_ore_factory", 5, 4.5, [anyof(factories("basic", ("purifying", "injecting")) + factories("advanced", ("purifying", "injecting")) +
                                         factories("elite", ("purifying", "injecting")) + factories("ultimate", ("purifying", "injecting")))],
      "Factories for the Ore Line", subtitle="Purifying and injecting in parallel", deps=["mk2_adv_factory", "t4_ore4"], xp=150, desc=[
        "&eWhat:&r a Purifying (O₂, 3x) or Injecting (HCl, 4x) Factory runs several ores at once. Ore processing is where factories pay off most.",
        "&eChemistry:&r the gas is consumed per operation: oxygen oxidises the ore surface into clumps, hydrogen chloride attacks it into shards. More slots means more gas, so size the separator to match.",
        "&eHow:&r build the factory from a Purification Chamber or Chemical Injection Chamber (both MV in this pack). Any tier and either type counts.",
        "&eTip:&r feed the gas into the factory's gas side with pressurized tubes, the same as the single machine."]),
    Q("mk2_combiner", 7, 4.5, [item(MEK + "combiner")], "Combiner", subtitle="Two inputs pressed into one block", deps=["t5_hv"], xp=80, desc=[
        "&eWhat:&r the Combiner presses a main input together with a second block, for example flint + cobblestone into gravel, or 4 obsidian dust + cobbled deepslate back into obsidian.",
        "&eChemistry:&r pressing powders into a solid below their melting point is sintering; it's how ceramics and many metal parts are made.",
        "&eHow:&r Reinforced Alloy, &eElite Control Circuits&r (HV) and a steel casing (check JEI). Press U on it in JEI for every recipe."]),
    Q("mk2_upgrades", 2, 6, [item(MEK + "upgrade_speed", 2), item(MEK + "upgrade_energy", 2)], "Speed and Energy Upgrades", subtitle="Faster machines, smaller bills", deps=["mk2_basic_factory"], xp=80, desc=[
        "&eWhat:&r slot them into any Mekanism machine. Speed upgrades make it work faster; energy upgrades cut its power use and enlarge its buffer.",
        "&eHow:&r Infused Alloy and glass around osmium dust (speed) or gold dust (energy). A machine takes up to 8 of each.",
        "&eTip:&r speed upgrades raise power use faster than they raise speed. Balance every speed upgrade with an energy upgrade."]),
    Q("mk2_upgrade_set", 2, 7.5, [item(MEK + "upgrade_filter"), item(MEK + "upgrade_chemical"), item(MEK + "upgrade_muffling"), item(MEK + "upgrade_anchor"), item(MEK + "upgrade_stone_generator")],
      "The Other Upgrades", subtitle="Filter, chemical, muffling, anchor, stone", deps=["mk2_upgrades"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the Filter upgrade lets the Electric Pump pick heavy water; Chemical cuts gas use in gas-fed machines; Muffling quiets machines; Anchor keeps a machine's chunk loaded.",
        "&eChemistry:&r the Stone Generator upgrade does what a cobble generator does: lava cooled by water solidifies into stone.",
        "&eHow:&r Infused Alloy and glass around tin dust, iron dust or diamond dust; wool for muffling; water and lava buckets for stone (check JEI).",
        "&eTip:&r a machine's tooltip lists which upgrades it accepts."]),
    Q("mk2_cardboard", 4, 6, [item(MEK + "cardboard_box")], "Moving Day", subtitle="Secret: pack a block in a box", deps=["mk2_sawmill"], xp=50, secret=True, loot="secret", desc=[
        "&eWhat:&r a Cardboard Box made from sawdust. Right-click almost any block (even a full chest or a spawner) to pack it up and carry it.",
        "&eChemistry:&r cardboard is pressed cellulose fibre, the same polymer that makes up most of the sawdust.",
        "&eTip:&r boxes can't pick up everything; blocks on the mod's blacklist won't pack."]),
    Q("mk2_ore_states", 6, 6, [item(MEK + "crystal_iron"), item(MEK + "shard_iron"), item(MEK + "clump_iron"), item(MEK + "dirty_dust_iron")],
      "Challenge: Every Stage of Iron", subtitle="Crystal, shard, clump, dirty dust", deps=["mk2_ore_factory", "t4_ore5"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the full 5x chain, one stage of each: crystal (5x) → shard (4x) → clump (3x) → dirty dust → dust.",
        "&eChemistry:&r sulfuric acid dissolves the iron oxide into iron sulfate (Fe₂O₃ + 3H₂SO₄ → Fe₂(SO₄)₃ + 3H₂O). Washing rinses out insoluble rock, and crystallising pulls pure salt back out of solution.",
        "&eHow:&r dissolve, wash and crystallise, then inject crystals with HCl, purify shards with O₂, crush clumps. Dirty dust goes to the MI Centrifuge for byproducts.",
        "&eTip:&r each stage can also be fed raw ore directly, so a half-built line still gives 3x or 4x."]),
    Q("mk2_heaters", 8, 6, [item(MEK + "resistive_heater"), item(MEK + "fuelwood_heater"), item(MEK + "basic_thermodynamic_conductor", 8)], "Heating the Plant", subtitle="Heat is a resource you can pipe", deps=["pw_brine"], xp=120, desc=[
        "&eWhat:&r the Resistive Heater turns FE into heat; the Fuelwood Heater burns furnace fuel. Thermodynamic Conductors carry the heat to where it's needed, such as a Thermal Evaporation Plant.",
        "&eChemistry:&r evaporation speeds up with temperature because more water molecules have enough energy to escape the surface. The conductors are copper in steel: copper conducts heat about 8 times better than steel.",
        "&eHow:&r heaters need a steel casing and a circuit or Energy Tablet; conductors are steel and copper (check JEI). Watch the plant's temperature in its GUI.",
        "&eTip:&r a hot plant in a desert biome runs much faster than a cold one in the snow."]),
    Q("mk2_salt", 10, 6, [item(MEK + "salt", 16)], "Salt and Sodium", subtitle="What brine leaves behind", deps=["mk2_heaters", "t4_separator"], xp=120, desc=[
        "&eWhat:&r brine from the evaporation plant crystallises into salt, and splits into sodium and chlorine in the Electrolytic Separator.",
        "&eChemistry:&r real sodium is made by electrolysing molten NaCl (2NaCl → 2Na + Cl₂, the Downs cell). Salt is also a classic HCl source: NaCl + H₂SO₄ → NaHSO₄ + HCl.",
        "&eHow:&r Chemical Crystallizer: 15 mB brine → 1 salt. Electrolytic Separator: brine → sodium + chlorine. Salt also counts as a hydrogen chloride source in an HCl machine's chemical item slot (press U on Salt in JEI).",
        "&eTip:&r sodium is the coolant for the best fission setups (see the generator band)."]),

    # --- Pressurized reactions, substrate, HDPE and Meka-gear (y = 9 / 10.5) -------------------
    Q("mk2_dynamic_tank", 0, 9, [item(MEK + "dynamic_tank", 16), item(MEK + "dynamic_valve", 2), item(MEK + "structural_glass", 4)], "Dynamic Tank", subtitle="Your first Mekanism multiblock", deps=["t3_mekcircuit"], xp=100, desc=[
        "&eWhat:&r a hollow multiblock tank of any size from 3x3x3 up, for huge amounts of a fluid or a chemical.",
        "&eHow:&r dynamic tank blocks (steel and a bucket) for the frame, structural glass for walls, and valves to pipe in and out. The layout is in &eJust Enough Mekanism Multiblocks&r in JEI.",
        "&eTip:&r one dynamic tank block is also a part in the PRC and the Chemical Oxidizer."]),
    Q("mk2_prc", 2, 9, [item(MEK + "pressurized_reaction_chamber")], "Pressurized Reaction Chamber", subtitle="Solid, liquid and gas in, products out", deps=["t4_separator", "mk2_dynamic_tank"], xp=120, desc=[
        "&eWhat:&r the PRC reacts an item, a fluid and a gas together under pressure. It makes substrate, HDPE, plutonium and polonium pellets, and gasifies coal and wood.",
        "&eChemistry:&r pressure pushes gas molecules closer together so they collide with the other reactants more often. Le Chatelier: a reaction that shrinks gas volume is favoured by high pressure.",
        "&eHow:&r Basic Control Circuits, Infused Alloy, steel, an Enrichment Chamber, a Dynamic Tank and chemical tanks (check JEI). Press &eU&r on it in JEI for every recipe.",
        "&eTip:&r it often makes two products at once (an item and a gas). Give each output side its own pipe."]),
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
    Q("mk2_module_base", 8, 9, [item(MEK + "module_base", 4), item(MEK + "modification_station")], "Modules", subtitle="The Modification Station", deps=["mk2_hdpe_parts", "t6_pu", "t6_polonium"], xp=250, desc=[
        "&eWhat:&r module bases are the blank every MekaSuit and Meka-Tool module is built on. The Modification Station installs modules into your gear.",
        "&eHow:&r module base: an HDPE sheet in tin ingots and bronze nuggets (makes 2). Station: HDPE sheets, a chest, Ultimate Control Circuits (EV), a steel casing and a polonium pellet (check JEI).",
        "&eTip:&r press U on a Module Base in JEI to see every module and what each one needs."]),
    Q("mk2_mekatool", 10, 8.25, [item(MEK + "meka_tool")], "Meka-Tool", subtitle="Every tool, upgradable", deps=["mk2_module_base"], xp=300, desc=[
        "&eWhat:&r the Atomic Disassembler grown up: one FE-powered tool that mines, digs, chops and fights, and takes modules for range, speed, silk touch, veinmining and more.",
        "&eHow:&r an Atomic Disassembler, a Configurator, HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI).",
        "&eTip:&r it drinks power fast with big modules. Carry a charged energy cube or wear the MekaSuit."]),
    Q("mk2_mekasuit_full", 10, 9.75, [item(MEK + "mekasuit_pants"), item(MEK + "mekasuit_boots")], "The Full MekaSuit", subtitle="Pants and boots finish the set", deps=["mk2_module_base", "tc_mekasuit"], xp=400, size=1.5, shape="hexagon", desc=[
        "&6Four pieces, one will. You remember standing in fire and feeling only warmth.&r",
        "&eWhat:&r the MekaSuit legs and boots, completing the armour started on the Tools page. Legs take movement and locomotion modules; boots take jump and fall protection.",
        "&eHow:&r netherite leggings / boots in HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI).",
        "&eTip:&r the full suit shares one energy pool through its modules. Charge it on a Chargepad or with a charging module."]),
    Q("mk2_pigment", 1, 10.5, [item(MEK + "pigment_extractor"), item(MEK + "painting_machine")], "Pigments", subtitle="Colour as a chemical", deps=["mk2_prc", "t4_mv"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r the Pigment Extractor pulls coloured pigment out of dyes; the Painting Machine applies it to blocks and items.",
        "&eChemistry:&r a pigment's colour comes from the light its molecules absorb: indigo absorbs orange-red light, so it looks blue.",
        "&eHow:&r the extractor needs Basic Circuits; the Painting Machine needs an Advanced Control Circuit (MV)."]),
    Q("mk2_coal_gas", 3, 10.5, [item(MEK + "dust_sulfur", 16)], "Coal Gasification", subtitle="Coal, steam and oxygen into hydrogen", deps=["mk2_prc"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the PRC can gasify coal: coal + water + oxygen → hydrogen gas, with the coal's sulfur left behind as sulfur dust.",
        "&eChemistry:&r the real water-gas reaction is C + H₂O → CO + H₂ at about 1,000 °C; a little oxygen burns part of the coal to keep it hot. Coal holds 0.5-5% sulfur, which refineries recover as elemental sulfur.",
        "&eHow:&r PRC with any coal or coal dust, water and O₂ (check JEI). Logs and sawdust gasify the same way into charcoal dust.",
        "&eTip:&r a handy extra sulfur source for the contact process."]),
    Q("mk2_chem_plant", 5, 10.5, [item(MEK + "chemical_infuser"), item(MEK + "chemical_oxidizer"), item(MEK + "electrolytic_separator"), item(MEK + "pressurized_reaction_chamber"),
                                  item(MEK + "chemical_washer"), item(MEK + "chemical_crystallizer"), item(MEK + "chemical_dissolution_chamber"),
                                  item(MEK + "isotopic_centrifuge"), item(MEK + "solar_neutron_activator"), item(MEK + "sps_port")],
      "Challenge: The Full Chemical Plant", subtitle="One of every Mekanism chemical machine", deps=["mk2_prc", "t7_sps"], xp=500, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each of Mekanism's ten chemical machines, from the Chemical Infuser to an SPS port.",
        "&eChemistry:&r together they cover the unit operations of a real chemical plant: reaction, oxidation, electrolysis, washing, crystallisation, dissolution and isotope separation.",
        "&eHow:&r most are on the main path (see the links on the left). The washer, crystallizer and dissolution chamber are MV in this pack; the centrifuge needs Ultimate Control Circuits (EV).",
        "&eTip:&r an optional collection. Keep spares in a chest as you build each one."]),

    # --- Transmitters and logistics (y = 12 / 13.5) ---------------------------------------------
    Q("mk2_cables", 0, 12, [item(MEK + "basic_universal_cable", 8), item(MEK + "basic_mechanical_pipe", 8)], "Cables and Pipes", subtitle="Energy and fluids, Mekanism style", deps=["t3_mekcircuit"], xp=50, desc=[
        "&eWhat:&r Universal Cable carries FE, Mechanical Pipe carries fluids. With pressurized tubes (gases) and conductors (heat) they make Mekanism's four transmitter types.",
        "&eHow:&r steel with redstone (cable) or a bucket (pipe), 8 per craft. Higher tiers wrap 8 of the lower tier around an alloy.",
        "&eTip:&r transmitters of the same type join into one network. Colour them with a Configurator or paint to keep two networks apart."]),
    Q("mk2_transporter", 2, 12, [item(MEK + "basic_logistical_transporter", 16)], "Logistical Transporters", subtitle="Item pipes you can see", deps=["mk2_cables"], xp=60, desc=[
        "&eWhat:&r item pipes that carry stacks to the nearest inventory that will take them, and show the items moving.",
        "&eHow:&r steel around a Basic Control Circuit, 8 per craft.",
        "&eTip:&r a transporter's colour (set with the Configurator) only delivers into sides of the same colour."]),
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
    Q("mk2_security", 11, 13.5, [item(MEK + "personal_chest"), item(MEK + "security_desk")], "Mine, Not Yours", subtitle="Personal storage and a security desk", deps=["mk2_transporter"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r a Personal Chest only opens for its owner. The Security Desk sets who may use your Mekanism blocks: you, a trusted list, or everyone.",
        "&eHow:&r personal chest: steel, glass, chests and a Basic Control Circuit. Security desk: steel, glass, a Network Reader and &eElite Control Circuits&r (HV) (check JEI).",
        "&eTip:&r on a shared server, lock your reactor controls."]),

    # --- Generators and reactor multiblocks (y = 16 / 17.5) -------------------------------------
    # Heat, gas-burning, bio, solar, wind, turbine casing, fission and fusion are in power.py and t6 (linked on the left).
    Q("mk2_boiler", 0, 16, [item(MEK + "boiler_casing", 16), item(MEK + "boiler_valve", 2), item(MEK + "superheating_element", 4), item(MEK + "pressure_disperser")],
      "Thermoelectric Boiler", subtitle="Water into steam, by the tank", deps=["t6_fission"], xp=150, desc=[
        "&eWhat:&r a multiblock boiler that turns water into steam, heated by Superheating Elements (power) or by hot coolant from a fission reactor.",
        "&eChemistry:&r boiling water takes 2,260 J per gram, far more than heating it. That latent heat is what the turbine later turns back into work.",
        "&eHow:&r the layout is in &eJust Enough Mekanism Multiblocks&r in JEI: casing walls, valves, a layer of pressure dispersers, and elements on the bottom.",
        "&eTip:&r a sodium-cooled fission reactor sends heated sodium here instead of boiling water itself."]),
    Q("mk2_sodium", 2, 16, [tick()], "Sodium Coolant", subtitle="A liquid metal carries the heat", deps=["mk2_boiler"], xp=200, desc=[
        "&eWhat:&r cool your fission reactor with sodium instead of water. It returns as superheated sodium, which the Thermoelectric Boiler uses to make steam before sending the sodium back.",
        "&eChemistry:&r sodium melts at 98 °C and boils at 883 °C, so it stays liquid at reactor temperatures without high pressure. Real fast reactors use it, and keep it away from water, which it reacts with violently.",
        "&eHow:&r sodium comes from brine in the Electrolytic Separator (see Salt and Sodium). Pipe it into the reactor, superheated sodium out to a boiler valve, and the cooled sodium back. Click to confirm once it runs.",
        "&eTip:&r one sodium loop feeds a much bigger boiler and turbine than water cooling does."]),
    Q("mk2_turbine_shell", 4, 16, [item(GEN + "turbine_valve", 2), item(GEN + "turbine_vent", 8)], "Turbine Valves and Vents", subtitle="Steam in, spent steam out", deps=["pw_turbine"], xp=150, desc=[
        "&eWhat:&r valves feed steam in and take power out; vents let the spent steam leave through the walls above the rotor.",
        "&eChemistry:&r a turbine extracts work as steam expands and cools. The more vent area, the more steam can pass per tick.",
        "&eHow:&r valve: turbine casings around an Advanced Control Circuit (MV). Vent: casings around iron bars (check JEI).",
        "&eTip:&r the turbine GUI shows whether vent flow or blade count is your limit."]),
    Q("mk2_turbine_parts", 6, 16, [item(GEN + "turbine_rotor", 4), item(GEN + "turbine_blade", 8), item(GEN + "rotational_complex"), item(GEN + "electromagnetic_coil", 2), item(GEN + "saturating_condenser", 4)],
      "Turbine Internals", subtitle="Rotor, blades, coils, condensers", deps=["mk2_turbine_shell"], xp=200, desc=[
        "&eWhat:&r the moving parts inside an Industrial Turbine. More blades and coils mean more power from the same steam.",
        "&eChemistry:&r condensers turn spent steam back into water, so the loop reuses the same water over and over.",
        "&eHow:&r stack rotors with two blades each on the centre column, a Rotational Complex on top, then coils and condensers above. See Just Enough Mekanism Multiblocks.",
        "&eTip:&r the turbine's GUI shows whether steam flow or blade count is the limit."]),
    Q("mk2_fusion_build", 8, 16, [item(GEN + "fusion_reactor_frame", 16), item(GEN + "reactor_glass", 4), item(GEN + "fusion_reactor_port", 2), item(GEN + "laser_focus_matrix")],
      "Building the Fusion Reactor", subtitle="Frame, glass, ports and a laser window", deps=["pw_dt_fuel"], xp=300, desc=[
        "&eWhat:&r the shell of the Fusion Reactor: frames, reactor glass, ports for fuel and output, and a Laser Focus Matrix to let the ignition laser in.",
        "&eHow:&r the 3D layout is in &eJust Enough Mekanism Multiblocks&r in JEI. The controller sits on top in the middle.",
        "&eTip:&r ports switch between input and output with a Configurator."]),
    Q("mk2_ignition", 10, 16, [item(MEK + "laser", 3), item(MEK + "laser_amplifier")], "Ignition", subtitle="A laser hot enough to start a star", deps=["mk2_fusion_build"], xp=200, desc=[
        "&eWhat:&r lasers charge a Laser Amplifier, which fires a single huge pulse into the reactor to ignite it.",
        "&eChemistry:&r deuterium and tritium only fuse above about 100 million °C, when the nuclei move fast enough to beat their electric repulsion.",
        "&eHow:&r put a filled Hohlraum in the controller, aim the amplifier at the Laser Focus Matrix and fire it with a redstone signal. Then go to the Fusion quest.",
        "&eTip:&r once lit, the reactor sustains itself as long as fuel keeps coming."]),
    Q("mk2_gen_field", 0, 17.5, [item(GEN + "heat_generator"), item(GEN + "solar_generator"), item(GEN + "advanced_solar_generator"), item(GEN + "wind_generator"), item(GEN + "gas_burning_generator"), item(GEN + "bio_generator")],
      "Challenge: Every Generator", subtitle="Six ways to make FE", deps=["pw_heat"], xp=300, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each Mekanism generator: heat, solar, advanced solar, wind, gas-burning and bio.",
        "&eChemistry:&r between them: combustion, the photovoltaic effect, kinetic energy of air, and the energy stored in plant sugars by photosynthesis.",
        "&eHow:&r each one has its own quest on the Power page. The wind generator needs an Energy Tablet; the advanced solar is built from four basic solar generators.",
        "&eTip:&r none of these beats fission or fusion, but they never need fuel deliveries."]),
    Q("mk2_waste_barrel", 3, 17.5, [item(MEK + "radioactive_waste_barrel", 2)], "Radioactive Waste Barrel", subtitle="Somewhere safe for the leftovers", deps=["t6_fission"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r a barrel that stores spent nuclear waste and other radioactive chemicals, and lets them slowly decay.",
        "&eChemistry:&r radioactive decay can't be sped up by chemistry; you can only wait out the half-life. Real spent fuel spends years in cooling ponds, then decades in dry casks.",
        "&eHow:&r check JEI for the recipe. Pipe waste into it with pressurized tubes; never vent it or break a full tube.",
        "&eTip:&r reprocessing waste into plutonium and polonium (the T6 page) is better than storing it."]),
    Q("mk2_fusion_logic", 10, 17.5, [item(GEN + "fusion_reactor_logic_adapter")], "Fusion Logic Adapter", subtitle="Let redstone watch the star", deps=["mk2_ignition"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r a reactor block that outputs redstone for things like ignition state, plasma temperature or low fuel.",
        "&eHow:&r a fusion reactor frame surrounded by redstone; swap one frame of the shell for it and pick the mode in its GUI.",
        "&eTip:&r wire \"ready for ignition\" to your laser amplifier to relight the reactor automatically."]),

    # --- Mekanism Tools armour (y = 19.5 / 21) --------------------------------------------------
    Q("mk2_armor_osmium", 0, 19.5, armour("osmium"), "Osmium Armour", subtitle="The densest metal, worn", deps=["t3_infuser"], xp=100, desc=[
        "&eWhat:&r Mekanism Tools adds a full armour set for each of its metals. Osmium is the first, and tougher than iron.",
        "&eChemistry:&r osmium is the densest natural element (22.6 g/cm³). Real osmium is brittle and its oxide, OsO₄, is volatile and very toxic, so nobody actually wears it.",
        "&eHow:&r osmium ingots in the usual armour shapes (check JEI).",
        "&eTip:&r bronze, steel and lapis sets exist too; see JEI for their stats."]),
    Q("mk2_armor_obsidian", 2, 19.5, armour("refined_obsidian"), "Refined Obsidian Armour", subtitle="The best of Mekanism Tools", deps=["mk2_armor_osmium", "tc_obsidian_paxel"], xp=250, desc=[
        "&eWhat:&r the strongest Mekanism Tools armour: high protection and toughness, good until the MekaSuit.",
        "&eChemistry:&r obsidian is volcanic glass: lava cooled too fast for crystals to form. Infusing it with diamond and pressing it with osmium makes Mekanism's refined form.",
        "&eHow:&r refined obsidian ingots from the Osmium Compressor, in armour shapes (check JEI)."]),
    Q("mk2_armor_glowstone", 4, 21, armour("refined_glowstone"), "Refined Glowstone Armour", subtitle="Light, pressed into metal", deps=["mk2_armor_obsidian"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the other Osmium Compressor metal as an armour set. Check JEI for how it compares with refined obsidian.",
        "&eChemistry:&r real glow-in-the-dark materials store energy in their crystal and release it as light (phosphorescence); glowstone is Minecraft's version.",
        "&eHow:&r Osmium Compressor: glowstone dust + osmium → refined glowstone ingots, then armour shapes."]),

    # --- Mekanism: More Machine (y = 22.5 .. 25.5) ----------------------------------------------
    Q("mk2_mm_cnc", 0, 24, [anyof([MM + "cnc_stamper", MM + "cnc_lathe", MM + "cnc_rolling_mill"])], "CNC Machines", subtitle="More Machine: stamp, turn and roll", deps=["t3_mekcircuit"], xp=80, desc=[
        "&eWhat:&r Mekanism: More Machine adds CNC machines: the Stamper presses plates, the Lathe turns rods, the Rolling Mill rolls wire.",
        "&eHow:&r the CNC Stamper needs Basic Control Circuits, Basic Alloy, pistons and a steel casing. The Lathe also needs a Robit (check JEI). Any one counts.",
        "&eTip:&r MI's machines make most plates already. Use CNC machines for the mod recipes that list them in JEI (the stamper also prints AE2 processors)."]),
    Q("mk2_mm_recycler", 2, 24, [item(MM + "recycler"), item(MM + "scrap", 8)], "Recycler", subtitle="Stone and dirt into scrap", deps=["mk2_mm_cnc", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the Recycler grinds cheap blocks (stone, dirt, substrate) and sometimes leaves Scrap.",
        "&eHow:&r a Crusher, Advanced Control Circuits (MV), Infused Alloy and osmium (check JEI). About 1 stone in 6 gives a scrap.",
        "&eTip:&r 64 scrap compress into a Scrap Box, the first step towards UU-Matter. Start stockpiling early."]),
    Q("mk2_mm_large", 2, 22.5, [anyof([MM + "large_heat_generator", MM + "large_gas_burning_generator", MM + "large_wind_generator", MM + "large_chemical_infuser",
                                       MM + "large_electrolytic_separator", MM + "large_rotary_condensentrator", MM + "large_solar_neutron_activator", MM + "large_pigment_mixer"])],
      "Large Machines", subtitle="Big single-block versions", deps=["mk2_mm_cnc", "t6_pu"], xp=250, desc=[
        "&eWhat:&r More Machine's large machines do the work of many normal ones, such as the Large Electrolytic Separator or Large Chemical Infuser.",
        "&eHow:&r most need a Robit, steel blocks and ultimate-tier tanks or circuits (EV). Any one counts; check JEI for each.",
        "&eTip:&r the Large Solar Neutron Activator is a big help for polonium and tritium."]),
    Q("mk2_mm_replicator", 4, 24, [item(MM + "replicator"), item(MM + "uu_matter")], "UU-Matter", subtitle="Matter from antimatter", deps=["mk2_mm_recycler", "t7_antimatter"], xp=500, size=1.5, shape="hexagon", desc=[
        "&6Scrap, crystal, antimatter, and then anything. You remember when making matter was just a thought.&r",
        "&eWhat:&r UU-Matter is More Machine's universal matter. The Replicator turns it back into items.",
        "&eHow:&r scrap boxes become Empty Crystals in the PRC (with fusion fuel and a special gas, check JEI). 64 crystals + antimatter in the Antiprotonic Nucleosynthesizer (an optional t7 quest) make one UU-Matter.",
        "&eTip:&r the Replicator needs Ultimate Control Circuits and Atomic Alloy. Check JEI for what it can copy."]),
    Q("mk2_mm_presser", 0, 25.5, [item(MM + "presser")], "Presser", subtitle="An upgraded stamper", deps=["mk2_mm_cnc", "t5_hv"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r the Presser builds on the CNC Stamper and makes processors and other pressed parts (check JEI for its recipes).",
        "&eHow:&r a CNC Stamper with Elite Control Circuits (HV), Reinforced Alloy and pistons.",
        "&eTip:&r press U on the Presser in JEI to see what it makes."]),
    Q("mk2_mm_planting", 2, 25.5, [item(MM + "planting_station")], "Planting Station", subtitle="Grow crops in a box", deps=["mk2_mm_recycler", "t5_hv"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r a machine that grows seeds and saplings indoors and outputs the harvest.",
        "&eChemistry:&r photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂, here powered by electricity instead of sunlight.",
        "&eHow:&r Elite Control Circuits (HV), Reinforced Alloy, bio fuel and a steel casing (check JEI)."]),
    Q("mk2_mm_doll", 4, 25.5, [item(MM + "author_doll")], "A Small Tribute", subtitle="Secret: the author, in doll form", deps=["mk2_mm_replicator"], xp=200, secret=True, loot="secret", desc=[
        "&eWhat:&r a decorative doll of More Machine's author, compressed out of 64 UU-Matter and a breath of antimatter in the Osmium Compressor.",
        "&eTip:&r the mod's modeller has a doll too, made from UU-Matter gas instead. Thank you, modders."]),
    Q("mk2_mm_gas", 6, 25.5, [item(MM + "ambient_gas_collector")], "Ambient Gas Collector", subtitle="Pull gas out of thin air", deps=["mk2_mm_recycler", "t6_pu"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r a machine that collects gas from its surroundings (check JEI and its GUI for what it gathers).",
        "&eChemistry:&r real air is 78% N₂, 21% O₂ and 1% argon; industry separates it by cooling it into a liquid and distilling it.",
        "&eHow:&r Atomic Alloy, an osmium block, an ultimate chemical tank and ultimate tubes (EV)."]),

    # --- Mekanism Extras (y = 28 / 29.5) --------------------------------------------------------
    Q("mk2_ex_radiance", 0, 28, [item(EX + "dust_radiance", 4), item(EX + "alloy_radiance", 2)], "Radiance", subtitle="Mekanism Extras begins", deps=["t6_pu", "t6_yellowcake"], xp=200, desc=[
        "&eWhat:&r Mekanism Extras adds four tiers beyond ultimate: absolute, supreme, cosmic and infinite. Each needs a new alloy, starting with Radiance.",
        "&eHow:&r Osmium Compressor: glowstone dust + uranium oxide gas → Radiance Dust. Enrich it, then infuse Atomic Alloy with radiance (check JEI).",
        "&eTip:&r uranium oxide comes from oxidising yellowcake in the Chemical Oxidizer."]),
    Q("mk2_ex_absolute", 2, 28, [item(EX + "absolute_control_circuit", 2)], "Absolute Control Circuit", subtitle="Tier five", deps=["mk2_ex_radiance"], xp=250, desc=[
        "&eWhat:&r the first Extras circuit: an Ultimate Control Circuit between two Radiance Alloys.",
        "&eHow:&r craft it, or infuse an ultimate circuit with radiance in the Metallurgic Infuser.",
        "&eTip:&r absolute factories, cubes and tanks all start here."]),
    Q("mk2_ex_supreme", 4, 28, [item(EX + "alloy_thermonuclear", 2), item(EX + "supreme_control_circuit")], "Supreme Control Circuit", subtitle="Thermonuclear alloy", deps=["mk2_ex_absolute"], xp=300, desc=[
        "&eWhat:&r tier six. Its alloy is Thermonuclear: Radiance Alloy infused with thermonuclear material.",
        "&eHow:&r enriched radiance reacts with lava and molten thermonuclear in the PRC (check JEI for the full chain).",
        "&eTip:&r the circuit is an Absolute Control Circuit between two Thermonuclear Alloys."]),
    Q("mk2_ex_cosmic", 6, 28, [item(EX + "alloy_shining", 2), item(EX + "cosmic_control_circuit")], "Cosmic Control Circuit", subtitle="Shining alloy, made with antimatter", deps=["mk2_ex_supreme", "t7_antimatter"], xp=400, desc=[
        "&eWhat:&r tier seven. Its alloy, Shining, needs enriched thermonuclear transmuted with antimatter.",
        "&eHow:&r Antiprotonic Nucleosynthesizer: enriched thermonuclear + antimatter → enriched shining. Then infuse Thermonuclear Alloy with it (check JEI).",
        "&eTip:&r the Nucleosynthesizer is slow; run it on fusion power."]),
    Q("mk2_ex_infinite", 8, 28, [item(EX + "alloy_spectrum", 2), item(EX + "infinite_control_circuit")], "Infinite Control Circuit", subtitle="The last tier", deps=["mk2_ex_cosmic"], xp=600, size=1.5, shape="gear", desc=[
        "&6Infinite, the circuit says. You remember when that word described you.&r",
        "&eWhat:&r tier eight, the top of Mekanism Extras. Its alloy is Spectrum.",
        "&eHow:&r Osmium Compressor: enriched shining + antimatter → enriched spectrum; infuse Shining Alloy with it, then craft the circuit (check JEI)."]),
    Q("mk2_ex_factory", 1, 29.5, [anyof(ex_factories("absolute"))], "Absolute Factory", subtitle="Factories beyond ultimate", deps=["mk2_ex_absolute"], xp=250, optional=True, tokens=1, desc=[
        "&eWhat:&r Extras factories have more slots than ultimate ones, and Extras adds factory types base Mekanism lacks (oxidizing, washing, crystallizing, centrifuging...).",
        "&eHow:&r upgrade an ultimate factory with Absolute Control Circuits and Radiance Alloy, or use an Absolute Tier Installer. Any absolute factory counts.",
        "&eTip:&r the extra factory types are the big win: a washing or crystallizing factory speeds up the whole 5x line."]),
    Q("mk2_ex_naquadah", 4, 29.5, [item(EX + "raw_naquadah", 8)], "Naquadah", subtitle="A metal from science fiction", deps=["mk2_ex_supreme"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r Naquadah ore, added by Mekanism Extras. It is the fuel for the Naquadah Reactor.",
        "&eChemistry:&r naquadah is not real; it comes from the Stargate films. Every other material on this page is real chemistry.",
        "&eHow:&r Naquadah ore generates underground and in the End. Jade shows the block name when you look at it.",
        "&eTip:&r it processes like other Mekanism ores: dissolve, wash and crystallise for the best yield."]),
    Q("mk2_ex_reactor", 8, 29.5, [item(EX + "naquadah_reactor_controller"), item(EX + "naquadah_reactor_casing", 16)], "Naquadah Reactor", subtitle="A fusion reactor on fictional fuel", deps=["mk2_ex_cosmic", "mk2_ex_naquadah"], xp=500, optional=True, tokens=2, desc=[
        "&eWhat:&r a fusion-style power multiblock from Mekanism Extras that runs on naquadah-based fuel.",
        "&eHow:&r casings are lead blocks transmuted with antimatter in the Nucleosynthesizer; the controller needs Cosmic Control Circuits. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r the fuel chain starts with fluorinated naquadah-uranium fuel. Check JEI for each step."]),
], links=[("t3_infuser", -4, 0), ("t3_mekcircuit", -4, 2), ("t4_mv", -6, 1), ("t4_ore4", -4, 4), ("t4_ore5", -4, 6), ("pw_brine", -6, 6),
          ("t4_separator", -4, 8), ("t5_hdpe", -6, 9), ("tc_mekasuit", -4, 10), ("t7_sps", -6, 11), ("t6_centrifuge", -4, 12),
          ("t6_fission", -4, 16), ("pw_turbine", -6, 16), ("pw_fusion", -4, 18), ("tc_obsidian_paxel", -4, 20),
          ("t7_opt_nucleo", -4, 24), ("t6_yellowcake", -4, 28)])
