"""Quest chapter: justdirethings (Just Dire Things side page). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

The short JDT line in tools.py (tc_jdt_*) stays where it is; this page goes deeper and links to it.
Pack gates: no JDT recipe is changed in KubeJS. The flight upgrade keeps its End Crystal recipe
(phase4_integration.js, docs/PROGRESSION.md section 7) and can only go on the Eclipse Alloy Chestplate, so JDT flight
needs tier 4 goo (Ancient City) and a netherite block.
Layout: y=0 materials spine; y=-2 coal tiers; y=-4 power and fuels; y=-6 time crystals (late, optional);
y=2 tools; y=4 upgrades, armour and flight; y=6/8 machines; y=10 wands and oddities. Links on x=-2.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

J = "justdirethings:"

CHAPTER = Chapter("justdirethings", "Just Dire Things", J + "gooblock_tier1",
        ["Living goo that rewrites the blocks it touches: new metals, denser coal, refined fuels, upgradeable tools and small automation machines."], SIDE, [
    # --- materials spine (y=0) -----------------------------------------------------------------
    Q("jdt_goo", 0, 0, [item(J + "gooblock_tier1"), item("minecraft:iron_block", 2)], "Feeding the Goo", deps=["gs_iron"], xp=30,
      subtitle="Goo converts the blocks around it", desc=[
        "&6You remember making things change just by touching them. The goo still can; you'll borrow the trick.&r",
        "&eWhat:&r goo blocks slowly convert the blocks touching them. Tier 1 (Primogel) turns iron blocks into raw ferricore ore.",
        "&eHow:&r place the goo, put iron blocks against its sides and wait. JEI's Goo Spreading tab lists every conversion, its tier and its time.",
        "&eTip:&r after a conversion the goo can die (a 10% chance in this pack's config). Right-click exhausted Primogel with sugar or rotten flesh to wake it."]),
    Q("jdt_ferricore", 2, 0, [item(J + "raw_ferricore", 8)], "Raw Ferricore", deps=["jdt_goo"], xp=30,
      subtitle="Mine what the goo made", desc=[
        "&eWhat:&r raw ferricore ore drops raw ferricore. Smelt or blast it into ferricore ingots, the base of everything on this page.",
        "&eHow:&r mine the converted block with a pickaxe. Silk Touch gives you the ore block itself instead.",
        "&eTip:&r one iron block (9 ingots) becomes one raw ferricore, so let a Create or MI line feed the goo once you need a lot."]),
    Q("jdt_blank", 4, 0, [item(J + "upgrade_blank", 2)], "Upgrade Blanks", deps=["jdt_ferricore"], xp=30,
      subtitle="Four ferricore ingots, one empty upgrade", desc=[
        "&eWhat:&r every Just Dire Things upgrade and smithing template starts from a blank.",
        "&eHow:&r four ferricore ingots in a diamond shape (check JEI).",
        "&eTip:&r keep a stack around; most upgrades are a blank plus a few vanilla items."]),
    Q("jdt_blazegold", 6, 0, [item(J + "gooblock_tier2"), item(J + "raw_blazegold", 4)], "Blazebloom and Blazegold", deps=["jdt_ferricore", "t2_nether"], xp=50,
      subtitle="Tier 2 goo turns gold into blazegold", desc=[
        "&eWhat:&r Blazebloom goo (tier 2) converts gold blocks into raw blazegold ore. Blazegold opens the second tier of tools and machines.",
        "&eHow:&r tier 1 goo ringed with blaze powder, redstone and Nether wart (check JEI). Smelt the raw blazegold.",
        "&eChemistry:&r real gold is famously unreactive: it doesn't tarnish in air because Au has a very high reduction potential (+1.50 V).",
        "&eTip:&r feed exhausted Blazebloom Nether wart or blaze powder."]),
    Q("jdt_celestigem", 8, 0, [item(J + "gooblock_tier3"), item(J + "celestigem", 4)], "VoidShimmer and Celestigem", deps=["jdt_blazegold", "w_dragon"], xp=80,
      subtitle="Tier 3 goo turns diamond into a gem", desc=[
        "&eWhat:&r VoidShimmer goo (tier 3) turns diamond blocks into celestigem ore, which drops celestigem directly. Advanced machines and the third tool tier use it.",
        "&eHow:&r tier 2 goo ringed with ender pearls, end stone and dragon's breath (check JEI). A diamond conversion takes twice as long as iron or gold.",
        "&eChemistry:&r diamond is pure carbon: every atom bonds to four neighbours in a tetrahedral (sp³) lattice, which is why it's so hard.",
        "&eTip:&r VoidShimmer revives with chorus fruit or an ender pearl."]),
    Q("jdt_eclipse", 10, 0, [item(J + "gooblock_tier4"), item(J + "raw_eclipsealloy", 2)], "Shadowpulse and Eclipse Alloy", deps=["jdt_celestigem", "w_ancient"], xp=120,
      size=1.5, shape="hexagon", subtitle="Tier 4 goo eats a netherite block", desc=[
        "&6The goo has learned to eat the hardest thing you own. You remember being that hungry.&r",
        "&eWhat:&r Shadowpulse goo (tier 4) turns netherite blocks into raw eclipse alloy ore, Just Dire Things' top material.",
        "&eHow:&r tier 3 goo ringed with sculk, sculk shriekers and echo shards from an Ancient City (check JEI). Smelt the raw eclipse alloy.",
        "&eTip:&r one netherite block is a big price. Plan which eclipse alloy item you want first; Shadowpulse revives with sculk or a sculk catalyst."]),

    # --- coal tiers (y=-2) ---------------------------------------------------------------------
    Q("jdt_coal_t1", 2, -2, [item(J + "coal_t1", 8)], "Primal Coal", deps=["jdt_goo"], xp=30,
      subtitle="Goo squeezes a coal block denser", desc=[
        "&eWhat:&r tier 1 goo turns a coal block (or a charcoal block) into Primal Coal ore. Primal Coal burns for 4,800 ticks, three times a piece of coal.",
        "&eChemistry:&r real coal ranks up with heat and pressure: lignite (~65% carbon) → bituminous (~80%) → anthracite (>90%). More carbon, more energy per kilogram.",
        "&eHow:&r place coal or charcoal blocks against tier 1 goo and mine the ore (it drops several pieces).",
        "&eTip:&r nine Primal Coal make a block, and that block is the input for the next tier."]),
    Q("jdt_coal_t2", 6, -2, [item(J + "coal_t2", 8)], "Blaze Ember", deps=["jdt_coal_t1", "jdt_blazegold"], xp=40,
      subtitle="The second coal tier", desc=[
        "&eWhat:&r tier 2 goo turns a Primal Coal block into Blaze Ember ore. Blaze Ember burns 14,400 ticks: nine coal's worth.",
        "&eHow:&r craft a Primal Coal block, put it against Blazebloom goo and mine the ore for 3 to 4 embers.",
        "&eTip:&r each coal tier burns three times longer than the one before, so the climb pays off quickly."]),
    Q("jdt_coal_t3", 8, -2, [item(J + "coal_t3", 8)], "Voidflame Coal", deps=["jdt_coal_t2", "jdt_celestigem"], xp=50,
      optional=True, tokens=1, subtitle="Optional: the third coal tier", desc=[
        "&eWhat:&r tier 3 goo turns a Blaze Ember block into Voidflame Coal ore: 43,200 ticks of burn per piece.",
        "&eHow:&r a block of Blaze Ember against VoidShimmer goo (check JEI for counts).",
        "&eTip:&r Voidflame Coal is also the catalyst for the tier 3 fluid fuel."]),
    Q("jdt_coal_t4", 10, -2, [item(J + "coal_t4", 4)], "Eclipse Ember", deps=["jdt_coal_t3", "jdt_eclipse"], xp=70,
      optional=True, tokens=2, subtitle="Optional: 81 coal in one lump", desc=[
        "&eWhat:&r tier 4 goo turns a Voidflame Coal block into Eclipse Ember ore. One ember burns 129,600 ticks, as long as 81 pieces of coal.",
        "&eHow:&r a block of Voidflame Coal against Shadowpulse goo.",
        "&eChemistry:&r burning carbon, C + O₂ → CO₂, gives about 394 kJ per mole. Denser fuel just packs more carbon into the same slot."]),
    Q("jdt_charcoal", 0, -2, [item(J + "charcoal", 4)], "Charcoal Blocks", deps=["jdt_goo"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a renewable way into Primal Coal", desc=[
        "&eWhat:&r Just Dire Things adds a charcoal block (nine charcoal). It burns for 16,000 ticks and tier 1 goo accepts it like a coal block.",
        "&eChemistry:&r charcoal is wood heated without air (pyrolysis): water and volatiles leave, mostly carbon stays.",
        "&eTip:&r a tree farm plus a furnace array makes the coal ladder fully renewable."]),

    # --- power and fuels (y=-4) ----------------------------------------------------------------
    Q("jdt_generator", 2, -4, [item(J + "generatort1")], "Simple Coal Generator", deps=["jdt_coal_t1"], xp=40,
      subtitle="Burn the coal tiers for FE", desc=[
        "&eWhat:&r burns solid fuel for Forge Energy: up to 1,000 FE/t into a 1,000,000 FE buffer.",
        "&eHow:&r ferricore, redstone, coal and a blast furnace (check JEI).",
        "&eTip:&r it burns fuel four times faster than a furnace, so the long-burning coal tiers are what make it worth having."]),
    Q("jdt_fuel_canister", 0, -4, [item(J + "fuel_canister")], "Fuel Canister", deps=["jdt_coal_t1"], xp=20,
      optional=True, tokens=1, subtitle="Optional: fuel in one slot", desc=[
        "&eWhat:&r a canister that soaks up furnace fuel and stores it as burn time. Its tooltip shows how much it holds.",
        "&eHow:&r ferricore around a piece of coal (check JEI).",
        "&eTip:&r pair it with the Pocket Generator from the Tools page so your FE tools recharge on long trips."]),
    Q("jdt_polymorphic", 6, -4, [item(J + "polymorphic_catalyst", 4), item(J + "polymorphic_fluid_bucket")], "Polymorphic Fluid", deps=["jdt_blazegold"], xp=40,
      subtitle="Drop a catalyst into water", desc=[
        "&eWhat:&r Polymorphic Fluid is the base for every Just Dire Things fluid: fuels, portal fluid and time fluid.",
        "&eHow:&r blazegold + Nether wart makes four catalysts. Throw one into a water source block and it becomes Polymorphic Fluid. Bucket it up.",
        "&eChemistry:&r a real catalyst speeds a reaction and comes out unchanged. This one is used up, so chemists would call it a reagent.",
        "&eTip:&r JEI shows these 'fluid drop' recipes; each catalyst converts one source block."]),
    Q("jdt_fuel_t2", 8, -4, [item(J + "refined_t2_fluid_bucket")], "Blaze Ember Fuel", deps=["jdt_polymorphic", "jdt_coal_t2"], xp=50,
      subtitle="Unrefined, then refined by goo", desc=[
        "&eWhat:&r liquid fuel for the Simple Fuel Generator. It comes from Polymorphic Fluid in two steps.",
        "&eHow:&r drop a Blaze Ember into a Polymorphic Fluid source to get Unrefined Blaze Ember Fuel, then let tier 2 goo touch that source to refine it.",
        "&eChemistry:&r real refineries separate crude oil by boiling point in a fractionating column; here the goo does the cleanup.",
        "&eTip:&r tier 3 and 4 fuels follow the same pattern: drop the next coal into the refined fuel below it, then refine with the next goo."]),
    Q("jdt_fluid_gen", 10, -4, [item(J + "generatorfluidt1")], "Simple Fuel Generator", deps=["jdt_fuel_t2"], xp=60,
      subtitle="Liquid fuel, more FE", desc=[
        "&eWhat:&r burns refined fuel for up to 5,000 FE/t. Blaze Ember Fuel gives 450 FE per mB, Voidflame 1,300 and Eclipse Ember 4,000.",
        "&eHow:&r blazegold, redstone, buckets and a blast furnace (check JEI). Pipe or bucket refined fuel in.",
        "&eTip:&r one bucket of Eclipse Ember Fuel is 4,000,000 FE, nearly the generator's whole 5,000,000 FE buffer."]),
    Q("jdt_fuel_high", 12, -4, [item(J + "refined_t3_fluid_bucket"), item(J + "refined_t4_fluid_bucket")], "Voidflame and Eclipse Fuels", deps=["jdt_fluid_gen", "jdt_coal_t4"], xp=80,
      optional=True, tokens=2, subtitle="Optional: the two top refined fuels", desc=[
        "&eWhat:&r the tier 3 and tier 4 liquid fuels, roughly 3x and 9x the energy of Blaze Ember Fuel per mB.",
        "&eHow:&r Voidflame Coal into refined Blaze Ember Fuel, then VoidShimmer goo; Eclipse Ember into refined Voidflame Fuel, then Shadowpulse goo.",
        "&eTip:&r one bucket of each. The refined fuel is consumed by the next step, so keep a source block of each tier going."]),
    Q("jdt_transmitter", 12, -2, [item(J + "energytransmitter", 2)], "Energy Transmitter", deps=["jdt_generator", "jdt_celestigem"], xp=50,
      optional=True, tokens=1, subtitle="Optional: power without cables", desc=[
        "&eWhat:&r Energy Transmitters move FE without cables, up to 1,000 FE/t, losing a little for every block of distance (check the GUI).",
        "&eHow:&r celestigem, redstone, an ender pearl and blazegold (check JEI).",
        "&eChemistry:&r real power lines lose energy as heat, P = I²R, which is why grids use high voltage and low current."]),

    # --- time crystals (y=-6) ------------------------------------------------------------------
    Q("jdt_time_crystal", 10, -6, [item(J + "time_crystal", 4)], "Time Crystals", deps=["jdt_eclipse"], xp=100,
      optional=True, tokens=2, subtitle="Optional: Shadowpulse goo on budding amethyst", desc=[
        "&eWhat:&r tier 4 goo turns budding amethyst into a Budding Time Crystal block, which grows time crystal clusters.",
        "&eHow:&r budding amethyst can't be moved, so take Shadowpulse goo to a geode and place it touching a budding block. The budding block has to mature in stages first; check JEI and its tooltip for what it needs.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured purple by iron (Fe³⁺) impurities and natural radiation.",
        "&eTip:&r a Time Crystal Block converts back into a budding block, so one success is enough."]),
    Q("jdt_time_wand", 8, -6, [item(J + "time_wand"), item(J + "time_fluid_bucket")], "The Time Wand", deps=["jdt_time_crystal", "jdt_polymorphic"], xp=80,
      optional=True, tokens=1, subtitle="Optional: speed up time on a block", desc=[
        "&eWhat:&r the Time Wand makes a block tick faster (up to 256x), paid for in FE and Time Fluid.",
        "&eHow:&r Time Fluid: drop a time crystal into a Polymorphic Fluid source. The wand is blazegold, ferricore and a time crystal (check JEI).",
        "&eTip:&r try it on a slow crop, a furnace or a budding block."]),
    Q("jdt_paradox", 12, -6, [item(J + "paradoxmachine")], "Paradox Machine", deps=["jdt_time_crystal", "jdt_time_wand"], xp=150,
      optional=True, tokens=2, subtitle="Optional: undo what happened to an area", desc=[
        "&eWhat:&r the Paradox Machine reverts blocks and entities in an area to an earlier state, paying FE and Time Fluid per block or entity.",
        "&eHow:&r eclipse alloy, time crystals, a time crystal block and a bucket of Time Fluid (check JEI).",
        "&eTip:&r it's powerful and expensive. Read its GUI before you aim it at your base."]),

    # --- tools (y=2) ---------------------------------------------------------------------------
    Q("jdt_tools_t1", 2, 2, [item(J + "ferricore_pickaxe"), item(J + "ferricore_axe"), item(J + "ferricore_shovel")], "Ferricore Tools", deps=["jdt_ferricore"], xp=40,
      subtitle="Tools that take upgrades", desc=[
        "&eWhat:&r Just Dire Things tools work like iron ones but accept ability upgrades. Each tier can hold more abilities and break more blocks at once.",
        "&eHow:&r the usual tool shapes with ferricore ingots and sticks.",
        "&eTip:&r vein-style abilities are capped per tier: 64 blocks for ferricore, 128 blazegold, 192 celestigem, 256 eclipse alloy."]),
    Q("jdt_oreminer", 4, 2, [item(J + "upgrade_oreminer")], "Ore Miner", deps=["jdt_tools_t1", "jdt_blank"], xp=40,
      subtitle="Your first ability: mine the whole vein", desc=[
        "&eWhat:&r Ore Miner harvests every connected ore when you break one.",
        "&eHow:&r a blank between two iron pickaxes, then combine the upgrade with your pickaxe in a smithing table (no template needed).",
        "&eTip:&r every ability goes on the same way. JEI shows which tools accept which upgrade."]),
    Q("jdt_tools_t2", 6, 2, [item(J + "template_blazegold"), item(J + "blazegold_pickaxe")], "Blazegold Upgrade", deps=["jdt_tools_t1", "jdt_blazegold"], xp=50,
      subtitle="Smith ferricore tools up a tier", desc=[
        "&eWhat:&r tools climb tiers in the smithing table: template + old tool + new ingot.",
        "&eHow:&r a blazegold template is a blank ringed with blazegold. Smith it with a ferricore pickaxe and a blazegold ingot.",
        "&eTip:&r a template plus two ingots crafts two templates, so never spend your last one."]),
    Q("jdt_tools_t3", 8, 2, [item(J + "celestigem_pickaxe"), item(J + "celestigem_paxel")], "Celestigem and the Paxel", deps=["jdt_tools_t2", "jdt_celestigem"], xp=80,
      subtitle="Pickaxe, axe and shovel in one", desc=[
        "&eWhat:&r from celestigem up you can fuse a pickaxe, axe and shovel of the same tier into a paxel.",
        "&eHow:&r smith the blazegold tools up with a celestigem template, then put pickaxe, axe and shovel together in the smithing table (check JEI).",
        "&eTip:&r one paxel instead of three tools frees two hotbar slots."]),
    Q("jdt_tools_t4", 10, 2, [item(J + "eclipsealloy_paxel")], "Eclipse Alloy Paxel", deps=["jdt_tools_t3", "jdt_eclipse"], xp=120,
      optional=True, tokens=2, subtitle="Optional: the last tool tier", desc=[
        "&eWhat:&r the top paxel. Eclipse alloy tools take the strongest abilities, such as Instant Break and Ore X-Ray.",
        "&eHow:&r smith celestigem tools with an eclipse alloy template, then fuse the three (check JEI).",
        "&eTip:&r Instant Break needs a Nether Star, a netherite pickaxe and time crystals."]),
    Q("jdt_bows", 4, 3.5, [anyof([J + "bow_ferricore", J + "bow_blazegold", J + "bow_celestigem", J + "bow_eclipsealloy"])], "Dire Bows", deps=["jdt_tools_t1"], xp=30,
      optional=True, tokens=1, subtitle="Optional: bows with abilities", desc=[
        "&eWhat:&r Just Dire Things bows tier up like the tools and take arrow abilities: Potion Arrow, Splash, Lingering, Homing and more.",
        "&eHow:&r a ferricore bow first (check JEI); smith it up with templates.",
        "&eTip:&r Potion Arrow uses a Potion Canister (ferricore around a glass bottle) instead of tipped arrows."]),

    # --- upgrades, armour and flight (y=4..5.5) ------------------------------------------------
    Q("jdt_upgrades", 6, 4, [anyof([J + "upgrade_hammer", J + "upgrade_treefeller", J + "upgrade_smelter", J + "upgrade_orescanner",
                                     J + "upgrade_lawnmower", J + "upgrade_leafbreaker", J + "upgrade_skysweeper", J + "upgrade_dropteleport"], 3)],
      "A Toolbox of Abilities", deps=["jdt_oreminer"], xp=50, optional=True, tokens=1, subtitle="Optional: any three tool upgrades", desc=[
        "&eWhat:&r Hammer (3x3 up to 7x7 by tier), Treefeller, Smelter (auto-smelts drops), Ore Scanner, Lawnmower, Leafbreaker, Skysweeper and Drops Teleport.",
        "&eHow:&r each is a blank plus vanilla parts, e.g. Hammer = blank + two diamond pickaxes, Smelter = blank + blast furnace + blaze rods (check JEI).",
        "&eChemistry:&r smelting ore is reduction: carbon pulls the oxygen off the metal, e.g. Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eTip:&r not every tier takes every upgrade; JEI's smithing recipes show the allowed pairs."]),
    Q("jdt_armor", 2, 5.5, [item(J + "ferricore_helmet"), item(J + "ferricore_chestplate"), item(J + "ferricore_leggings"), item(J + "ferricore_boots")],
      "Ferricore Armour", deps=["jdt_ferricore"], xp=40, optional=True, tokens=1, subtitle="Optional: armour that takes upgrades", desc=[
        "&eWhat:&r Just Dire Things armour takes upgrades too: Step Assist and Jump Boost on boots, Walk and Run Speed on leggings, Mind Fog on helmets.",
        "&eHow:&r the usual armour shapes in ferricore. Smith them up with templates later.",
        "&eTip:&r higher tiers add Night Vision, Water Breathing, Negate Fall Damage and Lava Immunity."]),
    Q("jdt_elytra", 8, 5.5, [item(J + "upgrade_elytra"), item(J + "celestigem_chestplate")], "Built-in Elytra", deps=["jdt_tools_t3"], xp=80,
      optional=True, tokens=1, subtitle="Optional: an elytra inside your chestplate", desc=[
        "&eWhat:&r the Elytra upgrade builds an elytra into a celestigem or eclipse alloy chestplate, so you keep armour and glide.",
        "&eHow:&r a blank plus an elytra (from an End City), then smith it onto the chestplate.",
        "&eTip:&r it's gliding, not flight. True flight is the next step."]),
    Q("jdt_flight", 10, 4, [item(J + "upgrade_flight"), item(J + "eclipsealloy_chestplate")], "Flight", deps=["jdt_eclipse", "jdt_blank"], xp=250,
      size=1.5, shape="gear", subtitle="Creative-style flight, the hard way", desc=[
        "&6You remember the sky. The goo had to eat netherite before it would give it back.&r",
        "&eWhat:&r the Flight upgrade gives creative-style flight. It only fits the Eclipse Alloy Chestplate, so it needs tier 4 goo and a netherite block.",
        "&eHow:&r a blank with phantom membranes, feathers and two End Crystals (check JEI), smithed onto an eclipse alloy chestplate.",
        "&eTip:&r this pack keeps the End Crystal recipe on purpose: JDT flight is a late reward, after the End and an Ancient City."]),
    Q("jdt_chest_more", 12, 5.5, [anyof([J + "upgrade_invulnerability", J + "upgrade_lavaimmunity", J + "upgrade_extinguish",
                                          J + "upgrade_deathprotection", J + "upgrade_time_protection", J + "upgrade_phase"], 2)],
      "Chestplate Defences", deps=["jdt_flight"], xp=80, optional=True, tokens=1, subtitle="Optional: two more chestplate abilities", desc=[
        "&eWhat:&r Invulnerability (a few seconds on demand), Lava Immunity, Extinguish, Death Protection (once every 5 minutes), Time Protection and Phase (walk through walls, on leggings).",
        "&eHow:&r check JEI for each; Death Protection takes a Totem of Undying and time crystals.",
        "&eTip:&r activated abilities sit on keybinds; look for Just Dire Things in Controls."]),

    # --- machines (y=6..8) ---------------------------------------------------------------------
    Q("jdt_breaker", 4, 7, [item(J + "blockbreakert1"), item(J + "blockplacert1")], "Breaker and Placer", deps=["jdt_ferricore"], xp=40,
      subtitle="The first automation pair", desc=[
        "&eWhat:&r the Simple Block Breaker mines the block in front of it; the Simple Block Placer puts blocks down. Together they automate a goo farm.",
        "&eHow:&r ferricore, a diamond, lapis, redstone and an observer (breaker) or dispenser (placer). Check JEI.",
        "&eTip:&r a placer feeding iron blocks to the goo and a breaker harvesting the ore makes ferricore hands-free."]),
    Q("jdt_clicker", 6, 7, [item(J + "clickert1"), item(J + "sensort1")], "Clicker and Sensor", deps=["jdt_breaker"], xp=40,
      subtitle="Fake clicks and redstone eyes", desc=[
        "&eWhat:&r the Simple Clicker right- or left-clicks like a player; the Simple Sensor emits a redstone signal when it sees a chosen block or mob.",
        "&eHow:&r both use ferricore, lapis, redstone and an eye of ender (clicker: dispenser core, sensor: observer core).",
        "&eTip:&r a sensor watching for the converted ore can tell the breaker exactly when to fire."]),
    Q("jdt_fluid_machines", 2, 8.5, [item(J + "fluidcollectort1"), item(J + "fluidplacert1")], "Fluid Collector and Placer", deps=["jdt_breaker"], xp=30,
      optional=True, tokens=1, subtitle="Optional: pick up and place fluid sources", desc=[
        "&eWhat:&r the fluid versions of the breaker and placer: collect source blocks into a tank, or set them down.",
        "&eHow:&r ferricore, lapis, redstone and a bucket around a dispenser or dropper (check JEI).",
        "&eTip:&r a placer and a collector around goo automate the refined fuel line."]),
    Q("jdt_item_collector", 0, 7, [item(J + "itemcollector"), item(J + "droppert1")], "Item Collector and Dropper", deps=["jdt_ferricore"], xp=30,
      optional=True, tokens=1, subtitle="Optional: vacuum up drops", desc=[
        "&eWhat:&r the Item Collector pulls dropped items from an area into an attached inventory; the Simple Dropper drops items out like a configurable dropper.",
        "&eHow:&r Item Collector: ferricore, a hopper, a diamond and an ender pearl. Dropper: ferricore, lapis, redstone and a dropper.",
        "&eTip:&r the Machine Settings Copier (Primal Coal, paper, ferricore) copies one machine's setup to another."]),
    Q("jdt_machines_t2", 8, 7, [anyof([J + "blockbreakert2", J + "blockplacert2", J + "clickert2", J + "sensort2", J + "droppert2",
                                        J + "fluidcollectort2", J + "fluidplacert2"], 2)], "Advanced Machines", deps=["jdt_clicker", "jdt_celestigem"], xp=60,
      subtitle="Any two tier 2 machines", desc=[
        "&eWhat:&r the Advanced versions do the same jobs with more range and settings (check each GUI).",
        "&eHow:&r the Simple machine in the centre, ringed with celestigem, eyes of ender and redstone (check JEI).",
        "&eTip:&r one Advanced Breaker can harvest a whole wall of goo conversions."]),
    Q("jdt_swapper", 10, 7, [item(J + "blockswappert1")], "The Swapper", deps=["jdt_clicker", "jdt_blazegold"], xp=50,
      optional=True, tokens=1, subtitle="Optional: trade two blocks' places", desc=[
        "&eWhat:&r Swappers exchange the blocks (and optionally entities) between two linked spots. The Advanced Swapper uses eclipse alloy.",
        "&eHow:&r blazegold, lapis, redstone, an eye of ender and an observer (check JEI).",
        "&eTip:&r swap freshly converted ore out and a new iron block in, without breaking anything."]),
    Q("jdt_player_stuff", 8, 8.5, [anyof([J + "playeraccessor", J + "inventory_holder", J + "experienceholder"], 2)], "Blazegold Utilities", deps=["jdt_blazegold"], xp=40,
      optional=True, tokens=1, subtitle="Optional: any two blazegold blocks", desc=[
        "&eWhat:&r the Player Accessor lets pipes reach a bound player's inventory; the Inventory Holder stores and swaps a loadout; the Experience Holder banks XP.",
        "&eHow:&r all three are blazegold plus vanilla parts (armour stand, books, emerald, ender pearls; check JEI).",
        "&eTip:&r the Experience Holder is the tidy place to keep levels between anvil and enchanting sessions."]),

    # --- wands and oddities (y=10) -------------------------------------------------------------
    Q("jdt_blazejet", 4, 10, [item(J + "blazejet_wand")], "Blazejet Wand", deps=["jdt_blazegold"], xp=40,
      optional=True, tokens=1, subtitle="Optional: launch yourself", desc=[
        "&eWhat:&r Air Burst: the wand launches you in the direction you're looking.",
        "&eHow:&r a blazegold ingot over two ferricore ingots (check JEI).",
        "&eTip:&r it's the base of the Voidshift Wand, so don't throw it away."]),
    Q("jdt_voidshift", 6, 10, [item(J + "voidshift_wand")], "Voidshift Wand", deps=["jdt_blazejet", "jdt_celestigem"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the next mobility wand", desc=[
        "&eWhat:&r the Blazejet Wand upgraded with celestigem. It adds Void Shift (read its tooltip for the details).",
        "&eHow:&r celestigem, the Blazejet Wand and blazegold in a column.",
        "&eTip:&r it upgrades again into the Eclipsegate Wand."]),
    Q("jdt_eclipsegate", 8, 10, [item(J + "eclipsegate_wand")], "Eclipsegate Wand", deps=["jdt_voidshift", "jdt_eclipse"], xp=100,
      optional=True, tokens=2, subtitle="Optional: a portable hole", desc=[
        "&eWhat:&r Eclipse Gate temporarily removes the blocks you click, then puts them back.",
        "&eHow:&r eclipse alloy, the Voidshift Wand and celestigem in a column.",
        "&eTip:&r perfect for stepping through your own base walls without breaking them."]),
    Q("jdt_polywand", 10, 10, [item(J + "polymorphic_wand")], "Polymorphic Wand", deps=["jdt_polymorphic"], xp=50,
      optional=True, tokens=1, subtitle="Optional: turn one mob into another", desc=[
        "&eWhat:&r the wand polymorphs a mob into a random one (or, on the Advanced wand, a chosen target), using Polymorphic Fluid.",
        "&eHow:&r a fluid canister, a polymorphic catalyst and blazegold in a column. Fill it with Polymorphic Fluid.",
        "&eTip:&r the Advanced Polymorphic Wand adds eclipse alloy and celestigem and also costs FE."]),
    Q("jdt_catcher", 2, 10, [item(J + "creaturecatcher"), item(J + "totem_of_death_recall")], "Catcher and Recall Totem", deps=["jdt_blazegold"], xp=40,
      optional=True, tokens=1, subtitle="Optional: two handy blazegold items", desc=[
        "&eWhat:&r the Creature Catcher captures a mob to carry and release elsewhere; the Totem of Death Recall is for getting back to where you died (read its tooltip).",
        "&eHow:&r both are blazegold and ender pearls (the totem adds diamonds and lapis). Check JEI.",
        "&eTip:&r it won't take the Ender Dragon, sadly."]),
    Q("jdt_portal_v2", 12, 10, [item(J + "portal_fluid_bucket"), item(J + "portalgun_v2")], "Portal Fluid", deps=["jdt_polymorphic", "jdt_celestigem"], xp=100,
      optional=True, tokens=2, subtitle="Optional: the Advanced Portal Gun", desc=[
        "&eWhat:&r Portal Fluid powers the Advanced Portal Gun, the upgrade of the Portal Gun on the Tools page.",
        "&eHow:&r a Portal Fluid Catalyst (chorus fruit and lapis) dropped into Polymorphic Fluid makes Unstable Portal Fluid; tier 3 goo stabilises it. The gun adds celestigem and a fluid canister (check JEI).",
        "&eTip:&r the Advanced Portal Gun holds 1,000,000 FE; the basic one only 100,000."]),
], links=[("gs_iron", -2, 0), ("tc_jdt_goo", -2, 2), ("t2_nether", -2, -2), ("w_dragon", -2, -4), ("w_ancient", -2, -6)])
