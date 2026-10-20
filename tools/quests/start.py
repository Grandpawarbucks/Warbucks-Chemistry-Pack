"""Quest chapter: start. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Shape (2026-10-19 rebuild): a first day, then iron, then a first look at the pack's main systems, then onward to T0.
Sections: First Day (wood, stone, fire, light), First Night (shelter, bed, food, leather), Iron Age (iron, tools,
armour, water, redstone, diamonds), A Taste of Everything (one small step into several mods, each pointing to its
category page), Onward (the first mining trip and the door to Chapter I).
Utility sub-systems live on their own pages: the backpack (gs_backpack) is in storage.py, the paxels (gs_paxel,
gs_opt_paxels) and the smithing table (gs_opt_smithing) in tools.py, the sleeping bag (gs_sleep) in qol.py. Their keys are unchanged.
"""
from questlib import Q, Chapter, item, dim, tick, anytag, anyof, MAIN, SIDE  # noqa: F401

COOKED_MEAT = ["minecraft:cooked_beef", "minecraft:cooked_porkchop", "minecraft:cooked_mutton",
               "minecraft:cooked_chicken", "minecraft:cooked_rabbit"]
HOES = ["minecraft:wooden_hoe", "minecraft:stone_hoe", "minecraft:iron_hoe", "minecraft:golden_hoe", "minecraft:diamond_hoe"]
COOKED_FISH = ["minecraft:cooked_cod", "minecraft:cooked_salmon"]
CHAINMAIL = ["minecraft:chainmail_helmet", "minecraft:chainmail_chestplate", "minecraft:chainmail_leggings", "minecraft:chainmail_boots"]
GOLD_ARMOUR = ["minecraft:golden_helmet", "minecraft:golden_chestplate", "minecraft:golden_leggings", "minecraft:golden_boots"]

