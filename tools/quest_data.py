"""Quest book content: the Demigod's Codex. Edit this file, then run python3 tools/build_quests.py.

Conventions:
- Each quest teaches one step and says HOW to do it ("How:" line), so a new player is never lost.
- Story beats are gold (&6), key terms yellow (&e). FTB Quests renders & colour codes.
- Main chapters follow the tiers in docs/PROGRESSION.md; side chapters hang off main quests.
"""
from questlib import Q, Chapter, item, dim, tick

MAIN, SIDE = "main", "side"
GROUPS = {MAIN: "The Demigod's Path", SIDE: "Divine Workshop"}
BOOK_TITLE = "Warbucks Chemistry: The Demigod's Codex"

CHAPTERS = [
    # =========================================================================================
    Chapter("welcome", "Welcome", "minecraft:nether_star",
            ["Read this first: who you are, how this world works, and how to use this book."], MAIN, [
        Q("wel_hello", 0, 0, [tick()], "Welcome, Demigod", size=2.0, shape="gear", tokens=3, items=[("comforts:sleeping_bag_white", 1)], desc=[
            "&6Welcome to Warbucks Chemistry.&r",
            "You're a demigod who has lost your power. You'll win it back by mastering chemistry: taking matter apart into its elements and building it back up.",
            "This book is your guide. Follow the lines from quest to quest; each one tells you &ewhat&r to do and &ehow&r to do it.",
            "How: click the checkmark to collect your first reward."]),
        Q("wel_progress", 2, -1, [tick()], "How Progression Works", deps=["wel_hello"], desc=[
            "The pack has 8 tiers. Each one is unlocked by a &echemistry milestone&r, not just more metal:",
            "Fire and bronze → coke and steel → hydrogen and flight → electricity → acids → oil and plastics → silicon, PVC and the atom → antimatter.",
            "Modern Industrialization's voltage tiers (LV, MV, HV, EV) are the spine. Other mods (Mekanism, AE2, Powah and more) unlock alongside them.",
            "If a recipe looks different from what you remember, it's been gated on purpose. JEI always shows the real recipe."]),
        Q("wel_keys", 2, 1, [tick()], "Your Toolkit", deps=["wel_hello"], desc=[
            "&eR&r / &eU&r over an item: recipes / uses (JEI). &eM&r: map and chunk claiming (FTB Chunks).",
            "&e`&r (hold) while mining: vein mine (FTB Ultimine). Look at a block: Jade shows what it is and what it's doing.",
            "Inventory sorting, crafting-grid tweaks and the trash slot are in your inventory screen; check Controls for their keys."]),
        Q("wel_tokens", 4, -1, [tick()], "Demigod Tokens", deps=["wel_progress"], tokens=5, desc=[
            "Most quests give &eDemigod Tokens&r. Spend them on convenience items by crafting: torches, food, XP, iron, coke, rubber, osmium, backpack upgrades and a Warp Stone.",
            "How: search &eDemigod Token&r in JEI and press U to see the whole shop.",
            "Bigger milestones pay more tokens, and later tiers pay more than early ones."]),
        Q("wel_team", 4, 1, [tick()], "Playing Together", deps=["wel_keys"], desc=[
            "On a server, make a team so you share quest progress and claimed land.",
            "How: &e/ftbteams party create <name>&r, then invite friends with &e/ftbteams party invite <player>&r."]),
        Q("wel_ready", 6, 0, [tick()], "Begin", deps=["wel_tokens", "wel_team"], size=1.5, shape="hexagon", desc=[
            "That's everything. Open &eGetting Started&r and take your first step."]),
    ]),

    # =========================================================================================
    Chapter("start", "Getting Started", "minecraft:oak_sapling",
            ["You wake in a world you didn't make, with a god's patience and none of a god's power.",
             "These first steps get you fed, armed, rested and ready for chemistry."], MAIN, [
        Q("gs_wake", 0, 0, [tick()], "The Awakening", size=2.0, shape="gear", xp=10, deps=["wel_ready"], desc=[
            "&6You remember being more than this.&r The memory is fading, but one idea stays clear:",
            "&eeverything is made of elements, and elements can be taken apart and put back together.&r",
            "",
            "This book walks you from your first log to antimatter. Follow the lines: each quest unlocks the next.",
            "How: click the checkmark on the right to begin."]),
        Q("gs_jei", 2, -2, [tick()], "Tip: Recipes (JEI)", deps=["gs_wake"], xp=10, desc=[
            "Press &eR&r over any item to see how it's made, or &eU&r to see what it's used in.",
            "Every recipe in this pack, including the ones changed for progression, shows in JEI.",
            "How: try it on a quest icon, then click the checkmark."]),
        Q("gs_table", 2, 0, [item("minecraft:crafting_table")], "Wood and a Workbench", deps=["gs_wake"], xp=10,
          items=[("minecraft:torch", 8)], desc=[
            "Punch a tree for logs, turn them into planks, and craft a crafting table.",
            "How: any wood works. Planks in a 2x2 grid make the table."]),
        Q("gs_stone", 4, 0, [item("minecraft:stone_pickaxe")], "Stone Age", deps=["gs_table"], xp=15, desc=[
            "Make a wooden pickaxe, mine some cobblestone, then craft a stone pickaxe.",
            "How: tip: FTB Ultimine lets you mine a whole vein at once. Hold the &e`&r key (grave/tilde) while breaking blocks."]),
        Q("gs_food", 4, -2, [item("minecraft:bread", 4)], "Something to Eat", deps=["gs_table"], xp=15,
          items=[("minecraft:bread", 8)], desc=[
            "Gods don't need to eat. You do, for now.",
            "How: break grass for seeds, farm wheat, and craft bread (3 wheat). AppleSkin shows the hunger each food restores."]),
        Q("gs_sleep", 6, -2, [item("comforts:sleeping_bag_white")], "Rest Anywhere", deps=["gs_food"], xp=20, desc=[
            "A &esleeping bag&r skips the night without moving your spawn point, so it's great while exploring.",
            "How: craft it from wool (any colour works for the recipe; this quest wants a white one). Hammocks skip the day."]),
        Q("gs_furnace", 6, 0, [item("minecraft:furnace"), item("minecraft:charcoal", 4)], "Fire", deps=["gs_stone"], xp=20, desc=[
            "Fire is your first chemistry tool. Cooking logs in a furnace makes &echarcoal&r (more on why in Chapter I).",
            "How: 8 cobblestone make a furnace. Smelt a log with a log or planks as fuel."]),
        Q("gs_iron", 8, 0, [item("minecraft:iron_ingot", 16)], "Iron", deps=["gs_furnace"], xp=25, desc=[
            "Mine iron ore (it's common around Y 16 and in mountains) and smelt it.",
            "How: Iron Furnaces (see the Storage and Logistics chapter) smelt faster once you have spare iron."]),
        Q("gs_ironpick", 10, -1, [item("minecraft:iron_pickaxe")], deps=["gs_iron"], xp=25, desc=[
            "Needed for diamonds, redstone and gold, and to start the journey to the Nether."]),
        Q("gs_bucket", 10, 1, [item("minecraft:water_bucket")], "Water", deps=["gs_iron"], xp=15, desc=[
            "Water is the most important chemical in this pack: steam, electrolysis and acids all start with it.",
            "How: 3 iron ingots make a bucket. Fill it at any water source."]),
        Q("gs_backpack", 8, 2, [item("sophisticatedbackpacks:backpack")], "A Backpack", deps=["gs_iron"], xp=20, desc=[
            "More inventory, and it can be upgraded later (pickup, magnet, feeding and more).",
            "How: craft it from leather, string and a chest. Wear it in the chest slot or keep it in your inventory."]),
        Q("gs_claim", 12, 0, [tick()], "Claim Your Land", deps=["gs_ironpick"], xp=20, desc=[
            "FTB Chunks protects your base and can keep it loaded while you're away.",
            "How: press &eM&r to open the map, then drag over chunks to claim them. Right-click a claimed chunk to force-load it (needed for the flight pylon later).",
            "Click the checkmark when done."]),
        Q("gs_paxel", 12, 2, [item("mekanismtools:iron_paxel")], "The Paxel", deps=["gs_iron"], xp=25, desc=[
            "A &epaxel&r is a pickaxe, axe and shovel in one tool. Mekanism Tools adds them for every material, from wood to refined obsidian.",
            "How: craft an iron pickaxe, axe and shovel together with sticks (check JEI)."]),
        Q("gs_silent", 14, 2, [item("silentgear:blueprint_paper"), item("silentgear:pickaxe")], "Tools from Parts", deps=["gs_paxel"], xp=40, desc=[
            "Silent Gear builds tools from parts. Each part's stats come from its &ematerial&r, so better chemistry means better tools.",
            "How: make Blueprint Paper, craft a Pickaxe Blueprint, then craft a pickaxe head and rod. The Tools and Comfort chapter goes deeper."]),
        Q("gs_ready", 14, 0, [tick()], "Ready for Chemistry", size=1.5, shape="hexagon", deps=["gs_claim", "gs_bucket"], xp=50, items=[("minecraft:copper_ingot", 16), ("modern_industrialization:tin_ingot", 8)], desc=[
            "&6Fed, armed, sheltered.&r Now the real work begins: fire, ore, alloys, and the slow road back to divinity.",
            "How: click to open Chapter I."]),
    ]),

    # =========================================================================================
    Chapter("t0", "I. Fire and Bronze", "modern_industrialization:bronze_ingot",
            ["Heat drives chemistry: reduce ore with carbon, mix metals into alloys, and let steam do the work."], MAIN, [
        Q("t0_charcoal", 0, 0, [item("minecraft:charcoal", 16)], "Pyrolysis", deps=["gs_ready"], xp=25, desc=[
            "Heat wood without enough oxygen to burn and the volatile compounds escape as smoke and tar.",
            "What's left is &echarcoal&r: almost pure carbon. This is &epyrolysis&r.",
            "How: smelt logs in a furnace."]),
        Q("t0_copper", 0, 2, [item("minecraft:copper_ingot", 16)], "Copper", deps=["gs_ready"], xp=20, desc=[
            "Smelting is &ereduction&r: carbon pulls oxygen away from the metal oxide and leaves metal behind.",
            "How: copper ore is common near the surface, especially in dripstone caves."]),
        Q("t0_tin", 2, 2, [item("modern_industrialization:raw_tin", 8), item("modern_industrialization:tin_ingot", 8)], "Tin", deps=["t0_copper"], xp=25, desc=[
            "Tin ore here comes from Modern Industrialization (MI). It's grey with pale specks and fairly common underground.",
            "How: mine it and smelt the raw tin."]),
        Q("t0_hammer", 2, 0, [item("modern_industrialization:forge_hammer")], "The Forge Hammer", deps=["t0_charcoal", "t0_copper"], xp=25, desc=[
            "MI's first workstation. It crushes ore into dust and hammers ingots into plates.",
            "Ores give at most &e2x&r here. Bigger yields come later from &eacids&r, not bigger hammers.",
            "How: craft it (check JEI), place it, and right-click to use."]),
        Q("t0_bronze", 4, 1, [item("modern_industrialization:bronze_ingot", 16)], "The First Alloy", deps=["t0_hammer", "t0_tin"], xp=50, size=1.5, desc=[
            "About 3 parts copper to 1 part tin gives &ebronze&r, which is harder than either metal alone.",
            "Humanity's first engineered material, and the frame of your steam age.",
            "How: crush copper and tin into dust with the Forge Hammer, mix the dusts by crafting, and smelt the bronze dust."]),
        Q("t0_casing", 6, 0, [item("modern_industrialization:bronze_machine_casing")], "Bronze Machine Casing", deps=["t0_bronze"], xp=40, desc=[
            "The block every steam machine is built around. You'll also need one for the Dissolver in Chapter II.",
            "How: bronze plates around a furnace-like core (check JEI)."]),
        Q("t0_boiler", 8, 0, [item("modern_industrialization:bronze_boiler")], "Steam Power", deps=["t0_casing"], xp=75, size=1.5, items=[("minecraft:charcoal", 32), ("modern_industrialization:bronze_furnace", 1)], desc=[
            "Burn fuel, boil water, and the expanding steam does work. Welcome to the industrial revolution.",
            "How: place the boiler, give it water and fuel (coal or charcoal), and place steam machines next to it. Steam flows into adjacent machines or through MI fluid pipes."]),
        Q("t0_pump", 8, 2, [item("modern_industrialization:bronze_water_pump")], "Endless Water", deps=["t0_boiler"], xp=40, desc=[
            "A steam-powered pump that pulls water from the ground, so your boiler never runs dry.",
            "How: place it next to the boiler, or pipe its water into it."]),
        Q("t0_furnace", 10, -2, [item("modern_industrialization:bronze_furnace")], "Steam Furnace", deps=["t0_boiler"], xp=30, desc=[
            "Smelts with steam instead of fuel. Your first automated machine."]),
        Q("t0_macerator", 10, -1, [item("modern_industrialization:bronze_macerator")], "Steam Macerator", deps=["t0_boiler"], xp=30, desc=[
            "Grinds ore and items into dust: 1 ore makes 2 raw ore here (capped at 2x until acids)."]),
        Q("t0_compressor", 10, 0, [item("modern_industrialization:bronze_compressor")], "Steam Compressor", deps=["t0_boiler"], xp=30, desc=[
            "Presses ingots into plates. Machines need lots of plates."]),
        Q("t0_mixer", 10, 1, [item("modern_industrialization:bronze_mixer")], "Steam Mixer", deps=["t0_boiler"], xp=30, desc=[
            "Mixes dusts (like copper + tin into bronze) and fluids."]),
        Q("t0_cutter", 10, 2, [item("modern_industrialization:bronze_cutting_machine")], "Steam Cutting Machine", deps=["t0_boiler"], xp=30, desc=[
            "Cuts ingots into rods and planks into more planks. It uses water as coolant."]),
        Q("t0_pipes", 12, 0, [item("modern_industrialization:item_pipe", 8), item("modern_industrialization:fluid_pipe", 8)], "Pipes", deps=["t0_furnace", "t0_macerator", "t0_compressor", "t0_mixer", "t0_cutter"], xp=50, desc=[
            "Connect your machines. MI pipes carry items or fluids, including steam.",
            "How: right-click a pipe end with an empty hand to set it to insert or extract."]),
    ]),

    # =========================================================================================
    Chapter("t1", "II. Steam and Steel", "modern_industrialization:coke",
            ["Destructive distillation turns coal into coke, and coke turns iron into steel.",
             "At the end of this chapter, matter itself opens up to you."], MAIN, [
        Q("t1_coke_oven", 0, 0, [item("modern_industrialization:coke_oven")], "The Coke Oven", deps=["t0_pipes"], xp=50, desc=[
            "Coal is carbon mixed with many other compounds. Bake it without air and those volatiles are driven off.",
            "This is &edestructive distillation&r.",
            "How: the Coke Oven is a small multiblock. Look at it in JEI or use MI's guidebook to see the shape, then power it with steam."]),
        Q("t1_coke", 2, -1, [item("modern_industrialization:coke", 16)], "Coke", deps=["t1_coke_oven"], xp=40, desc=[
            "Nearly pure carbon that burns hotter than coal. It's exactly what a blast furnace needs."]),
        Q("t1_creosote", 2, 1, [item("modern_industrialization:creosote_bucket")], "Byproduct: Creosote", deps=["t1_coke_oven"], xp=40, desc=[
            "The tar driven out of coal is &ecreosote&r. Nothing is wasted in chemistry: creosote is a fuel for your boilers.",
            "How: pipe it out of the Coke Oven into a tank, or straight into a boiler."]),
        Q("t1_blast", 4, 0, [item("modern_industrialization:steam_blast_furnace")], "The Steam Blast Furnace", deps=["t1_coke"], xp=75, desc=[
            "A multiblock that gets hot enough to melt iron and dissolve carbon into it.",
            "How: check the structure in JEI, then feed it steam."]),
        Q("t1_steel", 6, 0, [item("modern_industrialization:steel_ingot", 16)], "Steel", deps=["t1_blast"], xp=100, size=1.5, items=[("modern_industrialization:steel_ingot", 16)], desc=[
            "Iron with a small, controlled amount of carbon (about 0.2-2%) is &esteel&r: strong, tough, and the backbone of every machine to come.",
            "Too much carbon and you get brittle cast iron. Chemistry is about the right ratio.",
            "How: mix iron dust with coke dust, then melt it in the blast furnace (check JEI for the exact recipe)."]),
        Q("t1_steel_paxel", 6, 2, [item("mekanismtools:steel_paxel")], "Steel Paxel", deps=["t1_steel"], xp=40, desc=[
            "A sturdier paxel."]),
        Q("t1_steel_boiler", 8, -2, [item("modern_industrialization:steel_boiler")], "Steel Boiler", deps=["t1_steel"], xp=60, desc=[
            "More steam per tick. Steel versions of the steam machines (macerator, compressor and others) run faster too."]),
        Q("t1_power", 8, 2, [item("generatorgalore:iron_generator")], "Forge Energy", deps=["t1_steel"], xp=50, desc=[
            "Some machines run on &eFE&r (Forge Energy) instead of steam. You'll need it for the Dissolver.",
            "How: Generator Galore's Iron Generator burns fuel into FE. A Mekanism Heat Generator or Powah Furnator also works."]),
        Q("t1_dissolver", 10, -1, [item("alchemistry:dissolver")], "The Dissolver", deps=["t1_steel", "t1_power"], xp=150, size=1.75, shape="hexagon", items=[("minecraft:experience_bottle", 16)], desc=[
            "&6Your first divine gift returns.&r",
            "The Dissolver breaks any item into the &eelements and compounds&r it's made of.",
            "How: it needs steel plates and a Bronze Machine Casing. Power it with FE, insert anything, and collect the elements."]),
        Q("t1_combiner", 10, 1, [item("alchemistry:combiner")], "The Combiner", deps=["t1_steel", "t1_power"], xp=150, size=1.75, shape="hexagon", desc=[
            "The reverse: arrange elements and the Combiner builds them back into items and blocks.",
            "Taking the world apart and rebuilding it to your design is what this pack is about."]),
        Q("t1_elements", 12, 0, [item("chemlib:hydrogen", 16), item("chemlib:carbon", 16), item("chemlib:oxygen", 16), item("chemlib:iron", 16)],
          "First Entries in the Periodic Table", deps=["t1_dissolver", "t1_combiner"], xp=200, desc=[
            "Dissolve whatever you have lying around and collect your first elements:",
            "&eH&r (1), &eC&r (6), &eO&r (8), &eFe&r (26).",
            "How: wood and plants give carbon, hydrogen and oxygen. Iron ingots give iron."]),
        Q("t1_compound", 14, 0, [item("chemlib:water", 4)], "Your First Synthesis", deps=["t1_elements"], xp=200, desc=[
            "Two hydrogen, one oxygen: H₂O. Build water from its elements in the Combiner.",
            "It's a trivial compound, but you made it from scratch. That's the point.",
            "How: the Combiner shows the recipe once you pick the target item in its GUI."]),
    ]),

    # =========================================================================================
    Chapter("t2", "III. Divine Ascent", "pylons:infusion_pylon",
            ["Walk through fire, brew in the dark, and take back the sky.",
             "Flight needs the Nether and your first Alchemistry machine: fire and chemistry together."], MAIN, [
        Q("t2_obsidian", 0, 0, [item("minecraft:obsidian", 10), item("minecraft:flint_and_steel")], "A Door of Fire", deps=["gs_ironpick"], xp=30, desc=[
            "A Nether portal is a 4x5 frame of obsidian, lit with flint and steel.",
            "How: you need a diamond pickaxe to mine obsidian, or pour water over a lava source to make it in place."]),
        Q("t2_nether", 2, 0, [dim("minecraft:the_nether")], "Into the Fire", deps=["t2_obsidian"], xp=100, desc=[
            "The Nether is a chemistry lab: sulfur, quartz (SiO₂) and blaze powder all come from here.",
            "How: bring food, armour and blocks. NetherPortalFix keeps portals linked properly."]),
        Q("t2_blaze", 4, -1, [item("minecraft:blaze_rod", 4)], deps=["t2_nether"], xp=50, desc=[
            "Blaze powder fuels brewing, alchemy's oldest form of applied chemistry.",
            "How: blazes spawn in Nether Fortresses. Explorer's Compass can point you to one."]),
        Q("t2_wart", 4, 1, [item("minecraft:nether_wart", 8)], deps=["t2_nether"], xp=25, desc=[
            "The base reagent for almost every potion. It grows on soul sand in fortresses; replant it at home."]),
        Q("t2_quartz", 8, -2, [item("minecraft:quartz", 16)], "Nether Quartz", deps=["t2_nether"], xp=25, desc=[
            "Silicon dioxide, SiO₂. You'll need it for the Infusion Pylon, and much later for silicon."]),
        Q("t2_brewing", 6, 0, [item("minecraft:brewing_stand")], "The Brewer's Art", deps=["t2_blaze", "t2_wart"], xp=75, desc=[
            "Look up &ePotion of Flying&r in JEI (it comes from Apothic Attributes). That's your road back to the sky.",
            "How: awkward potion first (water bottle + nether wart), then follow the JEI recipe."]),
        Q("t2_filter", 8, 0, [item("pylons:potion_filter")], "Potion Filter", deps=["t2_brewing"], xp=75, desc=[
            "Drink a potion, then right-click a Potion Filter to store the effect.",
            "A filter needs &e1 hour&r of an effect to activate (about 7.5 extended potions). Combine filters with the same effect by holding one in each hand and right-clicking."]),
        Q("t2_hydrogen", 8, 2, [item("chemlib:hydrogen", 8)], "Lighter than Air", deps=["t1_dissolver"], xp=75, desc=[
            "Hydrogen is the lightest element. Balloons filled with it carried the first people into the sky in 1783.",
            "Your flight pylon needs it, and only the &eDissolver&r can pull it out of matter as an item.",
            "How: dissolve water, plants or wood and collect the hydrogen."]),
        Q("t2_pylon", 10, 0, [item("pylons:infusion_pylon")], "Wings of a God", deps=["t2_filter", "t2_quartz", "t2_hydrogen"], xp=500, size=2.0, shape="hexagon", items=[("minecraft:experience_bottle", 32)], desc=[
            "&6The sky is yours again.&r",
            "The &eInfusion Pylon&r needs Nether quartz and blackstone, plus &ehydrogen&r from your Dissolver. Fire and chemistry together.",
            "Put an activated Potion of Flying filter in it and you get creative-style flight anywhere.",
            "How: the pylon's chunk must stay loaded, so force-load it with FTB Chunks (press M, right-click the chunk)."]),
        Q("t2_ars", 2, 2, [item("ars_nouveau:worn_notebook"), item("ars_nouveau:source_gem", 4)], "Whispers of Magic", deps=["t2_nether"], xp=50, desc=[
            "Light magic suits a demigod. The Worn Notebook teaches Ars Nouveau spellcrafting.",
            "Its Ritual of Flight is another way to fly near your base. See the Divine Gifts chapter."]),
    ]),

    # =========================================================================================
    Chapter("t3", "IV. The Electric Age", "modern_industrialization:basic_machine_hull",
            ["Electricity is the tool that splits compounds apart. First you have to make it, and build the circuits that use it."], MAIN, [
        Q("t3_rubber", 0, -1, [item("modern_industrialization:rubber_sheet", 8)], "Rubber", deps=["t1_steel"], xp=40, desc=[
            "Insulation for cables. Without it, current goes everywhere.",
            "How: check JEI for MI's rubber recipes (from plant matter or, later, synthetic rubber)."]),
        Q("t3_wire", 0, 1, [item("modern_industrialization:copper_wire", 8), item("modern_industrialization:tin_cable", 8)], "Wires and Cables", deps=["t1_steel"], xp=40, desc=[
            "Copper conducts. Rubber-coated wire becomes cable.",
            "How: the Steel Wiremill pulls plates into wire. Cables combine wire with rubber."]),
        Q("t3_components", 2, 0, [item("modern_industrialization:resistor", 2), item("modern_industrialization:capacitor", 2), item("modern_industrialization:inductor", 2)], "Electronic Components", deps=["t3_rubber", "t3_wire"], xp=60, desc=[
            "Resistors limit current, capacitors store charge, inductors resist changes in current. Every circuit needs them.",
            "How: check JEI for each. They're small crafts from wire, plates and rubber."]),
        Q("t3_battery", 2, 2, [item("modern_industrialization:redstone_battery", 2)], "Redstone Battery", deps=["t3_wire"], xp=40, desc=[
            "A simple battery. The LV hull needs two."]),
        Q("t3_analog", 4, 0, [item("modern_industrialization:analog_circuit", 2)], "Analog Circuit", deps=["t3_components"], xp=75, desc=[
            "Your first circuit. Mekanism's Basic Control Circuit also needs one, so MI and Mekanism advance together."]),
        Q("t3_hull", 6, 1, [item("modern_industrialization:basic_machine_hull")], "LV Machine Hull", deps=["t3_analog", "t3_battery"], xp=150, size=1.5, items=[("modern_industrialization:analog_circuit", 4), ("modern_industrialization:electric_macerator", 1)], desc=[
            "&eLV&r (Low Voltage) is the first electric tier. Every LV machine is built on this hull.",
            "How: steel machine casing + analog circuit + 2 redstone batteries + tin cable."]),
        Q("t3_turbine", 8, -1, [item("modern_industrialization:lv_steam_turbine")], "Steam to Electricity", deps=["t3_hull"], xp=100, desc=[
            "A turbine turns your boiler's steam into &eEU&r, MI's electricity. Your steam setup becomes a power plant.",
            "How: pipe steam in, and connect tin cable from the turbine to your machines."]),
        Q("t3_efurnace", 10, -3, [item("modern_industrialization:electric_furnace")], deps=["t3_turbine"], xp=40, desc=["Faster, fuel-free smelting."]),
        Q("t3_emacerator", 10, -2, [item("modern_industrialization:electric_macerator")], deps=["t3_turbine"], xp=40, desc=["Still capped at 2x per ore until acids."]),
        Q("t3_assembler", 10, -1, [item("modern_industrialization:assembler")], "Assembler", deps=["t3_turbine"], xp=60, desc=[
            "Makes circuits and machine parts automatically. This is where MI automation really starts."]),
        Q("t3_ecompressor", 10, 0, [item("modern_industrialization:electric_compressor")], deps=["t3_turbine"], xp=40, desc=["Plates, faster."]),
        Q("t3_ewiremill", 10, 1, [item("modern_industrialization:electric_wiremill")], deps=["t3_turbine"], xp=40, desc=["Wire, faster."]),
        Q("t3_polarizer", 10, 2, [item("modern_industrialization:polarizer")], "Polarizer", deps=["t3_turbine"], xp=40, desc=["Magnetises steel rods, which motors need."]),
        Q("t3_infuser", 8, 3, [item("mekanism:metallurgic_infuser")], "Mekanism: Metallurgic Infuser", deps=["t3_hull"], xp=60, desc=[
            "Mekanism's entry machine. It infuses metals with carbon, redstone and more.",
            "How: you'll need osmium (a blue-grey ore found deep underground; it's unique to Mekanism)."]),
        Q("t3_mekcircuit", 10, 4, [item("mekanism:basic_control_circuit", 2), item("mekanism:steel_casing")], "Mekanism Circuits", deps=["t3_infuser", "t3_analog"], xp=75, desc=[
            "In this pack, a Basic Control Circuit is &eMI Analog Circuit + osmium&r. Each Mekanism circuit tier needs the matching MI circuit.",
            "The Steel Casing is the frame for most Mekanism machines."]),
        Q("t3_enrich", 12, 4, [item("mekanism:enrichment_chamber")], "Enrichment Chamber", deps=["t3_mekcircuit"], xp=60, desc=[
            "Mekanism's 2x ore processing. 3x, 4x and 5x need gases and acids: that's the next chapter."]),
    ]),

    # =========================================================================================
    Chapter("t4", "V. Electrochemistry and Acids", "modern_industrialization:sulfuric_acid_bucket",
            ["Electricity splits compounds into elements. Acids dissolve what fire can't.",
             "Ore processing becomes chemistry."], MAIN, [
        Q("t4_electrolyzer", 0, 0, [item("modern_industrialization:electrolyzer")], "Electrolysis", deps=["t3_assembler"], xp=150, desc=[
            "Pass current through a compound and it splits: water into &eH₂ + O₂&r, salt water into &eCl₂&r and sodium.",
            "This is &eelectrochemistry&r, and its gases drive everything in this chapter."]),
        Q("t4_salt", 2, -2, [item("modern_industrialization:salt_dust", 16)], "Salt", deps=["t4_electrolyzer"], xp=40, desc=[
            "Sodium chloride, NaCl. MI salt ore is found underground; macerate it into dust.",
            "Electrolysed, it gives &esodium&r and &echlorine&r, the start of the chlor-alkali industry."]),
        Q("t4_separator", 0, 2, [item("mekanism:electrolytic_separator")], "Mekanism Gases", deps=["t3_mekcircuit"], xp=100, desc=[
            "Mekanism's Electrolytic Separator makes hydrogen and oxygen as gases you can pipe and store.",
            "How: feed it water and FE. Use Mekanism pressurized tubes and chemical tanks for the gases."]),
        Q("t4_reactor", 2, 0, [item("modern_industrialization:chemical_reactor")], "The Chemical Reactor", deps=["t4_electrolyzer"], xp=100, desc=[
            "MI's general-purpose reaction vessel. It combines items and fluids into new compounds. You'll use it constantly."]),
        Q("t4_oxidizer", 2, 2, [item("mekanism:chemical_oxidizer"), item("mekanism:chemical_infuser")], "The Contact Process, Part 1", deps=["t4_separator"], xp=150, desc=[
            "Burn sulfur into &eSO₂&r in the Chemical Oxidizer, then combine it with oxygen into &eSO₃&r in the Chemical Infuser.",
            "How: sulfur comes from the Nether, or from macerating lignite coal."]),
        Q("t4_acid", 4, 1, [item("modern_industrialization:sulfuric_acid_bucket")], "Sulfuric Acid", deps=["t4_oxidizer", "t4_reactor"], xp=250, size=1.75, shape="hexagon", items=[("modern_industrialization:sulfuric_acid_bucket", 2)], desc=[
            "SO₃ + H₂O → &eH₂SO₄&r. Sulfuric acid is the most-produced chemical on Earth for a reason.",
            "How: make it in Mekanism or MI and fill one bucket."]),
        Q("t4_ore3", 6, -1, [item("mekanism:purification_chamber")], "3x Ore: Oxygen", deps=["t4_acid"], xp=150, desc=[
            "Before acids, every route caps out at &e2x&r per ore. Purifying ore with oxygen gives &e3x&r."]),
        Q("t4_ore4", 8, -1, [item("mekanism:chemical_injection_chamber")], "4x Ore: Hydrogen Chloride", deps=["t4_ore3"], xp=200, desc=[
            "H₂ + Cl₂ → &eHCl&r. Injecting hydrogen chloride splits ore into shards: &e4x&r.",
            "How: combine hydrogen and chlorine in the Chemical Infuser."]),
        Q("t4_ore5", 10, -1, [item("mekanism:chemical_dissolution_chamber"), item("mekanism:chemical_washer"), item("mekanism:chemical_crystallizer")], "5x Ore: Dissolution", deps=["t4_ore4"], xp=300, size=1.5, desc=[
            "Dissolve ore in sulfuric acid into a slurry, wash it, and crystallise it: &e5x&r.",
            "This is &ehydrometallurgy&r, the way most of the world's copper is really refined."]),
        Q("t4_mv", 6, 2, [item("modern_industrialization:electronic_circuit"), item("modern_industrialization:advanced_machine_hull")], "MV: Aluminum", deps=["t4_electrolyzer"], xp=250, size=1.5, items=[("modern_industrialization:electronic_circuit", 4)], desc=[
            "Aluminum is the most common metal in the crust, but it's locked tightly to oxygen in bauxite. It only became cheap once electrolysis could free it.",
            "How: process bauxite (MI ore) into aluminum (check JEI), then build electronic circuits and the &eMV hull&r."]),
        Q("t4_uraninite", 8, 2, [item("powah:energizing_orb"), item("powah:uraninite", 4)], "Uranium Dioxide", deps=["t4_mv", "t4_reactor"], xp=150, desc=[
            "Uraninite is UO₂. Make it by oxidising uranium dust with oxygen in MI's &eChemical Reactor&r.",
            "Powah's reactors run on it, and Powah's Energizing Orb needs an MV circuit."]),
        Q("t4_byproduct", 12, -1, [item("modern_industrialization:centrifuge"), item("modern_industrialization:silver_dust", 4)], "Ore Byproducts", deps=["t4_ore5"], xp=200, desc=[
            "Real ores are never pure. Send Mekanism's &edirty dust&r through MI's &eCentrifuge&r instead of the Enrichment Chamber and you get the same dust plus a chance at a bonus metal:",
            "iron → nickel, copper → gold, gold → silver, &elead → silver&r (galena is the world's main silver ore), tin → tungsten, osmium → iridium, uranium → lead (decay).",
            "How: route dirty dust to a Centrifuge. Rare metals start arriving as a bonus."]),
        Q("t4_undergarden", 4, 4, [item("undergarden:catalyst"), dim("undergarden:undergarden")], "The Undergarden", deps=["t4_acid"], xp=300, desc=[
            "A realm beneath the world. Its portal catalyst needs a bucket of sulfuric acid.",
            "How: build a stone-brick portal frame and right-click it with the catalyst."]),
    ]),

    # =========================================================================================
    Chapter("t5", "VI. Petrochemistry", "modern_industrialization:polyethylene_bucket",
            ["Crude oil is a mixture. Separate it by boiling point, then build polymers from the pieces."], MAIN, [
        Q("t5_oil", 0, 0, [item("modern_industrialization:oil_drilling_rig"), item("modern_industrialization:crude_oil_bucket")], "Black Gold", deps=["t4_mv"], xp=200, desc=[
            "Drill for crude oil: millions of years of compressed life, a soup of hydrocarbons.",
            "How: the Oil Drilling Rig goes on an MI Quarry (check JEI)."]),
        Q("t5_distill", 2, 0, [item("modern_industrialization:distillation_tower")], "Fractional Distillation", deps=["t5_oil"], xp=300, size=1.5, desc=[
            "Heat the crude and each fraction boils off at its own temperature: gases at the top, then naphtha, diesel and heavy oils lower down.",
            "This tower is &ethe refinery&r of the pack. Every other mod gets its fuel and plastic from here."]),
        Q("t5_diesel", 4, -2, [item("modern_industrialization:diesel_bucket"), item("modern_industrialization:lv_diesel_generator")], "Diesel Power", deps=["t5_distill"], xp=150, desc=[
            "Diesel burns in MI generators, and later fuels your rockets (Ad Astra runs on MI diesel)."]),
        Q("t5_ethylene", 4, 0, [item("modern_industrialization:ethylene_bucket")], "Cracking", deps=["t5_distill"], xp=150, desc=[
            "Breaking big hydrocarbon molecules into small ones gives &eethylene&r (C₂H₄), the most important building block in plastics."]),
        Q("t5_pe", 6, 0, [item("modern_industrialization:polyethylene_bucket")], "Polymerisation", deps=["t5_ethylene"], xp=250, desc=[
            "Chain thousands of ethylene molecules together and you get &epolyethylene&r.",
            "MI's ethylene also feeds Mekanism's HDPE plastic."]),
        Q("t5_hdpe", 6, 2, [item("mekanism:hdpe_pellet", 8)], "HDPE", deps=["t5_pe"], xp=150, desc=[
            "High-density polyethylene pellets, made in Mekanism's Pressurized Reaction Chamber."]),
        Q("t5_ebf", 6, -2, [item("modern_industrialization:electric_blast_furnace"), item("modern_industrialization:stainless_steel_ingot", 8)], "Stainless Steel", deps=["t5_distill"], xp=200, desc=[
            "Steel alloyed with chromium and nickel resists corrosion, so it can handle acids and hot fluids.",
            "How: the Electric Blast Furnace makes it. HV parts need it."]),
        Q("t5_hv", 8, 0, [item("modern_industrialization:digital_circuit"), item("modern_industrialization:turbo_machine_hull")], "HV: Digital Circuits", deps=["t5_pe", "t5_ebf"], xp=300, size=1.5, items=[("modern_industrialization:digital_circuit", 2)], desc=[
            "Digital circuit boards are laminated with polyethylene. The &eHV hull&r follows, with a &esodium&r battery made from your salt chemistry."]),
        Q("t5_ae2", 10, 0, [item("ae2:inscriber"), item("ae2:controller")], "The God's Archive", deps=["t5_hv"], xp=400, size=1.75, shape="hexagon", items=[("ae2:drive", 1)], desc=[
            "&6Your memory, rebuilt as a network.&r",
            "Applied Energistics 2 is gated by petrochemistry: the Inscriber needs a Turbo hull and the ME Controller a digital circuit.",
            "How: Tom's Simple Storage was your early network. AE2 takes over from here (see Storage and Logistics)."]),
        Q("t5_twilight", 10, -2, [dim("twilightforest:twilight_forest")], "The Twilight Forest", deps=["t5_hv"], xp=300, desc=[
            "A realm of permanent dusk.",
            "How: dig a 2x2 pool of water ringed with flowers, stand in it, and throw in a diamond."]),
    ]),

    # =========================================================================================
    Chapter("t6", "VII. Materials and Nuclear", "mekanism:pellet_polonium",
            ["Purity and precision: semiconductors, PVC, isotopes.",
             "Then transmutation: any element from any other."], MAIN, [
        Q("t6_silicon", 0, -2, [item("modern_industrialization:monocrystalline_silicon"), item("modern_industrialization:silicon_wafer", 4)], "Semiconductor Silicon", deps=["t5_hv"], xp=250, desc=[
            "Computer chips need silicon purer than 99.9999999%. A single crystal is grown from molten silicon and sliced into wafers."]),
        Q("t6_pvc", 0, 0, [item("modern_industrialization:polyvinyl_chloride_bucket")], "PVC", deps=["t5_hv", "t4_salt"], xp=250, desc=[
            "Ethylene plus chlorine makes vinyl chloride, which polymerises into &ePVC&r. Petrochemistry meets chlor-alkali chemistry."]),
        Q("t6_pu", 2, -1, [item("modern_industrialization:processing_unit"), item("modern_industrialization:highly_advanced_machine_hull")], "EV: Processing Units", deps=["t6_pvc", "t6_silicon"], xp=400, size=1.5, items=[("modern_industrialization:processing_unit", 2)], desc=[
            "Processing units are insulated with PVC and built on silicon. The &eEV hull&r follows."]),
        Q("t6_centrifuge", 4, -2, [item("mekanism:isotopic_centrifuge")], "Isotope Separation", deps=["t6_pu"], xp=300, desc=[
            "Uranium-235 and uranium-238 behave identically in reactions. Only mass tells them apart.",
            "How: turn uranium into gaseous &eUF₆&r using hydrofluoric acid (fluorite + H₂SO₄), then spin it."]),
        Q("t6_fission", 6, -2, [item("mekanismgenerators:fission_reactor_casing", 16)], "Fission", deps=["t6_centrifuge"], xp=400, desc=[
            "Split heavy nuclei and release enormous energy. Mind the temperature, and the waste.",
            "How: Just Enough Mekanism Multiblocks shows the reactor layout in JEI."]),
        Q("t6_waste", 8, -2, [item("mekanism:pellet_plutonium"), item("mekanism:pellet_polonium")], "Transmutation by Neutron", deps=["t6_fission"], xp=500, size=1.5, desc=[
            "Reprocess nuclear waste: neutron capture has turned some of it into &eplutonium&r and &epolonium&r.",
            "Real alchemy. Lead to gold was never the hard part."]),
        Q("t6_haber", 0, 2, [item("chemlib:ammonia_bucket")], "Haber-Bosch", deps=["t4_reactor", "t5_hv"], xp=250, desc=[
            "N₂ + 3H₂ → 2NH₃. The &eHaber-Bosch&r process makes ammonia from air and hydrogen. It feeds half the world's food through fertiliser.",
            "How: nitrogen + hydrogen in MI's Chemical Reactor. Fill a bucket from the output tank."]),
        Q("t6_ostwald", 2, 3, [item("chemlib:nitric_acid_bucket")], "Ostwald Process", deps=["t6_haber"], xp=250, desc=[
            "NH₃ + 2O₂ → HNO₃ + H₂O. Burning ammonia over a catalyst gives &enitric acid&r."]),
        Q("t6_pgm", 4, 3, [item("kubejs:pgm_sludge", 4), item("kubejs:chloroplatinic_acid", 2), item("modern_industrialization:platinum_dust", 4)], "The Platinum Line", deps=["t6_ostwald"], xp=500, size=1.5, desc=[
            "Platinum-group metals hide in the sludge left by refining nickel and copper.",
            "1. &eElectrolyzer&r: nickel or copper dust → dust + PGM sludge (25%).",
            "2. &eAqua regia&r (3 HCl : 1 HNO₃) in the Chemical Reactor dissolves platinum as chloroplatinic acid. Iridium, osmium, rhodium and ruthenium don't dissolve: they're left as residue.",
            "3. &eAmmonium chloride&r (NH₃ + HCl) precipitates ammonium hexachloroplatinate. 4. Heat it in the &eBlast Furnace&r: pure platinum.",
            "5. Centrifuge the residue for iridium, osmium, rhodium and ruthenium."]),
        Q("t6_flux", 4, 1, [item("fluxnetworks:flux_core")], "Wireless Power", deps=["t6_pu"], xp=200, desc=[
            "Flux Networks moves energy without cables. The Flux Core needs a processing unit."]),
        Q("t6_chambers", 6, 0, [item("alchemistry:fission_chamber_controller"), item("alchemistry:fusion_chamber_controller")], "Element Transmutation", deps=["t6_pu"], xp=500, size=1.5, desc=[
            "Alchemistry's fission chamber splits one element into two lighter ones; the fusion chamber merges two into a heavier one.",
            "With both, &eevery element&r is within reach."]),
        Q("t6_table", 8, 0, [item("chemlib:uranium", 16), item("chemlib:oganesson")], "The Complete Periodic Table", deps=["t6_chambers"], xp=1000, size=2.0, shape="gear", items=[("kubejs:energy_core_empty", 1)], desc=[
            "&6Element 118, oganesson.&r It barely exists in reality, but you made one.",
            "Every block in this world can now be built from chemicals. You're close to what you once were."]),
    ]),

    # =========================================================================================
    Chapter("t7", "VIII. Creation", "ad_astra:tier_1_rocket",
            ["Leave the cradle. Make matter from energy. Seed a new world."], MAIN, [
        Q("t7_nasa", 0, 0, [item("ad_astra:nasa_workbench")], "Leaving the Cradle", deps=["t6_pu"], xp=400, desc=[
            "The NASA Workbench needs an EV hull. Rockets burn MI diesel."]),
        Q("t7_suit", 2, -2, [item("ad_astra:space_helmet"), item("ad_astra:oxygen_loader")], "Breathe", deps=["t7_nasa"], xp=200, desc=[
            "Space has no air. Fill your space suit with oxygen from your electrolysis line."]),
        Q("t7_rocket", 2, 0, [item("ad_astra:tier_1_rocket"), dim("ad_astra:moon")], "One Small Step", deps=["t7_nasa"], xp=600, size=1.5, desc=[
            "Reach the Moon.",
            "How: build the rocket in the NASA Workbench, fuel it with diesel, and climb in."]),
        Q("t7_antimatter", 4, 0, [item("mekanism:sps_casing", 4), item("mekanism:pellet_antimatter")], "Antimatter", deps=["t7_rocket", "t6_waste"], xp=1000, size=1.75, shape="hexagon", desc=[
            "The Supercritical Phase Shifter turns polonium into &eantimatter&r: matter with every charge reversed.",
            "It's the most energy-dense substance there is."]),
        Q("t7_cores", 6, -2, [item("kubejs:energy_core"), item("kubejs:antimatter_core")], "Energy Cores", deps=["t7_antimatter"], xp=1000, size=1.5, desc=[
            "A stainless-steel shell with polonium and a processing unit becomes an &eEmpty Energy Core&r. Charge it in MI's Assembler (about 3 million EU).",
            "Add antimatter and a quantum circuit and it becomes an &eAntimatter Core&r: the most concentrated energy you can hold."]),
        Q("t7_seed", 8, -1, [item("kubejs:seed_of_a_new_world")], "Seed of a New World", deps=["t7_cores", "t6_table", "mf_ult_table"], xp=3000, size=2.0, shape="hexagon", desc=[
            "&6The endgame goal.&r A 9x9 recipe on the Ultimate Table that needs something from every tier:",
            "coke, synthesized water and hydrogen, sulfuric acid, polyethylene, stainless steel, processing units, oganesson, plutonium, polonium, Nether Stars, four Antimatter Cores, and a Dragon Egg at the centre.",
            "Check JEI for the exact layout."]),
        Q("t7_creation", 10, 0, [tick()], "A New World", deps=["t7_seed"], xp=2000, size=2.5, shape="gear", tokens=50, desc=[
            "&6You took the world apart, element by element, and learned to build it again.&r",
            "Fire, steel, acid, oil, silicon, the atom, antimatter. Every tier was a lesson in chemistry, and you mastered them all.",
            "The worlds out there are blank canvases now. Go make them yours."]),
    ]),

    # =========================================================================================
    Chapter("tools", "Tools and Comfort", "silentgear:pickaxe",
            ["Better tools from better materials, and a soft place to land."], SIDE, [
        Q("tc_grader", 0, 0, [item("silentgear:material_grader")], "Material Grader", deps=["gs_silent"], xp=40, desc=[
            "Grades Silent Gear materials for a stat bonus. Better grades make better parts."]),
        Q("tc_salvager", 2, 0, [item("silentgear:salvager")], "Salvager", deps=["tc_grader"], xp=40, desc=[
            "Breaks old Silent Gear tools back into parts, so upgrading doesn't waste materials."]),
        Q("tc_bronze_paxel", 0, 2, [item("mekanismtools:bronze_paxel")], deps=["gs_paxel", "t0_bronze"], xp=25),
        Q("tc_osmium_paxel", 2, 2, [item("mekanismtools:osmium_paxel")], deps=["tc_bronze_paxel", "t3_infuser"], xp=40),
        Q("tc_diamond_paxel", 4, 2, [item("mekanismtools:diamond_paxel")], deps=["tc_osmium_paxel"], xp=50),
        Q("tc_obsidian_paxel", 6, 2, [item("mekanismtools:refined_obsidian_paxel")], "The Ultimate Paxel", deps=["tc_diamond_paxel"], xp=100, desc=[
            "Refined obsidian is Mekanism's toughest material."]),
        Q("tc_jetpack", 8, 0, [item("ironjetpacks:basic_coil"), item("ironjetpacks:jetpack")], "Jetpacks", deps=["t3_analog"], xp=100, desc=[
            "Iron Jetpacks run on FE. Every jetpack tier needs a coil, and in this pack the coils need MI circuits:",
            "&eBasic&r = analog (LV), &eAdvanced&r = electronic (MV), &eElite&r = digital (HV), &eUltimate&r = processing unit (EV).",
            "How: craft a coil, then the cells, thrusters and jetpack for the material you want (check JEI). Better metals fly faster and longer."]),
        Q("tc_angel", 8, 2, [item("angelring:diamond_ring"), item("angelring:angel_ring")], "The Angel Ring", deps=["t5_hv", "w_end"], xp=500, size=1.5, shape="hexagon", desc=[
            "Portable creative flight from a ring.",
            "It needs an Elytra, ghast tears, diamond blocks and Nether Stars, plus an &eMI digital circuit&r (polyethylene chemistry, HV).",
            "How: craft the Diamond Ring first, then the Angel Ring. Wear it in a Curios ring slot."]),
        Q("tc_hammock", 0, 4, [item("comforts:hammock_white")], "Hammock", deps=["gs_sleep"], xp=15, desc=[
            "Skips the day the way a sleeping bag skips the night."]),
        Q("tc_waystone", 2, 4, [item("waystones:warp_stone")], "Waystones", deps=["gs_iron"], xp=40, desc=[
            "Waystones (found in villages, or crafted) let you teleport between places you've visited.",
            "A Warp Stone lets you warp to any waystone from anywhere."]),
    ]),

    Chapter("factory", "Mob Data and Big Crafting", "hostilenetworks:sim_chamber",
            ["Monifactory-inspired machinery: simulate mobs, craft on giant tables, and fold whole factories into a block."], SIDE, [
        Q("mf_learner", 0, 0, [item("hostilenetworks:deep_learner"), item("hostilenetworks:blank_data_model")], "Deep Learning", deps=["gs_iron"], xp=40, desc=[
            "Hostile Neural Networks: put a data model for a mob in the Deep Learner, then fight that mob to train it.",
            "How: right-click a blank data model on a mob type (or craft a specific one), and keep the Deep Learner in your inventory while you fight."]),
        Q("mf_sim", 2, 0, [item("hostilenetworks:sim_chamber"), item("hostilenetworks:prediction_matrix", 4)], "Simulation", deps=["mf_learner", "t4_mv"], xp=150, desc=[
            "The Simulation Chamber runs a trained model on power and prediction matrices to produce mob drops without the mob.",
            "In this pack it needs an &eMV electronic circuit&r, so a trained model pays off once you reach aluminum chemistry."]),
        Q("mf_fab", 4, 0, [item("hostilenetworks:loot_fabricator")], "Loot Fabricator", deps=["mf_sim"], xp=150, desc=[
            "Turns simulated predictions into specific drops. Also needs an MV electronic circuit."]),
        Q("mf_basic_table", 0, 2, [item("extendedcrafting:black_iron_ingot", 8), item("extendedcrafting:basic_table")], "Extended Crafting", deps=["t1_steel"], xp=50, desc=[
            "Black iron is the frame of Extended Crafting. The Basic Table is a 3x3 table for its recipes.",
            "How: check JEI for black iron. The bigger tables come later."]),
        Q("mf_adv_table", 2, 2, [item("extendedcrafting:advanced_table")], "5x5: Advanced Table", deps=["mf_basic_table", "t4_mv"], xp=100, desc=[
            "Needs an MV electronic circuit."]),
        Q("mf_elite_table", 4, 2, [item("extendedcrafting:elite_table")], "7x7: Elite Table", deps=["mf_adv_table", "t5_hv"], xp=200, desc=[
            "Needs an HV digital circuit."]),
        Q("mf_ult_table", 6, 2, [item("extendedcrafting:ultimate_table")], "9x9: Ultimate Table", deps=["mf_elite_table", "t6_pu"], xp=400, desc=[
            "Needs an EV processing unit. The endgame's biggest crafts happen here."]),
        Q("mf_packaged", 6, 0, [item("packagedauto:packager"), item("packagedauto:unpackager")], "Packaged Automation", deps=["t5_ae2", "mf_adv_table"], xp=150, desc=[
            "Packaged Auto lets AE2 autocraft with Extended Crafting tables (through the PackagedExCrafting addon). Put a big recipe in a pattern and AE2 does the rest."]),
        Q("mf_compact", 0, 4, [item("compactmachines:personal_shrinking_device")], "Compact Machines", deps=["t3_hull"], xp=75, desc=[
            "Fold an entire factory into a single block. The Personal Shrinking Device lets you walk inside it."]),
        Q("mf_facade", 2, 4, [item("cable_facades:facade_wrench")], "Hide the Cables", deps=["t3_hull"], xp=25, desc=[
            "Cable Facades disguise cables and pipes as any block. Tidy factories, same throughput."]),
        Q("mf_cake", 4, 4, [item("telepastries:overworld_cake")], "Teleporting Cake", deps=["t2_nether"], xp=40, desc=[
            "TelePastries: eat a slice to travel to that cake's dimension. Refill it with the right ingredient."]),
    ]),
    Chapter("qol", "Quality of Life", "akashictome:tome",
            ["Small things that make a big difference."], SIDE, [
        Q("q_tome", 0, 0, [item("akashictome:tome")], "One Book to Rule Them All", deps=["gs_table"], xp=20, desc=[
            "The Akashic Tome merges every mod's guidebook into one item.",
            "How: craft it, then right-click it with other guidebooks to add them."]),
        Q("q_compass", 2, 0, [item("naturescompass:naturescompass"), item("explorerscompass:explorerscompass")], "Find Anything", deps=["gs_iron"], xp=30, desc=[
            "Nature's Compass finds biomes; Explorer's Compass finds structures (Nether Fortresses, Ancient Cities, villages)."]),
        Q("q_torch", 4, 0, [item("torchmaster:megatorch")], "No More Mob Spawns", deps=["gs_iron"], xp=40, desc=[
            "The Mega Torch stops hostile mobs spawning in a huge radius. Great around your base."]),
        Q("q_grave", 6, 0, [tick()], "Graves", deps=["gs_iron"], xp=10, desc=[
            "If you die, Corail Tombstone keeps your items in a grave where you fell. Walk back and open it to recover everything."]),
        Q("q_bp_up", 0, 2, [item("sophisticatedbackpacks:pickup_upgrade"), item("sophisticatedbackpacks:magnet_upgrade")], "Backpack Upgrades", deps=["gs_backpack"], xp=40, desc=[
            "Pickup and magnet upgrades pull items straight into your backpack. There's also feeding, crafting, smelting and more (check JEI)."]),
        Q("q_waystone", 2, 2, [item("waystones:waystone")], "Waystones", deps=["gs_iron"], xp=40, desc=[
            "Place waystones at your important locations and teleport between them."]),
        Q("q_gadget", 4, 2, [item("buildinggadgets2:gadget_building")], "Building Gadgets", deps=["t3_hull"], xp=40, desc=[
            "Place and copy whole structures with FE-powered gadgets."]),
        Q("q_effortless", 6, 2, [item("effortlessbuilding:randomizer_tool")], "Effortless Building", deps=["gs_table"], xp=20, desc=[
            "Mirror, array and line building modes for big builds. The randomizer places a random mix of blocks."]),
        Q("q_backups", 8, 1, [tick()], "Backups", deps=["gs_iron"], xp=10, desc=[
            "Simple Backups saves your world automatically. On a server, backups live in the server's backups folder."]),
    ]),

    Chapter("storage", "Storage and Logistics", "sophisticatedbackpacks:backpack",
            ["A god needs somewhere to keep things."], SIDE, [
        Q("s_barrel", 0, 0, [item("sophisticatedstorage:barrel")], deps=["gs_backpack"], xp=25, desc=[
            "Upgradable chests and barrels. Sophisticated Storage Plus raises their limits."]),
        Q("s_drawers", 2, 0, [item("functionalstorage:oak_1")], deps=["s_barrel"], xp=25, desc=[
            "Functional Storage drawers hold lots of one item. Pair them with a storage controller."]),
        Q("s_toms", 4, 0, [item("toms_storage:storage_terminal"), item("toms_storage:inventory_connector")], "An Early Network", deps=["s_drawers"], xp=75, desc=[
            "Tom's Simple Storage connects your chests into one searchable terminal. It's your network until AE2.",
            "How: place an Inventory Connector touching your chests (or link them with Inventory Cables), and a Storage Terminal on it."]),
        Q("s_furnace", 0, 2, [item("ironfurnaces:iron_furnace")], "Faster Furnaces", deps=["gs_iron"], xp=25, desc=[
            "Iron Furnaces: faster furnaces, and some can generate power."]),
        Q("s_pipes", 2, 2, [item("pipez:item_pipe", 8)], "Pipez", deps=["gs_iron"], xp=25, desc=[
            "Simple item, fluid and energy pipes for moving things between non-MI machines."]),
        Q("s_laser", 4, 2, [item("laserio:laser_node", 2)], "LaserIO", deps=["s_pipes", "t3_hull"], xp=75, desc=[
            "Moves items, fluids and energy between nodes without cables."]),
        Q("s_ae_drive", 6, 0, [item("ae2:drive"), item("ae2:terminal")], "AE2 Storage", deps=["t5_ae2"], xp=150, desc=[
            "Drives hold storage cells, and terminals let you see everything. MEGA Cells adds much bigger cells later."]),
        Q("s_ae_craft", 8, 0, [item("ae2:crafting_terminal")], "Autocrafting", deps=["s_ae_drive"], xp=150, desc=[
            "Pattern providers plus molecular assemblers turn whole chemical chains into one click. ME Requester keeps stock topped up automatically."]),
    ]),

    Chapter("magic", "Divine Gifts", "ars_nouveau:novice_spell_book",
            ["Light magic, relics, and the enchanter's craft."], SIDE, [
        Q("m_book", 0, 0, [item("ars_nouveau:novice_spell_book")], deps=["t2_ars"], xp=50, desc=[
            "Write your first spells. Glyphs combine into effects."]),
        Q("m_jar", 2, 0, [item("ars_nouveau:source_jar"), item("ars_nouveau:imbuement_chamber")], deps=["m_book"], xp=75, desc=[
            "Source is magical energy. Store it in jars; the Imbuement Chamber uses it."]),
        Q("m_ritual", 4, 0, [item("ars_nouveau:ritual_flight")], "Ritual of Flight", deps=["m_jar"], xp=150, desc=[
            "Gives creative flight to players nearby, paid for with Source. Good for base flight."]),
        Q("m_apoth", 0, 2, [item("apotheosis:reforging_table")], "Apotheosis", deps=["gs_iron"], xp=50, desc=[
            "Gear with affixes and gems. Reforge, salvage and socket your way to divine equipment."]),
        Q("m_reliquary", 2, 2, [item("reliquary:mob_charm_fragment")], "Relics", deps=["m_apoth"], xp=50, desc=[
            "Reliquary, Relics and Artifacts add relics and artifacts to find and build. Some drop from mobs, others are hidden in structures."]),
    ]),

    Chapter("worlds", "Other Worlds", "deeperdarker:heart_of_the_deep",
            ["Realms beyond the Overworld."], SIDE, [
        Q("w_otherside", 0, 0, [item("deeperdarker:heart_of_the_deep"), dim("deeperdarker:otherside")], "The Otherside", deps=["t2_nether"], xp=300, desc=[
            "Beyond the Ancient City lies the Otherside. Take a Heart of the Deep from the Warden."]),
        Q("w_end", 2, 0, [dim("minecraft:the_end")], "The End", deps=["t2_nether"], xp=200, desc=[
            "End Crystals from here power Just Dire Things' flight upgrade."]),
    ]),

    Chapter("farming", "Farming", "botanypots:terracotta_hopper_botany_pot",
            ["Grow what you need, within the rules of chemistry."], SIDE, [
        Q("f_pot", 0, 0, [item("botanypots:terracotta_hopper_botany_pot")], "Hopper Botany Pots", deps=["gs_food"], xp=25, desc=[
            "Hopper Botany Pots grow crops and push the harvest into the container below.",
            "How: place one on a chest, add soil (dirt) and a seed."]),
        Q("f_altar", 2, 0, [item("mysticalagriculture:infusion_altar"), item("mysticalagriculture:inferium_essence", 16)], "Mystical Agriculture", deps=["f_pot"], xp=50, desc=[
            "Resource crops. Seeds are made on the Infusion Altar.",
            "&eTier 3/4/5 seeds need MI LV/MV/HV circuits&r, and crops for chemistry milestones (uranium, osmium, fluorite, silicon, steel, aluminum and others) can't be grown.",
            "Farming is a convenience here, not a shortcut."]),
    ]),
]

# Demigod Tokens per quest, scaled by tier (milestone quests, size >= 1.5, pay double).
TOKENS = {"welcome": 1, "start": 1, "t0": 1, "t1": 2, "t2": 2, "t3": 3, "t4": 3, "t5": 4, "t6": 5, "t7": 8}
for _c in CHAPTERS:
    _c.tokens = TOKENS.get(_c.key, 1)
