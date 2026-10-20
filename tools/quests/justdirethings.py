"""Quest chapter: justdirethings (Just Dire Things side page). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

The short JDT line in tools.py (tc_jdt_*) stays where it is; this page goes deeper and links to it.
Pack gates: no JDT recipe is changed in KubeJS. The flight upgrade keeps its End Crystal recipe
(phase4_integration.js, docs/PROGRESSION.md section 7) and can only go on the Eclipse Alloy Chestplate, so JDT flight
needs tier 4 goo (Ancient City) and a netherite block.
Layout: y=0 materials spine; y=-2 coal tiers; y=-4 power and fuels; y=-6 time crystals (late, optional);
y=2 tools; y=4 upgrades, armour and flight; y=6/8 machines; y=10 wands and oddities. Links on x=-2.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, MAIN, SIDE  # noqa: F401

J = "justdirethings:"

CHAPTER = Chapter("justdirethings", "Just Dire Things", J + "gooblock_tier1",
        ["Living goo that rewrites the blocks it touches: new metals, denser coal, refined fuels, upgradeable tools and small automation machines."], SIDE, [
    # --- materials spine (y=0) -----------------------------------------------------------------
    Q("jdt_goo", 0, 0, [item(J + "gooblock_tier1"), item("minecraft:iron_block", 2)], "Feeding the Goo", deps=['jdt_start'], xp=30,
      subtitle="Goo converts the blocks around it", desc=[
        "&6You remember making things change just by touching them. The goo still can; you'll borrow the trick.&r",
        "&eWhat:&r goo blocks slowly convert the blocks touching them. Tier 1 (Primogel) turns iron blocks into raw ferricore ore.",
        "&eHow:&r place the goo, put iron blocks against its sides and wait. JEI's Goo Spreading tab lists every conversion, its tier and its time.",
        "&eTip:&r after a conversion the goo can die (a 10% chance in this pack's config). Right-click exhausted Primogel with sugar or rotten flesh to wake it."], mirror="05D8C6EF8FCD6250", section="The Goo", size=1.5, shape="hexagon"),
    Q("jdt_ferricore", 2, 0, [item(J + "raw_ferricore"), item(J + "ferricore_ingot")], "Raw Ferricore", deps=['jdt_goo'], xp=30,
      subtitle="Mine what the goo made", desc=[
        "&eWhat:&r raw ferricore ore drops raw ferricore. Smelt or blast it into ferricore ingots, the base of everything on this page.",
        "&eHow:&r mine the converted block with a pickaxe. Silk Touch gives you the ore block itself instead.",
        "&eTip:&r one iron block (9 ingots) becomes one raw ferricore, so let a Create or MI line feed the goo once you need a lot."], mirror="5BD5737703F3F077", section="Materials"),
    Q("jdt_blank", 4, 0, [item(J + "upgrade_blank")], "Upgrade Blanks", deps=['jdt_tools_tip', 'jdt_armor_tip', 'jdt_ferricore'], xp=30,
      subtitle="Four ferricore ingots, one empty upgrade", desc=[
        "&eWhat:&r every Just Dire Things upgrade and smithing template starts from a blank.",
        "&eHow:&r four ferricore ingots in a diamond shape (check JEI).",
        "&eTip:&r keep a stack around; most upgrades are a blank plus a few vanilla items."], mirror="7305EE0F7D73C231", section="Tool Upgrades", size=1.5, shape="hexagon"),
    Q("jdt_blazegold", 6, 0, [item(J + "gooblock_tier2")], "Blazebloom and Blazegold", deps=['jdt_goo', 't2_nether'], xp=50,
      subtitle="Tier 2 goo turns gold into blazegold", desc=[
        "&eWhat:&r Blazebloom goo (tier 2) converts gold blocks into raw blazegold ore. Blazegold opens the second tier of tools and machines.",
        "&eHow:&r tier 1 goo ringed with blaze powder, redstone and Nether wart (check JEI). Smelt the raw blazegold.",
        "&eChemistry:&r real gold is famously unreactive: it doesn't tarnish in air because Au has a very high reduction potential (+1.50 V).",
        "&eTip:&r feed exhausted Blazebloom Nether wart or blaze powder."], mirror="4C54BD57CAB8A54B", section="The Goo", size=1.5, shape="hexagon"),
    Q("jdt_celestigem", 8, 0, [item(J + "gooblock_tier3")], "VoidShimmer and Celestigem", deps=['jdt_blazegold', 'w_dragon'], xp=80,
      subtitle="Tier 3 goo turns diamond into a gem", desc=[
        "&eWhat:&r VoidShimmer goo (tier 3) turns diamond blocks into celestigem ore, which drops celestigem directly. Advanced machines and the third tool tier use it.",
        "&eHow:&r tier 2 goo ringed with ender pearls, end stone and dragon's breath (check JEI). A diamond conversion takes twice as long as iron or gold.",
        "&eChemistry:&r diamond is pure carbon: every atom bonds to four neighbours in a tetrahedral (sp³) lattice, which is why it's so hard.",
        "&eTip:&r VoidShimmer revives with chorus fruit or an ender pearl."], mirror="5C6709350BEF4050", section="The Goo", size=1.5, shape="hexagon"),
    Q("jdt_eclipse", 10, 0, [item(J + "gooblock_tier4")], "Shadowpulse and Eclipse Alloy", deps=['jdt_celestigem', 'w_ancient'], xp=120,
      size=1.5, shape="hexagon", subtitle="Tier 4 goo eats a netherite block", desc=[
        "&6The goo has learned to eat the hardest thing you own. You remember being that hungry.&r",
        "&eWhat:&r Shadowpulse goo (tier 4) turns netherite blocks into raw eclipse alloy ore, Just Dire Things' top material.",
        "&eHow:&r tier 3 goo ringed with sculk, sculk shriekers and echo shards from an Ancient City (check JEI). Smelt the raw eclipse alloy.",
        "&eTip:&r one netherite block is a big price. Plan which eclipse alloy item you want first; Shadowpulse revives with sculk or a sculk catalyst."], mirror="25213DBA6E6CEDD2", section="The Goo"),

    # --- coal tiers (y=-2) ---------------------------------------------------------------------
    Q("jdt_coal_t1", 2, -2, [item(J + "coal_t1")], "Primal Coal", deps=['jdt_goo'], xp=30,
      subtitle="Goo squeezes a coal block denser", desc=[
        "&eWhat:&r tier 1 goo turns a coal block (or a charcoal block) into Primal Coal ore. Primal Coal burns for 4,800 ticks, three times a piece of coal.",
        "&eChemistry:&r real coal ranks up with heat and pressure: lignite (~65% carbon) → bituminous (~80%) → anthracite (>90%). More carbon, more energy per kilogram.",
        "&eHow:&r place coal or charcoal blocks against tier 1 goo and mine the ore (it drops several pieces).",
        "&eTip:&r nine Primal Coal make a block, and that block is the input for the next tier."], mirror="4B3F20E5C7E3BCFB", section="Coal and Fuel"),
    Q("jdt_coal_t2", 6, -2, [item(J + "coal_t2")], "Blaze Ember", deps=['jdt_blazegold', 'jdt_coal_t1'], xp=40,
      subtitle="The second coal tier", desc=[
        "&eWhat:&r tier 2 goo turns a Primal Coal block into Blaze Ember ore. Blaze Ember burns 14,400 ticks: nine coal's worth.",
        "&eHow:&r craft a Primal Coal block, put it against Blazebloom goo and mine the ore for 3 to 4 embers.",
        "&eTip:&r each coal tier burns three times longer than the one before, so the climb pays off quickly."], mirror="079A415488A32076", section="Coal and Fuel"),
    Q("jdt_coal_t3", 8, -2, [item(J + "coal_t3")], "Voidflame Coal", deps=['jdt_celestigem', 'jdt_coal_t2'], xp=50,
      optional=False, tokens=None, subtitle="Optional: the third coal tier", desc=[
        "&eWhat:&r tier 3 goo turns a Blaze Ember block into Voidflame Coal ore: 43,200 ticks of burn per piece.",
        "&eHow:&r a block of Blaze Ember against VoidShimmer goo (check JEI for counts).",
        "&eTip:&r Voidflame Coal is also the catalyst for the tier 3 fluid fuel."], mirror="446A37C7FCDACF84", section="Coal and Fuel"),
    Q("jdt_coal_t4", 10, -2, [item(J + "coal_t4")], "Eclipse Ember", deps=['jdt_eclipse', 'jdt_coal_t3'], xp=70,
      optional=False, tokens=None, subtitle="Optional: 81 coal in one lump", desc=[
        "&eWhat:&r tier 4 goo turns a Voidflame Coal block into Eclipse Ember ore. One ember burns 129,600 ticks, as long as 81 pieces of coal.",
        "&eHow:&r a block of Voidflame Coal against Shadowpulse goo.",
        "&eChemistry:&r burning carbon, C + O₂ → CO₂, gives about 394 kJ per mole. Denser fuel just packs more carbon into the same slot."], mirror="09D2137B4F42006E", section="Coal and Fuel"),
    Q("jdt_charcoal", 0, -2, [item(J + "charcoal", 4)], "Charcoal Blocks", deps=["jdt_goo"], xp=20,
      optional=True, tokens=1, subtitle="Optional: a renewable way into Primal Coal", desc=[
        "&eWhat:&r Just Dire Things adds a charcoal block (nine charcoal). It burns for 16,000 ticks and tier 1 goo accepts it like a coal block.",
        "&eChemistry:&r charcoal is wood heated without air (pyrolysis): water and volatiles leave, mostly carbon stays.",
        "&eTip:&r a tree farm plus a furnace array makes the coal ladder fully renewable."]),

    # --- power and fuels (y=-4) ----------------------------------------------------------------
    Q("jdt_generator", 2, -4, [item(J + "generatort1")], "Simple Coal Generator", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40,
      subtitle="Burn the coal tiers for FE", desc=[
        "&eWhat:&r burns solid fuel for Forge Energy: up to 1,000 FE/t into a 1,000,000 FE buffer.",
        "&eHow:&r ferricore, redstone, coal and a blast furnace (check JEI).",
        "&eTip:&r it burns fuel four times faster than a furnace, so the long-burning coal tiers are what make it worth having."], mirror="70AD088336748892", section="Simple Machines"),
    Q("jdt_fuel_canister", 0, -4, [item(J + "fuel_canister")], "Fuel Canister", deps=['jdt_util_tip', 'jdt_ferricore'], xp=20,
      optional=False, tokens=None, subtitle="Optional: fuel in one slot", desc=[
        "&eWhat:&r a canister that soaks up furnace fuel and stores it as burn time. Its tooltip shows how much it holds.",
        "&eHow:&r ferricore around a piece of coal (check JEI).",
        "&eTip:&r pair it with the Pocket Generator from the Tools page so your FE tools recharge on long trips."], mirror="242F74010488F261", section="Gadgets"),
    Q("jdt_polymorphic", 6, -4, [item(J + "polymorphic_fluid_bucket")], "Polymorphic Fluid", deps=['jdt_fluid_tip'], xp=40,
      subtitle="Drop a catalyst into water", desc=[
        "&eWhat:&r Polymorphic Fluid is the base for every Just Dire Things fluid: fuels, portal fluid and time fluid.",
        "&eHow:&r blazegold + Nether wart makes four catalysts. Throw one into a water source block and it becomes Polymorphic Fluid. Bucket it up.",
        "&eChemistry:&r a real catalyst speeds a reaction and comes out unchanged. This one is used up, so chemists would call it a reagent.",
        "&eTip:&r JEI shows these 'fluid drop' recipes; each catalyst converts one source block."], mirror="4458F8829800A950", section="Fluids"),
    Q("jdt_fuel_t2", 8, -4, [item(J + "refined_t2_fluid_bucket")], "Blaze Ember Fuel", deps=['jdt_polymorphic', 'jdt_coal_t2'], xp=50,
      subtitle="Unrefined, then refined by goo", desc=[
        "&eWhat:&r liquid fuel for the Simple Fuel Generator. It comes from Polymorphic Fluid in two steps.",
        "&eHow:&r drop a Blaze Ember into a Polymorphic Fluid source to get Unrefined Blaze Ember Fuel, then let tier 2 goo touch that source to refine it.",
        "&eChemistry:&r real refineries separate crude oil by boiling point in a fractionating column; here the goo does the cleanup.",
        "&eTip:&r tier 3 and 4 fuels follow the same pattern: drop the next coal into the refined fuel below it, then refine with the next goo."], mirror="3D9964CB0440DD5A", section="Fluids"),
    Q("jdt_fluid_gen", 10, -4, [item(J + "generatorfluidt1")], "Simple Fuel Generator", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=60,
      subtitle="Liquid fuel, more FE", desc=[
        "&eWhat:&r burns refined fuel for up to 5,000 FE/t. Blaze Ember Fuel gives 450 FE per mB, Voidflame 1,300 and Eclipse Ember 4,000.",
        "&eHow:&r blazegold, redstone, buckets and a blast furnace (check JEI). Pipe or bucket refined fuel in.",
        "&eTip:&r one bucket of Eclipse Ember Fuel is 4,000,000 FE, nearly the generator's whole 5,000,000 FE buffer."], mirror="4A5937F6E5D06BE1", section="Simple Machines"),
    Q("jdt_fuel_high", 12, -4, [item(J + "refined_t3_fluid_bucket")], "Voidflame Fuel", deps=['jdt_fuel_t2', 'jdt_coal_t3'], xp=80,
      optional=False, tokens=None, subtitle="Optional: the two top refined fuels", desc=[
        "&eWhat:&r the tier 3 and tier 4 liquid fuels, roughly 3x and 9x the energy of Blaze Ember Fuel per mB.",
        "&eHow:&r Voidflame Coal into refined Blaze Ember Fuel, then VoidShimmer goo; Eclipse Ember into refined Voidflame Fuel, then Shadowpulse goo.",
        "&eTip:&r one bucket of each. The refined fuel is consumed by the next step, so keep a source block of each tier going."], mirror="70BF85E2D235BAD5", section="Fluids"),
    Q("jdt_transmitter", 12, -2, [item(J + "energytransmitter")], "Energy Transmitter", deps=['jdt_blazegold_raw', 'jdt_t2_tip'], xp=50,
      optional=False, tokens=None, subtitle="Optional: power without cables", desc=[
        "&eWhat:&r Energy Transmitters move FE without cables, up to 1,000 FE/t, losing a little for every block of distance (check the GUI).",
        "&eHow:&r celestigem, redstone, an ender pearl and blazegold (check JEI).",
        "&eChemistry:&r real power lines lose energy as heat, P = I²R, which is why grids use high voltage and low current."], mirror="6F709652A2B88C78", section="Advanced Machines"),

    # --- time crystals (y=-6) ------------------------------------------------------------------
    Q("jdt_time_crystal", 10, -6, [item(J + "time_crystal")], "Time Crystals", deps=['jdt_eclipse'], xp=100,
      optional=False, tokens=None, subtitle="Optional: Shadowpulse goo on budding amethyst", desc=[
        "&eWhat:&r tier 4 goo turns budding amethyst into a Budding Time Crystal block, which grows time crystal clusters.",
        "&eHow:&r budding amethyst can't be moved, so take Shadowpulse goo to a geode and place it touching a budding block. The budding block has to mature in stages first; check JEI and its tooltip for what it needs.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured purple by iron (Fe³⁺) impurities and natural radiation.",
        "&eTip:&r a Time Crystal Block converts back into a budding block, so one success is enough."], mirror="6ADE6F9E004055F7", section="Time"),
    Q("jdt_time_wand", 8, -6, [item(J + "time_wand")], "The Time Wand", deps=['jdt_util_tip', 'jdt_time_crystal', 'jdt_blazegold_raw', 'jdt_ferricore', 'jdt_time_fluid'], xp=80,
      optional=False, tokens=None, subtitle="Optional: speed up time on a block", desc=[
        "&eWhat:&r the Time Wand makes a block tick faster (up to 256x), paid for in FE and Time Fluid.",
        "&eHow:&r Time Fluid: drop a time crystal into a Polymorphic Fluid source. The wand is blazegold, ferricore and a time crystal (check JEI).",
        "&eTip:&r try it on a slow crop, a furnace or a budding block."], mirror="76B1C5AFC5D6B7CF", section="Gadgets"),
    Q("jdt_paradox", 12, -6, [item(J + "paradoxmachine")], "Paradox Machine", deps=['jdt_time_crystal', 'jdt_eclipse_ingot', 'jdt_time_fluid', 'jdt_t2_tip'], xp=150,
      optional=False, tokens=None, subtitle="Optional: undo what happened to an area", desc=[
        "&eWhat:&r the Paradox Machine reverts blocks and entities in an area to an earlier state, paying FE and Time Fluid per block or entity.",
        "&eHow:&r eclipse alloy, time crystals, a time crystal block and a bucket of Time Fluid (check JEI).",
        "&eTip:&r it's powerful and expensive. Read its GUI before you aim it at your base."], mirror="41E8C93A44559E48", section="Advanced Machines"),

    # --- tools (y=2) ---------------------------------------------------------------------------
    Q("jdt_tools_t1", 2, 2, [item(J + "ferricore_pickaxe")], "Ferricore Pickaxe", deps=['jdt_tools_tip', 'jdt_ferricore'], xp=40,
      subtitle="Tools that take upgrades", desc=[
        "&eWhat:&r Just Dire Things tools work like iron ones but accept ability upgrades. Each tier can hold more abilities and break more blocks at once.",
        "&eHow:&r the usual tool shapes with ferricore ingots and sticks.",
        "&eTip:&r vein-style abilities are capped per tier: 64 blocks for ferricore, 128 blazegold, 192 celestigem, 256 eclipse alloy."], mirror="5BBE8B30ED7518B8", section="Tools"),
    Q("jdt_oreminer", 4, 2, [item(J + "upgrade_oreminer")], "Ore Miner", deps=['jdt_tool_tag'], xp=40,
      subtitle="Your first ability: mine the whole vein", desc=[
        "&eWhat:&r Ore Miner harvests every connected ore when you break one.",
        "&eHow:&r a blank between two iron pickaxes, then combine the upgrade with your pickaxe in a smithing table (no template needed).",
        "&eTip:&r every ability goes on the same way. JEI shows which tools accept which upgrade."], mirror="2A01CE9206DD4F8A", section="Tool Upgrades"),
    Q("jdt_tools_t2", 6, 2, [item(J + "blazegold_pickaxe")], "Blazegold Pickaxe", deps=['jdt_tools_tip', 'jdt_blazegold_raw'], xp=50,
      subtitle="Smith ferricore tools up a tier", desc=[
        "&eWhat:&r tools climb tiers in the smithing table: template + old tool + new ingot.",
        "&eHow:&r a blazegold template is a blank ringed with blazegold. Smith it with a ferricore pickaxe and a blazegold ingot.",
        "&eTip:&r a template plus two ingots crafts two templates, so never spend your last one."], mirror="199388A311FAC14C", section="Tools"),
    Q("jdt_tools_t3", 8, 2, [item(J + "celestigem_pickaxe")], "Celestigem Pickaxe", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=80,
      subtitle="Pickaxe, axe and shovel in one", desc=[
        "&eWhat:&r from celestigem up you can fuse a pickaxe, axe and shovel of the same tier into a paxel.",
        "&eHow:&r smith the blazegold tools up with a celestigem template, then put pickaxe, axe and shovel together in the smithing table (check JEI).",
        "&eTip:&r one paxel instead of three tools frees two hotbar slots."], mirror="6FD4C60B547F4131", section="Tools"),
    Q("jdt_tools_t4", 10, 2, [item(J + "eclipsealloy_paxel")], "Eclipse Alloy Paxel", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=120,
      optional=False, tokens=None, subtitle="Optional: the last tool tier", desc=[
        "&eWhat:&r the top paxel. Eclipse alloy tools take the strongest abilities, such as Instant Break and Ore X-Ray.",
        "&eHow:&r smith celestigem tools with an eclipse alloy template, then fuse the three (check JEI).",
        "&eTip:&r Instant Break needs a Nether Star, a netherite pickaxe and time crystals."], mirror="6A4D31194C4CE156", section="Tools"),
    Q("jdt_bows", 4, 3.5, [item(J + "bow_ferricore")], "Ferricore Bow", deps=['jdt_tools_tip', 'jdt_ferricore'], xp=30,
      optional=False, tokens=None, subtitle="Optional: bows with abilities", desc=[
        "&eWhat:&r Just Dire Things bows tier up like the tools and take arrow abilities: Potion Arrow, Splash, Lingering, Homing and more.",
        "&eHow:&r a ferricore bow first (check JEI); smith it up with templates.",
        "&eTip:&r Potion Arrow uses a Potion Canister (ferricore around a glass bottle) instead of tipped arrows."], mirror="5A9436B100FC1E67", section="Tools"),

    # --- upgrades, armour and flight (y=4..5.5) ------------------------------------------------
    Q("jdt_upgrades", 6, 4, [item(J + "upgrade_hammer")],
      "Hammer", deps=['jdt_tool_tag'], xp=50, optional=False, tokens=None, subtitle="Mine a square, not a block", desc=[
        "&eWhat:&r Hammer (3x3 up to 7x7 by tier), Treefeller, Smelter (auto-smelts drops), Ore Scanner, Lawnmower, Leafbreaker, Skysweeper and Drops Teleport.",
        "&eHow:&r each is a blank plus vanilla parts, e.g. Hammer = blank + two diamond pickaxes, Smelter = blank + blast furnace + blaze rods (check JEI).",
        "&eChemistry:&r smelting ore is reduction: carbon pulls the oxygen off the metal, e.g. Fe₂O₃ + 3CO → 2Fe + 3CO₂.",
        "&eTip:&r not every tier takes every upgrade; JEI's smithing recipes show the allowed pairs."], mirror="6690AEE064DC2A7C", section="Tool Upgrades"),
    Q("jdt_armor", 2, 5.5, [item(J + "ferricore_helmet")],
      "Ferricore Helmet", deps=['jdt_armor_tip', 'jdt_ferricore'], xp=40, optional=False, tokens=None, subtitle="Optional: armour that takes upgrades", desc=[
        "&eWhat:&r Just Dire Things armour takes upgrades too: Step Assist and Jump Boost on boots, Walk and Run Speed on leggings, Mind Fog on helmets.",
        "&eHow:&r the usual armour shapes in ferricore. Smith them up with templates later.",
        "&eTip:&r higher tiers add Night Vision, Water Breathing, Negate Fall Damage and Lava Immunity."], mirror="24BA4B4EED0A9DBD", section="Armour"),
    Q("jdt_elytra", 8, 5.5, [item(J + "upgrade_elytra")], "Elytra Upgrade", deps=['jdt_armor_tag'], xp=80,
      optional=False, tokens=None, subtitle="Optional: an elytra inside your chestplate", desc=[
        "&eWhat:&r the Elytra upgrade builds an elytra into a celestigem or eclipse alloy chestplate, so you keep armour and glide.",
        "&eHow:&r a blank plus an elytra (from an End City), then smith it onto the chestplate.",
        "&eTip:&r it's gliding, not flight. True flight is the next step."], mirror="3A471716A29F5172", section="Armour Upgrades"),
    Q("jdt_flight", 10, 4, [item(J + "upgrade_flight")], "Flight", deps=['jdt_armor_tag', 'jdt_eclipse'], xp=250,
      size=1.0, shape=None, subtitle="Creative-style flight, the hard way", desc=[
        "&6You remember the sky. The goo had to eat netherite before it would give it back.&r",
        "&eWhat:&r the Flight upgrade gives creative-style flight. It only fits the Eclipse Alloy Chestplate, so it needs tier 4 goo and a netherite block.",
        "&eHow:&r a blank with phantom membranes, feathers and two End Crystals (check JEI), smithed onto an eclipse alloy chestplate.",
        "&eTip:&r this pack keeps the End Crystal recipe on purpose: JDT flight is a late reward, after the End and an Ancient City."], mirror="515C0527226BA50C", section="Armour Upgrades"),
    Q("jdt_chest_more", 12, 5.5, [item(J + "upgrade_invulnerability")],
      "Invulnerability", deps=['jdt_armor_tag'], xp=80, optional=False, tokens=None, subtitle="Optional: two more chestplate abilities", desc=[
        "&eWhat:&r Invulnerability (a few seconds on demand), Lava Immunity, Extinguish, Death Protection (once every 5 minutes), Time Protection and Phase (walk through walls, on leggings).",
        "&eHow:&r check JEI for each; Death Protection takes a Totem of Undying and time crystals.",
        "&eTip:&r activated abilities sit on keybinds; look for Just Dire Things in Controls."], mirror="0C2EC56133D3CC6C", section="Armour Upgrades"),

    # --- machines (y=6..8) ---------------------------------------------------------------------
    Q("jdt_breaker", 4, 7, [item(J + "blockbreakert1")], "Simple Block Breaker", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40,
      subtitle="The first automation pair", desc=[
        "&eWhat:&r the Simple Block Breaker mines the block in front of it; the Simple Block Placer puts blocks down. Together they automate a goo farm.",
        "&eHow:&r ferricore, a diamond, lapis, redstone and an observer (breaker) or dispenser (placer). Check JEI.",
        "&eTip:&r a placer feeding iron blocks to the goo and a breaker harvesting the ore makes ferricore hands-free."], mirror="7D1D2A4E07E98709", section="Simple Machines"),
    Q("jdt_clicker", 6, 7, [item(J + "clickert1")], "Simple Clicker", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40,
      subtitle="Fake clicks and redstone eyes", desc=[
        "&eWhat:&r the Simple Clicker right- or left-clicks like a player; the Simple Sensor emits a redstone signal when it sees a chosen block or mob.",
        "&eHow:&r both use ferricore, lapis, redstone and an eye of ender (clicker: dispenser core, sensor: observer core).",
        "&eTip:&r a sensor watching for the converted ore can tell the breaker exactly when to fire."], mirror="6737CB17D562B134", section="Simple Machines"),
    Q("jdt_fluid_machines", 2, 8.5, [item(J + "fluidcollectort1")], "Simple Fluid Collector", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=30,
      optional=False, tokens=None, subtitle="Optional: pick up and place fluid sources", desc=[
        "&eWhat:&r the fluid versions of the breaker and placer: collect source blocks into a tank, or set them down.",
        "&eHow:&r ferricore, lapis, redstone and a bucket around a dispenser or dropper (check JEI).",
        "&eTip:&r a placer and a collector around goo automate the refined fuel line."], mirror="1B173E7533E1171F", section="Simple Machines"),
    Q("jdt_item_collector", 0, 7, [item(J + "itemcollector")], "Item Collector", deps=['jdt_ferricore', 'jdt_t2_tip'], xp=30,
      optional=False, tokens=None, subtitle="Optional: vacuum up drops", desc=[
        "&eWhat:&r the Item Collector pulls dropped items from an area into an attached inventory; the Simple Dropper drops items out like a configurable dropper.",
        "&eHow:&r Item Collector: ferricore, a hopper, a diamond and an ender pearl. Dropper: ferricore, lapis, redstone and a dropper.",
        "&eTip:&r the Machine Settings Copier (Primal Coal, paper, ferricore) copies one machine's setup to another."], mirror="3C8C80345D3F5FE8", section="Advanced Machines"),
    Q("jdt_machines_t2", 8, 7, [item(J + "blockbreakert2")], "Advanced Block Breaker", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=60,
      subtitle="Any two tier 2 machines", optional=False, tokens=None, desc=[
        "&eWhat:&r the Advanced versions do the same jobs with more range and settings (check each GUI).",
        "&eHow:&r the Simple machine in the centre, ringed with celestigem, eyes of ender and redstone (check JEI).",
        "&eTip:&r one Advanced Breaker can harvest a whole wall of goo conversions."], mirror="16772C399861783D", section="Advanced Machines"),
    Q("jdt_swapper", 10, 7, [item(J + "blockswappert1")], "The Swapper", deps=['jdt_t1_tip', 'jdt_blazegold_raw'], xp=50,
      optional=False, tokens=None, subtitle="Optional: trade two blocks' places", desc=[
        "&eWhat:&r Swappers exchange the blocks (and optionally entities) between two linked spots. The Advanced Swapper uses eclipse alloy.",
        "&eHow:&r blazegold, lapis, redstone, an eye of ender and an observer (check JEI).",
        "&eTip:&r swap freshly converted ore out and a new iron block in, without breaking anything."], mirror="0B9BBE2A764631BF", section="Simple Machines"),
    Q("jdt_player_stuff", 8, 8.5, [anyof([J + "playeraccessor", J + "inventory_holder", J + "experienceholder"], 2)], "Blazegold Utilities", deps=["jdt_blazegold"], xp=40,
      optional=True, tokens=1, subtitle="Optional: any two blazegold blocks", desc=[
        "&eWhat:&r the Player Accessor lets pipes reach a bound player's inventory; the Inventory Holder stores and swaps a loadout; the Experience Holder banks XP.",
        "&eHow:&r all three are blazegold plus vanilla parts (armour stand, books, emerald, ender pearls; check JEI).",
        "&eTip:&r the Experience Holder is the tidy place to keep levels between anvil and enchanting sessions."]),

    # --- wands and oddities (y=10) -------------------------------------------------------------
    Q("jdt_blazejet", 4, 10, [item(J + "blazejet_wand")], "Blazejet Wand", deps=['jdt_blazegold_raw', 'jdt_tools_tip'], xp=40,
      optional=False, tokens=None, subtitle="Optional: launch yourself", desc=[
        "&eWhat:&r Air Burst: the wand launches you in the direction you're looking.",
        "&eHow:&r a blazegold ingot over two ferricore ingots (check JEI).",
        "&eTip:&r it's the base of the Voidshift Wand, so don't throw it away."], mirror="5D4E51471F3939E0", section="Tools"),
    Q("jdt_voidshift", 6, 10, [item(J + "voidshift_wand")], "Voidshift Wand", deps=['jdt_celestigem_gem', 'jdt_tools_tip'], xp=60,
      optional=False, tokens=None, subtitle="Optional: the next mobility wand", desc=[
        "&eWhat:&r the Blazejet Wand upgraded with celestigem. It adds Void Shift (read its tooltip for the details).",
        "&eHow:&r celestigem, the Blazejet Wand and blazegold in a column.",
        "&eTip:&r it upgrades again into the Eclipsegate Wand."], mirror="5B910F1389C0B915", section="Tools"),
    Q("jdt_eclipsegate", 8, 10, [item(J + "eclipsegate_wand")], "Eclipsegate Wand", deps=['jdt_eclipse_ingot', 'jdt_tools_tip'], xp=100,
      optional=False, tokens=None, subtitle="Optional: a portable hole", desc=[
        "&eWhat:&r Eclipse Gate temporarily removes the blocks you click, then puts them back.",
        "&eHow:&r eclipse alloy, the Voidshift Wand and celestigem in a column.",
        "&eTip:&r perfect for stepping through your own base walls without breaking them."], mirror="5B02719C13B1FFE2", section="Tools"),
    Q("jdt_polywand", 10, 10, [item(J + "polymorphic_wand")], "Polymorphic Wand", deps=["jdt_polymorphic"], xp=50,
      optional=True, tokens=1, subtitle="Optional: turn one mob into another", desc=[
        "&eWhat:&r the wand polymorphs a mob into a random one (or, on the Advanced wand, a chosen target), using Polymorphic Fluid.",
        "&eHow:&r a fluid canister, a polymorphic catalyst and blazegold in a column. Fill it with Polymorphic Fluid.",
        "&eTip:&r the Advanced Polymorphic Wand adds eclipse alloy and celestigem and also costs FE."]),
    Q("jdt_catcher", 2, 10, [item(J + "creaturecatcher")], "Creature Catcher", deps=['jdt_util_tip', 'jdt_blazegold_raw'], xp=40,
      optional=False, tokens=None, subtitle="Optional: two handy blazegold items", desc=[
        "&eWhat:&r the Creature Catcher captures a mob to carry and release elsewhere; the Totem of Death Recall is for getting back to where you died (read its tooltip).",
        "&eHow:&r both are blazegold and ender pearls (the totem adds diamonds and lapis). Check JEI.",
        "&eTip:&r it won't take the Ender Dragon, sadly."], mirror="53F9E5CE7EE6F852", section="Gadgets"),
    Q("jdt_portal_v2", 12, 10, [item(J + "portalgun_v2")], "Advanced Portal Gun", deps=['jdt_util_tip', 'jdt_celestigem_gem'], xp=100,
      optional=False, tokens=None, subtitle="Optional: the Advanced Portal Gun", desc=[
        "&eWhat:&r Portal Fluid powers the Advanced Portal Gun, the upgrade of the Portal Gun on the Tools page.",
        "&eHow:&r a Portal Fluid Catalyst (chorus fruit and lapis) dropped into Polymorphic Fluid makes Unstable Portal Fluid; tier 3 goo stabilises it. The gun adds celestigem and a fluid canister (check JEI).",
        "&eTip:&r the Advanced Portal Gun holds 1,000,000 FE; the basic one only 100,000."], mirror="4F9932477EDDCB8E", section="Gadgets"),

    # --- ATM10-alignment round (2026-10-19) ----------------------------------------------------
    # Metals and tool kits by tier
    Q("jdt_ferricore_ingot", 0, 0, [item(J + "template_ferricore")], "Ferricore Template",
      subtitle="The goo's first metal, and its template", deps=['jdt_armor_tag', 'jdt_ferricore'], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r ferricore ingots, plus the Ferricore template that smiths ordinary iron gear up into ferricore.",
        "&eChemistry:&r 'ferri-' means iron (Latin ferrum, symbol Fe). The goo has rearranged the iron into something new; real iron would need an alloying element to change this much.",
        "&eHow:&r smelt raw ferricore. The template is a blank ringed with ferricore ingots (check JEI).",
        "&eTip:&r a template plus ingots crafts a copy of itself, so you only make the first one by hand."], mirror="49636B3C6E6D0C2A", section="Armour Upgrades"),
    Q("jdt_ferricore_kit", 0, 0, [item(J + "ferricore_sword")], "Ferricore Sword",
      subtitle="The rest of the ferricore set", deps=['jdt_tools_tip', 'jdt_ferricore'], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r the ferricore sword and hoe take abilities like the other tools. The Ferricore Wrench rotates blocks and Just Dire Things machines.",
        "&eHow:&r the usual tool shapes; the wrench is four ferricore ingots (check JEI).",
        "&eTip:&r the hoe can take tilling and harvesting abilities at higher tiers; JEI lists which."], mirror="2F86FB9E4D49E4B0", section="Tools"),
    Q("jdt_blazegold_kit", 0, 0, [item(J + "blazegold_sword")],
      "Blazegold Sword", subtitle="Every blazegold tool", deps=['jdt_tools_tip', 'jdt_blazegold_raw'], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r blazegold versions of every tool. Each tier holds more abilities and reaches further with them.",
        "&eHow:&r smith ferricore tools with a blazegold template and a blazegold ingot (check JEI).",
        "&eTip:&r upgrade the tools you actually use first; the hoe can wait."], mirror="46E6B1600AA8A61E", section="Tools"),
    Q("jdt_blazegold_armor", 0, 0, [item(J + "blazegold_helmet")],
      "Blazegold Helmet", subtitle="Armour with more upgrade slots", deps=['jdt_armor_tip', 'jdt_blazegold_raw'], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r the second armour tier. More abilities fit, and some only unlock here.",
        "&eHow:&r smith each ferricore piece with a blazegold template and ingot (check JEI).",
        "&eChemistry:&r gold reflects infrared well, which is why astronaut visors are gold-coated. Blazegold is the goo's version."], mirror="03ED9B0DFE8B4574", section="Armour"),
    Q("jdt_celestigem_kit", 0, 0, [item(J + "celestigem_sword")],
      "Celestigem Sword", subtitle="Every celestigem tool", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=70, optional=False, tokens=None, desc=[
        "&eWhat:&r the third tier of every tool, with its template.",
        "&eHow:&r the template is a blank ringed with celestigem; smith each blazegold tool with it and a celestigem (check JEI).",
        "&eTip:&r axe, shovel and pickaxe of one tier fuse into the paxel."], mirror="4E03AE15BEF86178", section="Tools"),
    Q("jdt_celestigem_armor", 0, 0, [item(J + "celestigem_helmet")],
      "Celestigem Helmet", subtitle="Helmet, leggings and boots", deps=['jdt_armor_tip', 'jdt_celestigem_gem'], xp=80, optional=False, tokens=None, desc=[
        "&eWhat:&r the rest of the celestigem set (the chestplate has its own quest with the elytra).",
        "&eHow:&r smith each blazegold piece with a celestigem template and a celestigem (check JEI).",
        "&eChemistry:&r a celestigem forms from diamond, and diamond is pure carbon in a tetrahedral lattice; the hardest natural material known."], mirror="71441DFA05FD73E5", section="Armour"),
    Q("jdt_eclipse_kit", 0, 0, [item(J + "eclipsealloy_sword")],
      "Eclipse Alloy Sword", subtitle="Challenge: every eclipse alloy tool", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=150, optional=False, tokens=None, desc=[
        "&eWhat:&r the last tier of every tool. Each one starts from a netherite block fed to tier 4 goo, so this is a real investment.",
        "&eHow:&r smelt raw eclipse alloy; the template is a blank ringed with it. Smith each celestigem tool up (check JEI).",
        "&eTip:&r the sword takes the strongest combat abilities; check JEI before you spend the alloy."], mirror="37B903620493A354", section="Tools"),
    Q("jdt_eclipse_armor", 0, 0, [item(J + "eclipsealloy_helmet")],
      "Eclipse Alloy Helmet", subtitle="Challenge: finish the set", deps=['jdt_armor_tip', 'jdt_eclipse_ingot'], xp=150, optional=False, tokens=None, desc=[
        "&6Helmet, legs, boots: the last pieces fall into place. You remember being hard to hurt.&r",
        "&eWhat:&r helmet, leggings and boots in eclipse alloy, matching the chestplate from the Flight quest. The best Just Dire Things armour.",
        "&eHow:&r smith each celestigem piece with an eclipse alloy template and ingot (check JEI)."], mirror="0A02DBE226C3F44E", section="Armour"),
    Q("jdt_bow_set", 0, 0, [item(J + "bow_eclipsealloy")],
      "Eclipse Alloy Bow", subtitle="Four tiers of bow", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=120, optional=False, tokens=None, desc=[
        "&eWhat:&r one bow of each tier. Higher tiers draw faster and hold more arrow abilities.",
        "&eHow:&r smith each bow up with the next template (check JEI). Keep one of each, or craft spares on the way up."], mirror="71128E508D810DDF", section="Tools"),

    # Abilities
    Q("jdt_arrow_abilities", 0, 0, [item(J + "upgrade_potionarrow")],
      "Potion Arrow", subtitle="Any two bow upgrades", deps=['jdt_tool_tag'], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r Potion Arrow (fires a potion from a canister), Splash and Lingering (change how that potion spreads), Homing, and Yondu Arrow (arrows that pass through several targets).",
        "&eChemistry:&r splash and lingering potions are the same mixture delivered as a spray or a cloud; real aerosols work the same way, spreading a dose over more surface.",
        "&eHow:&r each is a blank plus vanilla items; Yondu Arrow also needs a Nether Star (check JEI)."], mirror="05056CAA64E3971B", section="Tool Upgrades"),
    Q("jdt_move_abilities", 0, 0, [item(J + "upgrade_runspeed")],
      "Run Speed", subtitle="Any two movement abilities", deps=['jdt_armor_tag'], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r Step Assist, Jump Boost, Walk Speed, Run Speed, Swim Speed, Negate Fall Damage and Ground Stomp (push mobs away).",
        "&eHow:&r a blank plus vanilla items, e.g. Step Assist is a blank ringed with ladders (check JEI). Smith onto boots or leggings.",
        "&eTip:&r none of these is flight. In this pack JDT flight is a late reward on eclipse alloy."], mirror="3B3E3D81843BB358", section="Armour Upgrades"),
    Q("jdt_sense_abilities", 0, 0, [item(J + "upgrade_mobscanner")],
      "Mob Scanner", subtitle="Any two helmet or senses abilities", deps=['jdt_tool_tag'], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r Night Vision, Mob X-Ray (see mobs through walls), Mob Scanner, Ore X-Ray, Mind Fog (mobs notice you less) and Water Breathing.",
        "&eChemistry:&r Night Vision's recipe uses golden carrots: carrots really are rich in beta-carotene, which the body turns into vitamin A for the eye's light-sensing pigment.",
        "&eHow:&r a blank plus vanilla items each (check JEI); Ore X-Ray needs a high tier."], mirror="17C4F6EC1AFBC3AA", section="Tool Upgrades"),
    Q("jdt_combat_abilities", 0, 0, [item(J + "upgrade_cauterizewounds")],
      "Cauterize Wounds", subtitle="Any two combat abilities", deps=['jdt_tool_tag'], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r Cauterize Wounds (heal), Debuff Remover, Decoy (mobs attack a dummy), Earthquake (slows nearby mobs), Stupefy (a mob forgets you) and Mental Obliteration (nearby mobs stop for good).",
        "&eHow:&r a blank plus vanilla items each, e.g. Earthquake uses soul sand, sticky pistons and fermented spider eyes (check JEI).",
        "&eTip:&r activated abilities have keybinds; find them under Just Dire Things in Controls."], mirror="2875FACD3BFB0A8E", section="Tool Upgrades"),
    Q("jdt_smoker", 0, 0, [item(J + "upgrade_smoker")], "Cooked on the Spot",
      subtitle="Mob drops come out cooked", deps=['jdt_tool_tag'], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r the Smoker ability auto-smelts mob drops: raw meat drops as cooked meat.",
        "&eChemistry:&r cooking meat is chemistry: proteins denature, and the Maillard reaction between amino acids and sugars makes the brown crust and the flavour.",
        "&eHow:&r a blank, a smoker and blaze rods (check JEI). Smith it onto a weapon."], mirror="61213012615619C5", section="Tool Upgrades"),
    Q("jdt_instabreak", 0, 0, [item(J + "upgrade_instabreak")], "Instant Break",
      subtitle="Challenge: every block breaks at once", deps=['jdt_tool_tag'], xp=150, optional=False, tokens=None, desc=[
        "&eWhat:&r the strongest tool ability: blocks break instantly.",
        "&eHow:&r a blank, two Nether Stars, two netherite pickaxes and four time crystals (check JEI). Only top-tier tools take it.",
        "&eTip:&r combine it with a hammer ability and a 5x5 hole is one click."], mirror="45D683D7F1A32B04", section="Tool Upgrades"),

    # Machines and utilities
    Q("jdt_workshop", 0, 0, [item(J + "blockswappert2")],
      "Advanced Swapper", subtitle="Swap blocks at a distance", deps=['jdt_t2_tip', 'jdt_eclipse_ingot'], xp=200, optional=False, tokens=None, desc=[
        "&eWhat:&r all eight advanced machines: breaker, placer, clicker, sensor, dropper, fluid collector, fluid placer and swapper.",
        "&eHow:&r each wraps its Simple version in celestigem and more; the Advanced Swapper needs eclipse alloy (check JEI).",
        "&eTip:&r together they can run a whole goo farm, from feeding iron blocks to collecting the ore."], mirror="4C40699E0A9A5BE6", section="Advanced Machines"),
    Q("jdt_xp_bank", 0, 0, [item(J + "experienceholder"), item(J + "xp_fluid_bucket")], "Liquid Experience",
      subtitle="Bank your levels as a fluid", deps=["jdt_player_stuff"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r the Experience Holder stores your levels, and holds them as XP Fluid you can pipe or bucket out.",
        "&eHow:&r blazegold, a book, an ender pearl and an emerald (check JEI). Use its GUI to deposit or withdraw levels.",
        "&eTip:&r the fluid lets one XP store feed anvils, enchanters and other XP machines."]),
    Q("jdt_player_accessor", 0, 0, [item(J + "playeraccessor")], "Player Accessor",
      subtitle="Pipes into your own inventory", deps=['jdt_blazegold_raw', 'jdt_t2_tip'], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r a block bound to you that pipes can push into or pull out of, as if it were your inventory.",
        "&eHow:&r blazegold, eyes of ender, ender pearls, a dispenser and lapis (check JEI), then bind it to yourself (its tooltip shows how).",
        "&eTip:&r pipe arrows or fuel straight into your inventory from base while you're out."], mirror="02B0CCD5607FF3B5", section="Advanced Machines"),
    Q("jdt_canisters", 0, 0, [item(J + "fluid_canister")], "Fluid Canister",
      subtitle="Carry a fluid, copy a setup", deps=['jdt_util_tip', 'jdt_ferricore'], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r the Fluid Canister holds a fluid for wands and guns; the Machine Settings Copier copies one machine's settings onto another.",
        "&eHow:&r canister: ferricore around glass. Copier: Primal Coal, paper and ferricore (check JEI).",
        "&eTip:&r set up one breaker perfectly, then copy it down a whole row."], mirror="200ECDC70E97D254", section="Gadgets"),
    Q("jdt_portal_catalyst", 0, 0, [item(J + "portal_fluid_catalyst", 2)], "Portal Fluid Catalyst",
      subtitle="Chorus fruit and lapis", deps=["jdt_polymorphic", "w_end"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r the catalyst that turns Polymorphic Fluid into Unstable Portal Fluid, the first step to the Advanced Portal Gun's fuel.",
        "&eHow:&r chorus fruit around lapis (check JEI). Drop one into a Polymorphic Fluid source block.",
        "&eTip:&r chorus fruit grows on the outer End islands. Bring some back and plant it."]),

    # --- ATM10 mirror round (2026-10-20): one quest per ATM10 Just Dire Things quest ------------------------------
    Q("jdt_start", 0, 0, [tick()], "The Living Goo", subtitle="Blocks that change the blocks around them", deps=['gs_iron'], xp=10, mirror="7F0B2D58361FB00E", section="The Goo", icon=J + "gooblock_tier1", desc=[
        "&6Matter that rewrites matter. You remember being able to do this with a thought.&r",
        "&eWhat:&r Just Dire Things is built on goo: four tiers of living blocks that slowly convert what touches them into new materials.",
        "&eHow:&r every conversion is in JEI under Goo Spreading. Each tier of goo opens a new metal, a new coal and a new tier of tools.",
        "&eTip:&r click to begin."]),
    Q("jdt_blazegold_raw", 0, 0, [item(J + "raw_blazegold"), item(J + "blazegold_ingot")], "Blazegold", subtitle="Gold, changed by the goo", deps=['jdt_blazegold'], xp=40, mirror="2D86D4403E0F4EB9", section="Materials", desc=[
        "&eWhat:&r tier 2 goo turns gold blocks into raw blazegold ore. Smelt it into blazegold ingots.",
        "&eChemistry:&r gold barely reacts with anything; it's the goo, not chemistry, that changes it.",
        "&eHow:&r gold blocks against Blazebloom goo; mine the result."]),
    Q("jdt_celestigem_gem", 0, 0, [item(J + "celestigem")], "Celestigem", subtitle="A gem from tier 3 goo", deps=['jdt_celestigem'], xp=40, mirror="60A4994078500F63", section="Materials", desc=[
        "&eWhat:&r tier 3 goo grows celestigem: the material for the third tier of tools, armour and machines.",
        "&eHow:&r check JEI's Goo Spreading tab for what tier 3 goo converts."]),
    Q("jdt_eclipse_ingot", 0, 0, [item(J + "raw_eclipsealloy"), item(J + "eclipsealloy_ingot")], "Eclipse Alloy", subtitle="The top goo metal", deps=['jdt_eclipse'], xp=40, mirror="1705175C20CE91DD", section="Materials", desc=[
        "&eWhat:&r tier 4 goo makes raw eclipse alloy; smelt it into ingots for the best tools, armour and flight.",
        "&eHow:&r check JEI's Goo Spreading tab for tier 4 (it needs a netherite block)."]),
    Q("jdt_t1_tip", 0, 0, [tick()], "Simple Machines", subtitle="Small automation, ferricore tier", deps=['jdt_ferricore'], xp=10, mirror="517F0135926B15EE", section="Simple Machines", icon=J + "blockbreakert1", desc=[
        "&eWhat:&r Just Dire Things machines are small blocks that each do one job: break, place, click, sense, drop, collect.",
        "&eHow:&r each Simple machine is ferricore with a few vanilla parts (check JEI). They run on redstone or on their own timers.",
        "&eTip:&r a breaker facing a goo block harvests the conversion for you."]),
    Q("jdt_placer", 0, 0, [item(J + "blockplacert1")], "Simple Block Placer", subtitle="Puts a block back", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40, mirror="70C404E5685E4E91", section="Simple Machines", desc=[
        "&eWhat:&r places the blocks in its inventory in front of it.",
        "&eHow:&r ferricore and a dispenser (check JEI).",
        "&eTip:&r pair it with a breaker to feed goo automatically."]),
    Q("jdt_sensor", 0, 0, [item(J + "sensort1")], "Simple Sensor", subtitle="Redstone when something is there", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40, mirror="19E678E6EF9539DC", section="Simple Machines", desc=[
        "&eWhat:&r gives a redstone signal when it sees a chosen block or entity in front of it.",
        "&eHow:&r ferricore and an observer (check JEI).",
        "&eTip:&r it can tell a breaker when a goo conversion has finished."]),
    Q("jdt_dropper", 0, 0, [item(J + "droppert1")], "Simple Dropper", subtitle="Drops items on a timer", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40, mirror="1ECFA72CF2BA4B45", section="Simple Machines", desc=[
        "&eWhat:&r drops items from its inventory in front of it.",
        "&eHow:&r ferricore and a dropper (check JEI)."]),
    Q("jdt_fluid_placer", 0, 0, [item(J + "fluidplacert1")], "Simple Fluid Placer", subtitle="Puts a fluid block down", deps=['jdt_t1_tip', 'jdt_ferricore'], xp=40, mirror="433117EEA55B6A54", section="Simple Machines", desc=[
        "&eWhat:&r places a source block of the fluid inside it.",
        "&eHow:&r ferricore and a bucket (check JEI).",
        "&eTip:&r useful for polymorphic fluid crafting."]),
    Q("jdt_t2_tip", 0, 0, [tick()], "Advanced Machines", subtitle="Celestigem-tier automation", deps=['jdt_blazegold'], xp=10, mirror="5F5120451BA5B2FE", section="Advanced Machines", icon=J + "blockbreakert2", desc=[
        "&eWhat:&r Advanced machines do the same jobs with more range, filters and settings.",
        "&eHow:&r the Simple machine in the centre, ringed with celestigem and more (check JEI)."]),
    Q("jdt_placer_t2", 0, 0, [item(J + "blockplacert2")], "Advanced Block Placer", subtitle="The tier 2 version", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=40, mirror="5D182815CB167405", section="Advanced Machines", desc=[
        "&eWhat:&r places blocks over a larger area.",
        "&eHow:&r the Simple version ringed with celestigem (check JEI)."]),
    Q("jdt_clicker_t2", 0, 0, [item(J + "clickert2")], "Advanced Clicker", subtitle="The tier 2 version", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=40, mirror="0D32774710EC9900", section="Advanced Machines", desc=[
        "&eWhat:&r right- or left-clicks with an item, with more settings.",
        "&eHow:&r the Simple version ringed with celestigem (check JEI)."]),
    Q("jdt_sensor_t2", 0, 0, [item(J + "sensort2")], "Advanced Sensor", subtitle="The tier 2 version", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=40, mirror="55E882E7FA36AFC6", section="Advanced Machines", desc=[
        "&eWhat:&r watches a larger area with filters.",
        "&eHow:&r the Simple version ringed with celestigem (check JEI)."]),
    Q("jdt_dropper_t2", 0, 0, [item(J + "droppert2")], "Advanced Dropper", subtitle="The tier 2 version", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=40, mirror="15AD6698663D4A42", section="Advanced Machines", desc=[
        "&eWhat:&r drops items with more control.",
        "&eHow:&r the Simple version ringed with celestigem (check JEI)."]),
    Q("jdt_fluid_placer_t2", 0, 0, [item(J + "fluidplacert2")], "Advanced Fluid Placer", subtitle="The tier 2 version", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=40, mirror="6D60602560F35F87", section="Advanced Machines", desc=[
        "&eWhat:&r places fluid over a larger area.",
        "&eHow:&r the Simple version ringed with celestigem (check JEI)."]),
    Q("jdt_fluid_collector_t2", 0, 0, [item(J + "fluidcollectort2")], "Advanced Fluid Collector", subtitle="The tier 2 version", deps=['jdt_t2_tip', 'jdt_celestigem_gem'], xp=40, mirror="4D45C0CFF11191ED", section="Advanced Machines", desc=[
        "&eWhat:&r picks up fluid over a larger area.",
        "&eHow:&r the Simple version ringed with celestigem (check JEI)."]),
    Q("jdt_tools_tip", 0, 0, [tick()], "Dire Tools", subtitle="Four metals, every tool", deps=['jdt_ferricore'], xp=10, mirror="7AEFF81E7C8CF300", section="Tools", icon=J + "ferricore_pickaxe", desc=[
        "&eWhat:&r each goo metal makes a full set: sword, pickaxe, axe, shovel, hoe and bow, plus paxels at the top tiers.",
        "&eHow:&r craft the ferricore set, then move each tool up a tier at the smithing table with a template and the next metal.",
        "&eTip:&r Dire tools run on FE or fuel and take ability upgrades."]),
    Q("jdt_fc_axe", 0, 0, [item(J + "ferricore_axe")], "Ferricore Axe", subtitle="The ferricore axe", deps=['jdt_tools_tip', 'jdt_ferricore'], xp=30, mirror="5054977BD5354561", section="Tools", desc=[
        "&eWhat:&r the ferricore axe.",
        "&eHow:&r ferricore ingots in the usual tool shape (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_fc_shovel", 0, 0, [item(J + "ferricore_shovel")], "Ferricore Shovel", subtitle="The ferricore shovel", deps=['jdt_tools_tip', 'jdt_ferricore'], xp=30, mirror="19E6757F04098A0C", section="Tools", desc=[
        "&eWhat:&r the ferricore shovel.",
        "&eHow:&r ferricore ingots in the usual tool shape (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_fc_hoe", 0, 0, [item(J + "ferricore_hoe")], "Ferricore Hoe", subtitle="The ferricore hoe", deps=['jdt_tools_tip', 'jdt_ferricore'], xp=30, mirror="4773421DC70009AB", section="Tools", desc=[
        "&eWhat:&r the ferricore hoe.",
        "&eHow:&r ferricore ingots in the usual tool shape (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_bg_axe", 0, 0, [item(J + "blazegold_axe")], "Blazegold Axe", subtitle="The blazegold axe", deps=['jdt_tools_tip', 'jdt_blazegold_raw'], xp=30, mirror="21147C8CBF98AEB4", section="Tools", desc=[
        "&eWhat:&r the blazegold axe.",
        "&eHow:&r smith the tier below with a blazegold template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_bg_shovel", 0, 0, [item(J + "blazegold_shovel")], "Blazegold Shovel", subtitle="The blazegold shovel", deps=['jdt_tools_tip', 'jdt_blazegold_raw'], xp=30, mirror="1DAA5DD81EF96469", section="Tools", desc=[
        "&eWhat:&r the blazegold shovel.",
        "&eHow:&r smith the tier below with a blazegold template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_bg_hoe", 0, 0, [item(J + "blazegold_hoe")], "Blazegold Hoe", subtitle="The blazegold hoe", deps=['jdt_tools_tip', 'jdt_blazegold_raw'], xp=30, mirror="52EC86E03EB50525", section="Tools", desc=[
        "&eWhat:&r the blazegold hoe.",
        "&eHow:&r smith the tier below with a blazegold template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_cg_axe", 0, 0, [item(J + "celestigem_axe")], "Celestigem Axe", subtitle="The celestigem axe", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=30, mirror="2B1BAEC5DAAF9DAC", section="Tools", desc=[
        "&eWhat:&r the celestigem axe.",
        "&eHow:&r smith the tier below with a celestigem template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_cg_shovel", 0, 0, [item(J + "celestigem_shovel")], "Celestigem Shovel", subtitle="The celestigem shovel", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=30, mirror="0C1D55AA9CC902BD", section="Tools", desc=[
        "&eWhat:&r the celestigem shovel.",
        "&eHow:&r smith the tier below with a celestigem template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_cg_hoe", 0, 0, [item(J + "celestigem_hoe")], "Celestigem Hoe", subtitle="The celestigem hoe", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=30, mirror="237D11FF5B09BA88", section="Tools", desc=[
        "&eWhat:&r the celestigem hoe.",
        "&eHow:&r smith the tier below with a celestigem template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_cg_paxel", 0, 0, [item(J + "celestigem_paxel")], "Celestigem Paxel", subtitle="The celestigem paxel", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=30, mirror="0272E58516A0C284", section="Tools", desc=[
        "&eWhat:&r the celestigem paxel. A paxel is a pickaxe, axe and shovel in one.",
        "&eHow:&r smith the tier below with a celestigem template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_ec_pickaxe", 0, 0, [item(J + "eclipsealloy_pickaxe")], "Eclipse Alloy Pickaxe", subtitle="The eclipse alloy pickaxe", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=30, mirror="0C9DD8E53A1B92C0", section="Tools", desc=[
        "&eWhat:&r the eclipse alloy pickaxe.",
        "&eHow:&r smith the tier below with a eclipse alloy template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_ec_axe", 0, 0, [item(J + "eclipsealloy_axe")], "Eclipse Alloy Axe", subtitle="The eclipse alloy axe", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=30, mirror="78840993C7832E89", section="Tools", desc=[
        "&eWhat:&r the eclipse alloy axe.",
        "&eHow:&r smith the tier below with a eclipse alloy template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_ec_shovel", 0, 0, [item(J + "eclipsealloy_shovel")], "Eclipse Alloy Shovel", subtitle="The eclipse alloy shovel", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=30, mirror="703BDCDC88DD813C", section="Tools", desc=[
        "&eWhat:&r the eclipse alloy shovel.",
        "&eHow:&r smith the tier below with a eclipse alloy template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_ec_hoe", 0, 0, [item(J + "eclipsealloy_hoe")], "Eclipse Alloy Hoe", subtitle="The eclipse alloy hoe", deps=['jdt_tools_tip', 'jdt_eclipse_ingot'], xp=30, mirror="3138B83ABC2930F9", section="Tools", desc=[
        "&eWhat:&r the eclipse alloy hoe.",
        "&eHow:&r smith the tier below with a eclipse alloy template and ingot (check JEI).",
        "&eTip:&r ability upgrades go on at the smithing table."]),
    Q("jdt_bow_bg", 0, 0, [item(J + "bow_blazegold")], "Blazegold Bow", subtitle="A Dire bow, one tier up", deps=['jdt_tools_tip', 'jdt_blazegold_raw'], xp=30, mirror="567005978482235F", section="Tools", desc=[
        "&eWhat:&r a stronger Dire bow that takes arrow abilities.",
        "&eHow:&r smith the bow below with a template and ingot (check JEI)."]),
    Q("jdt_bow_cg", 0, 0, [item(J + "bow_celestigem")], "Celestigem Bow", subtitle="A Dire bow, one tier up", deps=['jdt_tools_tip', 'jdt_celestigem_gem'], xp=30, mirror="35A78E04092767AD", section="Tools", desc=[
        "&eWhat:&r a stronger Dire bow that takes arrow abilities.",
        "&eHow:&r smith the bow below with a template and ingot (check JEI)."]),
    Q("jdt_armor_tip", 0, 0, [tick()], "Dire Armour", subtitle="Four metals, four pieces each", deps=['jdt_ferricore'], xp=10, mirror="3971FF7D044D1FE5", section="Armour", icon=J + "ferricore_helmet", desc=[
        "&eWhat:&r each goo metal makes an armour set; higher tiers hold more abilities.",
        "&eHow:&r craft ferricore armour, then smith it up tier by tier.",
        "&eTip:&r flight only goes on the eclipse alloy chestplate."]),
    Q("jdt_fc_chestplate", 0, 0, [item(J + "ferricore_chestplate")], "Ferricore Chestplate", subtitle="Ferricore armour", deps=['jdt_armor_tip', 'jdt_ferricore'], xp=30, mirror="7464CA1290B3474B", section="Armour", desc=[
        "&eWhat:&r the ferricore chestplate.",
        "&eHow:&r ferricore ingots in the usual armour shape (check JEI)."]),
    Q("jdt_fc_leggings", 0, 0, [item(J + "ferricore_leggings")], "Ferricore Leggings", subtitle="Ferricore armour", deps=['jdt_armor_tip', 'jdt_ferricore'], xp=30, mirror="04A1D582003A0D9A", section="Armour", desc=[
        "&eWhat:&r the ferricore leggings.",
        "&eHow:&r ferricore ingots in the usual armour shape (check JEI)."]),
    Q("jdt_fc_boots", 0, 0, [item(J + "ferricore_boots")], "Ferricore Boots", subtitle="Ferricore armour", deps=['jdt_armor_tip', 'jdt_ferricore'], xp=30, mirror="454CA1F8CC198D9D", section="Armour", desc=[
        "&eWhat:&r the ferricore boots.",
        "&eHow:&r ferricore ingots in the usual armour shape (check JEI)."]),
    Q("jdt_bg_chestplate", 0, 0, [item(J + "blazegold_chestplate")], "Blazegold Chestplate", subtitle="Blazegold armour", deps=['jdt_armor_tip', 'jdt_blazegold_raw'], xp=30, mirror="1CBA0D7DA0558EBC", section="Armour", desc=[
        "&eWhat:&r the blazegold chestplate.",
        "&eHow:&r smith the piece below with a blazegold template and ingot (check JEI)."]),
    Q("jdt_bg_leggings", 0, 0, [item(J + "blazegold_leggings")], "Blazegold Leggings", subtitle="Blazegold armour", deps=['jdt_armor_tip', 'jdt_blazegold_raw'], xp=30, mirror="5A38E9F68570F7F3", section="Armour", desc=[
        "&eWhat:&r the blazegold leggings.",
        "&eHow:&r smith the piece below with a blazegold template and ingot (check JEI)."]),
    Q("jdt_bg_boots", 0, 0, [item(J + "blazegold_boots")], "Blazegold Boots", subtitle="Blazegold armour", deps=['jdt_armor_tip', 'jdt_blazegold_raw'], xp=30, mirror="176A1CC43467EF23", section="Armour", desc=[
        "&eWhat:&r the blazegold boots.",
        "&eHow:&r smith the piece below with a blazegold template and ingot (check JEI)."]),
    Q("jdt_cg_chestplate", 0, 0, [item(J + "celestigem_chestplate")], "Celestigem Chestplate", subtitle="Celestigem armour", deps=['jdt_armor_tip', 'jdt_celestigem_gem'], xp=30, mirror="4B1E4FC4599DB916", section="Armour", desc=[
        "&eWhat:&r the celestigem chestplate.",
        "&eHow:&r smith the piece below with a celestigem template and ingot (check JEI)."]),
    Q("jdt_cg_leggings", 0, 0, [item(J + "celestigem_leggings")], "Celestigem Leggings", subtitle="Celestigem armour", deps=['jdt_armor_tip', 'jdt_celestigem_gem'], xp=30, mirror="3BF32843DE3CF3C2", section="Armour", desc=[
        "&eWhat:&r the celestigem leggings.",
        "&eHow:&r smith the piece below with a celestigem template and ingot (check JEI)."]),
    Q("jdt_cg_boots", 0, 0, [item(J + "celestigem_boots")], "Celestigem Boots", subtitle="Celestigem armour", deps=['jdt_armor_tip', 'jdt_celestigem_gem'], xp=30, mirror="1FE7C52491E7499B", section="Armour", desc=[
        "&eWhat:&r the celestigem boots.",
        "&eHow:&r smith the piece below with a celestigem template and ingot (check JEI)."]),
    Q("jdt_ec_chestplate", 0, 0, [item(J + "eclipsealloy_chestplate")], "Eclipse Alloy Chestplate", subtitle="Eclipse Alloy armour", deps=['jdt_armor_tip', 'jdt_eclipse_ingot'], xp=30, mirror="5A1AB1AD7DEFDD9A", section="Armour", desc=[
        "&eWhat:&r the eclipse alloy chestplate.",
        "&eHow:&r smith the piece below with a eclipse alloy template and ingot (check JEI)."]),
    Q("jdt_ec_leggings", 0, 0, [item(J + "eclipsealloy_leggings")], "Eclipse Alloy Leggings", subtitle="Eclipse Alloy armour", deps=['jdt_armor_tip', 'jdt_eclipse_ingot'], xp=30, mirror="2A919F73CB09CF8B", section="Armour", desc=[
        "&eWhat:&r the eclipse alloy leggings.",
        "&eHow:&r smith the piece below with a eclipse alloy template and ingot (check JEI)."]),
    Q("jdt_ec_boots", 0, 0, [item(J + "eclipsealloy_boots")], "Eclipse Alloy Boots", subtitle="Eclipse Alloy armour", deps=['jdt_armor_tip', 'jdt_eclipse_ingot'], xp=30, mirror="1FFA1DA6A5EA4E70", section="Armour", desc=[
        "&eWhat:&r the eclipse alloy boots.",
        "&eHow:&r smith the piece below with a eclipse alloy template and ingot (check JEI)."]),
    Q("jdt_util_tip", 0, 0, [tick()], "Dire Gadgets", subtitle="Wands, guns and odd tools", deps=['jdt_ferricore'], xp=10, mirror="6AB45CC4CE4570E6", section="Gadgets", icon=J + "fluid_canister", desc=[
        "&eWhat:&r the rest of Just Dire Things: canisters, a pocket generator, portal guns, a mob catcher and more.",
        "&eHow:&r most are ferricore or blazegold with vanilla parts (check JEI)."]),
    Q("jdt_pocket_gen", 0, 0, [item(J + "pocket_generator")], "Pocket Generator", subtitle="Burn coal, charge your tools", deps=['jdt_util_tip', 'jdt_ferricore'], xp=40, mirror="40C5C355B6DA1893", section="Gadgets", desc=[
        "&eWhat:&r burns fuel in your inventory to charge your FE items.",
        "&eHow:&r ferricore and a furnace (check JEI)."]),
    Q("jdt_copier", 0, 0, [item(J + "machinesettingscopier")], "Machine Settings Copier", subtitle="Set one up, copy the rest", deps=['jdt_util_tip', 'jdt_ferricore'], xp=40, mirror="0B485DB737A036E9", section="Gadgets", desc=[
        "&eWhat:&r copies one machine's settings onto another.",
        "&eHow:&r Primal Coal, paper and ferricore (check JEI).",
        "&eTip:&r set up one breaker perfectly, then copy it down a whole row."]),
    Q("jdt_wrench", 0, 0, [item(J + "ferricore_wrench")], "Ferricore Wrench", subtitle="Turn and pick up machines", deps=['jdt_util_tip', 'jdt_ferricore'], xp=40, mirror="45A25221F54A1DEC", section="Gadgets", desc=[
        "&eWhat:&r rotates and picks up Just Dire Things machines.",
        "&eHow:&r ferricore ingots (check JEI)."]),
    Q("jdt_portalgun", 0, 0, [item(J + "portalgun")], "Portal Gun", subtitle="Two holes in the world", deps=['jdt_util_tip', 'jdt_blazegold_raw'], xp=40, mirror="16E02F671FBE9148", section="Gadgets", desc=[
        "&eWhat:&r fires two linked portals you can walk through.",
        "&eHow:&r blazegold, ender pearls and a fluid canister (check JEI)."]),
    Q("jdt_totem", 0, 0, [item(J + "totem_of_death_recall")], "Totem of Death Recall", subtitle="Back to where you fell", deps=['jdt_util_tip', 'jdt_blazegold_raw'], xp=40, mirror="27FD46A8C958D259", section="Gadgets", desc=[
        "&eWhat:&r helps you get back to where you died. Read its tooltip.",
        "&eHow:&r blazegold, ender pearls, diamonds and lapis (check JEI)."]),
    Q("jdt_fluid_tip", 0, 0, [tick()], "Dire Fluids", subtitle="Polymorphic fluid and refined fuels", deps=['jdt_blazegold'], xp=10, mirror="66F79F0F1E05D163", section="Fluids", icon=J + "polymorphic_fluid_bucket", desc=[
        "&eWhat:&r Polymorphic Fluid takes on the nature of what you drop in it: refined fuels, portal fluid, time fluid.",
        "&eHow:&r every fluid recipe is in JEI (search the fluid's bucket)."]),
    Q("jdt_fuel_t4", 0, 0, [item(J + "refined_t4_fluid_bucket")], "Eclipse Fuel", subtitle="The best Dire fuel", deps=['jdt_fuel_high', 'jdt_coal_t4'], xp=40, mirror="49EF8A4346AEF582", section="Fluids", desc=[
        "&eWhat:&r the top refined fuel for the Simple Fuel Generator.",
        "&eHow:&r Eclipse Ember in Polymorphic Fluid (check JEI).",
        "&eChemistry:&r a denser fuel stores more energy per litre, the way diesel beats ethanol."]),
    Q("jdt_portal_fluid", 0, 0, [item(J + "portal_fluid_bucket")], "Portal Fluid", subtitle="Fuel for the advanced portal gun", deps=['jdt_polymorphic'], xp=40, mirror="0FAF274ADA65B26A", section="Fluids", desc=[
        "&eWhat:&r Portal Fluid powers the Advanced Portal Gun.",
        "&eHow:&r a Portal Fluid Catalyst in Polymorphic Fluid makes unstable portal fluid; tier 3 goo stabilises it (check JEI)."]),
    Q("jdt_time_fluid", 0, 0, [item(J + "time_fluid_bucket")], "Time Fluid", subtitle="Liquid time", deps=['jdt_time_crystal', 'jdt_polymorphic'], xp=40, mirror="48E4D75FD3145AD6", section="Time", desc=[
        "&eWhat:&r Time Fluid powers the Time Wand and the Paradox Machine.",
        "&eHow:&r drop a time crystal into a Polymorphic Fluid source."]),
    Q("jdt_tool_tag", 0, 0, [anytag("c:tools")], "A Tool to Upgrade", subtitle="Any tool counts", deps=['jdt_blank'], xp=10, mirror="4E9B35DCA018FD42", section="Tool Upgrades", desc=[
        "&eWhat:&r tool abilities go on Dire tools at the smithing table: tool, upgrade, and nothing else.",
        "&eHow:&r hold any tool to complete this; the Dire tools are the ones that take upgrades."]),
    Q("jdt_armor_tag", 0, 0, [anytag("c:armors")], "Armour to Upgrade", subtitle="Any armour counts", deps=['jdt_blank'], xp=10, mirror="67B87570C340C243", section="Armour Upgrades", desc=[
        "&eWhat:&r armour abilities go on Dire armour the same way: piece, upgrade, smithing table.",
        "&eHow:&r hold any armour piece to complete this."]),
    Q("jdt_upg_tip", 0, 0, [tick()], "Using Abilities", subtitle="Keybinds and costs", deps=['jdt_tool_tag', 'jdt_armor_tag'], xp=10, mirror="73552A4BA0687962", section="Tool Upgrades", icon=J + "upgrade_blank", desc=[
        "&eWhat:&r passive abilities just work; active ones sit on keybinds (Controls, Just Dire Things).",
        "&eTip:&r most abilities cost FE or fuel per use. Keep a Pocket Generator on you."]),
    Q("jdt_lawnmower", 0, 0, [item(J + "upgrade_lawnmower")], "Lawnmower", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="07655CA904354E9E", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability cuts grass and flowers around you.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_skysweeper", 0, 0, [item(J + "upgrade_skysweeper")], "Skysweeper", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="46EE2F9818F8D1D9", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability is a clearing ability for tools; read its tooltip for what it sweeps.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_treefeller", 0, 0, [item(J + "upgrade_treefeller")], "Treefeller", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="4D98D2123BD5BFB3", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability fells a whole tree from one log.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_leafbreaker", 0, 0, [item(J + "upgrade_leafbreaker")], "Leafbreaker", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="0E3FDD8BB6D17A30", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability breaks the connected leaves of a tree.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_smelter", 0, 0, [item(J + "upgrade_smelter")], "Smelter", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="171DB70D0D19A942", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability smelts what you mine as it drops.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_dropteleport", 0, 0, [item(J + "upgrade_dropteleport")], "Drop Teleport", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="636854555AD75DC3", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability sends your drops to a bound inventory.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_orexray", 0, 0, [item(J + "upgrade_orexray")], "Ore X-Ray", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="18032636A60D0B2C", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability shows nearby ores through stone.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_glowing", 0, 0, [item(J + "upgrade_glowing")], "Mob X-Ray", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="283D7E65F2AD45F2", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability outlines mobs through walls.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_orescanner", 0, 0, [item(J + "upgrade_orescanner")], "Ore Scanner", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="5EE7D5DE07A83C7D", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability scans for ore around you.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_splash", 0, 0, [item(J + "upgrade_splash")], "Splash", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="3CFD798362605880", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability makes potion arrows burst like splash potions.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_lingering", 0, 0, [item(J + "upgrade_lingering")], "Lingering", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="6720F863B907A5F1", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability makes potion arrows leave a lingering cloud.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_homing", 0, 0, [item(J + "upgrade_homing")], "Homing", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="3F3559EF5D08B706", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability steers arrows towards their target.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_epicarrow", 0, 0, [item(J + "upgrade_epicarrow")], "Yondu Arrow", subtitle="An ability upgrade", deps=['jdt_tool_tag'], xp=30, mirror="1256F280F3669DDA", section="Tool Upgrades", desc=[
        "&eWhat:&r this ability makes arrows pass through several targets.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_walkspeed", 0, 0, [item(J + "upgrade_walkspeed")], "Walk Speed", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="132F4671E121C7B8", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability makes you walk faster.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_stepheight", 0, 0, [item(J + "upgrade_stepheight")], "Step Assist", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="17A9D2CA160561D9", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability lets you walk up full blocks.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_jumpboost", 0, 0, [item(J + "upgrade_jumpboost")], "Jump Boost", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="0CBFE2CE53DCACD5", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability makes you jump higher.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_mindfog", 0, 0, [item(J + "upgrade_mindfog")], "Mind Fog", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="3CBB78C9B8D3665E", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability makes mobs notice you less.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_swimspeed", 0, 0, [item(J + "upgrade_swimspeed")], "Swim Speed", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="4ACB72F3A23A5A19", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability makes you swim faster.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_groundstomp", 0, 0, [item(J + "upgrade_groundstomp")], "Ground Stomp", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="6889EFC6CC291463", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability pushes nearby mobs away.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_extinguish", 0, 0, [item(J + "upgrade_extinguish")], "Extinguish", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="3AE1811C32B94A66", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability puts you out when you catch fire.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_stupefy", 0, 0, [item(J + "upgrade_stupefy")], "Stupefy", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="09485B63483B7A15", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability makes a mob forget you.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_negatefall", 0, 0, [item(J + "upgrade_negatefalldamage")], "Negate Fall Damage", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="02B8F50721F12CFF", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability stops fall damage.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_nightvision", 0, 0, [item(J + "upgrade_nightvision")], "Night Vision", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="120DCA89A919C7AF", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability lets you see in the dark.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_decoy", 0, 0, [item(J + "upgrade_decoy")], "Decoy", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="5961C1ED32522BEF", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability makes mobs attack a dummy instead of you.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_earthquake", 0, 0, [item(J + "upgrade_earthquake")], "Earthquake", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="1E0C6409B2573CCA", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability slows the mobs around you.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_noai", 0, 0, [item(J + "upgrade_noai")], "Mental Obliteration", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="7B9486981786AC47", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability stops nearby mobs for good.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_lavaimmunity", 0, 0, [item(J + "upgrade_lavaimmunity")], "Lava Immunity", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="6D9CFCD81A23BB3B", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability lets you swim in lava.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_deathprotection", 0, 0, [item(J + "upgrade_deathprotection")], "Death Protection", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="79BBCC1BEE90DBBB", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability saves you from death once every few minutes.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_debuffremover", 0, 0, [item(J + "upgrade_debuffremover")], "Debuff Remover", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="026C63594F813BCC", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability clears bad potion effects.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_time_protection", 0, 0, [item(J + "upgrade_time_protection")], "Time Protection", subtitle="An ability upgrade", deps=['jdt_armor_tag'], xp=30, mirror="4987759CF379C1EB", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability shields you from time effects.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_phase", 0, 0, [item(J + "upgrade_phase")], "Phase", subtitle="An ability upgrade", deps=['jdt_upg_tip'], xp=30, mirror="454662617304E299", section="Armour Upgrades", desc=[
        "&eWhat:&r this ability lets you walk through walls.",
        "&eHow:&r an upgrade blank plus vanilla items (check JEI). Smith it onto a Dire tool or armour piece that takes it."]),
    Q("jdt_tpl_bg", 0, 0, [item(J + "template_blazegold")], "Blazegold Template", subtitle="Smith gear up a tier", deps=['jdt_armor_tag', 'jdt_blazegold_raw'], xp=30, mirror="2409EAD96CE3BDF7", section="Armour Upgrades", desc=[
        "&eWhat:&r the smithing template that moves Dire gear up to blazegold.",
        "&eHow:&r an upgrade blank ringed with blazegold (check JEI).",
        "&eTip:&r a template plus two ingots crafts two templates, so never spend your last one."]),
    Q("jdt_tpl_cg", 0, 0, [item(J + "template_celestigem")], "Celestigem Template", subtitle="Smith gear up a tier", deps=['jdt_armor_tag', 'jdt_celestigem_gem'], xp=30, mirror="25E915AE1FC53254", section="Armour Upgrades", desc=[
        "&eWhat:&r the smithing template that moves Dire gear up to celestigem.",
        "&eHow:&r an upgrade blank ringed with celestigem (check JEI).",
        "&eTip:&r a template plus two ingots crafts two templates, so never spend your last one."]),
    Q("jdt_tpl_ec", 0, 0, [item(J + "template_eclipsealloy")], "Eclipse Alloy Template", subtitle="Smith gear up a tier", deps=['jdt_armor_tag', 'jdt_eclipse_ingot'], xp=30, mirror="1EA02BA24AF02256", section="Armour Upgrades", desc=[
        "&eWhat:&r the smithing template that moves Dire gear up to eclipse alloy.",
        "&eHow:&r an upgrade blank ringed with eclipse alloy (check JEI).",
        "&eTip:&r a template plus two ingots crafts two templates, so never spend your last one."]),
    Q("jdt_center_tip", 0, 0, [tick()], "Waking the Goo", subtitle="When goo stops working", deps=['jdt_goo'], xp=10, mirror="441F37A95AB66E6B", section="The Goo", optional=True, tokens=1, icon=J + "gooblock_tier1", desc=[
        "&eWhat:&r after a conversion, goo can go dormant (a 10% chance in this pack).",
        "&eHow:&r right-click dormant goo with sugar or rotten flesh to wake it, or keep a spare.",
        "&eTip:&r a Simple Clicker holding sugar keeps a goo farm running."]),
], links=[("gs_iron", -2, 0), ("tc_jdt_goo", -2, 2), ("t2_nether", -2, -2), ("w_dragon", -2, -4), ("w_ancient", -2, -6)], mirror="justdirethings")
