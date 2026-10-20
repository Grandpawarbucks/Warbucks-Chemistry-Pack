"""Quest chapter: create. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, MAIN, SIDE  # noqa: F401

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
    Q("cr_alloy", 0, 0, [item("create:andesite_alloy")], "Andesite Alloy", subtitle="The frame of every early machine", deps=["cr_andesite"], xp=30, desc=[
        "&6Gears and shafts. You remember a world that ran on clockwork, and you liked it.&r",
        "&eWhat:&r andesite alloy, Create's first building material.",
        "&eHow:&r craft andesite with iron nuggets (zinc nuggets work too). Later a Mechanical Mixer makes it in bulk.",
        "&eTip:&r hold &eW&r over almost any Create block to watch its Ponder tutorial."], mirror="0F16498769DFB3B0", section="First Steps", size=2.0, shape="gear", loot="t1"),
    Q("cr_casing", 2, 0, [item("create:andesite_casing")], "Andesite Casing", subtitle="Alloy pressed onto wood", deps=["cr_alloy"], xp=30, desc=[
        "&eWhat:&r casing blocks are the shell for gearboxes, deployers and more.",
        "&eHow:&r right-click a stripped log or stripped wood with andesite alloy. That's 'item application', and Create uses it a lot.",
        "&eTip:&r strip logs with an axe first. Any wood type works."], mirror="3AF2BC9A0E298882", section="Machines"),
    Q("cr_power", 4, 0, [item("create:shaft")], "Shafts", subtitle="Rotation, carried straight", deps=["cr_alloy"], xp=40, desc=[
        "&eWhat:&r Create runs on rotation, not electricity. Shafts carry it in a straight line from a source to the machines.",
        "&eChemistry:&r it's mechanics, not chemistry: power = torque x angular speed. Create shows the load as stress units (SU).",
        "&eHow:&r andesite alloy, 4 shafts per craft. Place them end to end.",
        "&eTip:&r hold &eW&r over any Create block to watch its Ponder."], mirror="5B36DE3826F26963", section="Kinetics"),
    Q("cr_cogs", 6, 0, [item("create:large_cogwheel"), item("create:cogwheel")], "Gear Ratios", subtitle="Big gear, small gear, double speed", deps=["cr_cog"], xp=40, desc=[
        "&eWhat:&r a large cogwheel meshed with a small one doubles the speed (or halves it the other way).",
        "&eChemistry:&r physics, really: power is torque times speed. Gearing trades one for the other, and Create shows the trade as stress: a machine's SU cost grows with its speed.",
        "&eHow:&r a shaft and two planks make a large cogwheel. Place it diagonally next to a small one so the teeth mesh.",
        "&eTip:&r run slow machines (like mixers you don't need fast) at low speed to save stress."], mirror="3C892B33758B7BA6", section="Kinetics"),
    Q("cr_windmill", 8, 0, [item("create:windmill_bearing"), anyof(["create:white_sail", "create:sail_frame"], 8)], "Windmills", subtitle="More stress capacity, anywhere", deps=["cr_cog"], xp=50, desc=[
        "&eWhat:&r a windmill bearing with sails attached spins without water.",
        "&eHow:&r place the bearing, build at least 8 sails onto the front of it (the Ponder shows how), and right-click the bearing.",
        "&eTip:&r more sails means more stress capacity but slower speed. Check the numbers with your goggles."], mirror="76CBFA38D021AC95", section="Kinetics"),
    Q("cr_belts", 10, 0, [item("create:belt_connector")], "Belts", subtitle="Rotation and items, side by side", deps=["cr_andesite"], xp=50, desc=[
        "&eWhat:&r a belt links two shafts: it carries rotation between them and moves items along its top.",
        "&eHow:&r dried kelp makes belt connectors. Click one shaft with it, then a second shaft up to 20 blocks away in a straight line.",
        "&eTip:&r a belt past a press, a fan or a deployer is the simplest Create production line."], mirror="13AEBC331F29BC3D", section="Belts and Logistics", size=2.0, shape="gear"),
    Q("cr_press", 12, 0, [item("create:mechanical_press")], "Mechanical Press", subtitle="Plates and compacting", deps=["cr_casing"], xp=50, desc=[
        "&eWhat:&r the Mechanical Press flattens ingots into plates and compacts items in a basin.",
        "&eHow:&r put the press over a depot, a belt or a basin, and power it.",
        "&eTip:&r plates are shared with MI in this pack, so pressed plates work in MI recipes too."], mirror="2D41B04C75FA02BC", section="Machines"),
    Q("cr_mixer", 14, 0, [item("create:mechanical_mixer")], "Mechanical Mixer", subtitle="Create's chemistry bench", deps=["cr_casing"], xp=75, desc=[
        "&eWhat:&r a mixer over a basin, heated by a Blaze Burner, makes alloys and fluids.",
        "&eChemistry:&r heat speeds up reactions and melts metals so they can mix into alloys.",
        "&eHow:&r catch a blaze in an Empty Blaze Burner (iron plates around netherrack), put it under the basin, feed it fuel, and put the mixer above.",
        "&eTip:&r feed the burner with a deployer or a mechanical arm so it never goes cold."], mirror="5DC892BA79EB52EC", section="Machines"),
    Q("cr_brass", 16, 0, [item("create:zinc_ingot", 8), item("create:brass_ingot", 8)], "Brass", subtitle="Copper plus zinc, mixed hot", deps=["cr_mixer", "cr_burner"], xp=100, size=1.5, desc=[
        "&6A golden metal, mixed in a basin. The old skill comes back to your hands.&r",
        "&eWhat:&r brass, the key metal of Create's second age.",
        "&eChemistry:&r brass is a copper-zinc alloy, usually about two-thirds copper. Zinc makes it harder and gives the gold colour.",
        "&eHow:&r 1 copper + 1 zinc in a heated mixer gives 2 brass. Zinc ore generates in the world."], section="Machines"),
    Q("cr_brass_casing", 18, 0, [item("create:brass_casing")], "Brass Casing", subtitle="The shell of smart machines", deps=["cr_mixer", "cr_burner", "cr_brass"], xp=60, desc=[
        "&eWhat:&r brass casing, for mechanical crafters, arms and brass tunnels.",
        "&eHow:&r right-click a stripped log or stripped wood with a brass ingot.",
        "&eTip:&r a deployer holding brass ingots can apply it automatically."], mirror="3C99017FD32B6DE2", section="Machines"),
    Q("cr_precision", 22, 0, [item("create:precision_mechanism")], "Precision", subtitle="Your first sequenced assembly", deps=["cr_deployer"], xp=150, size=1.0, desc=[
        "&6Each step in its place, every time. You used to build worlds this way.&r",
        "&eWhat:&r the precision mechanism, made by sequenced assembly: one item passes the same stations several times. Mechanical Crafters join into a big grid for recipes too large for a crafting table.",
        "&eHow:&r start with a gold plate, then deploy a cogwheel, a large cogwheel and an iron nugget onto it, 5 loops. JEI shows the sequence. Crafters are an electron tube, brass casing and crafting table.",
        "&eTip:&r some outputs are scrap. Sort them off the end of the belt and recycle them."], mirror="1712C3B3CF158843", section="Machines", shape=None),

    # --- Kinetic extras (x = 0..8) -------------------------------------------------------------
    Q("cr_crank", 2, -2, [item("create:hand_crank")], "Hand Crank", subtitle="Optional: rotation by muscle", deps=["cr_cog"], xp=20, optional=False, tokens=None, desc=[
        "&eWhat:&r the simplest power source: you turn it yourself.",
        "&eHow:&r three planks over an andesite alloy. Hold right-click on it to spin whatever it's attached to.",
        "&eTip:&r handy for testing a contraption before you build a real generator for it."], mirror="72C7698072BF0F1D", section="Kinetics"),
    Q("cr_goggles", 4, -2, [item("create:goggles")], "Engineer's Goggles", subtitle="See the stress", deps=["cr_andesite"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r Engineer's Goggles show speed and stress when you look at a machine; the wrench rotates and picks up Create blocks.",
        "&eHow:&r wear the goggles in your helmet slot and look at a shaft or generator.",
        "&eTip:&r sneak-right-click with the wrench to pick a block up instantly."], mirror="72537968598AB884", section="Tools"),
    Q("cr_gauges", 6, -2, [item("create:speedometer")], "Speedometer", subtitle="Read the RPM", deps=["cr_cogs", "cr_casing"], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r the Speedometer reads RPM; the Stressometer shows how much of your network's capacity is in use.",
        "&eHow:&r a compass on an andesite casing makes the speedometer (check JEI for the stressometer). Put them inline on a shaft.",
        "&eTip:&r both give a comparator signal, so a nearly full network can switch things off by redstone."], mirror="29917E6196649F5D", section="Kinetics"),
    Q("cr_gearshift", 6, 2, [item("create:clutch")], "Clutch", subtitle="Cut the rotation with redstone", deps=["cr_power"], xp=40, desc=[
        "&eWhat:&r a powered Clutch stops the rotation passing through it; unpowered, it passes rotation like a shaft.",
        "&eHow:&r andesite casing, a shaft and redstone.",
        "&eTip:&r a clutch on a lever is the off switch every machine line needs."], mirror="2BB3DB19D5EFC7E2", section="Kinetics"),
    Q("cr_chain_drive", 6, 4, [item("create:encased_chain_drive")], "Chain Drives", subtitle="Optional: rotation along a chain", deps=["cr_power"], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r encased chain drives pass rotation between each other in a line, in any direction, like a bike chain.",
        "&eHow:&r an andesite casing and three iron nuggets. The Adjustable Chain Gearshift version changes speed with a redstone signal (check JEI).",
        "&eTip:&r a neat way to bring power up a wall without shafts sticking out."], mirror="7F8E50FA436DB4E6", section="Kinetics"),
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
    Q("cr_bearing", 2, 4, [item("create:mechanical_bearing")], "Mechanical Bearing", subtitle="Make blocks spin", deps=["cr_contraptions"], xp=50, desc=[
        "&eWhat:&r a bearing turns the blocks attached to its face into a moving 'contraption': doors, rotors, fans, ferris wheels.",
        "&eHow:&r a wooden slab, an andesite casing and a shaft. Build onto its face, power it, and right-click to start.",
        "&eTip:&r moving blocks keep working: a spinning contraption can carry drills, harvesters and seats."], mirror="078C5B50CDC174CB", section="Contraptions"),
    Q("cr_clockwork", 0, 4, [item("create:clockwork_bearing")], "Clockwork Bearing", subtitle="Optional: a bearing that tells time", deps=["cr_contraptions"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r the Clockwork Bearing points its contraption at the current in-game time, like the hands of a clock.",
        "&eHow:&r a wooden slab, a brass casing and an electron tube. Build an hour hand on it, and a second layer for the minute hand.",
        "&eTip:&r a giant clock tower is a classic Create build."], mirror="18914FDF9CF9EEA8", section="Contraptions"),
    Q("cr_glue", 2, 6, [item("create:super_glue")], "Super Glue", subtitle="Stick blocks into one contraption", deps=["cr_andesite"], xp=40, desc=[
        "&eWhat:&r Super Glue marks blocks that should move together when a piston, bearing or gantry moves them.",
        "&eHow:&r slime, an iron plate and an iron nugget. Click two corners to glue the whole box between them.",
        "&eTip:&r glue is reusable: a glued area costs no extra glue to resize."], mirror="38CB5044AB3F859B", section="Contraptions"),
    Q("cr_pulley", 0, 6, [item("create:rope_pulley")], "Rope Pulley", subtitle="Optional: lift things straight up", deps=["cr_contraptions"], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r the Rope Pulley lowers and raises a contraption on a rope, which makes a simple lift.",
        "&eHow:&r an andesite casing, wool and an iron plate. Glue a platform under it and power it.",
        "&eTip:&r the brass Elevator Pulley (check JEI) adds floor buttons and stops at contacts."], mirror="24E658BA47367A44", section="Contraptions"),
    Q("cr_piston", 4, 6, [anyof(["create:mechanical_piston", "create:sticky_mechanical_piston"])], "Mechanical Piston", subtitle="Push a contraption in a line", deps=["cr_pole", "cr_contraptions"], xp=50, desc=[
        "&eWhat:&r a mechanical piston pushes and pulls glued blocks along a straight line, as far as its poles reach.",
        "&eHow:&r a wooden slab, an andesite casing and an extension pole. Put poles behind the piston head; each pole adds one block of travel.",
        "&eTip:&r rotation direction decides push or pull, so a gearshift reverses it."], mirror="45EC31812FB9934D", section="Contraptions"),
    Q("cr_drill", 6, 6, [item("create:mechanical_drill")], "Mechanical Drill", subtitle="Break blocks on the move", deps=["cr_contraptions"], xp=60, desc=[
        "&eWhat:&r a moving Drill breaks the blocks in front of it and drops them.",
        "&eHow:&r andesite casing, alloy and iron (check JEI). Mount it on a piston, bearing or gantry.",
        "&eTip:&r a drill on a slow bearing makes a cobblestone or tree farm."], mirror="3029E1E133B91ED8", section="Contraptions"),
    Q("cr_gantry", 4, 8, [item("create:gantry_carriage"), item("create:gantry_shaft")], "Gantries", subtitle="A carriage that rides a shaft", deps=["cr_contraptions"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r a Gantry Carriage runs along a powered gantry shaft, carrying its contraption with it, with no length limit.",
        "&eHow:&r gantry shafts are alloy and redstone; the carriage is a slab, a casing and a cogwheel. Power the shaft and the carriage moves.",
        "&eTip:&r gantries can carry other gantries, which makes an X-Y frame for a big drill or quarry."], mirror="75B14A09FE39EDDA", section="Contraptions"),
    Q("cr_cart", 2, 8, [item("create:cart_assembler")], "Minecart Contraptions", subtitle="Contraptions on rails", deps=["cr_contraptions"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r a Cart Assembler on a rail turns a passing minecart and the blocks glued to it into a moving contraption.",
        "&eHow:&r andesite alloy, redstone and logs. Place it as a rail, build on top, then send a minecart through with the assembler powered.",
        "&eTip:&r a minecart contraption with a drill digs its own tunnel along the track."], mirror="09936F8FCEA72C5C", section="Contraptions"),

    # --- Milling, copper and fluids (x = 10..16, y < 0) ----------------------------------------
    Q("cr_millstone", 10, -2, [item("create:millstone")], "Millstone", subtitle="Slow and steady grinding", deps=["cr_casing"], xp=40, desc=[
        "&eWhat:&r the Millstone grinds cobblestone to gravel, wheat to flour, flowers to dye, bones to bone meal and more.",
        "&eChemistry:&r grinding raises surface area: a powder reacts, dissolves and mixes much faster than a lump.",
        "&eHow:&r a cogwheel, an andesite casing and stone. Power it from the side or below and drop items in on top.",
        "&eTip:&r it doesn't take ores here. Ore crushing needs Crushing Wheels later."], mirror="64FF7118E29931C0", section="Machines"),
    Q("cr_saw", 10, -4, [item("create:mechanical_saw")], "Mechanical Saw", subtitle="A stonecutter with a motor", deps=["cr_contraptions"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r a still saw over a belt cuts logs into planks and acts as a stonecutter; on a contraption it fells whole trees.",
        "&eHow:&r iron plates, an iron ingot and an andesite casing. Set its target recipe with a filter if it has several.",
        "&eTip:&r a row of saws on a bearing makes a tree farm that never misses a log."], mirror="72DCE154E1714890", section="Contraptions"),
    Q("cr_copper_casing", 12, -2, [item("create:copper_casing")], "Copper Casing", subtitle="The shell for fluid machines", deps=["cr_copper"], xp=40, desc=[
        "&eWhat:&r copper casing is the base for spouts, item drains and hose pulleys.",
        "&eHow:&r right-click a stripped log or stripped wood with a copper ingot.",
        "&eTip:&r press a stack of copper sheets while you're at it. Pipes need them next."], mirror="3F663416E824720C", section="Fluids"),
    Q("cr_pipes", 12, -4, [item("create:fluid_pipe")], "Fluid Pipes", subtitle="Fluids go where you push them", deps=["cr_copper"], xp=50, desc=[
        "&eWhat:&r fluid pipes carry liquids, but only while a Mechanical Pump pushes them along.",
        "&eChemistry:&r a pump makes a pressure difference, and fluid always flows from high pressure to low.",
        "&eHow:&r copper sheets around a copper ingot make 4 pipes; a pipe and a cogwheel make a pump. The arrow on the pump shows the flow direction.",
        "&eTip:&r reverse the pump's rotation to reverse the flow."], mirror="483892F0A0F75B97", section="Fluids"),
    Q("cr_hose", 10, -6, [item("create:hose_pulley")], "Hose Pulley", subtitle="Optional: drain or fill a lake", deps=["cr_copper_casing"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r the Hose Pulley lowers a hose into a pool and sucks the fluid up, or fills an area from your pipes.",
        "&eHow:&r a copper casing, a dried kelp block and a copper plate. Power it and pipe its output away with a pump.",
        "&eTip:&r a big enough body of water or lava counts as endless (check the Ponder), so it's a free fluid source."], mirror="77382D4114E901CB", section="Fluids"),
    Q("cr_biofuel", 12, -6, [item("createaddition:seed_oil_bucket"), item("createaddition:bioethanol_bucket")], "Bioethanol", deps=["cr_pipes"], xp=75,
      optional=True, tokens=1, subtitle="Optional: fuel from fermented plants", desc=[
        "&eWhat:&r Crafts and Additions makes liquid fuel from plants: seed oil, then biomass, then bioethanol, which burns in a Liquid Blaze Burner.",
        "&eChemistry:&r real bioethanol comes from yeast fermenting sugar: C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂. Plant oils are triglycerides, long carbon chains that store a lot of energy.",
        "&eHow:&r compact seeds in a press and basin for seed oil; mix crops with seed oil over heat for biomass; mix biomass, sugar and cinder flour for bioethanol (check JEI).",
        "&eTip:&r it's a renewable fuel for Create steam engines that never touches your oil wells."]),
    Q("cr_spout", 14, -4, [item("create:spout")], "Spout", subtitle="Fill whatever passes underneath", deps=["cr_copper_casing"], xp=50, desc=[
        "&eWhat:&r the Spout pours fluid into items below it on a depot or belt: water bottles, buckets, honey, lava cakes and more.",
        "&eHow:&r a copper casing over dried kelp. Pipe fluid into it and put a depot underneath.",
        "&eTip:&r spouts are a station in many sequenced assembly recipes, so you'll use them again."], mirror="1C2309DB4B890E71", section="Fluids"),
    Q("cr_drain", 14, -6, [item("create:item_drain")], "Item Drain", subtitle="Empty buckets on the way past", deps=["cr_copper_casing"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r the Item Drain empties fluid containers that roll over it and holds the fluid for your pipes.",
        "&eHow:&r iron bars over a copper casing. Put it in a belt line and pull the fluid out with a pump.",
        "&eTip:&r it's the easy way to turn buckets from another mod into piped fluid."], mirror="39A7619B4C5592BE", section="Fluids"),
    Q("cr_steam", 16, -6, [item("create:steam_engine"), item("create:fluid_tank"), item("create:shaft")], "Steam Engines", subtitle="Fire, water and pistons", deps=["cr_cog"], xp=150, optional=False, tokens=None, desc=[
        "&eWhat:&r Create's boiler: a fluid tank full of water, heated by Blaze Burners, drives steam engines on its sides.",
        "&eChemistry:&r water expands about 1,600 times when it boils. That pressure pushes the pistons.",
        "&eHow:&r pump water into the tank, put fuelled Blaze Burners underneath, and place engines on its sides with a shaft in front. Check the Ponder.",
        "&eTip:&r a bigger tank and more burners raise the boiler level. Goggles show what's limiting it."], mirror="3697AAF8F281B247", section="Kinetics"),
    Q("cr_blaze_cake", 16, -4, [item("create:blaze_cake")], "Blaze Cake", subtitle="Optional: superheat a burner", deps=["cr_spout"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r feeding a Blaze Cake to a burner makes it &esuperheated&r for a while, hotter than any normal fuel.",
        "&eHow:&r compact an egg, sugar and cinder flour into a cake base, then spout 250 mB of lava into it.",
        "&eTip:&r some recipes need superheat (New Age's blank circuits, for one). Check the heat icon in JEI."], mirror="4C77ABCD41383F32", section="Fluids"),

    # --- Fans (x = 14..18, y = -2) ------------------------------------------------------------
    Q("cr_fan", 14, -2, [item("create:encased_fan")], "Encased Fan", subtitle="Air that cooks, washes and haunts", deps=["cr_casing"], xp=50, desc=[
        "&eWhat:&r an Encased Fan blows items along and processes them depending on what the air passes through.",
        "&eHow:&r a shaft, an andesite casing and a propeller (iron plates around alloy). Water in front washes, fire smokes, lava blasts, soul fire haunts.",
        "&eTip:&r items on a belt or depot in the air stream are processed; loose items on the ground are too."], mirror="1E9B2D814F50A265", section="Machines"),
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
    Q("cr_depot", 10, 2, [item("create:depot")], "Depots", subtitle="A table for machines to work on", deps=["cr_belts"], xp=30, desc=[
        "&eWhat:&r a Depot holds one stack of items for a press, fan, spout or deployer to work on.",
        "&eHow:&r andesite alloy and an andesite casing. Right-click to put items on it.",
        "&eTip:&r a depot under a press is the cheapest plate maker in the game."], mirror="2AEA51044AD44BE8", section="Belts and Logistics"),
    Q("cr_funnel", 10, 4, [item("create:andesite_funnel")], "Andesite Funnel", subtitle="Items in, items out", deps=["cr_belts"], xp=40, desc=[
        "&eWhat:&r funnels pull items out of chests and machines onto belts, or insert items from a belt; tunnels split a belt line evenly.",
        "&eHow:&r andesite alloy over dried kelp makes 2 funnels. Place them on a chest face or at the end of a belt (check JEI for tunnels).",
        "&eTip:&r a redstone signal shuts a funnel off, which is an easy on/off switch."], mirror="47A6769B6BF1A46D", section="Belts and Logistics"),
    Q("cr_ejector", 10, 6, [item("create:weighted_ejector")], "Weighted Ejector", subtitle="Optional: throw items across a gap", deps=["cr_depot"], xp=30, optional=False, tokens=None, desc=[
        "&eWhat:&r the Weighted Ejector flings items (or you) to a target block in an arc.",
        "&eHow:&r a gold plate, a depot and a cogwheel. Hold it and click the target before you place it.",
        "&eTip:&r stand on it for a free launch pad. The landing is your problem."], mirror="476C7317510198D9", section="Belts and Logistics"),
    Q("cr_chute", 12, 4, [item("create:chute")], "Chutes", subtitle="Let gravity do the hauling", deps=["cr_belts"], xp=30, desc=[
        "&eWhat:&r chutes drop items straight down between machines and chests; a fan under or over one blows items upward.",
        "&eHow:&r iron plates and an iron ingot make 4 chutes.",
        "&eTip:&r a chute into a crushing wheel or basin is the simplest feeder there is."], mirror="3D2A03EB2B91E9C1", section="Belts and Logistics"),
    Q("cr_vault", 14, 4, [item("create:item_vault")], "Item Vaults", subtitle="Storage that grows as you build", deps=["cr_belts"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r Item Vaults merge into one big storage block when placed together.",
        "&eHow:&r iron plates around a barrel. Place several side by side; funnels and pipes reach the whole vault.",
        "&eTip:&r vaults also go into frogports, so make a few extra."], mirror="0A4962728C98DAD9", section="Belts and Logistics"),
    Q("cr_brass_logistics", 18, 4, [item("create:brass_funnel")], "Brass Funnel", subtitle="A funnel with a filter", deps=["cr_belts", "cr_brass"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r brass funnels, tunnels and smart chutes take a filter, so you choose exactly which items pass and how many.",
        "&eHow:&r each uses an electron tube and brass (check JEI). Put an item or a Create Filter in the slot on the block.",
        "&eTip:&r a brass tunnel set to 'synchronise' only lets items through when every lane has one: perfect for 1:1 recipes."], mirror="495B0CC178B4CFA9", section="Belts and Logistics"),

    # --- Packages (x = 14..20, y = 6..8) --------------------------------------------------------
    Q("cr_cardboard", 14, 6, [item("create:cardboard")], "Cardboard", subtitle="Pulp, pressed flat", deps=["cr_belts", "cr_mixer"], xp=40, desc=[
        "&eWhat:&r cardboard, for Create's package logistics.",
        "&eChemistry:&r paper and card are mats of cellulose fibres; water lets the fibres bond as it dries, which is why pulp holds together.",
        "&eHow:&r mix 4 pulpable items (like sticks or sugar cane; check JEI) with 250 mB of water for pulp, then press the pulp into cardboard."], mirror="2C2958E38293717E", section="Packages"),
    Q("cr_packager", 16, 6, [item("create:packager")], "Packagers", subtitle="Box it up, send it off", deps=["cr_cardboard"], xp=50, desc=[
        "&eWhat:&r a Packager boxes items from the inventory behind it into a package with an address, or unpacks packages addressed to it.",
        "&eHow:&r a cardboard block, iron ingots and redstone. Put a sign or name on it for its address (see the Ponder).",
        "&eTip:&r packages ride belts, chutes and chain conveyors like any other item."], mirror="672F9CF5B0E626F1", section="Packages"),
    Q("cr_frogport", 18, 6, [item("create:package_frogport")], "Package Frogport", subtitle="A frog that catches your mail", deps=["cr_chain_conveyor"], xp=60, desc=[
        "&eWhat:&r chain conveyors carry packages through the air; a Package Frogport tongues them off the chain at the right stop.",
        "&eHow:&r a frogport is a slimeball, an item vault and andesite alloy; a chain conveyor is a large cogwheel in andesite casings. Link chains with iron chains.",
        "&eTip:&r a chain network with frogports at each base is a whole-base mail system."], mirror="3B3B38B17CF5D81C", section="Packages"),
    Q("cr_stock", 20, 6, [item("create:stock_link")], "Stock Link", subtitle="Order from a counter", deps=["cr_packages"], xp=75, desc=[
        "&eWhat:&r a Stock Link reports what a packager can reach; a Stock Ticker lets you browse that stock and order items to be packed and sent.",
        "&eHow:&r a transmitter (lightning rod, copper plates, redstone) on an item vault makes the link; add glass and gold for the ticker.",
        "&eTip:&r put the ticker by your workbench and order ingredients without walking to storage."], mirror="6353A39CBEE599A0", section="Packages"),
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
    Q("cr_deployer", 20, 2, [item("create:deployer")], "Deployer", subtitle="A hand that uses items", deps=["cr_casing", "cr_tube", "cr_brass"], xp=100, desc=[
        "&eWhat:&r a deployer acts like a player's hand: it places, uses and applies items.",
        "&eHow:&r an andesite casing, an electron tube and a brass hand (pressed brass sheets).",
        "&eTip:&r deployers over a belt are how Create builds things in steps: that's sequenced assembly."], mirror="3314FBC4FEAE1D08", section="Machines"),

    # --- After precision (x = 22..26) ----------------------------------------------------------
    Q("cr_arm", 22, -2, [item("create:mechanical_arm")], "Mechanical Arm", subtitle="Pick up here, put down there", deps=["cr_precision", "cr_brass_casing"], xp=100, optional=False, tokens=None, desc=[
        "&eWhat:&r the mechanical arm moves items between depots, belts, basins and machines in its reach.",
        "&eHow:&r hold the arm and click inputs and outputs before you place it. Check the Ponder.",
        "&eTip:&r one arm can feed a whole ring of depots around it."], mirror="3F2C1A81C17D2D67", section="Machines"),
    Q("cr_speed_ctrl", 24, -2, [item("create:rotation_speed_controller")], "Speed Controller", subtitle="Optional: dial in the exact RPM", deps=["cr_gauges", "cr_precision", "cr_brass_casing"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r the Rotation Speed Controller sets the speed of the cogwheel on top of it to any RPM you choose.",
        "&eHow:&r a precision mechanism over a brass casing. Power it from below and set the speed on its face.",
        "&eTip:&r faster costs more stress, so only speed up what needs it."], mirror="7BB3BF6162F05265", section="Kinetics"),
    Q("cr_crush", 24, 2, [item("create:crushing_wheel", 2)], "Crushing Wheels", subtitle="Ore into crushed ore", deps=["cr_casing"], xp=60, desc=[
        "&eWhat:&r two Crushing Wheels spinning toward each other grind ore blocks into crushed ore, obsidian into powder, and stone into gravel and sand.",
        "&eHow:&r each wheel is a mechanical crafting recipe (check JEI). Place them side by side, spin them inward, and drop items in from above.",
        "&eHow:&r yields: an ore block gives 1 crushed ore plus a 75% chance of a second; deepslate and modded ores are &ecapped at 2&r in this pack. Raw ore gives just 1 crushed ore (no gain), plus an XP nugget chance.",
        "&eTip:&r crush ore blocks (silk touch), not raw ore. Even so it's the same 2x ceiling as every route before acids; Mekanism's acid chain is where 3x and up begins."], mirror="3F02EF19112D23BE", section="Machines"),
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
    Q("cr_railway", 26, 7, [item("create:railway_casing")], "Train Casing", subtitle="The body of every train", deps=["cr_brass_casing", "cr_sturdy"], xp=50, desc=[
        "&eWhat:&r train casing is the base block for stations, controls, signals and bogeys.",
        "&eHow:&r right-click a brass casing with a sturdy sheet.",
        "&eTip:&r right-clicking a track with train casing places a bogey: the wheels your train sits on."], mirror="4EE10B8E194F5CA9", section="Trains"),
    Q("cr_track", 28, 7, [item("create:track", 16)], "Train Track", subtitle="Sleepers, nuggets, a press", deps=["cr_deployer"], xp=60, desc=[
        "&eWhat:&r Create's train track, which can curve, slope and cross.",
        "&eHow:&r sequenced assembly on stone slabs (the 'sleepers'): deploy an iron or zinc nugget, deploy another, then press. Check JEI.",
        "&eTip:&r click one track end, then another, to lay a curve or slope between them."], mirror="5979DE0E2BA3DAE5", section="Trains"),
    Q("cr_station", 30, 7, [item("create:track_station")], "Train Station", subtitle="Where trains are born", deps=["cr_railway", "cr_track"], xp=75, desc=[
        "&eWhat:&r a Train Station assembles a train from the casing, bogeys and blocks on the track beside it; Train Controls let you drive it.",
        "&eHow:&r a station is train casing and a compass; controls are a lever, train casing and a precision mechanism.",
        "&eTip:&r stand at the station's GUI and press assemble once the controls face the way you want to go."], mirror="77BE3D9D274F72F1", section="Trains"),
    Q("cr_train", 32, 7, [item("create:schedule"), anytag("create:seats")], "Your First Train", subtitle="A schedule and somewhere to go", deps=["cr_train_build"], xp=200, size=1.0, shape=None, desc=[
        "&6A machine that carries itself across the world. You used to move whole mountains like this.&r",
        "&eWhat:&r a Train Schedule tells a train where to stop and when to leave, so it runs by itself.",
        "&eHow:&r a sturdy sheet and paper make 4. Write stops in it and give it to the conductor (a mob in a seat behind the controls).",
        "&eTip:&r a train with portable storage interfaces at each station moves ore and goods on its own."], mirror="2D96965317D3CFEC", section="Trains"),
    Q("cr_signal", 30, 9, [item("create:track_signal")], "Signals", subtitle="Optional: more than one train", deps=["cr_train_build"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r signals split a line into sections so two trains never share one. Real railways use the same 'block' idea.",
        "&eHow:&r train casing and an electron tube make 4. Place them on the track at each junction.",
        "&eTip:&r check the Ponder for chain signals at crossings."], mirror="30AC43222FF9B18A", section="Trains"),

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

    # --- ATM10-alignment round (2026-10-19) ----------------------------------------------------
    Q("cr_large_wheel", 0, 0, [anyof(["create:water_wheel", "create:large_water_wheel"])], "Water Wheels",
      subtitle="Slower, but far stronger", deps=["cr_cog"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r a 3x3 water wheel. It turns at half the speed of the small one but gives more stress capacity in total (check with goggles).",
        "&eChemistry:&r physics again: a bigger wheel catches the flow further from its axle, so the same water gives more torque.",
        "&eHow:&r a water wheel ringed with planks. Give it flowing water across the whole face.",
        "&eTip:&r follow it with a large cogwheel to get the speed back."], mirror="5DD6631F5996BA71", section="Kinetics"),
    Q("cr_rotation_control", 0, 0, [item("create:adjustable_chain_gearshift")], "Adjustable Chain Gearshift",
      subtitle="Redstone strength sets the speed", deps=["cr_chain_drive"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r a chain drive that changes its speed ratio with the strength of a redstone signal.",
        "&eHow:&r an encased chain drive with an electron tube (check JEI).",
        "&eTip:&r a comparator on a chest makes a line speed up as the chest fills."], mirror="54EC1C7FC1DA9107", section="Kinetics"),
    Q("cr_burner_kit", 0, 0, [item("create:empty_blaze_burner", 2), item("create:blaze_cake_base")], "Spare Burners",
      subtitle="More burners, and the cake base", deps=["cr_mixer"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r empty Blaze Burners to catch more blazes, and a Blaze Cake base ready to fill with lava.",
        "&eChemistry:&r a superheated burner runs hotter because the cake gives it richer fuel; as a rule of thumb, many reactions run about twice as fast for every 10 °C hotter.",
        "&eHow:&r burners are iron plates around netherrack; right-click a blaze with one, or use it on a monster spawner. The cake base is compacted egg, sugar and cinder flour (check JEI).",
        "&eTip:&r a big steam boiler wants nine or more burners. Catch them early."]),
    Q("cr_fluid_control", 0, 0, [item("create:fluid_valve")], "Fluid Valve",
      subtitle="Open and close a pipe by rotation", deps=["cr_pipes"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r a Fluid Valve opens or closes a pipe when rotation turns it; a valve handle turns it by hand.",
        "&eHow:&r an iron plate and a fluid pipe (check JEI).",
        "&eTip:&r a clutch on the valve's shaft gives you a redstone-controlled pipe."], mirror="50DBB87E53017E60", section="Fluids"),
    Q("cr_nozzle", 0, 0, [item("create:nozzle")], "Nozzle",
      subtitle="Spread a fan's effect in a circle", deps=["cr_fan"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r a Nozzle on the front of an Encased Fan spreads its air all around instead of in a line, and pushes or pulls mobs in range.",
        "&eHow:&r andesite alloy and wool (check JEI).",
        "&eTip:&r a fan, a nozzle and a fire behind it make a warm room. A water source behind it, a mob wash."]),
    Q("cr_plough", 0, 0, [item("create:mechanical_plough")], "Mechanical Plough",
      subtitle="Till fields, grab whole rings", deps=["cr_contraptions"], xp=40, optional=False, tokens=None, desc=[
        "&eWhat:&r the Mechanical Plough tills dirt and breaks small blocks as a contraption moves; Radial Chassis grabs blocks around it in a ring, for bearing contraptions.",
        "&eHow:&r plough: iron plates, andesite alloy and a casing. Radial chassis: logs and andesite alloy, three at a time (check JEI).",
        "&eTip:&r a plough leading a row of harvesters and seed deployers is a field that farms itself."], mirror="0759CA52EECF3B49", section="Contraptions"),
    Q("cr_interfaces", 0, 0, [item("create:portable_fluid_interface"), item("create:portable_storage_interface")], "Portable Interfaces",
      subtitle="Load a moving contraption", deps=["cr_copper_casing", "cr_contraptions"], xp=60, optional=False, tokens=None, desc=[
        "&eWhat:&r a pair of Portable Storage (or Fluid) Interfaces, one on the contraption and one on the ground, swap items or fluids whenever they line up.",
        "&eHow:&r an andesite casing (items) or copper casing (fluids) with a chute (check JEI).",
        "&eTip:&r a train with fluid interfaces can haul acid from a remote plant without a single pipe."], mirror="71B1B53A03A16296", section="Contraptions"),
    Q("cr_seat", 0, 0, [anytag("create:seats")], "Take a Seat",
      subtitle="Somewhere to sit, and a seat for a conductor", deps=["cr_casing"], xp=20, optional=True, tokens=1, desc=[
        "&eWhat:&r Create seats. You can sit on them, mobs sit on them, and a seated mob (or you) is what drives a train or moving contraption.",
        "&eHow:&r a wooden slab and wool of any colour. Dye one seat to recolour it.",
        "&eTip:&r a villager in a seat behind train controls becomes your conductor."]),
    Q("cr_displays", 0, 0, [item("create:display_link"), item("create:nixie_tube", 4)], "Display Links and Nixie Tubes",
      subtitle="Put your numbers on the wall", deps=["cr_stock", "cr_tube"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r a Display Link reads a block (a stockpile, a tank, a station, a speedometer) and writes it onto Nixie Tubes, signs or display boards.",
        "&eHow:&r a transmitter on brass casing makes the link; two electron tubes make four nixie tubes (check JEI).",
        "&eTip:&r link a tank of seed oil to a nixie row and you'll see the level from across the room."]),
    Q("cr_repackager", 0, 0, [item("create:repackager")], "Re-Packager",
      subtitle="Merge and split packages", deps=["cr_packager"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r a Re-Packager opens incoming packages and repacks their contents, so a recipe's ingredients arrive at a machine in one box.",
        "&eHow:&r a Packager converted in the crafting grid (check JEI).",
        "&eTip:&r use it in front of a mechanical crafter that needs many different items at once."]),
    Q("cr_train_fittings", 0, 0, [item("create:track_observer"), item("create:train_door", 2)], "Train Fittings",
      subtitle="Doors that stay shut, and a track sensor", deps=["cr_train_build"], xp=50, optional=False, tokens=None, desc=[
        "&eWhat:&r Train Doors and Trapdoors open only when the train is stopped at a station. A Train Observer gives a redstone signal when a train passes over it.",
        "&eHow:&r a wooden door or trapdoor with train casing; the observer is train casing and a pressure plate (check JEI).",
        "&eTip:&r a train observer before a station can open a loading gate in time."], mirror="5134C81D96C55375", section="Trains"),

    # --- ATM10 mirror round (2026-10-20): ATM10's Create quests we didn't have yet ---------------------------------
    Q("cr_andesite", 0, 0, [item("minecraft:andesite")], "Andesite", subtitle="The grey stone that starts it all", deps=['gs_iron'], xp=20, mirror="57A7A5C79389A96A", section="First Steps", size=2.0, shape="gear", desc=[
        "&eWhat:&r andesite is the stone Create is built on: alloy, casings and every early machine start with it.",
        "&eHow:&r find it in the hills or underground, or mix diorite with cobblestone.",
        "&eTip:&r andesite is a real volcanic rock, rich in plagioclase feldspar. Mine a stack."]),
    Q("cr_cog", 0, 0, [anyof(["create:cogwheel", "create:large_cogwheel"])], "Cogwheels", subtitle="Pass rotation sideways", deps=['cr_power'], xp=40, mirror="6893D537716AA748", section="Kinetics", desc=[
        "&eWhat:&r cogwheels hand rotation to the cogs next to them, so it can turn corners.",
        "&eHow:&r a shaft and planks. Large cogs mesh diagonally with small ones.",
        "&eTip:&r any cog counts here."]),
    Q("cr_gearbox", 0, 0, [item("create:gearbox")], "Gearbox", subtitle="Rotation round a corner", deps=['cr_power'], xp=40, mirror="4285510271B5223D", section="Kinetics", desc=[
        "&eWhat:&r a gearbox passes rotation out of all four of its side faces.",
        "&eHow:&r four cogwheels around an andesite casing.",
        "&eTip:&r it reverses the direction on opposite sides; check with goggles."]),
    Q("cr_gearshift2", 0, 0, [item("create:gearshift")], "Gearshift", subtitle="Reverse with redstone", deps=['cr_power'], xp=40, mirror="67A46ED73E488CEE", section="Kinetics", desc=[
        "&eWhat:&r a powered Gearshift reverses the rotation passing through it.",
        "&eHow:&r andesite casing, a cogwheel and redstone.",
        "&eTip:&r pistons and gantries need it to come back home."]),
    Q("cr_sequenced", 0, 0, [item("create:sequenced_gearshift")], "Sequenced Gearshift", subtitle="A programmed list of turns", deps=['cr_gearshift2'], xp=40, mirror="1BA11428DF7541AD", section="Kinetics", desc=[
        "&eWhat:&r runs a list of steps: turn so many degrees, wait, reverse, repeat.",
        "&eHow:&r brass casing, a cogwheel and an electron tube (check JEI).",
        "&eTip:&r perfect for doors and drawbridges."]),
    Q("cr_vgearbox", 0, 0, [item("create:vertical_gearbox")], "Vertical Gearbox", subtitle="Up and down instead of sideways", deps=['cr_power'], xp=40, mirror="09E34E1F9C751458", section="Kinetics", desc=[
        "&eWhat:&r a gearbox turned on its side, passing rotation up and down.",
        "&eHow:&r a gearbox in the crafting grid."]),
    Q("cr_stressometer", 0, 0, [item("create:stressometer")], "Stressometer", subtitle="How close to the limit?", deps=['cr_cogs', 'cr_casing'], xp=30, mirror="48BE7DAC5082044D", section="Kinetics", desc=[
        "&eWhat:&r shows how much of your network's stress capacity is in use.",
        "&eHow:&r check JEI. Put it inline on a shaft.",
        "&eTip:&r it gives a comparator signal: switch things off before the network stalls."]),
    Q("cr_burner", 0, 0, [item("create:blaze_burner")], "Blaze Burner", subtitle="A blaze in a cage, for heat", deps=['t2_blaze'], xp=50, mirror="1B182A30604655E2", section="Machines", desc=[
        "&eWhat:&r a Blaze Burner heats a basin from below, for mixing alloys and some fluids.",
        "&eHow:&r make an Empty Blaze Burner (iron plates around netherrack) and right-click a blaze with it. Feed it fuel.",
        "&eTip:&r a blaze cake makes it superheated for the hottest recipes."]),
    Q("cr_basin", 0, 0, [item("create:basin")], "Basin", subtitle="Where pressing and mixing happen", deps=['cr_pipes', 'cr_belts'], xp=30, mirror="75CBB5BD8C1DFEA1", section="Machines", desc=[
        "&eWhat:&r the basin holds items and fluids for a press or mixer above it.",
        "&eHow:&r an andesite alloy (check JEI). Put it under the machine; output comes out its sides.",
        "&eTip:&r a funnel or spout on it automates the inputs."]),
    Q("cr_crafter", 0, 0, [item("create:mechanical_crafter")], "Mechanical Crafter", subtitle="A crafting grid as big as you like", deps=['cr_brass_casing'], xp=40, mirror="4194397DFD0199C2", section="Machines", desc=[
        "&eWhat:&r crafters join into grids for recipes too big for a crafting table, and craft by themselves.",
        "&eHow:&r an electron tube, brass casing and a crafting table.",
        "&eTip:&r the precision mechanism and Create's big recipes need these."]),
    Q("cr_train_build", 0, 0, [item("create:controls"), item("create:super_glue"), item("create:railway_casing")], "Building a Train", subtitle="Controls, glue and a bogey", deps=['cr_track', 'cr_station'], xp=150, mirror="3FBCBBEBB78B83FC", section="Trains", size=1.5, shape="hexagon", loot="t2", desc=[
        "&eWhat:&r a train is glued blocks on bogeys, with controls at the front.",
        "&eHow:&r put a railway casing on the track to make a bogey, build on it, glue it, place the controls and click the station to assemble.",
        "&eTip:&r see the Ponder on the station for each step."]),
    Q("cr_controls", 0, 0, [item("create:controls")], "Train Controls", subtitle="Drive it yourself", deps=['cr_train_build'], xp=40, mirror="7F0F7111552F95A9", section="Trains", desc=[
        "&eWhat:&r the controls let you drive a train by hand, or seat a conductor for a schedule.",
        "&eHow:&r check JEI."]),
    Q("cr_train_glue", 0, 0, [item("create:super_glue")], "More Glue", subtitle="Every carriage needs its own", deps=['cr_train_build'], xp=20, mirror="12274935C3D20C74", section="Trains", desc=[
        "&eWhat:&r each carriage of a train is glued on its own bogeys.",
        "&eHow:&r glue each carriage before you assemble it."]),
    Q("cr_contraptions", 0, 0, [item("create:super_glue"), item("create:andesite_casing")], "Contraptions", subtitle="Blocks that move", deps=['cr_casing', 'cr_glue'], xp=80, mirror="69EE22CB4FF1E591", section="Contraptions", size=2.0, shape="gear", loot="t1", desc=[
        "&eWhat:&r a contraption is a group of glued blocks moved by a piston, bearing, gantry, pulley or cart.",
        "&eHow:&r glue the blocks to each other and to the mover's face, then power the mover.",
        "&eTip:&r drills, saws and harvesters on a contraption work as it moves."]),
    Q("cr_chassis", 0, 0, [item("create:linear_chassis")], "Linear Chassis", subtitle="Grab a whole row", deps=['cr_contraptions'], xp=40, mirror="51EA6B1452883AB2", section="Contraptions", desc=[
        "&eWhat:&r a chassis pulls in the blocks next to it in a line, without glue.",
        "&eHow:&r andesite alloy and logs. Use slime on a face to make it sticky."]),
    Q("cr_radial", 0, 0, [item("create:radial_chassis")], "Radial Chassis", subtitle="Grab a whole layer", deps=['cr_contraptions'], xp=40, mirror="459BA85E48B343AE", section="Contraptions", desc=[
        "&eWhat:&r a radial chassis pulls in a circle of blocks around it: windmill sails, doors, platforms.",
        "&eHow:&r andesite alloy and logs (check JEI)."]),
    Q("cr_harvester", 0, 0, [item("create:mechanical_harvester")], "Mechanical Harvester", subtitle="Pick crops as you pass", deps=['cr_contraptions'], xp=40, mirror="4C31649D721F76B5", section="Contraptions", desc=[
        "&eWhat:&r a moving Harvester picks grown crops and leaves the plant to regrow.",
        "&eHow:&r andesite casing, alloy and iron plates (check JEI).",
        "&eTip:&r a slow piston sweep over a field is a full farm."]),
    Q("cr_pole", 0, 0, [item("create:piston_extension_pole")], "Piston Poles", subtitle="How far the piston reaches", deps=['cr_contraptions'], xp=20, mirror="47897D827C50629D", section="Contraptions", desc=[
        "&eWhat:&r extension poles behind a mechanical piston set how far it pushes.",
        "&eHow:&r andesite alloy and planks (check JEI)."]),
    Q("cr_tunnel", 0, 0, [item("create:andesite_tunnel")], "Andesite Tunnel", subtitle="Split a belt", deps=['cr_belts'], xp=40, mirror="7C8CDD259495A31A", section="Belts and Logistics", desc=[
        "&eWhat:&r a tunnel on a belt splits items evenly to the sides and to belts beside it.",
        "&eHow:&r andesite alloy and dried kelp."]),
    Q("cr_brass_tunnel", 0, 0, [item("create:brass_tunnel")], "Brass Tunnel", subtitle="Split a belt, by filter", deps=['cr_belts', 'cr_brass'], xp=40, mirror="78656C89EEE80DB5", section="Belts and Logistics", desc=[
        "&eWhat:&r a brass tunnel splits by filter and by rule (round robin, prefer nearest and so on).",
        "&eHow:&r brass, dried kelp and an electron tube (check JEI)."]),
    Q("cr_smart_chute", 0, 0, [item("create:smart_chute")], "Smart Chute", subtitle="A chute with a filter", deps=['cr_chute'], xp=40, mirror="7EEEEDD5FF31ACD3", section="Belts and Logistics", desc=[
        "&eWhat:&r a smart chute only lets the filtered items fall.",
        "&eHow:&r a chute with brass and an electron tube (check JEI)."]),
    Q("cr_packages", 0, 0, [anytag("create:packages")], "A Package", subtitle="Items boxed and addressed", deps=['cr_packager'], xp=30, mirror="16B0C1F7B951C19D", section="Packages", desc=[
        "&eWhat:&r a package is a box of items with an address on it.",
        "&eHow:&r a Packager boxes whatever is in the inventory behind it."]),
    Q("cr_chain_conveyor", 0, 0, [item("create:chain_conveyor")], "Chain Conveyor", subtitle="Packages through the air", deps=['cr_packages'], xp=40, mirror="737DC37E4310090C", section="Packages", desc=[
        "&eWhat:&r chain conveyors carry packages between them on a chain.",
        "&eHow:&r a large cogwheel in andesite casing; link two with iron chains."]),
    Q("cr_postbox", 0, 0, [anytag("create:postboxes")], "Postbox", subtitle="Packages to and from trains", deps=['cr_packages'], xp=30, mirror="57A18F2E51952EB8", section="Packages", desc=[
        "&eWhat:&r a postbox sends and receives packages by train.",
        "&eHow:&r check JEI. Put it next to a station."]),
    Q("cr_ticker", 0, 0, [item("create:stock_ticker")], "Stock Ticker", subtitle="Browse and order your stock", deps=['cr_stock'], xp=40, mirror="754B8F1FBCD983C5", section="Packages", desc=[
        "&eWhat:&r the ticker shows what your linked packagers can reach and lets you order items to be packed and sent.",
        "&eHow:&r a stock link with glass and gold (check JEI)."]),
    Q("cr_tablecloth", 0, 0, [anytag("create:table_cloths")], "Table Cloth", subtitle="Open a shop", deps=['cr_stock', 'cr_ticker'], xp=30, mirror="64860340A5BEBAB9", section="Packages", desc=[
        "&eWhat:&r a table cloth on a table shows items for sale; a stock ticker behind it fills the orders.",
        "&eHow:&r wool and an item (check JEI).",
        "&eTip:&r on a shared server, it's a real shop."]),
    Q("cr_copper", 0, 0, [item("minecraft:copper_ingot")], "Copper", subtitle="Create's fluid metal", deps=['cr_andesite'], xp=30, mirror="7242F591DA474B37", section="Fluids", size=2.0, shape="gear", desc=[
        "&eWhat:&r copper makes Create's pipes, tanks, spouts and casings.",
        "&eHow:&r smelt raw copper. Copper sheets come from a press.",
        "&eTip:&r copper oxidises green in air (a copper carbonate patina); wax it with honeycomb to stop it."]),
    Q("cr_pump", 0, 0, [item("create:mechanical_pump")], "Mechanical Pump", subtitle="Pipes only flow when pushed", deps=['cr_pipes'], xp=40, mirror="133CA315A1443A49", section="Fluids", desc=[
        "&eWhat:&r a pump pushes fluid along pipes in the direction of its arrow.",
        "&eHow:&r a fluid pipe and a cogwheel.",
        "&eTip:&r faster rotation pumps faster."]),
    Q("cr_smart_pipe", 0, 0, [item("create:smart_fluid_pipe")], "Smart Fluid Pipe", subtitle="Only the fluid you choose", deps=['cr_pipes'], xp=40, mirror="087F6C09CB5B2D1A", section="Fluids", desc=[
        "&eWhat:&r a smart pipe lets only the fluid you set pass.",
        "&eHow:&r a pipe with a brass plate and an electron tube (check JEI)."]),
    Q("cr_fluid_tank", 0, 0, [item("create:fluid_tank")], "Fluid Tank", subtitle="Stack it into a big tank", deps=['cr_copper'], xp=40, mirror="3A4C62865C7CC862", section="Fluids", desc=[
        "&eWhat:&r fluid tanks join into large tanks when placed next to and on top of each other.",
        "&eHow:&r copper sheets and a barrel (check JEI).",
        "&eTip:&r a tank is also the boiler for steam engines."]),
    Q("cr_wrench", 0, 0, [item("create:wrench")], "Wrench", subtitle="Rotate and pick up Create blocks", deps=['cr_andesite'], xp=30, mirror="127F9EAC7C305BF5", section="Tools", desc=[
        "&eWhat:&r the wrench rotates Create blocks, and sneak-click picks them up instantly.",
        "&eHow:&r gold plate, a cogwheel and a stick (check JEI)."]),
], links=[("gs_iron", -2, 0), ("t2_blaze", 14, 2), ("t3_analog", 28, -3), ("t6_pu", 36, -3)], mirror="create")
