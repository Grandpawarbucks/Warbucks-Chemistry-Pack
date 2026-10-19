"""Quest chapter: create. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

# Layout (grid cells):
#   y=0          kinetic spine: alloy -> casing -> power -> cogs -> windmill -> belts -> press -> mixer
#                -> brass -> brass casing -> precision (x=0..22)
#   x=0..8       kinetic extras at y=-2 / y=2..4; contraptions at y=4..8
#   x=10..18     y<0: milling, copper and fluids, fans; y=2..8: depots, logistics, packages
#   x=16..20     y=2: rose quartz -> electron tube -> deployer
#   x=22..32     after precision: arm and speed control (y=-2), crushing and washing (y=2..4),
#                trains (y=5..9)
#   x>=28        electricity (y=-7..1: Crafts & Additions, New Age) and experience (y=3)
# Optional quests sit off the main lines.
CHAPTER = Chapter("create", "The Mechanical Age", "create:cogwheel",
        ["Create: rotation, presses and mixers. An early mechanical age that runs alongside steam and feeds into Modern Industrialization."], SIDE, [
    # --- Kinetic spine (y = 0) ----------------------------------------------------------------
    Q("cr_alloy", 0, 0, [item("create:andesite_alloy", 16)], "Andesite Alloy", subtitle="The frame of every early machine", deps=["gs_iron"], xp=30, desc=[
        "&6Gears and shafts. You remember a world that ran on clockwork, and you liked it.&r",
        "&eWhat:&r andesite alloy, Create's first building material.",
        "&eHow:&r craft andesite with iron nuggets (zinc nuggets work too). Later a Mechanical Mixer makes it in bulk.",
        "&eTip:&r hold &eW&r over almost any Create block to watch its Ponder tutorial."]),
    Q("cr_casing", 2, 0, [item("create:andesite_casing", 8)], "Andesite Casing", subtitle="Alloy pressed onto wood", deps=["cr_alloy"], xp=30, desc=[
        "&eWhat:&r casing blocks are the shell for gearboxes, deployers and more.",
        "&eHow:&r right-click a stripped log or stripped wood with andesite alloy. That's 'item application', and Create uses it a lot.",
        "&eTip:&r strip logs with an axe first. Any wood type works."]),
    Q("cr_power", 4, 0, [item("create:shaft", 8), item("create:cogwheel", 8), item("create:water_wheel")], "Rotational Power", subtitle="Create runs on rotation", deps=["cr_casing"], xp=40, desc=[
        "&eWhat:&r Create runs on rotation, not electricity. A water wheel on flowing water turns shafts and cogs.",
        "&eHow:&r water must flow across the wheel's blades. Shafts carry rotation straight; cogwheels pass it sideways.",
        "&eTip:&r every machine costs stress units (SU). If the network is over capacity, everything stops."]),
    Q("cr_cogs", 6, 0, [item("create:large_cogwheel", 4)], "Gear Ratios", subtitle="Big gear, small gear, double speed", deps=["cr_power"], xp=40, desc=[
        "&eWhat:&r a large cogwheel meshed with a small one doubles the speed (or halves it the other way).",
        "&eChemistry:&r physics, really: power is torque times speed. Gearing trades one for the other, and Create shows the trade as stress: a machine's SU cost grows with its speed.",
        "&eHow:&r a shaft and two planks make a large cogwheel. Place it diagonally next to a small one so the teeth mesh.",
        "&eTip:&r run slow machines (like mixers you don't need fast) at low speed to save stress."]),
    Q("cr_windmill", 8, 0, [item("create:windmill_bearing"), item("create:white_sail", 8)], "Windmills", subtitle="More stress capacity, anywhere", deps=["cr_cogs"], xp=50, desc=[
        "&eWhat:&r a windmill bearing with sails attached spins without water.",
        "&eHow:&r place the bearing, build at least 8 sails onto the front of it (the Ponder shows how), and right-click the bearing.",
        "&eTip:&r more sails means more stress capacity but slower speed. Check the numbers with your goggles."]),
    Q("cr_belts", 10, 0, [item("create:gearbox", 2), item("create:belt_connector", 4)], "Gearboxes and Belts", subtitle="Move rotation and items", deps=["cr_windmill"], xp=50, desc=[
        "&eWhat:&r gearboxes turn rotation through corners; belts carry both rotation and items between two shafts.",
        "&eHow:&r belts are made from dried kelp. Click one shaft with a belt, then the other, to link them.",
        "&eTip:&r belts make great machine feeders: items ride past presses and fans on their own."]),
    Q("cr_press", 12, 0, [item("create:mechanical_press"), item("create:basin")], "Pressing and Mixing", subtitle="Plates and compacting", deps=["cr_belts"], xp=50, desc=[
        "&eWhat:&r the Mechanical Press flattens ingots into plates and compacts items in a basin.",
        "&eHow:&r put the press over a depot, a belt or a basin, and power it.",
        "&eTip:&r plates are shared with MI in this pack, so pressed plates work in MI recipes too."]),
    Q("cr_mixer", 14, 0, [item("create:mechanical_mixer"), item("create:blaze_burner")], "Heated Mixing", subtitle="Create's chemistry bench", deps=["cr_press", "t2_blaze"], xp=75, desc=[
        "&eWhat:&r a mixer over a basin, heated by a Blaze Burner, makes alloys and fluids.",
        "&eChemistry:&r heat speeds up reactions and melts metals so they can mix into alloys.",
        "&eHow:&r catch a blaze in an Empty Blaze Burner (iron plates around netherrack), put it under the basin, feed it fuel, and put the mixer above.",
        "&eTip:&r feed the burner with a deployer or a mechanical arm so it never goes cold."]),
    Q("cr_brass", 16, 0, [item("create:zinc_ingot", 8), item("create:brass_ingot", 8)], "Brass", subtitle="Copper plus zinc, mixed hot", deps=["cr_mixer"], xp=100, size=1.5, desc=[
        "&6A golden metal, mixed in a basin. The old skill comes back to your hands.&r",
        "&eWhat:&r brass, the key metal of Create's second age.",
        "&eChemistry:&r brass is a copper-zinc alloy, usually about two-thirds copper. Zinc makes it harder and gives the gold colour.",
        "&eHow:&r 1 copper + 1 zinc in a heated mixer gives 2 brass. Zinc ore generates in the world."]),
    Q("cr_brass_casing", 18, 0, [item("create:brass_casing", 8)], "Brass Casing", subtitle="The shell of smart machines", deps=["cr_brass"], xp=60, desc=[
        "&eWhat:&r brass casing, for mechanical crafters, arms and brass tunnels.",
        "&eHow:&r right-click a stripped log or stripped wood with a brass ingot.",
        "&eTip:&r a deployer holding brass ingots can apply it automatically."]),
    Q("cr_precision", 22, 0, [item("create:precision_mechanism"), item("create:mechanical_crafter", 4)], "Precision", subtitle="Your first sequenced assembly", deps=["cr_deployer"], xp=150, size=1.5, desc=[
        "&6Each step in its place, every time. You used to build worlds this way.&r",
        "&eWhat:&r the precision mechanism, made by sequenced assembly: one item passes the same stations several times. Mechanical Crafters join into a big grid for recipes too large for a crafting table.",
        "&eHow:&r start with a gold plate, then deploy a cogwheel, a large cogwheel and an iron nugget onto it, 5 loops. JEI shows the sequence. Crafters are an electron tube, brass casing and crafting table.",
        "&eTip:&r some outputs are scrap. Sort them off the end of the belt and recycle them."]),

    # --- Kinetic extras (x = 0..8) -------------------------------------------------------------
    Q("cr_crank", 2, -2, [item("create:hand_crank")], "Hand Crank", subtitle="Optional: rotation by muscle", deps=["cr_casing"], xp=20, optional=True, tokens=1, desc=[
        "&eWhat:&r the simplest power source: you turn it yourself.",
        "&eHow:&r three planks over an andesite alloy. Hold right-click on it to spin whatever it's attached to.",
        "&eTip:&r handy for testing a contraption before you build a real generator for it."]),
    Q("cr_goggles", 4, -2, [item("create:goggles"), item("create:wrench")], "Goggles and Wrench", subtitle="See the stress", deps=["cr_power"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r Engineer's Goggles show speed and stress when you look at a machine; the wrench rotates and picks up Create blocks.",
        "&eHow:&r wear the goggles in your helmet slot and look at a shaft or generator.",
        "&eTip:&r sneak-right-click with the wrench to pick a block up instantly."]),
    Q("cr_gauges", 6, -2, [item("create:speedometer"), item("create:stressometer")], "Gauges", subtitle="Optional: dials for your network", deps=["cr_cogs"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r the Speedometer reads RPM; the Stressometer shows how much of your network's capacity is in use.",
        "&eHow:&r a compass on an andesite casing makes the speedometer (check JEI for the stressometer). Put them inline on a shaft.",
        "&eTip:&r both give a comparator signal, so a nearly full network can switch things off by redstone."]),
    Q("cr_gearshift", 6, 2, [item("create:clutch"), item("create:gearshift")], "Clutch and Gearshift", subtitle="Redstone control for rotation", deps=["cr_cogs"], xp=40, desc=[
        "&eWhat:&r a powered Clutch cuts the rotation passing through it; a powered Gearshift reverses it.",
        "&eHow:&r andesite casing + redstone, with a shaft (clutch) or a cogwheel (gearshift).",
        "&eTip:&r a gearshift on a timer makes a piston or gantry go back and forth by itself."]),
    Q("cr_chain_drive", 6, 4, [item("create:encased_chain_drive", 2)], "Chain Drives", subtitle="Optional: rotation along a chain", deps=["cr_gearshift"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r encased chain drives pass rotation between each other in a line, in any direction, like a bike chain.",
        "&eHow:&r an andesite casing and three iron nuggets. The Adjustable Chain Gearshift version changes speed with a redstone signal (check JEI).",
        "&eTip:&r a neat way to bring power up a wall without shafts sticking out."]),
    Q("cr_deco", 0, 2, [item("createdeco:brass_catwalk", 8), item("createdeco:andesite_sheet_metal", 8)], "Create Deco", subtitle="Make the factory look like one", deps=["cr_casing"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r catwalks, sheet metal, cage lamps and other industrial building blocks.",
        "&eHow:&r check JEI for Create Deco recipes. Many use a press or the stonecutter.",
        "&eTip:&r catwalks over your machine lines make maintenance much easier."]),
    Q("cr_connected", 8, 2, [item("create_connected:brass_gearbox"), item("create_connected:kinetic_bridge")], "Create: Connected", subtitle="Handy kinetic parts", deps=["cr_windmill"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r Create: Connected adds small conveniences: compact gearboxes, a kinetic bridge that carries rotation across gaps, and more.",
        "&eHow:&r check JEI for everything the mod adds.",
        "&eTip:&r the kinetic bridge saves long runs of shafts."]),
    Q("cr_battery", 8, 4, [item("create_connected:kinetic_battery")], "Kinetic Battery", deps=["cr_connected"], xp=40,
      optional=True, tokens=1, subtitle="Optional: store rotation for later", desc=[
        "&eWhat:&r the Kinetic Battery charges from rotation and gives it back later, so a windmill's power isn't wasted when nothing is running.",
        "&eHow:&r check JEI and its Ponder scene (hold W over it). Put it on a shaft line to charge it.",
        "&eTip:&r a charged battery can be picked up and moved, like a wind-up spring."]),

    # --- Contraptions (x = 0..6, y = 4..8) ------------------------------------------------------
    Q("cr_bearing", 2, 4, [item("create:mechanical_bearing")], "Mechanical Bearing", subtitle="Make blocks spin", deps=["cr_power"], xp=50, desc=[
        "&eWhat:&r a bearing turns the blocks attached to its face into a moving 'contraption': doors, rotors, fans, ferris wheels.",
        "&eHow:&r a wooden slab, an andesite casing and a shaft. Build onto its face, power it, and right-click to start.",
        "&eTip:&r moving blocks keep working: a spinning contraption can carry drills, harvesters and seats."]),
    Q("cr_clockwork", 0, 4, [item("create:clockwork_bearing")], "Clockwork Bearing", subtitle="Optional: a bearing that tells time", deps=["cr_bearing"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r the Clockwork Bearing points its contraption at the current in-game time, like the hands of a clock.",
        "&eHow:&r a wooden slab, a brass casing and an electron tube. Build an hour hand on it, and a second layer for the minute hand.",
        "&eTip:&r a giant clock tower is a classic Create build."]),
    Q("cr_glue", 2, 6, [item("create:super_glue"), item("create:linear_chassis", 4)], "Glue and Chassis", subtitle="Tell a contraption what to carry", deps=["cr_bearing"], xp=40, desc=[
        "&eWhat:&r Super Glue sticks blocks together so they move as one; chassis blocks grab whole rows and layers at once.",
        "&eHow:&r super glue is slime, an iron plate and an iron nugget; drag it across a region to glue it. Linear chassis is alloy and logs.",
        "&eTip:&r a slimeball on a chassis face makes it sticky. Check the Ponder for range settings."]),
    Q("cr_pulley", 0, 6, [item("create:rope_pulley")], "Rope Pulley", subtitle="Optional: lift things straight up", deps=["cr_glue"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r the Rope Pulley lowers and raises a contraption on a rope, which makes a simple lift.",
        "&eHow:&r an andesite casing, wool and an iron plate. Glue a platform under it and power it.",
        "&eTip:&r the brass Elevator Pulley (check JEI) adds floor buttons and stops at contacts."]),
    Q("cr_piston", 4, 6, [item("create:mechanical_piston"), item("create:piston_extension_pole", 8)], "Mechanical Piston", subtitle="Push a contraption in a line", deps=["cr_glue"], xp=50, desc=[
        "&eWhat:&r a mechanical piston pushes and pulls glued blocks along a straight line, as far as its poles reach.",
        "&eHow:&r a wooden slab, an andesite casing and an extension pole. Put poles behind the piston head; each pole adds one block of travel.",
        "&eTip:&r rotation direction decides push or pull, so a gearshift reverses it."]),
    Q("cr_drill", 6, 6, [item("create:mechanical_drill"), item("create:mechanical_harvester")], "Drills and Harvesters", subtitle="Contraptions that do the work", deps=["cr_piston"], xp=60, desc=[
        "&eWhat:&r a moving Drill breaks blocks in front of it; a Harvester picks crops and leaves the plant to regrow.",
        "&eHow:&r both use andesite casing and alloy, with iron (drill) or iron plates (harvester). Mount them on a piston, bearing or gantry.",
        "&eTip:&r a slow bearing with harvesters sweeping a round field is a cheap automatic farm."]),
    Q("cr_gantry", 4, 8, [item("create:gantry_carriage"), item("create:gantry_shaft", 8)], "Gantries", subtitle="A carriage that rides a shaft", deps=["cr_piston"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r a Gantry Carriage runs along a powered gantry shaft, carrying its contraption with it, with no length limit.",
        "&eHow:&r gantry shafts are alloy and redstone; the carriage is a slab, a casing and a cogwheel. Power the shaft and the carriage moves.",
        "&eTip:&r gantries can carry other gantries, which makes an X-Y frame for a big drill or quarry."]),
    Q("cr_cart", 2, 8, [item("create:cart_assembler", 2)], "Minecart Contraptions", subtitle="Contraptions on rails", deps=["cr_glue"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r a Cart Assembler on a rail turns a passing minecart and the blocks glued to it into a moving contraption.",
        "&eHow:&r andesite alloy, redstone and logs. Place it as a rail, build on top, then send a minecart through with the assembler powered.",
        "&eTip:&r a minecart contraption with a drill digs its own tunnel along the track."]),

    # --- Milling, copper and fluids (x = 10..16, y < 0) ----------------------------------------
    Q("cr_millstone", 10, -2, [item("create:millstone")], "Millstone", subtitle="Slow and steady grinding", deps=["cr_belts"], xp=40, desc=[
        "&eWhat:&r the Millstone grinds cobblestone to gravel, wheat to flour, flowers to dye, bones to bone meal and more.",
        "&eChemistry:&r grinding raises surface area: a powder reacts, dissolves and mixes much faster than a lump.",
        "&eHow:&r a cogwheel, an andesite casing and stone. Power it from the side or below and drop items in on top.",
        "&eTip:&r it doesn't take ores here. Ore crushing needs Crushing Wheels later."]),
    Q("cr_saw", 10, -4, [item("create:mechanical_saw")], "Mechanical Saw", subtitle="A stonecutter with a motor", deps=["cr_millstone"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r a still saw over a belt cuts logs into planks and acts as a stonecutter; on a contraption it fells whole trees.",
        "&eHow:&r iron plates, an iron ingot and an andesite casing. Set its target recipe with a filter if it has several.",
        "&eTip:&r a row of saws on a bearing makes a tree farm that never misses a log."]),
    Q("cr_copper_casing", 12, -2, [item("create:copper_casing", 8)], "Copper Casing", subtitle="The shell for fluid machines", deps=["cr_press"], xp=40, desc=[
        "&eWhat:&r copper casing is the base for spouts, item drains and hose pulleys.",
        "&eHow:&r right-click a stripped log or stripped wood with a copper ingot.",
        "&eTip:&r press a stack of copper sheets while you're at it. Pipes need them next."]),
    Q("cr_pipes", 12, -4, [item("create:fluid_pipe", 16), item("create:mechanical_pump")], "Pipes and Pumps", subtitle="Fluids go where you push them", deps=["cr_copper_casing"], xp=50, desc=[
        "&eWhat:&r fluid pipes carry liquids, but only while a Mechanical Pump pushes them along.",
        "&eChemistry:&r a pump makes a pressure difference, and fluid always flows from high pressure to low.",
        "&eHow:&r copper sheets around a copper ingot make 4 pipes; a pipe and a cogwheel make a pump. The arrow on the pump shows the flow direction.",
        "&eTip:&r reverse the pump's rotation to reverse the flow."]),
    Q("cr_hose", 10, -6, [item("create:hose_pulley")], "Hose Pulley", subtitle="Optional: drain or fill a lake", deps=["cr_pipes"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r the Hose Pulley lowers a hose into a pool and sucks the fluid up, or fills an area from your pipes.",
        "&eHow:&r a copper casing, a dried kelp block and a copper plate. Power it and pipe its output away with a pump.",
        "&eTip:&r a big enough body of water or lava counts as endless (check the Ponder), so it's a free fluid source."]),
    Q("cr_biofuel", 12, -6, [item("createaddition:seed_oil_bucket"), item("createaddition:bioethanol_bucket")], "Bioethanol", deps=["cr_pipes"], xp=75,
      optional=True, tokens=1, subtitle="Optional: fuel from fermented plants", desc=[
        "&eWhat:&r Crafts & Additions makes liquid fuel from plants: seed oil, then biomass, then bioethanol, which burns in a Liquid Blaze Burner.",
        "&eChemistry:&r real bioethanol comes from yeast fermenting sugar: C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂. Plant oils are triglycerides, long carbon chains that store a lot of energy.",
        "&eHow:&r compact seeds in a press and basin for seed oil; mix crops with seed oil over heat for biomass; mix biomass, sugar and cinder flour for bioethanol (check JEI).",
        "&eTip:&r it's a renewable fuel for Create steam engines that never touches your oil wells."]),
    Q("cr_spout", 14, -4, [item("create:spout")], "Spout", subtitle="Fill whatever passes underneath", deps=["cr_pipes"], xp=50, desc=[
        "&eWhat:&r the Spout pours fluid into items below it on a depot or belt: water bottles, buckets, honey, lava cakes and more.",
        "&eHow:&r a copper casing over dried kelp. Pipe fluid into it and put a depot underneath.",
        "&eTip:&r spouts are a station in many sequenced assembly recipes, so you'll use them again."]),
    Q("cr_drain", 14, -6, [item("create:item_drain")], "Item Drain", subtitle="Empty buckets on the way past", deps=["cr_spout"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r the Item Drain empties fluid containers that roll over it and holds the fluid for your pipes.",
        "&eHow:&r iron bars over a copper casing. Put it in a belt line and pull the fluid out with a pump.",
        "&eTip:&r it's the easy way to turn buckets from another mod into piped fluid."]),
    Q("cr_steam", 16, -6, [item("create:steam_engine", 2), item("create:fluid_tank", 4)], "Steam Engines", subtitle="Fire, water and pistons", deps=["cr_spout"], xp=150, optional=True, tokens=2, desc=[
        "&eWhat:&r Create's boiler: a fluid tank full of water, heated by Blaze Burners, drives steam engines on its sides.",
        "&eChemistry:&r water expands about 1,600 times when it boils. That pressure pushes the pistons.",
        "&eHow:&r pump water into the tank, put fuelled Blaze Burners underneath, and place engines on its sides with a shaft in front. Check the Ponder.",
        "&eTip:&r a bigger tank and more burners raise the boiler level. Goggles show what's limiting it."]),
    Q("cr_blaze_cake", 16, -4, [item("create:blaze_cake", 2)], "Blaze Cake", subtitle="Optional: superheat a burner", deps=["cr_spout"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r feeding a Blaze Cake to a burner makes it &esuperheated&r for a while, hotter than any normal fuel.",
        "&eHow:&r compact an egg, sugar and cinder flour into a cake base, then spout 250 mB of lava into it.",
        "&eTip:&r some recipes need superheat (New Age's blank circuits, for one). Check the heat icon in JEI."]),

    # --- Fans (x = 14..18, y = -2) ------------------------------------------------------------
    Q("cr_fan", 14, -2, [item("create:encased_fan", 2)], "Encased Fan", subtitle="Air that cooks, washes and haunts", deps=["cr_press"], xp=50, desc=[
        "&eWhat:&r an Encased Fan blows items along and processes them depending on what the air passes through.",
        "&eHow:&r a shaft, an andesite casing and a propeller (iron plates around alloy). Water in front washes, fire smokes, lava blasts, soul fire haunts.",
        "&eTip:&r items on a belt or depot in the air stream are processed; loose items on the ground are too."]),
    Q("cr_fan_heat", 16, -2, [item("minecraft:campfire"), item("minecraft:lava_bucket")], "Smoking and Blasting", subtitle="A furnace with no fuel slot", deps=["cr_fan"], xp=40, desc=[
        "&eWhat:&r a fan blowing through fire or a campfire cooks food (smoking); through lava it smelts like a blast furnace (blasting).",
        "&eChemistry:&r hot air carries heat by convection, which is why a fan oven cooks faster than a still one.",
        "&eHow:&r put a lit campfire or a lava source block a block or two in front of the fan and send items through the stream.",
        "&eTip:&r one lava block never runs out, so bulk blasting costs nothing but rotation."]),
    Q("cr_fan_haunt", 18, -2, [item("minecraft:soul_campfire"), item("minecraft:soul_sand", 16)], "Haunting", subtitle="Soul fire changes things", deps=["cr_fan_heat"], xp=40, desc=[
        "&eWhat:&r air blown through soul fire 'haunts' items: sand becomes soul sand, stone bricks infested, fungi swap Nether types.",
        "&eHow:&r a soul campfire or soul fire in front of a fan. Pass sand through it for soul sand. JEI lists every haunting recipe.",
        "&eTip:&r it's a renewable source of soul sand and soul soil, handy for Nether wart and soul torches."]),
    Q("cr_fan_catalyst", 18, -4, [item("create_connected:empty_fan_catalyst")], "Fan Catalysts", subtitle="Optional: processing without the mess", deps=["cr_fan_haunt"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r Create: Connected's fan catalysts hold the 'fire' or 'water' for a fan in one tidy block.",
        "&eHow:&r brass and iron bars make the empty catalyst; fill it to pick its processing type (check JEI).",
        "&eTip:&r no more flowing water flooding your belt line."]),

    # --- Depots and logistics (x = 10..20, y = 2..4) -------------------------------------------
    Q("cr_depot", 10, 2, [item("create:depot", 2)], "Depots", subtitle="A table for machines to work on", deps=["cr_belts"], xp=30, desc=[
        "&eWhat:&r a Depot holds one stack of items for a press, fan, spout or deployer to work on.",
        "&eHow:&r andesite alloy and an andesite casing. Right-click to put items on it.",
        "&eTip:&r a depot under a press is the cheapest plate maker in the game."]),
    Q("cr_funnel", 10, 4, [item("create:andesite_funnel", 4), item("create:andesite_tunnel", 2)], "Funnels and Tunnels", subtitle="Items in, items out", deps=["cr_depot"], xp=40, desc=[
        "&eWhat:&r funnels pull items out of chests and machines onto belts, or insert items from a belt; tunnels split a belt line evenly.",
        "&eHow:&r andesite alloy over dried kelp makes 2 funnels. Place them on a chest face or at the end of a belt (check JEI for tunnels).",
        "&eTip:&r a redstone signal shuts a funnel off, which is an easy on/off switch."]),
    Q("cr_ejector", 10, 6, [item("create:weighted_ejector")], "Weighted Ejector", subtitle="Optional: throw items across a gap", deps=["cr_funnel"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r the Weighted Ejector flings items (or you) to a target block in an arc.",
        "&eHow:&r a gold plate, a depot and a cogwheel. Hold it and click the target before you place it.",
        "&eTip:&r stand on it for a free launch pad. The landing is your problem."]),
    Q("cr_chute", 12, 4, [item("create:chute", 4)], "Chutes", subtitle="Let gravity do the hauling", deps=["cr_funnel"], xp=30, desc=[
        "&eWhat:&r chutes drop items straight down between machines and chests; a fan under or over one blows items upward.",
        "&eHow:&r iron plates and an iron ingot make 4 chutes.",
        "&eTip:&r a chute into a crushing wheel or basin is the simplest feeder there is."]),
    Q("cr_vault", 14, 4, [item("create:item_vault", 4)], "Item Vaults", subtitle="Storage that grows as you build", deps=["cr_chute"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r Item Vaults merge into one big storage block when placed together.",
        "&eHow:&r iron plates around a barrel. Place several side by side; funnels and pipes reach the whole vault.",
        "&eTip:&r vaults also go into frogports, so make a few extra."]),
    Q("cr_brass_logistics", 18, 4, [item("create:brass_funnel", 2), item("create:brass_tunnel", 2), item("create:smart_chute")], "Smart Logistics", subtitle="Brass parts that read filters", deps=["cr_chute"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r brass funnels, tunnels and smart chutes take a filter, so you choose exactly which items pass and how many.",
        "&eHow:&r each uses an electron tube and brass (check JEI). Put an item or a Create Filter in the slot on the block.",
        "&eTip:&r a brass tunnel set to 'synchronise' only lets items through when every lane has one: perfect for 1:1 recipes."]),

    # --- Packages (x = 14..20, y = 6..8) --------------------------------------------------------
    Q("cr_cardboard", 14, 6, [item("create:cardboard", 8)], "Cardboard", subtitle="Pulp, pressed flat", deps=["cr_mixer"], xp=40, desc=[
        "&eWhat:&r cardboard, for Create's package logistics.",
        "&eChemistry:&r paper and card are mats of cellulose fibres; water lets the fibres bond as it dries, which is why pulp holds together.",
        "&eHow:&r mix 4 pulpable items (like sticks or sugar cane; check JEI) with 250 mB of water for pulp, then press the pulp into cardboard."]),
    Q("cr_packager", 16, 6, [item("create:packager", 2)], "Packagers", subtitle="Box it up, send it off", deps=["cr_cardboard"], xp=50, desc=[
        "&eWhat:&r a Packager boxes items from the inventory behind it into a package with an address, or unpacks packages addressed to it.",
        "&eHow:&r a cardboard block, iron ingots and redstone. Put a sign or name on it for its address (see the Ponder).",
        "&eTip:&r packages ride belts, chutes and chain conveyors like any other item."]),
    Q("cr_frogport", 18, 6, [item("create:package_frogport", 2), item("create:chain_conveyor", 2)], "Frogports and Chains", subtitle="A frog that catches your mail", deps=["cr_packager"], xp=60, desc=[
        "&eWhat:&r chain conveyors carry packages through the air; a Package Frogport tongues them off the chain at the right stop.",
        "&eHow:&r a frogport is a slimeball, an item vault and andesite alloy; a chain conveyor is a large cogwheel in andesite casings. Link chains with iron chains.",
        "&eTip:&r a chain network with frogports at each base is a whole-base mail system."]),
    Q("cr_stock", 20, 6, [item("create:stock_link"), item("create:stock_ticker")], "Stock Keeping", subtitle="Order from a counter", deps=["cr_frogport"], xp=75, desc=[
        "&eWhat:&r a Stock Link reports what a packager can reach; a Stock Ticker lets you browse that stock and order items to be packed and sent.",
        "&eHow:&r a transmitter (lightning rod, copper plates, redstone) on an item vault makes the link; add glass and gold for the ticker.",
        "&eTip:&r put the ticker by your workbench and order ingredients without walking to storage."]),
    Q("cr_factory", 20, 8, [item("create:factory_gauge", 2)], "Factory Gauges", subtitle="Optional: production on demand", deps=["cr_stock"], xp=60, optional=True, tokens=2, desc=[
        "&eWhat:&r Factory Gauges watch your stock and request ingredients for a recipe whenever a target amount runs low.",
        "&eHow:&r a stock link and a precision mechanism make 2. Place them on a packager and link them in their panel (see the Ponder).",
        "&eTip:&r chain gauges together and one order can run a whole production line."]),

    # --- Rose quartz, tubes and deployers (y = 2) ------------------------------------------------
    Q("cr_rose", 16, 2, [item("create:rose_quartz", 4), item("create:polished_rose_quartz", 4)], "Rose Quartz", subtitle="Quartz soaked in redstone", deps=["cr_mixer"], xp=60, desc=[
        "&eWhat:&r rose quartz, for electron tubes.",
        "&eHow:&r craft 1 Nether quartz with 8 redstone, then polish it: hold sandpaper with the rose quartz in your off-hand and use it (a deployer can do this too).",
        "&eTip:&r washing crushed iron makes redstone as a byproduct, so a later ore line can feed this."]),
    Q("cr_tube", 18, 2, [item("create:electron_tube", 4)], "Electron Tubes", subtitle="Create's 'smart' component", deps=["cr_rose"], xp=60, desc=[
        "&eWhat:&r electron tubes go into deployers, mechanical crafters and other smart machines.",
        "&eHow:&r polished rose quartz on top of an iron plate.",
        "&eTip:&r make a stack. You'll need more than you think."]),
    Q("cr_deployer", 20, 2, [item("create:brass_hand"), item("create:deployer", 2)], "Deployers", subtitle="A hand that uses items", deps=["cr_brass_casing", "cr_tube"], xp=100, desc=[
        "&eWhat:&r a deployer acts like a player's hand: it places, uses and applies items.",
        "&eHow:&r an andesite casing, an electron tube and a brass hand (pressed brass sheets).",
        "&eTip:&r deployers over a belt are how Create builds things in steps: that's sequenced assembly."]),

    # --- After precision (x = 22..26) ----------------------------------------------------------
    Q("cr_arm", 22, -2, [item("create:mechanical_arm")], "Mechanical Arm", subtitle="Pick up here, put down there", deps=["cr_precision"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the mechanical arm moves items between depots, belts, basins and machines in its reach.",
        "&eHow:&r hold the arm and click inputs and outputs before you place it. Check the Ponder.",
        "&eTip:&r one arm can feed a whole ring of depots around it."]),
    Q("cr_speed_ctrl", 24, -2, [item("create:rotation_speed_controller")], "Speed Controller", subtitle="Optional: dial in the exact RPM", deps=["cr_precision"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r the Rotation Speed Controller sets the speed of the cogwheel on top of it to any RPM you choose.",
        "&eHow:&r a precision mechanism over a brass casing. Power it from below and set the speed on its face.",
        "&eTip:&r faster costs more stress, so only speed up what needs it."]),
    Q("cr_crush", 24, 2, [item("create:millstone"), item("create:crushing_wheel", 2)], "Crushing Wheels", subtitle="Ore into crushed ore", deps=["cr_precision"], xp=60, desc=[
        "&eWhat:&r two Crushing Wheels spinning toward each other grind ore blocks into crushed ore, obsidian into powder, and stone into gravel and sand.",
        "&eHow:&r each wheel is a mechanical crafting recipe (check JEI). Place them side by side, spin them inward, and drop items in from above.",
        "&eHow:&r yields: an ore block gives 1 crushed ore plus a 75% chance of a second; deepslate and modded ores are &ecapped at 2&r in this pack. Raw ore gives just 1 crushed ore (no gain), plus an XP nugget chance.",
        "&eTip:&r crush ore blocks (silk touch), not raw ore. Even so it's the same 2x ceiling as every route before acids; Mekanism's acid chain is where 3x and up begins."]),
    Q("cr_wash", 24, 4, [item("create:encased_fan"), item("create:crushed_raw_iron", 8)], "Bulk Washing", subtitle="Water, a fan and a bonus", deps=["cr_crush"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r an encased fan blowing through water washes crushed ore into nuggets plus a byproduct.",
        "&eHow:&r put flowing water in front of the fan and pass items through the air stream (a belt works).",
        "&eTip:&r washed crushed iron gives 9 nuggets (one ingot's worth) and a 75% chance of redstone. The byproduct is the bonus, not extra iron."]),

    # --- Trains (x = 26..32, y = 5..9) ---------------------------------------------------------
    Q("cr_sturdy", 26, 5, [item("create:powdered_obsidian", 4), item("create:sturdy_sheet", 4)], "Sturdy Sheets", subtitle="Obsidian, lava and two presses", deps=["cr_crush"], xp=75, desc=[
        "&eWhat:&r sturdy sheets, the armour plate for train casings and schedules.",
        "&eChemistry:&r obsidian is volcanic glass: lava cooled so fast that its silica never formed crystals.",
        "&eHow:&r crush obsidian into powder, then a sequenced assembly: spout 500 mB of lava onto it, press, press. JEI shows the loop.",
        "&eTip:&r the crushing wheels give the obsidian back 75% of the time, so feed it in until it's all powder."]),
    Q("cr_railway", 26, 7, [item("create:railway_casing", 8)], "Train Casing", subtitle="The body of every train", deps=["cr_sturdy"], xp=50, desc=[
        "&eWhat:&r train casing is the base block for stations, controls, signals and bogeys.",
        "&eHow:&r right-click a brass casing with a sturdy sheet.",
        "&eTip:&r right-clicking a track with train casing places a bogey: the wheels your train sits on."]),
    Q("cr_track", 28, 7, [item("create:track", 32)], "Train Track", subtitle="Sleepers, nuggets, a press", deps=["cr_railway"], xp=60, desc=[
        "&eWhat:&r Create's train track, which can curve, slope and cross.",
        "&eHow:&r sequenced assembly on stone slabs (the 'sleepers'): deploy an iron or zinc nugget, deploy another, then press. Check JEI.",
        "&eTip:&r click one track end, then another, to lay a curve or slope between them."]),
    Q("cr_station", 30, 7, [item("create:track_station", 2), item("create:controls")], "Stations and Controls", subtitle="Where trains are born", deps=["cr_track"], xp=75, desc=[
        "&eWhat:&r a Train Station assembles a train from the casing, bogeys and blocks on the track beside it; Train Controls let you drive it.",
        "&eHow:&r a station is train casing and a compass; controls are a lever, train casing and a precision mechanism.",
        "&eTip:&r stand at the station's GUI and press assemble once the controls face the way you want to go."]),
    Q("cr_train", 32, 7, [item("create:schedule", 2)], "Your First Train", subtitle="A schedule and somewhere to go", deps=["cr_station"], xp=200, size=1.5, shape="gear", desc=[
        "&6A machine that carries itself across the world. You used to move whole mountains like this.&r",
        "&eWhat:&r a Train Schedule tells a train where to stop and when to leave, so it runs by itself.",
        "&eHow:&r a sturdy sheet and paper make 4. Write stops in it and give it to the conductor (a mob in a seat behind the controls).",
        "&eTip:&r a train with portable storage interfaces at each station moves ore and goods on its own."]),
    Q("cr_signal", 30, 9, [item("create:track_signal", 4)], "Signals", subtitle="Optional: more than one train", deps=["cr_station"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r signals split a line into sections so two trains never share one. Real railways use the same 'block' idea.",
        "&eHow:&r train casing and an electron tube make 4. Place them on the track at each junction.",
        "&eTip:&r check the Ponder for chain signals at crossings."]),

    # --- Electricity (x >= 28) -----------------------------------------------------------------
    Q("cr_alternator", 28, -1, [item("createaddition:alternator")], "Rotation to Electricity", subtitle="Spin a shaft, get FE", deps=["cr_precision", "t3_analog"], xp=150, desc=[
        "&eWhat:&r Crafts and Additions' Alternator turns rotation into FE.",
        "&eChemistry:&r a coil turning in a magnetic field pushes electrons along the wire: electromagnetic induction.",
        "&eHow:&r in this pack its core is an &eMI analog circuit&r (LV), so electricity from rotation waits for the LV age. Feed it fast rotation."]),
    Q("cr_motor", 28, 1, [item("createaddition:electric_motor")], "Electricity to Rotation", subtitle="Run contraptions off the grid", deps=["cr_alternator"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the Electric Motor turns FE back into rotation, with a speed you set.",
        "&eHow:&r give it FE from your MI or Mekanism grid and set the speed in its GUI.",
        "&eTip:&r motors free you from water wheels and windmills. Put a Create line anywhere."]),
    Q("cr_rolling", 30, -1, [item("createaddition:rolling_mill"), item("createaddition:connector", 4), item("createaddition:copper_spool")], "Wires and Connectors", subtitle="Overhead power lines", deps=["cr_alternator"], xp=100, desc=[
        "&eWhat:&r the Rolling Mill turns ingots into rods and plates into wire. Spools of wire link connectors into power lines.",
        "&eHow:&r roll copper plates into wire, wind it onto a spool, then click two connectors with the spool to string a wire.",
        "&eTip:&r connectors carry power over long gaps without cables on the ground."]),
    Q("cr_accumulator", 32, -1, [item("createaddition:capacitor", 2), item("createaddition:modular_accumulator")], "Accumulators", subtitle="Store FE in brass and capacitors", deps=["cr_rolling"], xp=100, desc=[
        "&eWhat:&r the Modular Accumulator stores FE, and several placed together merge into one bigger battery.",
        "&eChemistry:&r the capacitor here is zinc over copper, the same pair Volta used in the first battery in 1800.",
        "&eHow:&r needs brass casing, capacitors, copper rods and electrum wire. Electrum is gold + silver mixed hot.",
        "&eTip:&r put it between your alternators and your machines to smooth out spikes."]),
    Q("cr_tesla", 34, 0.5, [item("createaddition:tesla_coil")], "Tesla Coil", deps=["cr_accumulator"], xp=60,
      optional=True, tokens=1, subtitle="Optional: charge items with lightning", desc=[
        "&eWhat:&r the Tesla Coil charges FE items on belts or depots below it, and zaps anything that walks under it.",
        "&eHow:&r a mechanical crafting recipe with brass, a capacitor, electron tubes and a copper spool (check JEI). Power it with FE.",
        "&eTip:&r put a belt of jetpacks or gadgets under it for an automatic charging station."]),
    Q("cr_newage", 30, -3, [item("create_new_age:generator_coil"), item("create_new_age:basic_energiser")], "Create: New Age", subtitle="Magnets, coils and energisers", deps=["cr_alternator"], xp=150, desc=[
        "&eWhat:&r magnet-and-coil generators, and Energisers that charge items with electricity.",
        "&eHow:&r the Generator Coil's core is an &eMI analog circuit&r (LV) in this pack. Spin it among magnets; the Ponder shows the layout.",
        "&eTip:&r the Basic Energiser is just an andesite casing and a lightning rod."]),
    Q("cr_na_motor", 28, -5, [item("create_new_age:basic_motor"), item("create_new_age:carbon_brushes")], "New Age Motors", subtitle="Optional: FE in, rotation out", deps=["cr_newage"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r New Age's Basic Motor runs on FE and spins a shaft; carbon brushes and motor extensions tune it.",
        "&eChemistry:&r a motor is a generator run backwards: current in a coil inside a magnetic field feels a force and turns.",
        "&eHow:&r an andesite casing, a magnetite block, a shaft and iron nuggets (check JEI for magnetite). Brushes are alloy, coal and a shaft."]),
    Q("cr_stirling", 30, -5, [item("create_new_age:stirling_engine"), item("create_new_age:basic_solar_heating_plate")], "Heat Engines", deps=["cr_newage"], xp=60,
      optional=True, tokens=1, subtitle="Optional: rotation from sunlight and heat", desc=[
        "&eWhat:&r New Age moves heat through heat pipes. Solar heating plates collect it from sunlight; a Stirling Engine turns it into slow rotation, and a Boiler Heater uses it in place of a blaze burner.",
        "&eChemistry:&r a real Stirling engine heats and cools a sealed gas. Hot gas expands and pushes a piston; cooled gas contracts and pulls it back. No fuel burns inside it.",
        "&eHow:&r heat pipes, iron and glass for the plate; a copper block, heat pipes and a shaft for the engine (check JEI and the Ponder scenes)."]),
    Q("cr_energiser", 32, -3, [item("create_new_age:overcharged_iron", 4)], "Charging Metal", subtitle="Iron soaked in electricity", deps=["cr_newage"], xp=100, desc=[
        "&eWhat:&r overcharged iron, made by charging an iron ingot in an Energiser.",
        "&eHow:&r power the Energiser with FE and put iron underneath it (on a depot or belt). Each ingot takes 1,000 FE.",
        "&eTip:&r overcharged metals make better wire and magnets."]),
    Q("cr_na_circuit", 34, -1.5, [item("create_new_age:blank_circuit", 4), item("create_new_age:copper_circuit")], "New Age Circuits", subtitle="Optional: superheated circuit boards", deps=["cr_energiser"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r New Age's own circuit boards, used in its better machines (check JEI for uses).",
        "&eChemistry:&r real boards are an insulating base with copper traces; here quartz, stone, iron and redstone fuse into the base.",
        "&eHow:&r compact stone, redstone, iron and quartz over a &esuperheated&r burner (blaze cake) for 4 blanks, then deploy copper wire onto one."]),
    Q("cr_magnet", 32, -5, [item("create_new_age:layered_magnet", 4)], "Layered Magnets", subtitle="Stronger fields, more power", deps=["cr_energiser"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r stronger magnets for New Age generators.",
        "&eHow:&r overcharged iron and overcharged gold in layers (check JEI).",
        "&eTip:&r a stronger field induces more current in the same coil."]),
    Q("cr_reactor", 34, -3, [item("create_new_age:thorium", 8), item("create_new_age:reactor_rod")], "Thorium Reactor", subtitle="New Age goes nuclear", deps=["cr_energiser", "t6_pu"], xp=400, desc=[
        "&eWhat:&r New Age's nuclear reactor, fuelled by &ethorium&r.",
        "&eChemistry:&r thorium-232 isn't fissile itself; it absorbs a neutron and becomes uranium-233, which is.",
        "&eHow:&r the rods need &eMI processing units&r (EV) in this pack, so it arrives alongside Mekanism fission. Check JEI and the Ponder for the build.",
        "&eTip:&r treat it like any reactor: cooling first, then power."]),

    # --- Experience (y = 3) --------------------------------------------------------------------
    Q("cr_xp", 28, 3, [item("create_enchantment_industry:mechanical_grindstone"), item("create_enchantment_industry:experience_bucket")], "Liquid Experience", subtitle="XP you can pipe", deps=["cr_precision"], xp=100, desc=[
        "&eWhat:&r Enchantment Industry turns experience into a fluid you can store and pipe.",
        "&eHow:&r the Mechanical Grindstone strips enchantments off items; a Grindstone Drain collects the XP as fluid. Check JEI.",
        "&eTip:&r feed it the enchanted junk from your mob farm."]),
    Q("cr_enchant", 30, 3, [item("create_enchantment_industry:blaze_enchanter")], "Automated Enchanting", subtitle="A blaze that reads spellbooks", deps=["cr_xp"], xp=100, desc=[
        "&eWhat:&r the Blaze Enchanter spends liquid XP to enchant items automatically.",
        "&eHow:&r it's a smithing upgrade of a Blaze Burner with an enchanting table (check JEI). Give it an enchanting template and XP.",
        "&eTip:&r put it beside a belt and a deployer for a hands-free enchanting line."]),
    Q("cr_printer", 32, 3, [item("create_enchantment_industry:printer")], "The Printer", subtitle="Copy books with XP", deps=["cr_enchant"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the Printer copies written and enchanted books, paid for in liquid XP.",
        "&eHow:&r check JEI and the Ponder for the setup.",
        "&eTip:&r find a good enchanted book once, then print it as often as your XP lasts."]),
    Q("cr_xp_lantern", 30, 5, [item("create_enchantment_industry:experience_lantern")], "Experience Lantern", subtitle="Optional: collect XP as it drops", deps=["cr_xp"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r the Experience Lantern pulls nearby experience orbs in and stores them as liquid XP.",
        "&eHow:&r check JEI for the recipe. Hang it over a mob farm's kill zone and pipe its XP away.",
        "&eTip:&r pair it with the Blaze Enchanter and your farm pays for its own enchanting."]),
], links=[("gs_iron", -2, 0), ("t2_blaze", 14, 2), ("t3_analog", 28, -3), ("t6_pu", 36, -3)])
