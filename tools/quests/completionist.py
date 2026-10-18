"""Quest chapter: completionist (collection challenges). See tools/quests/STYLE.md.
Every quest here is optional. Each one depends on the main-path quest that makes the collection possible.
"""
from questlib import Q, Chapter, item, tick, biome, anytag, anyof, SIDE  # noqa: F401

MC = "minecraft"
MI = "modern_industrialization"
COLORS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
          "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]


def els(*names):
    """One item task per ChemLib element."""
    return [item(f"chemlib:{n}") for n in names]


def ore(*ids):
    """One task per ore: stone or deepslate variant both count."""
    return [anyof(list(pair)) for pair in ids]


def biomes(*ids):
    return [biome(b) for b in ids]


FACTORIES = ["smelting", "enriching", "crushing", "compressing", "combining",
             "purifying", "injecting", "infusing", "sawing"]
FACTORY_TIER = {t: [f"mekanism:{t}_{f}_factory" for f in FACTORIES]
                for t in ("basic", "advanced", "elite", "ultimate")}

CHAPTER = Chapter("completionist", "Completionist", "minecraft:white_wool",
        ["Collections for the thorough demigod. All optional."], SIDE, [
    # --- Colours and trees (y=0) ---------------------------------------------------------------
    Q("cp_wool", 0, 0, [item(f"{MC}:{c}_wool") for c in COLORS], "Sixteen Colours of Wool",
      deps=["gs_wake"], xp=50, optional=True, tokens=1, subtitle="One block of every wool colour", desc=[
        "&6You remember making a world with every colour in it. Start small: sixteen.&r",
        "&eWhat:&r a collection page. Nothing here is needed to progress; every quest is a bragging right with a small reward.",
        "&eHow:&r shear sheep and dye white wool in a crafting grid (wool + dye). Sheep can also be dyed before shearing.",
        "&eTip:&r dye a sheep once and it grows that colour back forever. A pen of sixteen sheep is a wool farm."]),
    Q("cp_dyes", 2, 0, [item(f"{MC}:{c}_dye") for c in COLORS], "The Dyer's Palette",
      deps=["cp_wool"], xp=50, optional=True, tokens=1, subtitle="All sixteen dyes", desc=[
        "&eWhat:&r every dye colour, from flowers, plants, minerals and mixing.",
        "&eChemistry:&r real dyes are molecules that absorb some wavelengths of light. Lapis gets its blue from lazurite, a sodium aluminosilicate with sulfur ions trapped in its cage.",
        "&eHow:&r flowers give most primaries; cocoa gives brown, cactus smelts into green, ink sacs give black. Mix the rest (JEI shows every recipe).",
        "&eTip:&r bone meal on grass and flowers gives you endless primaries."]),
    Q("cp_concrete", 4, 0, [item(f"{MC}:{c}_concrete") for c in COLORS], "Concrete Rainbow",
      deps=["cp_dyes"], xp=75, optional=True, tokens=2, subtitle="All sixteen concretes", desc=[
        "&eWhat:&r one block of every concrete colour.",
        "&eChemistry:&r real concrete sets by hydration, not drying: water reacts with the calcium silicates in cement to grow a stiff mesh of calcium silicate hydrate.",
        "&eHow:&r craft concrete powder (4 sand, 4 gravel, 1 dye), then place it in water or touch it with water to set it.",
        "&eTip:&r place powder in front of a water stream and mine it with a good pickaxe: fast and repeatable."]),
    Q("cp_saplings", 8, 0, [item(f"{MC}:{s}_sapling") for s in ("oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "cherry")]
      + [item(f"{MC}:mangrove_propagule"), item(f"{MC}:azalea"), item(f"{MC}:flowering_azalea")],
      "Every Vanilla Tree", deps=["gs_table"], xp=50, optional=True, tokens=1, subtitle="Ten saplings from the vanilla world", desc=[
        "&eWhat:&r one sapling from every vanilla tree, including the mangrove propagule and both azaleas.",
        "&eChemistry:&r every tree builds itself from air and water: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂, powered by sunlight.",
        "&eHow:&r break leaves in each biome. Cherry groves sit on mountain meadows; azaleas grow above lush caves; propagules hang under mangrove leaves.",
        "&eTip:&r a Nature's Compass finds the biome you need."]),
    Q("cp_world_trees", 10, 0, [item(f"biomesoplenty:{s}_sapling") for s in ("redwood", "jacaranda", "magic", "palm", "snowblossom")]
      + [item(f"regions_unexplored:{s}_sapling") for s in ("baobab", "eucalyptus", "joshua", "sky_wisteria", "kapok")],
      "Trees of Distant Lands", deps=["cp_saplings"], xp=100, optional=True, tokens=2, subtitle="Ten saplings from modded biomes", desc=[
        "&eWhat:&r saplings from Biomes O' Plenty and Regions Unexplored trees.",
        "&eHow:&r find the biome first: redwood and jacaranda groves, mystic groves (magic), tropics (palm), snowblossom groves; baobab savannas, eucalyptus forests, Joshua deserts, wisteria groves and rainforests.",
        "&eTip:&r JEI shows each sapling's leaves. Botany Pots grow any of them without a forest."]),

    # --- Music discs (y=2) ---------------------------------------------------------------------
    Q("cp_discs_creeper", 0, 2, [item(f"{MC}:music_disc_{d}") for d in
      ("13", "cat", "blocks", "chirp", "far", "mall", "mellohi", "stal", "strad", "ward", "11", "wait")],
      "The Creeper Collection", deps=["gs_shield"], xp=150, optional=True, tokens=2, subtitle="Twelve discs that creepers drop", desc=[
        "&eWhat:&r the twelve classic discs. A creeper drops one when a skeleton (or stray or bogged) kills it.",
        "&eHow:&r lure creepers into a skeleton's line of fire, or build a mob farm that lets skeletons do the shooting. Dungeon chests also hold a few.",
        "&eTip:&r a skeleton spawner dungeon is perfect: trap the skeletons, then walk creepers past them."]),
    Q("cp_discs_treasure", 2, 2, [item(f"{MC}:music_disc_pigstep"), item(f"{MC}:music_disc_otherside"),
      item(f"{MC}:music_disc_relic"), item(f"{MC}:music_disc_5")],
      "Treasure Discs", deps=["cp_discs_creeper", "t2_nether", "w_ancient"], xp=200, optional=True, tokens=2,
      subtitle="Pigstep, otherside, Relic and 5", desc=[
        "&eWhat:&r four discs that only come from structures.",
        "&eHow:&r Pigstep: bastion remnant chests. otherside: dungeon and stronghold chests (rare). Relic: brush suspicious gravel in trail ruins. 5: craft nine disc fragments found in ancient city chests.",
        "&eTip:&r an Explorer's Compass points to the structure you need."]),
    Q("cp_discs_trial", 4, 2, [item(f"{MC}:music_disc_creator"), item(f"{MC}:music_disc_creator_music_box"),
      item(f"{MC}:music_disc_precipice")],
      "Trial Discs", deps=["cp_discs_creeper"], xp=200, optional=True, tokens=2, subtitle="Three discs from trial chambers", desc=[
        "&eWhat:&r the discs added with trial chambers.",
        "&eHow:&r Precipice comes from vaults opened with a trial key; Creator from ominous vaults (ominous trial key); Creator (Music Box) from decorated pots in the chambers.",
        "&eTip:&r drink an ominous bottle before a trial spawner to turn it ominous. Bring food, a shield and fire resistance."]),

    # --- Armor trims (y=2, right) ------------------------------------------------------------------
    Q("cp_trims_overworld", 8, 2, [item(f"{MC}:{t}_armor_trim_smithing_template") for t in
      ("coast", "dune", "wild", "sentry", "vex", "tide", "eye")],
      "Overworld Trims", deps=["gs_ironpick"], xp=150, optional=True, tokens=2, subtitle="Seven templates from Overworld structures", desc=[
        "&eWhat:&r armour trim templates decorate armour in a smithing table.",
        "&eHow:&r coast: shipwrecks. dune: desert pyramids. wild: jungle temples. sentry: pillager outposts. vex: woodland mansions. tide: elder guardians in ocean monuments. eye: strongholds.",
        "&eTip:&r copy a template with 7 diamonds and the block it's made of (check JEI) instead of hunting a second one."]),
    Q("cp_trims_archaeology", 10, 2, [item(f"{MC}:{t}_armor_trim_smithing_template") for t in
      ("wayfinder", "raiser", "shaper", "host")],
      "Dug-Up Trims", deps=["cp_trims_overworld"], xp=150, optional=True, tokens=2, subtitle="Four templates from trail ruins", desc=[
        "&eWhat:&r four trims buried in trail ruins.",
        "&eHow:&r brush suspicious gravel in trail ruins with a brush (feather, copper, stick). These are rare drops, so brush a lot.",
        "&eTip:&r the same gravel holds pottery sherds and the Relic disc."]),
    Q("cp_trims_deep", 12, 2, [item(f"{MC}:ward_armor_trim_smithing_template"), item(f"{MC}:silence_armor_trim_smithing_template")],
      "Trims of the Deep Dark", deps=["cp_trims_overworld", "w_ancient"], xp=200, optional=True, tokens=2,
      subtitle="Ward and Silence", desc=[
        "&eWhat:&r the two ancient city trims. Silence is the rarest template in the game.",
        "&eHow:&r loot ancient city chests. Sneak, wool on the floor, and don't let the shriekers call the Warden.",
        "&eTip:&r a stack of wool carpets silences your footsteps on sculk sensors."]),
    Q("cp_trims_nether_end", 14, 2, [item(f"{MC}:rib_armor_trim_smithing_template"), item(f"{MC}:snout_armor_trim_smithing_template"),
      item(f"{MC}:spire_armor_trim_smithing_template")],
      "Trims of Fire and Void", deps=["cp_trims_overworld", "t2_fortress", "w_elytra"], xp=200, optional=True, tokens=2,
      subtitle="Rib, Snout and Spire", desc=[
        "&eWhat:&r one trim each from Nether fortresses (rib), bastions (snout) and End cities (spire).",
        "&eHow:&r fortress chests, bastion chests and End city chests. Bring gold armour for the bastion.",
        "&eTip:&r bastion treasure rooms also hold the netherite upgrade template."]),
    Q("cp_trims_trial", 16, 2, [item(f"{MC}:flow_armor_trim_smithing_template"), item(f"{MC}:bolt_armor_trim_smithing_template")],
      "Trial Trims", deps=["cp_trims_overworld"], xp=150, optional=True, tokens=2, subtitle="Flow and Bolt", desc=[
        "&eWhat:&r the two trial chamber trims.",
        "&eHow:&r bolt comes from regular vaults (trial key); flow from ominous vaults (ominous trial key).",
        "&eTip:&r every player gets their own loot from each vault, so bring friends."]),

    # --- Ores (y=4) ----------------------------------------------------------------------------
    Q("cp_ores_overworld", 0, 4, ore(*[(f"{MC}:{o}_ore", f"{MC}:deepslate_{o}_ore") for o in
      ("coal", "iron", "copper", "gold", "redstone", "lapis", "diamond", "emerald")]),
      "Ore Cabinet: Overworld", deps=["gs_ironpick"], xp=100, optional=True, tokens=1, subtitle="Every vanilla Overworld ore, as a block", desc=[
        "&eWhat:&r one ore block of each vanilla Overworld ore (stone or deepslate both count).",
        "&eChemistry:&r real ores are minerals: iron as hematite (Fe₂O₃), copper as chalcopyrite (CuFeS₂), lapis as lazurite. Diamond is pure carbon.",
        "&eHow:&r you need a &eSilk Touch&r pickaxe so the ore drops itself. Emerald only grows under mountains.",
        "&eTip:&r place them in item frames as a display: a real geology cabinet."]),
    Q("cp_ores_nether", 2, 4, [item(f"{MC}:nether_gold_ore"), item(f"{MC}:nether_quartz_ore"), item(f"{MC}:ancient_debris")],
      "Ore Cabinet: Nether", deps=["cp_ores_overworld", "t2_debris"], xp=100, optional=True, tokens=1, subtitle="Three ores from the Nether", desc=[
        "&eWhat:&r Nether gold, Nether quartz and ancient debris.",
        "&eChemistry:&r real quartz is silicon dioxide, SiO₂, the same thing as sand and the silicon you refine later.",
        "&eHow:&r Silk Touch for the gold and quartz ores. Ancient debris always drops itself; mine around Y 15.",
        "&eTip:&r beds explode in the Nether. That's a fast (and loud) way to find debris."]),
    Q("cp_ores_mi", 4, 4, ore(*[(f"{MI}:{o}_ore", f"{MI}:deepslate_{o}_ore") for o in
      ("tin", "lead", "nickel", "bauxite", "antimony", "salt", "lignite_coal", "monazite")]),
      "Ore Cabinet: Industrial", deps=["cp_ores_overworld", "t0_tin"], xp=150, optional=True, tokens=2,
      subtitle="Eight Modern Industrialization ores", desc=[
        "&eWhat:&r one block of each common MI ore.",
        "&eChemistry:&r bauxite is aluminium hydroxide; antimony is mined as stibnite (Sb₂S₃); monazite is a rare-earth phosphate, (Ce,La,Nd)PO₄, often with thorium.",
        "&eHow:&r Silk Touch. Rich deposits sit at metal-specific depths: lead around Y −24 to 16, nickel lower at Y −32 to 8.",
        "&eTip:&r Jade shows the ore name as you look at it, so you can tell tin from lead in the dark."]),
    Q("cp_ores_deep", 6, 4, ore((f"{MI}:uranium_ore", f"{MI}:deepslate_uranium_ore"), (f"{MI}:tungsten_ore", f"{MI}:deepslate_tungsten_ore"),
      ("mekanism:osmium_ore", "mekanism:deepslate_osmium_ore"), ("mekanism:fluorite_ore", "mekanism:deepslate_fluorite_ore")),
      "Ore Cabinet: Deep and Rare", deps=["cp_ores_mi", "t3_osmium"], xp=200, optional=True, tokens=2,
      subtitle="Uranium, tungsten, osmium and fluorite", desc=[
        "&eWhat:&r the deep ores, as blocks.",
        "&eChemistry:&r uranium ore is uraninite (UO₂); tungsten comes from wolframite and scheelite (CaWO₄); fluorite is calcium fluoride, CaF₂, the source of the hydrofluoric acid you'll need for uranium.",
        "&eHow:&r Silk Touch. Uranium and tungsten deposits sit deep, around Y −56 to −24.",
        "&eTip:&r Mekanism's radiation comes from its nuclear fluids and waste later on. Hazmat gear is in Tools and Comfort."]),
    Q("cp_ore_hoard", 8, 4, [anytag("c:ores", 256)], "Ore Hoarder", deps=["cp_ores_mi"], xp=150,
      optional=True, tokens=1, subtitle="256 ore blocks of any kind", desc=[
        "&eWhat:&r four stacks of unprocessed ore blocks (anything tagged as an ore).",
        "&eHow:&r Silk Touch plus FTB Ultimine makes this quick. Keep them as blocks: Mekanism and MI process ore blocks too.",
        "&eTip:&r ore blocks wait patiently. Store them until your 5x line is ready and every block is worth more."]),

    # --- Circuits and factories (y=6) ----------------------------------------------------------
    Q("cp_circuits", 0, 6, [item(f"{MI}:analog_circuit"), item(f"{MI}:electronic_circuit"), item(f"{MI}:digital_circuit"),
      item(f"{MI}:processing_unit")], "Circuit Collection", deps=["t6_pu"], xp=200, optional=True, tokens=1,
      subtitle="LV, MV, HV and EV, side by side", desc=[
        "&eWhat:&r one of each MI circuit tier you have built: analog, electronic, digital, processing unit.",
        "&eChemistry:&r each tier stands on new chemistry: rubber, then aluminium, then polyethylene, then PVC and pure silicon.",
        "&eHow:&r you made all of these on the main path. Keep one of each.",
        "&eTip:&r frame them in order. It's a history of everything you've learned."]),
    Q("cp_quantum", 2, 6, [item(f"{MI}:quantum_circuit")], "Quantum Circuit", deps=["cp_circuits", "t6_plutonium", "t6_rare_pgm"],
      xp=500, optional=True, tokens=2, subtitle="The circuit beyond the main path", desc=[
        "&eWhat:&r MI's top circuit. Nothing on the main path needs it, which makes it the perfect trophy.",
        "&eHow:&r an Assembler: 4 processing units, 2 cooling cells, 2 qubits and a quantum circuit board. The board needs superconductor cable, plutonium batteries, iridium plates and helium-3 (check JEI for each).",
        "&eTip:&r iridium comes from the PGM residue line; plan the iridium before you start."]),
    Q("cp_fac_basic", 6, 6, [anyof(FACTORY_TIER["basic"])], "Basic Factory", deps=["t3_mekcircuit"], xp=75,
      optional=True, tokens=1, subtitle="Three items at once", desc=[
        "&eWhat:&r a Mekanism factory runs several copies of one machine in one block. Basic factories have 3 slots.",
        "&eHow:&r right-click a placed Mekanism machine with a Basic Tier Installer, or craft the factory (check JEI). Any basic factory counts.",
        "&eTip:&r a basic smelting factory with speed upgrades already beats a row of furnaces."]),
    Q("cp_fac_adv", 8, 6, [anyof(FACTORY_TIER["advanced"])], "Advanced Factory", deps=["cp_fac_basic", "t4_circuit"], xp=100,
      optional=True, tokens=1, subtitle="Five items at once", desc=[
        "&eWhat:&r advanced factories have 5 slots.",
        "&eHow:&r an Advanced Tier Installer on a basic factory. Its control circuit needs an MI electronic circuit (MV) and infused alloy.",
        "&eTip:&r upgrade in place: the installer keeps the factory's contents and settings."]),
    Q("cp_fac_elite", 10, 6, [anyof(FACTORY_TIER["elite"])], "Elite Factory", deps=["cp_fac_adv", "t5_hv"], xp=150,
      optional=True, tokens=1, subtitle="Seven items at once", desc=[
        "&eWhat:&r elite factories have 7 slots.",
        "&eHow:&r an Elite Tier Installer; its circuit needs an MI digital circuit (HV) and reinforced alloy.",
        "&eTip:&r factories sort their own input slots if you turn on auto-sort in the GUI."]),
    Q("cp_fac_ult", 12, 6, [anyof(FACTORY_TIER["ultimate"])], "Ultimate Factory", deps=["cp_fac_elite", "t6_pu"], xp=200,
      optional=True, tokens=2, subtitle="Nine items at once", desc=[
        "&eWhat:&r ultimate factories have 9 slots, the most Mekanism offers.",
        "&eHow:&r an Ultimate Tier Installer; its circuit needs an MI processing unit (EV) and atomic alloy.",
        "&eTip:&r one ultimate enriching factory can feed a whole 5x ore line's first step."]),
    Q("cp_fac_all", 14, 6, [item(i) for i in FACTORY_TIER["ultimate"]], "The Full Line-Up", deps=["cp_fac_ult"], xp=500,
      optional=True, tokens=2, subtitle="All nine ultimate factories", desc=[
        "&eWhat:&r every factory type at ultimate tier: smelting, enriching, crushing, compressing, combining, purifying, injecting, infusing and sawing.",
        "&eHow:&r build or upgrade one of each. Purifying and injecting are the 4x and 5x ore steps; infusing makes alloys.",
        "&eTip:&r this is a lot of atomic alloy. Automate the refined obsidian first."]),

    # --- The periodic table, block by block (y=8) ----------------------------------------------
    Q("cp_el_s", 0, 8, els("hydrogen", "helium", "lithium", "beryllium", "sodium", "magnesium", "potassium", "calcium",
      "rubidium", "strontium", "cesium", "barium", "francium", "radium"),
      "The s-Block", deps=["t6_chambers"], xp=300, optional=True, tokens=2, subtitle="Groups 1 and 2, plus helium", desc=[
        "&eWhat:&r every s-block element: the alkali metals, the alkaline earth metals, hydrogen and helium.",
        "&eChemistry:&r their outermost electrons sit in an s orbital. One or two to give away, which makes them reactive metals (helium's full 1s² shell is the exception).",
        "&eHow:&r the Dissolver gives most of the light metals (helium needs fusion: H + H). Rubidium, cesium, francium and radium are rare: build them in the Fusion Chamber by adding proton numbers (check JEI).",
        "&eTip:&r francium is so unstable that no one has ever seen a visible amount of it."]),
    Q("cp_el_p_light", 2, 8, els("boron", "carbon", "nitrogen", "oxygen", "fluorine", "neon", "aluminum", "silicon", "phosphorus",
      "sulfur", "chlorine", "argon", "gallium", "germanium", "arsenic", "selenium", "bromine", "krypton"),
      "The p-Block: Light", deps=["cp_el_s"], xp=300, optional=True, tokens=2, subtitle="Periods 2 to 4 of groups 13–18", desc=[
        "&eWhat:&r the lighter p-block elements: the non-metals of life and most of what you've refined so far.",
        "&eChemistry:&r these elements fill p orbitals. Across a row they go from metals that lose electrons to halogens that grab them, ending at a noble gas.",
        "&eHow:&r most come from the Dissolver. Neon, argon and krypton need the Fusion Chamber (check JEI).",
        "&eTip:&r carbon, nitrogen, oxygen and phosphorus are most of the mass of a living thing besides hydrogen."]),
    Q("cp_el_p_heavy", 4, 8, els("indium", "tin", "antimony", "tellurium", "iodine", "xenon", "thallium", "lead", "bismuth",
      "polonium", "astatine", "radon", "nihonium", "flerovium", "moscovium", "livermorium", "tennessine", "oganesson"),
      "The p-Block: Heavy", deps=["cp_el_p_light"], xp=500, optional=True, tokens=2, subtitle="Periods 5 to 7, ending at element 118", desc=[
        "&eWhat:&r the heavy p-block, including the superheavy elements made only in particle accelerators.",
        "&eChemistry:&r past lead, every element is radioactive. Bismuth's half-life is a billion times the age of the universe; oganesson's is under a millisecond.",
        "&eHow:&r the Fusion and Fission Chambers. Pick pairs whose proton numbers add up (check JEI).",
        "&eTip:&r astatine is the rarest naturally occurring element: less than a gram exists in Earth's crust at any time."]),
    Q("cp_el_d4", 6, 8, els("scandium", "titanium", "vanadium", "chromium", "manganese", "iron", "cobalt", "nickel", "copper", "zinc"),
      "The d-Block: Period 4", deps=["cp_el_s"], xp=250, optional=True, tokens=1, subtitle="Scandium to zinc", desc=[
        "&eWhat:&r the first row of transition metals, the workhorses of industry.",
        "&eChemistry:&r transition metals fill d orbitals, which gives them colourful compounds, several oxidation states and catalytic tricks (iron in Haber-Bosch, platinum in Ostwald).",
        "&eHow:&r dissolve their ingots and dusts; build scandium and vanadium by fusion if you can't find a source (check JEI).",
        "&eTip:&r stainless steel is iron, chromium and nickel: three boxes in this row."]),
    Q("cp_el_d5", 8, 8, els("yttrium", "zirconium", "niobium", "molybdenum", "technetium", "ruthenium", "rhodium", "palladium",
      "silver", "cadmium"), "The d-Block: Period 5", deps=["cp_el_d4"], xp=300, optional=True, tokens=2, subtitle="Yttrium to cadmium", desc=[
        "&eWhat:&r the second transition row, including three platinum-group metals.",
        "&eChemistry:&r technetium (43) was the first element made artificially, in 1937. It has no stable isotope at all.",
        "&eHow:&r ruthenium and rhodium come from your PGM residue; the rest by dissolving or fusion (check JEI).",
        "&eTip:&r rhodium is one of the most expensive metals on Earth, mostly used in car catalytic converters."]),
    Q("cp_el_d6", 10, 8, els("hafnium", "tantalum", "tungsten", "rhenium", "osmium", "iridium", "platinum", "gold", "mercury"),
      "The d-Block: Period 6", deps=["cp_el_d5"], xp=350, optional=True, tokens=2, subtitle="Hafnium to mercury", desc=[
        "&eWhat:&r the heaviest stable transition metals: refractory tungsten, dense osmium, noble platinum and gold.",
        "&eChemistry:&r osmium is the densest element (22.6 g/cm³). Gold is yellow and mercury is liquid because of relativity: their inner electrons move fast enough to change the orbitals' energies.",
        "&eHow:&r the PGM line gives platinum, iridium and osmium; the rest by dissolving or fusion (check JEI).",
        "&eTip:&r tungsten has the highest melting point of any metal, 3422 °C."]),
    Q("cp_el_d7", 12, 8, els("rutherfordium", "dubnium", "seaborgium", "bohrium", "hassium", "meitnerium", "darmstadtium",
      "roentgenium", "copernicium"), "The d-Block: Period 7", deps=["cp_el_d6", "pt_superheavy"], xp=500, optional=True, tokens=2,
      subtitle="The transactinides", desc=[
        "&eWhat:&r the superheavy transition metals, 104 to 112.",
        "&eChemistry:&r each was made a few atoms at a time by smashing nuclei together. Several are named after scientists: Rutherford, Seaborg, Bohr, Meitner, Röntgen, Copernicus.",
        "&eHow:&r only the Fusion Chamber makes these. Check JEI for pairs that add up.",
        "&eTip:&r seaborgium was named while Glenn Seaborg was alive, a rare honour."]),
    Q("cp_el_lan", 14, 8, els("lanthanum", "cerium", "praseodymium", "neodymium", "promethium", "samarium", "europium", "gadolinium",
      "terbium", "dysprosium", "holmium", "erbium", "thulium", "ytterbium", "lutetium"),
      "The Lanthanides", deps=["cp_el_s", "pt_rare_earth"], xp=400, optional=True, tokens=2, subtitle="All fifteen rare earths of the f-block", desc=[
        "&eWhat:&r the whole lanthanide row, 57 to 71.",
        "&eChemistry:&r they fill the 4f orbitals, which sit deep inside the atom, so their chemistry is almost identical. That's why separating them takes hundreds of extraction steps.",
        "&eHow:&r press U on each element in JEI for Dissolver sources; fuse the rest in the Fusion Chamber. Promethium has no stable isotope.",
        "&eTip:&r four of them are named after one Swedish village, Ytterby: yttrium, ytterbium, terbium, erbium."]),
    Q("cp_el_act", 16, 8, els("actinium", "thorium", "protactinium", "uranium", "neptunium", "plutonium", "americium", "curium",
      "berkelium", "californium", "einsteinium", "fermium", "mendelevium", "nobelium", "lawrencium"),
      "The Actinides", deps=["cp_el_s", "pt_actinides"], xp=500, optional=True, tokens=2, subtitle="All fifteen of the 5f row", desc=[
        "&eWhat:&r the whole actinide row, 89 to 103. Every one is radioactive.",
        "&eChemistry:&r only thorium and uranium last long enough to be found in quantity. Everything past uranium was first made in reactors or in the debris of bomb tests.",
        "&eHow:&r dissolve uranium and thorium materials; fuse the heavier ones (check JEI).",
        "&eTip:&r americium is in most household smoke detectors."]),
    Q("cp_el_all", 18, 8, [tick()], "Every Box Filled", deps=["cp_el_p_heavy", "cp_el_d7", "cp_el_lan", "cp_el_act"],
      xp=1000, optional=True, tokens=2, size=1.5, shape="gear", subtitle="All 118 elements, held in your hands", desc=[
        "&6Every element, in a chest. You remember when this was how you made worlds.&r",
        "&eWhat:&r you've collected every block of the periodic table.",
        "&eHow:&r click to claim. Keep the chest; a periodic table wall of item frames is a fine way to show it off.",
        "&eTip:&r the Combiner can now build almost any compound you can name."]),

    # --- Biome tours (y=10: Overworld, Nether, End) ---------------------------------------------
    Q("cp_bi_cold", 0, 10, biomes(f"{MC}:snowy_plains", f"{MC}:ice_spikes", f"{MC}:snowy_taiga", f"{MC}:grove",
      f"{MC}:snowy_slopes", f"{MC}:frozen_peaks", f"{MC}:frozen_river"),
      "Tour: The Frozen North", deps=["gs_ironpick"], xp=100, optional=True, tokens=1, subtitle="Seven cold Overworld biomes", desc=[
        "&eWhat:&r visit seven snowy biomes.",
        "&eChemistry:&r ice floats because water expands about 9% when it freezes: hydrogen bonds lock the molecules into an open hexagonal lattice.",
        "&eHow:&r walk in. A Nature's Compass finds each one.",
        "&eTip:&r powder snow on frozen peaks swallows players. Leather boots let you walk on it."]),
    Q("cp_bi_hot", 2, 10, biomes(f"{MC}:desert", f"{MC}:badlands", f"{MC}:eroded_badlands", f"{MC}:savanna",
      f"{MC}:jungle", f"{MC}:bamboo_jungle", f"{MC}:mangrove_swamp"),
      "Tour: Heat and Rain", deps=["gs_ironpick"], xp=100, optional=True, tokens=1, subtitle="Seven warm Overworld biomes", desc=[
        "&eWhat:&r visit seven warm biomes, from dry desert to jungle.",
        "&eChemistry:&r badlands terracotta gets its reds and oranges from iron oxides, the same rust you can make in the Combiner.",
        "&eHow:&r walk in. Badlands have gold at every height, so bring a pickaxe.",
        "&eTip:&r jungle temples and desert pyramids hold trim templates for the trim quests."]),
    Q("cp_bi_rare", 4, 10, biomes(f"{MC}:mushroom_fields", f"{MC}:cherry_grove", f"{MC}:lush_caves", f"{MC}:dripstone_caves",
      f"{MC}:deep_dark", f"{MC}:old_growth_pine_taiga"),
      "Tour: Hidden Places", deps=["cp_bi_cold", "cp_bi_hot"], xp=150, optional=True, tokens=2, subtitle="Six rare Overworld biomes", desc=[
        "&eWhat:&r the rare and underground biomes.",
        "&eChemistry:&r dripstone forms when water with dissolved calcium bicarbonate drips and loses CO₂, leaving calcium carbonate behind: Ca(HCO₃)₂ → CaCO₃ + H₂O + CO₂.",
        "&eHow:&r mushroom fields are islands far out at sea. Lush and dripstone caves sit under the surface; the deep dark sits below Y 0 under mountains.",
        "&eTip:&r no hostile mobs spawn on mushroom fields. Safe camping."]),
    Q("cp_bi_exotic", 6, 10, biomes("biomesoplenty:redwood_forest", "biomesoplenty:lavender_field", "biomesoplenty:volcano",
      "biomesoplenty:mystic_grove", "regions_unexplored:bayou", "regions_unexplored:redwoods", "regions_unexplored:prismachasm"),
      "Tour: Strange Lands", deps=["cp_bi_rare"], xp=200, optional=True, tokens=2, subtitle="Seven biomes from the biome mods", desc=[
        "&eWhat:&r seven biomes from Biomes O' Plenty and Regions Unexplored.",
        "&eHow:&r Nature's Compass lists modded biomes too. Prismachasm is a cave biome, so dig.",
        "&eTip:&r volcanoes have lava at the top. Bring fire resistance."]),
    Q("cp_bi_nether", 8, 10, biomes(f"{MC}:nether_wastes", f"{MC}:crimson_forest", f"{MC}:warped_forest", f"{MC}:soul_sand_valley",
      f"{MC}:basalt_deltas"), "Tour: The Five Fires", deps=["t2_nether"], xp=150, optional=True, tokens=1,
      subtitle="Every vanilla Nether biome", desc=[
        "&eWhat:&r visit all five vanilla Nether biomes.",
        "&eChemistry:&r basalt is cooled lava, mostly silicates of iron and magnesium. Nether quartz is SiO₂.",
        "&eHow:&r walk in. Warped forests are the safest place in the Nether: endermen only.",
        "&eTip:&r ghasts hunt soul sand valleys. A shield blocks fireballs."]),
    Q("cp_bi_nether_mod", 10, 10, biomes("biomesoplenty:crystalline_chasm", "biomesoplenty:undergrowth", "biomesoplenty:visceral_heap",
      "biomesoplenty:withered_abyss", "regions_unexplored:infernal_holt", "regions_unexplored:blackstone_basin"),
      "Tour: The Deeper Fires", deps=["cp_bi_nether"], xp=200, optional=True, tokens=2, subtitle="Six modded Nether biomes", desc=[
        "&eWhat:&r Nether biomes from Biomes O' Plenty and Regions Unexplored.",
        "&eHow:&r Nature's Compass works in the Nether too. Withered abyss is a void: don't fall in.",
        "&eTip:&r crystalline chasm's crystals are pretty and brittle. Mine with care."]),
    Q("cp_bi_end", 12, 10, biomes(f"{MC}:the_end", f"{MC}:end_highlands", f"{MC}:end_midlands", f"{MC}:small_end_islands",
      f"{MC}:end_barrens"), "Tour: The Void", deps=["w_dragon"], xp=150, optional=True, tokens=1, subtitle="Every vanilla End biome", desc=[
        "&eWhat:&r visit the five End biomes, from the central island to the outer islands.",
        "&eHow:&r after the dragon, throw an ender pearl into an end gateway to reach the outer islands.",
        "&eTip:&r end cities sit in the highlands. Bring slow falling against shulkers."]),

    # --- Biome tours (y=12: other dimensions) ---------------------------------------------------
    Q("cp_bi_tf_low", 0, 12, biomes("twilightforest:forest", "twilightforest:dense_forest", "twilightforest:firefly_forest",
      "twilightforest:clearing", "twilightforest:mushroom_forest", "twilightforest:enchanted_forest", "twilightforest:spooky_forest",
      "twilightforest:oak_savannah", "twilightforest:lake"),
      "Tour: Twilight Lowlands", deps=["t5_twilight"], xp=150, optional=True, tokens=1, subtitle="Nine open Twilight Forest biomes", desc=[
        "&eWhat:&r the Twilight Forest biomes you can walk into from day one.",
        "&eHow:&r walk in. The Magic Map shows biomes as you explore.",
        "&eTip:&r enchanted forests hold rainbow oak and the odd quest ram."]),
    Q("cp_bi_tf_high", 2, 12, biomes("twilightforest:swamp", "twilightforest:fire_swamp", "twilightforest:dark_forest",
      "twilightforest:dark_forest_center", "twilightforest:snowy_forest", "twilightforest:glacier", "twilightforest:highlands",
      "twilightforest:thornlands", "twilightforest:final_plateau"),
      "Tour: Twilight Frontier", deps=["cp_bi_tf_low", "w_urghast", "w_snow_queen"], xp=300, optional=True, tokens=2,
      subtitle="Nine biomes locked behind bosses", desc=[
        "&eWhat:&r the Twilight biomes that open as you beat its bosses.",
        "&eHow:&r locked biomes hurt or block you until you beat the boss before them. Follow the Twilight boss order in Worlds.",
        "&eTip:&r the final plateau is the last place in the Twilight Forest. Enjoy the view."]),
    Q("cp_bi_under", 4, 12, biomes("undergarden:forgotten_field", "undergarden:smogstem_forest", "undergarden:wigglewood_forest",
      "undergarden:gronglegrowth", "undergarden:frostfields", "undergarden:barren_abyss", "undergarden:ancient_sea",
      "undergarden:indigo_mushroom_bog"),
      "Tour: The Undergarden", deps=["t4_undergarden"], xp=150, optional=True, tokens=1, subtitle="Eight Undergarden biomes", desc=[
        "&eWhat:&r explore the Undergarden's biomes.",
        "&eHow:&r walk in. Bring light: the Undergarden has no sun.",
        "&eTip:&r smog spires and smogstem forests are where you'll find the strangest mobs."]),
    Q("cp_bi_otherside", 6, 12, biomes("deeperdarker:deeplands", "deeperdarker:echoing_forest", "deeperdarker:overcast_columns",
      "deeperdarker:blooming_caverns"), "Tour: The Otherside", deps=["w_otherside"], xp=200, optional=True, tokens=2,
      subtitle="Four biomes beyond the deep dark", desc=[
        "&eWhat:&r the four Otherside biomes from Deeper and Darker.",
        "&eHow:&r walk in. Sculk listens here too: sneak.",
        "&eTip:&r echo trees in the echoing forest give wood you can't get anywhere else."]),
    Q("cp_bi_space", 8, 12, biomes("ad_astra:lunar_wastelands", "ad_astra:martian_wastelands", "ad_astra:martian_canyon_creek",
      "ad_astra:martian_polar_caps", "ad_astra:venus_wastelands", "ad_astra:infernal_venus_barrens", "ad_astra:mercury_deltas",
      "ad_astra:glacio_snowy_barrens", "ad_astra:glacio_ice_peaks"),
      "Tour: The Solar System", deps=["w_glacio", "w_mercury"], xp=500, optional=True, tokens=2, size=1.5,
      subtitle="Nine biomes on five worlds", desc=[
        "&eWhat:&r stand in every planetary biome Ad Astra adds.",
        "&eChemistry:&r Mars is red from iron(III) oxide dust; Venus's clouds are sulfuric acid droplets, the same H₂SO₄ you make in the Contact Process.",
        "&eHow:&r fly to the Moon, Mars, Venus, Mercury and Glacio. Wear the right suit: Venus and Mercury need heat protection.",
        "&eTip:&r martian polar caps are frozen CO₂ and water in real life; in game, bring an oxygen supply."]),

    # --- Secrets ----------------------------------------------------------------------------------
    Q("cp_sec_boron", 6, 2, [item(f"{MC}:music_disc_5"), item("chemlib:boron", 5)], "Element 5, Track 5",
      deps=["cp_discs_creeper"], secret=True, optional=True, tokens=1, loot="secret", subtitle="A very specific pun", desc=[
        "&eWhat:&r disc 5 and five boron. Boron is element 5.",
        "&eChemistry:&r boron is in borosilicate glass, which barely expands when heated. That's why lab glassware survives a flame.",
        "&eTip:&r the demigod finds this funnier than anyone else will."]),
    Q("cp_sec_sniffer", 10, -1.5, [item(f"{MC}:sniffer_egg")], "An Egg from the Past",
      deps=["cp_trims_archaeology"], secret=True, optional=True, tokens=1, loot="secret", subtitle="Something older than you", desc=[
        "&eWhat:&r a sniffer egg, brushed out of warm ocean ruins.",
        "&eHow:&r place it on moss to hatch it faster. Adult sniffers dig up ancient seeds.",
        "&eTip:&r torchflowers and pitcher plants only come from sniffers."]),
    Q("cp_sec_egg", 14, 11.5, [item(f"{MC}:dragon_egg")], "The Only One",
      deps=["cp_bi_end"], secret=True, optional=True, tokens=1, loot="secret", subtitle="There is exactly one per world", desc=[
        "&eWhat:&r the dragon egg. It teleports when you hit it.",
        "&eHow:&r push it off the portal with a piston, or let it fall onto a torch, then pick it up.",
        "&eTip:&r you'll need it for the Seed of a New World. Don't drop it in the void."]),
], links=[("gs_ironpick", -2, 4), ("t6_chambers", -2, 8), ("t2_nether", -2, 10), ("t5_twilight", -2, 12)])