CHAPTER = Chapter("start", "Getting Started", "minecraft:oak_sapling",
        ["You wake in a world you didn't make, with a god's patience and none of a god's power.",
         "A first day, a first night, first iron, and a first look at everything this world offers."], MAIN, [
    # === First Day: wood, stone, fire, light ===================================================
    Q("gs_wake", 0, 0, [tick()], "The Awakening", subtitle="Everything is made of elements",
      size=2.0, shape="gear", xp=10, deps=["wel_ready"], desc=[
        "&6You were more than this once. The book in your hands is in your own handwriting, though you don't remember writing it.&r",
        "&eWhat:&r One idea stayed with you: everything is made of elements, and elements can be taken apart and put back together. This chapter gets you through your first day and night, to iron, and gives you a first look at the rest of the book.",
        "&eHow:&r Click the checkmark on the right to begin. Follow the lines: each quest leads to the next."]),
    Q("gs_jei", 0, 0, [tick()], "Tip: Recipes and Jade", subtitle="R for recipes, U for uses", section="First Day", deps=["gs_wake"], xp=10, desc=[
        "&eWhat:&r JEI shows every recipe in the pack, including the ones changed for progression. Jade shows a small panel at the top of the screen for whatever block you're looking at.",
        "&eHow:&r Press &eR&r over any item to see how it's made, or &eU&r to see what it's used in. Try it on the crafting table you're about to make, then click the checkmark.",
        "&eTip:&r Type &e@modname&r in the JEI search bar to list a mod's items. When a machine isn't working, look at it: Jade shows its progress, energy and fluids, and usually why."]),
    Q("gs_logs", 0, 0, [anytag("minecraft:logs", 16)], "Punch a Tree", subtitle="Bare hands, sixteen logs", deps=["gs_wake"], xp=10, desc=[
        "&eWhat:&r You start with nothing. Logs are the first thing you can take with bare hands, and everything early is made from them.",
        "&eChemistry:&r Wood is mostly &ecellulose&r, (C₆H₁₀O₅)ₙ, long chains of glucose, bound together by &elignin&r, a tough aromatic polymer that keeps trees standing.",
        "&eHow:&r Hold left-click on a tree trunk. Any kind of log counts.",
        "&eTip:&r FTB Ultimine fells a whole tree at once: hold the &e`&r key (grave/tilde) while you break the bottom log."]),
    Q("gs_table", 0, 0, [item("minecraft:crafting_table")], "Planks and a Workbench", subtitle="One log, four planks; four planks, one table",
      deps=["gs_logs"], xp=10, items=[("minecraft:torch", 8)], desc=[
        "&eWhat:&r Planks are the basic building material for tables, tools, chests and beds. Your inventory only has a 2x2 grid; almost every tool and machine needs the full 3x3 grid of a crafting table.",
        "&eHow:&r Put a log in the 2x2 grid in your inventory: each log gives 4 planks. Then 4 planks in the 2x2 grid make the table. Place it and right-click it.",
        "&eTip:&r Keep a few logs as logs: some shortcuts below use them directly. The 8 torches in the reward get you through your first night."]),
    Q("gs_chest", 0, 0, [item("minecraft:chest")], "Somewhere to Put Things", subtitle="A chest for your first stockpile", section="First Day", deps=["gs_table"], xp=10, desc=[
        "&eWhat:&r You'll collect far more than you can carry. Chests hold 27 stacks each, and two side by side make a double chest.",
        "&eHow:&r 8 planks in a ring make one chest. The &eUtilitarian&r shortcut is better: 8 &elogs&r in a ring make 4 chests.",
        "&eTip:&r A chest is also the heart of your first backpack. That quest, and everything else about storage, is on the &eStorage and Logistics&r page."]),
    Q("gs_opt_boat", 0, 0, [anytag("minecraft:boats")], "Messing About in Boats", subtitle="Faster than walking along a coast", section="First Day", deps=["gs_table"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A boat crosses rivers and oceans much faster than swimming, and you can scout coastlines for villages and exposed ore.",
        "&eChemistry:&r Dry wood is about 0.4 to 0.7 g/cm³, lighter than water at 1.0 g/cm³, so it floats. That's density, nothing more.",
        "&eHow:&r 5 planks of one wood in a U shape. Check JEI for the chest boat too.",
        "&eTip:&r Mobs that touch a boat get pulled into it. Handy for moving a cow home."]),
    Q("gs_woodpick", 0, 0, [item("minecraft:wooden_pickaxe")], "Sticks and a Wooden Pick", subtitle="Just enough to break stone", deps=["gs_table"], xp=10, desc=[
        "&eWhat:&r Sticks are the handle of every tool and torch. A wooden pickaxe is weak, but it can mine stone, and stone is your next step.",
        "&eHow:&r 2 planks stacked vertically make 4 sticks. Then 3 planks across the top and 2 sticks down the middle of a crafting table make the pickaxe.",
        "&eTip:&r &eUtilitarian&r adds a shortcut: 2 &elogs&r stacked vertically make &e16 sticks&r, twice as many per log as going through planks."]),
    Q("gs_stone", 0, 0, [item("minecraft:cobblestone", 16), item("minecraft:stone_pickaxe")], "Stone Age", subtitle="Cobblestone, and a pickaxe that can mine iron", deps=["gs_woodpick"], xp=15, desc=[
        "&eWhat:&r Cobblestone makes stone tools, a furnace and a safe first shelter. A stone pickaxe can mine iron ore.",
        "&eChemistry:&r Stone is a mix of &esilicate minerals&r: quartz (SiO₂) and feldspars, aluminium silicates of sodium, potassium and calcium. Silicon and oxygen are the two most common elements in the Earth's crust.",
        "&eHow:&r Dig a few blocks down or mine a cliff face: stone drops cobblestone. The stone pickaxe is the wooden shape with 3 cobblestone in place of planks.",
        "&eTip:&r FTB Ultimine mines a whole vein at once. Hold the &e`&r key (grave/tilde) while breaking blocks."]),
    Q("gs_coal", 0, 0, [item("minecraft:coal", 8)], "Coal", subtitle="Ancient carbon from the ground", section="First Day", deps=["gs_stone"], xp=15, desc=[
        "&eWhat:&r Coal fuels furnaces now, and becomes coke and steel in Chapter II.",
        "&eChemistry:&r Coal is plant matter buried for millions of years. Heat and pressure drove off most of its hydrogen and oxygen and left mostly carbon.",
        "&eHow:&r Coal ore is the black-speckled stone common in exposed cliffs and mountains. Mine it with any pickaxe.",
        "&eTip:&r Save extra coal for torches on your first mining trip. The Coke Oven in Chapter II eats a lot of it too."]),
    Q("gs_stonetools", 0, 0, [item("minecraft:stone_sword"), item("minecraft:stone_axe"), item("minecraft:stone_shovel")], "A Full Toolkit",
      subtitle="Sword, axe and shovel", deps=["gs_stone"], xp=15, desc=[
        "&eWhat:&r A sword for the first night, an axe for faster wood, and a shovel for dirt, sand and gravel.",
        "&eHow:&r Each takes 1 to 3 cobblestone and 1 or 2 sticks. Press &eR&r on each one if you forget the shape.",
        "&eTip:&r An axe is also a decent weapon: it hits harder than a sword but swings slower."]),
    Q("gs_opt_bow", 0, 0, [item("minecraft:bow"), item("minecraft:arrow", 16)], "Bow and Arrow", subtitle="Deal with creepers from a distance",
      section="First Day", deps=["gs_stonetools"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A bow lets you kill creepers and skeletons before they reach you.",
        "&eHow:&r 3 sticks and 3 string make a bow. Arrows are flint, a stick and a feather. Spiders drop string, chickens drop feathers, and gravel sometimes drops flint.",
        "&eTip:&r Hold right-click to draw the bow fully. A half-drawn shot does little damage."]),
    Q("gs_furnace", 0, 0, [item("minecraft:furnace")], "Fire", subtitle="Your first chemistry tool", deps=["gs_stonetools"], xp=20, desc=[
        "&eWhat:&r Fire is your first chemistry tool. It cooks food, turns sand into glass and ore into metal, and chars logs into charcoal (more on that in Chapter I).",
        "&eChemistry:&r A furnace drives reactions with heat. Most of what it does is breaking bonds and letting atoms find new partners.",
        "&eHow:&r 8 cobblestone in a ring make a furnace. Logs, planks, coal and charcoal all burn as fuel.",
        "&eTip:&r Furnaces in this pack cook about &e4x faster&r than vanilla, so you rarely wait on one."]),
    Q("gs_opt_campfire", 0, 0, [item("minecraft:campfire")], "Campfire", subtitle="Cooks without fuel", section="Fire and Light", deps=["gs_furnace"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A campfire cooks up to 4 pieces of food at once and never needs fuel.",
        "&eChemistry:&r A log on a campfire chars slowly without enough air to burn through: that's &epyrolysis&r, the same reaction as the furnace, just slower.",
        "&eHow:&r 3 sticks, 1 coal or charcoal and 3 logs (check JEI). Right-click food onto it.",
        "&eTip:&r &eUtilitarian&r lets a campfire cook any log that burns into charcoal. Smoke rising from it also helps you find home."]),
    Q("gs_opt_glass", 0, 0, [item("minecraft:glass", 16)], "Glass", subtitle="Melted sand", section="Fire and Light", deps=["gs_furnace"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Windows let you see out of your shelter, and glass shows up in many machine recipes later.",
        "&eChemistry:&r Sand is mostly silica, SiO₂. Melted and cooled quickly, it can't line up into crystals and freezes into a disordered solid: glass. Real glassmakers add soda (Na₂CO₃) to lower its melting point of about 1,700 °C.",
        "&eHow:&r Smelt sand in a furnace. Beaches, deserts and riverbeds are full of it."]),
    Q("gs_torch", 0, 0, [item("minecraft:torch", 16)], "Light in the Dark", subtitle="Combustion you can carry", deps=["gs_furnace"], xp=15, desc=[
        "&eWhat:&r Torches stop monsters spawning and light up caves.",
        "&eChemistry:&r A torch is &ecombustion&r: carbon reacting with oxygen, C + O₂ → CO₂, releasing heat and light.",
        "&eHow:&r One coal or charcoal on top of one stick makes 4 torches. No coal yet? Smelt a log into charcoal: it works just as well."]),

    # === First Night: shelter, bed, food, leather ==============================================
    Q("gs_shelter", 0, 0, [tick()], "A Roof Overhead", subtitle="Walls, a door, and light", deps=["gs_torch"], xp=15, desc=[
        "&eWhat:&r Monsters spawn in the dark. A small, lit, enclosed room keeps you safe while you work.",
        "&eHow:&r Build four walls and a roof from planks or cobblestone, add a door, and light the inside with torches. Click the checkmark when you're done.",
        "Days here last about &etwice as long&r as in vanilla (roughly 20 minutes of daylight); nights are normal length, and rain is rarer and shorter.",
        "&eTip:&r Leave room to grow: your steam machines in Chapter I need floor space. The &eBuilding and Decoration&r page has ideas for later."]),
    Q("gs_bed", 0, 0, [anytag("minecraft:beds")], "A Bed", subtitle="Skip the night, set your spawn", deps=["gs_shelter"], xp=20, desc=[
        "&6You never needed sleep before. Lying in the dark, you remember why mortals feared it.&r",
        "&eWhat:&r Sleeping skips the night and sets your spawn point, so you wake up here if you die.",
        "&eChemistry:&r Wool is &ekeratin&r, a protein held together by sulfur-sulfur bonds between cysteine units. The same protein makes up your hair and nails.",
        "&eHow:&r 3 wool of one colour over 3 planks. Shear sheep or kill them for wool.",
        "&eTip:&r Going exploring? A sleeping bag skips the night without moving your spawn (see the &eQuality of Life&r page)."]),
    Q("gs_farm", 0, 0, [anyof(HOES), item("minecraft:wheat", 8)], "A First Field", subtitle="Seeds, hoe, water, wheat", deps=["gs_bed"], xp=15, desc=[
        "&eWhat:&r A small wheat field feeds you for the whole early game.",
        "&eChemistry:&r A plant builds itself out of air and water using sunlight: &ephotosynthesis&r, 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂.",
        "&eHow:&r Break grass and tall grass for seeds. Craft a hoe, till dirt next to water and plant them. Farmland stays wet up to 4 blocks from water. Harvest when the wheat turns golden.",
        "&eTip:&r Bone meal (from skeleton bones) is calcium phosphate, a real fertiliser. Right-click a crop with it to grow it faster."]),
    Q("gs_opt_canes", 0, 0, [item("minecraft:sugar_cane", 16)], "Sugar Cane", subtitle="Sugar and paper", section="First Night", deps=["gs_farm"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Sugar cane gives sugar for food and paper for books, maps and Silent Gear blueprints.",
        "&eChemistry:&r Table sugar is &esucrose&r, C₁₂H₂₂O₁₁: one glucose and one fructose joined together. Paper is pressed cellulose fibres, the same polymer as wood.",
        "&eHow:&r Find cane growing on sand or dirt right next to water. Plant it the same way to farm it; break the top and leave the bottom block.",
        "&eTip:&r &eUtilitarian&r makes paper in the 2x2 grid: 3 cane in an L shape give 3 paper."]),
    Q("gs_food", 0, 0, [item("minecraft:bread", 2)], "Something to Eat", subtitle="Wheat, bread, and a full belly",
      deps=["gs_farm"], xp=15, items=[("minecraft:bread", 8)], desc=[
        "&eWhat:&r Gods don't need to eat. You do, for now.",
        "&eChemistry:&r Baking turns starch and protein into new compounds. The brown crust comes from the &eMaillard reaction&r between sugars and amino acids.",
        "&eHow:&r 3 wheat in a row on a crafting table make 1 bread. With &eUtilitarian&r you can also put 3 wheat in an L shape in your 2x2 grid.",
        "&eTip:&r AppleSkin shows how much hunger and saturation each food restores."]),
    Q("gs_meat", 0, 0, [anyof(COOKED_MEAT, 4)], "Cooked Meat", subtitle="Much better than bread", deps=["gs_food"], xp=15, desc=[
        "&eWhat:&r Cooked meat restores far more hunger and saturation than bread. Cows also drop the leather you need next.",
        "&eChemistry:&r Heat &edenatures&r proteins: it unfolds them so they firm up, and turns tough collagen into soft gelatin. It also kills bacteria.",
        "&eHow:&r Kill cows, pigs, sheep, chickens or rabbits and cook the raw meat in a furnace, smoker or on a campfire. Any mix of cooked meat counts.",
        "&eTip:&r Breed animals with wheat (cows, sheep) or carrots (pigs) next to your base so you never have to hunt far."]),
    Q("gs_fish", 0, 0, [item("minecraft:fishing_rod"), anyof(COOKED_FISH, 2)], "Gone Fishing", subtitle="Food from any patch of water", section="First Night", deps=["gs_meat"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A fishing rod gets you food anywhere there's water, plus the odd treasure.",
        "&eHow:&r 3 sticks and 2 string. Cast it into water and pull it in when the bobber dips. Cook the cod or salmon you catch.",
        "&eTip:&r A rod also reels in mobs and items, and fishing in the rain is faster."]),
    Q("gs_leather", 0, 0, [item("minecraft:leather_chestplate"), item("minecraft:leather_boots")], "Leather Armour", subtitle="Better than nothing", deps=["gs_meat"], xp=15, desc=[
        "&eWhat:&r Leather armour is weak, but it's the first protection you can make, and it's dyeable.",
        "&eChemistry:&r Leather is animal skin that's been &etanned&r: tannins or chromium salts cross-link the collagen proteins so the hide stops rotting and stays flexible.",
        "&eHow:&r Cows drop leather. A tunic takes 8 leather and boots take 4.",
        "&eTip:&r Save spare leather: your first backpack needs some (on the &eStorage and Logistics&r page)."]),

    # === Iron Age: iron, tools, armour, water, redstone, diamonds ==============================
    Q("gs_iron", 0, 0, [item("minecraft:iron_ingot", 8)], "Iron", subtitle="Ore, heat, and carbon make metal", deps=["gs_leather"], xp=25, desc=[
        "&6The ore gives up its metal in the fire. Once, you did this with a thought.&r",
        "&eWhat:&r Iron is the metal of your first real tools, buckets and armour, and the key to most of the other pages in this book.",
        "&eChemistry:&r Iron ore is iron oxide. In the furnace, carbon pulls the oxygen away: Fe₂O₃ + 3C → 2Fe + 3CO. That's &ereduction&r.",
        "&eHow:&r Mine iron ore with a stone pickaxe (it's common around Y 16 and in mountains) and smelt the raw iron.",
        "&eTip:&r Iron Furnaces (on the &eStorage and Logistics&r page) smelt faster once you have spare iron."]),
    Q("gs_shield", 0, 0, [item("minecraft:shield")], "Shield", subtitle="Block the arrows", section="Iron Age", deps=["gs_iron"], xp=15, desc=[
        "&eWhat:&r A shield blocks arrows, melee hits and creeper blasts while you hold right-click.",
        "&eHow:&r 1 iron ingot and 6 planks (check JEI for the shape).",
        "&eTip:&r Hold it in your off-hand so you can block and swing at the same time. The &eMonster Hunting&r page opens from here."]),
    Q("gs_opt_shears", 0, 0, [item("minecraft:shears"), anytag("minecraft:wool", 16)], "Shearing Season", subtitle="Wool without killing the sheep",
      section="Iron Age", deps=["gs_iron"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Shears take 1 to 3 wool from a sheep without hurting it, and the wool grows back after the sheep eats grass.",
        "&eChemistry:&r Raw wool is coated in &elanolin&r, a waxy mix of esters that keeps the sheep dry. It's the base of many skin creams.",
        "&eHow:&r 2 iron ingots placed diagonally make shears. Right-click a sheep.",
        "&eTip:&r Dye a sheep before you shear it to get coloured wool every time it regrows."]),
    Q("gs_ironpick", 0, 0, [item("minecraft:iron_pickaxe")], "Iron Pickaxe", subtitle="Diamonds, gold and redstone open up", deps=["gs_iron"], xp=25, desc=[
        "&eWhat:&r Needed for diamonds, redstone and gold, and to start the journey to the Nether.",
        "&eChemistry:&r Iron is harder than stone because its atoms sit in a regular metal lattice held by metallic bonds, which bend rather than shatter.",
        "&eHow:&r 3 iron ingots and 2 sticks."]),
    Q("gs_redstone", 0, 0, [item("minecraft:redstone", 8)], "Redstone", subtitle="A red dust that carries a signal", section="Going Deeper", deps=["gs_ironpick"], xp=15, desc=[
        "&eWhat:&r Redstone powers doors, lamps and contraptions now, and goes into circuits and machines all through the book.",
        "&eChemistry:&r Redstone has no real-world twin, but its ore looks a lot like &ecinnabar&r, mercury sulfide (HgS): the red mineral people once ground into vermilion paint.",
        "&eHow:&r Redstone ore sits deep, mostly below Y 16, and needs an iron pickaxe. Each block drops several dust.",
        "&eTip:&r Levers, repeaters and the rest are on the &eQuality of Life&r page (Redstone Basics)."]),
    Q("gs_opt_gold", 0, 0, [anyof(GOLD_ARMOUR)], "All That Glitters", subtitle="Pretty, soft, and useful in the Nether",
      section="Going Deeper", deps=["gs_ironpick"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r Gold armour is weaker than iron and wears out fast, but in the Nether piglins leave you alone while you wear one piece.",
        "&eChemistry:&r Gold is a &enoble metal&r: it hardly reacts with oxygen or water, so it never tarnishes. That's why ancient gold still shines.",
        "&eHow:&r Mine gold ore with an iron pickaxe and smelt it. Any one piece of gold armour counts."]),
    Q("gs_diamond", 0, 0, [item("minecraft:diamond")], "Carbon Under Pressure", subtitle="Your first diamond", section="Going Deeper", deps=["gs_ironpick"], xp=25, desc=[
        "&eWhat:&r Diamonds make the toughest vanilla tools, and a diamond pickaxe is the only early way to mine obsidian.",
        "&eChemistry:&r A diamond is the same element as coal: carbon. Here every atom is bonded to four others in a rigid 3D lattice, formed about 150 km underground under enormous pressure.",
        "&eHow:&r Diamond ore sits in the deepslate layers, most of it near the bottom of the world. Mine it with an iron pickaxe.",
        "&eTip:&r Obsidian is the frame of the Nether portal in Chapter III. Keep your first diamonds for a pickaxe."]),
    Q("gs_irontools", 0, 0, [item("minecraft:iron_sword"), item("minecraft:iron_axe"), item("minecraft:iron_shovel")], "Iron Tools",
      subtitle="Sword, axe and shovel in iron", deps=["gs_ironpick"], xp=20, desc=[
        "&eWhat:&r Iron tools are faster and last far longer than stone, and an iron sword handles anything the early nights throw at you.",
        "&eHow:&r Same shapes as the stone tools, with iron ingots in place of cobblestone.",
        "&eTip:&r Your iron pickaxe, axe and shovel combine into one &epaxel&r: that quest is on the &eGear and Comfort&r page."]),
    Q("gs_armor", 0, 0, [item("minecraft:iron_helmet"), item("minecraft:iron_chestplate"), item("minecraft:iron_leggings"), item("minecraft:iron_boots")],
      "Iron Armour", subtitle="A full set before you dig deep", deps=["gs_irontools"], xp=30, desc=[
        "&eWhat:&r A full set of iron armour makes caves and the night survivable.",
        "&eHow:&r Helmet, chestplate, leggings and boots take 24 iron ingots in total.",
        "&eTip:&r Ultimine through an iron vein and you'll have this set in minutes."]),
    Q("gs_opt_chain", 0, 0, [anyof(CHAINMAIL)], "Chainmail", subtitle="Rings of iron, linked together", section="Iron Age", deps=["gs_iron"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Chainmail sits between leather and iron. It isn't craftable in vanilla, but you can trade an armourer villager for it or take it from a mob that spawned wearing it.",
        "&eChemistry:&r Interlocked rings spread the force of a blow across many links, so no single point takes the whole hit.",
        "&eHow:&r Modern Industrialization adds a recipe from &eIron Rings&r once you have its tools (check JEI for both). Any one piece counts."]),
    Q("gs_bucket", 0, 0, [item("minecraft:water_bucket")], "Water", subtitle="The most important chemical in the pack", deps=["gs_armor"], xp=15, desc=[
        "&eWhat:&r Water is the most important chemical in this pack: steam, electrolysis and acids all start with it.",
        "&eChemistry:&r H₂O is a small, polar molecule. That polarity lets it dissolve salts and acids, which is why chemists call it the universal solvent.",
        "&eHow:&r 3 iron ingots in a V make a bucket. Fill it at any water source.",
        "&eTip:&r Two water sources in a 2x2 hole make an infinite spring. Carry a water bucket while mining: it puts out fire and breaks falls."]),

    # === A Taste of Everything: one small step into several mods, each pointing to its page =====
    Q("gs_taste", 0, 0, [tick()], "A Taste of Everything", subtitle="The book is wider than one road", deps=["gs_armor"], section="A Taste of Everything",
      size=1.5, shape="hexagon", xp=15, desc=[
        "&6Your memories come back in pieces, and not in order. Gears, spirits, strange seeds: you knew all of it once.&r",
        "&eWhat:&r The Demigod's Path is the main road, but every category in the sidebar is a mod with its own chapters. The quests here are one small step into a few of them, and each says where to go next.",
        "&eHow:&r Click the checkmark, then try whichever look fun. Most of these are optional.",
        "&eTip:&r None of these block Chapter I. Claim Your Land and Tools from Parts are worth doing early; the rest can wait for a quiet evening."]),
    Q("gs_silent", 0, 0, [item("silentgear:blueprint_paper"), item("silentgear:pickaxe")], "Tools from Parts", subtitle="Silent Gear: stats come from materials",
      deps=["gs_taste"], xp=40, desc=[
        "&eWhat:&r Silent Gear builds tools from parts. Each part's stats come from its &ematerial&r, so better chemistry means better tools.",
        "&eHow:&r Make Blueprint Paper, craft a Pickaxe Blueprint, then craft a pickaxe head and rod (check JEI). An iron head is a good start.",
        "&eTip:&r Repair kits, better materials and the paxels are on the &eGear and Comfort&r page."]),
    Q("gs_taste_create", 0, 0, [item("create:andesite_alloy", 2)], "Clockwork", subtitle="Create: a first piece of machinery", deps=["gs_taste"],
      optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Create is the pack's early mechanical tier: shafts, water wheels, presses and mixers that turn by rotation, before you have electricity.",
        "&eChemistry:&r Andesite is a grey volcanic rock, rich in feldspar. Bound with metal it makes a cheap, sturdy frame material, which is all Create needs from it.",
        "&eHow:&r Andesite and iron nuggets in a 2x2 grid (check JEI). Andesite is the speckled grey stone common in hills and caves.",
        "&eTip:&r &eThe Mechanical Age&r category picks up from here. Create feeds Modern Industrialization later; it doesn't replace it."]),
    Q("gs_opt_cook", 0, 0, [item("farmersdelight:cooking_pot"), item("farmersdelight:beef_stew")], "Kitchen Chemistry", subtitle="Farmer's Delight: a proper meal",
      deps=["gs_taste"], section="A Taste of Everything", optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Farmer's Delight meals restore more hunger and give the Nourishment and Comfort effects.",
        "&eChemistry:&r Stewing denatures proteins: heat unfolds them, which is why meat turns firm and tender.",
        "&eHow:&r Craft a Cooking Pot (iron, bricks, a water bucket and a wooden shovel), set it over a campfire or stove, and cook raw beef, a carrot and a potato.",
        "&eTip:&r The &eFarming and Food&r category has knives, crops, feasts and more."]),
    Q("gs_taste_inferium", 0, 0, [item("mysticalagriculture:inferium_essence", 4)], "Seeds of Plenty", subtitle="Mystical Agriculture: essence from the ground",
      deps=["gs_taste"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Inferium essence is the base of Mystical Agriculture, whose crops grow resources instead of food.",
        "&eHow:&r Inferium ore is green-flecked stone found underground; mine it with any pickaxe. Mobs drop a little essence too.",
        "&eTip:&r The &eMystical Agriculture&r category starts with the Infusion Altar. Higher seed tiers need MI circuits, and the chemistry milestones can't be grown at all."]),
    Q("gs_taste_datura", 0, 0, [item("occultism:datura_seeds")], "Strange Seeds", subtitle="Occultism: a plant that shows hidden things",
      deps=["gs_taste"], optional=True, tokens=1, xp=20, desc=[
        "&eWhat:&r Demon's Dream seeds are the first step into Occultism, the pack's spirit magic.",
        "&eChemistry:&r Real datura plants are full of &etropane alkaloids&r such as scopolamine and atropine. They're poisonous, and they cause vivid hallucinations. Never eat the real thing.",
        "&eHow:&r Break grass: the seeds drop now and then.",
        "&eTip:&r The &eOccultism&r category shows what the fruit does and what the spirits can do for you."]),
    Q("gs_claim", 0, 0, [tick()], "Claim Your Land", subtitle="Protect your base with FTB Chunks", deps=["gs_taste"], section="A Taste of Everything", xp=20, desc=[
        "&eWhat:&r FTB Chunks protects your base and can keep it loaded while you're away.",
        "&eHow:&r Press &eM&r to open the map, then drag over chunks to claim them. Click the checkmark when done.",
        "&eTip:&r Right-click a claimed chunk to force-load it. You'll need that for the flight pylon later. More conveniences like this are on the &eQuality of Life&r page."]),

    # === Onward: the first mining trip and the door to Chapter I ===============================
    Q("gs_mine", 0, 0, [item("minecraft:raw_copper", 16), item("minecraft:raw_iron", 16)], "A First Mining Trip", subtitle="Go down, come back richer",
      deps=["gs_bucket"], xp=25, desc=[
        "&eWhat:&r Chapter I needs copper and plenty of iron. Time for a proper trip underground.",
        "&eChemistry:&r Below about Y 0, stone gives way to &edeepslate&r: older, denser rock formed under more heat and pressure. Ores near the surface are often oxidised by air and water, which is why copper ore has green streaks.",
        "&eHow:&r Pack torches, food, a water bucket and spare tools. Dig a staircase down (never straight down) or explore a cave, and bring back raw copper and raw iron.",
        "&eTip:&r &eUtilitarian&r turns 7 logs (in the ladder shape) into 24 ladders. Place a ladder line in your shaft so you can always climb out."]),
    Q("gs_opt_ores", 0, 0, [item("minecraft:coal"), item("minecraft:raw_iron"), item("minecraft:raw_copper"), item("minecraft:raw_gold"),
                            item("minecraft:redstone"), item("minecraft:lapis_lazuli"), item("minecraft:diamond"), item("minecraft:emerald")],
      "Rock Collector", subtitle="One of every vanilla ore drop", section="Onward", deps=["gs_mine"], optional=True, tokens=2, xp=30, desc=[
        "&eWhat:&r Collect one drop from every vanilla ore. Emeralds only generate in mountain biomes.",
        "&eChemistry:&r Real ores are minerals: iron comes from oxides like hematite (Fe₂O₃), copper often from sulfides like chalcopyrite (CuFeS₂), and diamond is pure carbon.",
        "&eTip:&r Every one of these can go into the Dissolver later. Keep spares."]),
    Q("gs_opt_spyglass", 0, 0, [item("minecraft:spyglass")], "A Closer Look", subtitle="Copper and amethyst", section="Onward", deps=["gs_mine"], optional=True, tokens=1, xp=15, desc=[
        "&eWhat:&r A spyglass lets you scout terrain and spot ore in cliff faces from far away.",
        "&eChemistry:&r Amethyst is quartz (SiO₂). Its purple colour comes from traces of iron in the crystal.",
        "&eHow:&r 2 copper ingots and 1 amethyst shard. Amethyst geodes sit underground, ringed with smooth basalt."]),
    Q("gs_ready", 0, 0, [tick()], "Ready for Chemistry", subtitle="Fed, armed, sheltered", size=1.5, shape="hexagon",
      deps=["gs_mine"], xp=50, items=[("minecraft:copper_ingot", 16), ("modern_industrialization:tin_ingot", 8)], desc=[
        "&6Fed, armed, sheltered: a good day, by mortal standards. Now the real work begins, the long road back to what you were.&r",
        "&eWhat:&r Chapter I, Fire and Bronze, starts the Demigod's Path proper: charcoal, your first alloy and steam power.",
        "&eHow:&r Click to open Chapter I. The copper and tin in the reward are a head start on bronze.",
        "&eTip:&r Bring spare coal and iron. Chapter I eats both."]),
], links=[("gs_backpack", 0, 0), ("gs_paxel", 0, 0), ("gs_sleep", 0, 0)])
