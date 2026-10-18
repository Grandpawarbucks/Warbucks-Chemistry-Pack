"""Quest chapter: create. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

# Layout: y=0 kinetic spine (alloy -> brass -> precision), y=-2 pressing/mixing, y=2 ores and
# electron tubes; electricity from x=20 (y=-1 Crafts & Additions, y=-3 New Age, y=1/3 motor and XP).
# Optional quests sit off those rows.
CHAPTER = Chapter("create", "The Mechanical Age", "create:cogwheel",
        ["Create: rotation, presses and mixers. An early mechanical age that runs alongside steam and feeds into Modern Industrialization."], SIDE, [
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
    Q("cr_goggles", 4, -2, [item("create:goggles"), item("create:wrench")], "Goggles and Wrench", subtitle="See the stress", deps=["cr_power"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r Engineer's Goggles show speed and stress when you look at a machine; the wrench rotates and picks up Create blocks.",
        "&eHow:&r wear the goggles in your helmet slot and look at a shaft or generator.",
        "&eTip:&r sneak-right-click with the wrench to pick a block up instantly."]),
    Q("cr_windmill", 6, 0, [item("create:windmill_bearing"), item("create:white_sail", 8)], "Windmills", subtitle="More stress capacity, anywhere", deps=["cr_power"], xp=50, desc=[
        "&eWhat:&r a windmill bearing with sails attached spins without water.",
        "&eHow:&r place the bearing, build at least 8 sails onto the front of it (the Ponder shows how), and right-click the bearing.",
        "&eTip:&r more sails means more stress capacity but slower speed. Check the numbers with your goggles."]),
    Q("cr_connected", 6, 2, [item("create_connected:brass_gearbox"), item("create_connected:kinetic_bridge")], "Create: Connected", subtitle="Handy kinetic parts", deps=["cr_windmill"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r Create: Connected adds small conveniences: compact gearboxes, a kinetic bridge that carries rotation across gaps, and more.",
        "&eHow:&r check JEI for everything the mod adds.",
        "&eTip:&r the kinetic bridge saves long runs of shafts."]),
    Q("cr_deco", 2, 2, [item("createdeco:brass_catwalk", 8), item("createdeco:andesite_sheet_metal", 8)], "Create Deco", subtitle="Make the factory look like one", deps=["cr_casing"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r catwalks, sheet metal, cage lamps and other industrial building blocks.",
        "&eHow:&r check JEI for Create Deco recipes. Many use a press or the stonecutter.",
        "&eTip:&r catwalks over your machine lines make maintenance much easier."]),
    Q("cr_belts", 8, 0, [item("create:gearbox", 2), item("create:belt_connector", 4)], "Gearboxes and Belts", subtitle="Move rotation and items", deps=["cr_windmill"], xp=50, desc=[
        "&eWhat:&r gearboxes turn rotation through corners; belts carry both rotation and items between two shafts.",
        "&eHow:&r belts are made from dried kelp. Click one shaft with a belt, then the other, to link them.",
        "&eTip:&r belts make great machine feeders: items ride past presses and fans on their own."]),
    Q("cr_steam", 10, -4, [item("create:steam_engine", 2), item("create:fluid_tank", 4)], "Steam Engines", subtitle="Fire, water and pistons", deps=["cr_mixer"], xp=150, optional=True, tokens=2, desc=[
        "&eWhat:&r Create's boiler: a fluid tank full of water, heated by Blaze Burners, drives steam engines on its sides.",
        "&eChemistry:&r water expands about 1,600 times when it boils. That pressure pushes the pistons.",
        "&eHow:&r pump water into the tank, put fuelled Blaze Burners underneath, and place engines on its sides with a shaft in front. Check the Ponder.",
        "&eTip:&r a bigger tank and more burners raise the boiler level. Goggles show what's limiting it."]),

    # --- Pressing and mixing (y = -2) ----------------------------------------------------------
    Q("cr_press", 8, -2, [item("create:mechanical_press"), item("create:basin")], "Pressing and Mixing", subtitle="Plates and compacting", deps=["cr_belts"], xp=50, desc=[
        "&eWhat:&r the Mechanical Press flattens ingots into plates and compacts items in a basin.",
        "&eHow:&r put the press over a depot, a belt or a basin, and power it.",
        "&eTip:&r plates are shared with MI in this pack, so pressed plates work in MI recipes too."]),
    Q("cr_mixer", 10, -2, [item("create:mechanical_mixer"), item("create:blaze_burner")], "Heated Mixing", subtitle="Create's chemistry bench", deps=["cr_press", "t2_blaze"], xp=75, desc=[
        "&eWhat:&r a mixer over a basin, heated by a Blaze Burner, makes alloys and fluids.",
        "&eChemistry:&r heat speeds up reactions and melts metals so they can mix into alloys.",
        "&eHow:&r catch a blaze in an Empty Blaze Burner, put it under the basin, feed it fuel, and put the mixer above.",
        "&eTip:&r feed the burner with a deployer or a mechanical arm so it never goes cold."]),

    # --- Ores and tubes (y = 2) ----------------------------------------------------------------
    Q("cr_crush", 8, 2, [item("create:millstone"), item("create:crushing_wheel", 2)], "Crushing", subtitle="Ore into crushed ore", deps=["cr_belts"], xp=60, desc=[
        "&eWhat:&r millstones and crushing wheels grind ore into crushed ore and stone into gravel and sand.",
        "&eHow:&r two crushing wheels side by side, spinning toward each other. Drop items in from above.",
        "&eTip:&r in this pack they give at most &e2x per ore block&r, like everything before acids."]),
    Q("cr_wash", 10, 2, [item("create:encased_fan"), item("create:crushed_raw_iron", 8)], "Bulk Washing", subtitle="Water, a fan and a bonus", deps=["cr_crush"], xp=60, desc=[
        "&eWhat:&r an encased fan blowing through water washes crushed ore into nuggets plus a byproduct.",
        "&eHow:&r put flowing water in front of the fan and pass items through the air stream (a belt works).",
        "&eTip:&r washed crushed iron gives 9 nuggets and a 75% chance of redstone."]),
    Q("cr_rose", 12, 2, [item("create:rose_quartz", 4), item("create:polished_rose_quartz", 4)], "Rose Quartz", subtitle="Quartz soaked in redstone", deps=["cr_wash"], xp=60, desc=[
        "&eWhat:&r rose quartz, for electron tubes.",
        "&eHow:&r craft 1 Nether quartz with 8 redstone, then polish it: hold sandpaper with the rose quartz in your off-hand and use it (a deployer can do this too).",
        "&eTip:&r washing iron makes redstone, so your ore line can feed this."]),
    Q("cr_tube", 14, 2, [item("create:electron_tube", 4)], "Electron Tubes", subtitle="Create's 'smart' component", deps=["cr_rose"], xp=60, desc=[
        "&eWhat:&r electron tubes go into deployers, mechanical crafters and other smart machines.",
        "&eHow:&r polished rose quartz on top of an iron plate.",
        "&eTip:&r make a stack. You'll need more than you think."]),

    # --- Brass and precision (y = 0) ------------------------------------------------------------
    Q("cr_brass", 12, 0, [item("create:zinc_ingot", 8), item("create:brass_ingot", 8)], "Brass", subtitle="Copper plus zinc, mixed hot", deps=["cr_mixer"], xp=100, size=1.5, desc=[
        "&6A golden metal, mixed in a basin. The old skill comes back to your hands.&r",
        "&eWhat:&r brass, the key metal of Create's second age.",
        "&eChemistry:&r brass is a copper-zinc alloy, usually about two-thirds copper. Zinc makes it harder and gives the gold colour.",
        "&eHow:&r 1 copper + 1 zinc in a heated mixer gives 2 brass. Zinc ore generates in the world."]),
    Q("cr_brass_casing", 14, -1, [item("create:brass_casing", 8)], "Brass Casing", subtitle="The shell of smart machines", deps=["cr_brass"], xp=60, desc=[
        "&eWhat:&r brass casing, for mechanical crafters, arms and brass tunnels.",
        "&eHow:&r right-click a stripped log or stripped wood with a brass ingot.",
        "&eTip:&r a deployer holding brass ingots can apply it automatically."]),
    Q("cr_deployer", 16, 1, [item("create:brass_hand"), item("create:deployer", 2)], "Deployers", subtitle="A hand that uses items", deps=["cr_brass", "cr_tube"], xp=100, desc=[
        "&eWhat:&r a deployer acts like a player's hand: it places, uses and applies items.",
        "&eHow:&r an andesite casing, an electron tube and a brass hand (pressed brass sheets).",
        "&eTip:&r deployers over a belt are how Create builds things in steps: that's sequenced assembly."]),
    Q("cr_precision", 18, 0, [item("create:precision_mechanism"), item("create:mechanical_crafter", 4)], "Precision", subtitle="Your first sequenced assembly", deps=["cr_deployer", "cr_brass_casing"], xp=150, size=1.5, desc=[
        "&6Each step in its place, every time. You used to build worlds this way.&r",
        "&eWhat:&r the precision mechanism, made by sequenced assembly: one item passes the same stations several times.",
        "&eHow:&r start with a gold plate, then deploy a cogwheel, a large cogwheel and an iron nugget onto it, 5 loops. JEI shows the sequence.",
        "&eTip:&r some outputs are scrap. Sort them off the end of the belt and recycle them."]),
    Q("cr_arm", 18, -2, [item("create:mechanical_arm")], "Mechanical Arm", subtitle="Pick up here, put down there", deps=["cr_precision"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the mechanical arm moves items between depots, belts, basins and machines in its reach.",
        "&eHow:&r hold the arm and click inputs and outputs before you place it. Check the Ponder.",
        "&eTip:&r one arm can feed a whole ring of depots around it."]),

    # --- Electricity (x >= 20) ----------------------------------------------------------------
    Q("cr_alternator", 20, -1, [item("createaddition:alternator")], "Rotation to Electricity", subtitle="Spin a shaft, get FE", deps=["cr_precision", "t3_analog"], xp=150, desc=[
        "&eWhat:&r Crafts and Additions' Alternator turns rotation into FE.",
        "&eChemistry:&r a coil turning in a magnetic field pushes electrons along the wire: electromagnetic induction.",
        "&eHow:&r in this pack it needs an &eMI analog circuit&r (LV). Feed it fast rotation."]),
    Q("cr_motor", 20, 1, [item("createaddition:electric_motor")], "Electricity to Rotation", subtitle="Run contraptions off the grid", deps=["cr_alternator"], xp=100, desc=[
        "&eWhat:&r the Electric Motor turns FE back into rotation, with a speed you set.",
        "&eHow:&r give it FE from your MI or Mekanism grid and set the speed in its GUI.",
        "&eTip:&r motors free you from water wheels and windmills. Put a Create line anywhere."]),
    Q("cr_rolling", 22, -1, [item("createaddition:rolling_mill"), item("createaddition:connector", 4), item("createaddition:copper_spool")], "Wires and Connectors", subtitle="Overhead power lines", deps=["cr_alternator"], xp=100, desc=[
        "&eWhat:&r the Rolling Mill turns ingots into rods and plates into wire. Spools of wire link connectors into power lines.",
        "&eHow:&r roll copper plates into wire, wind it onto a spool, then click two connectors with the spool to string a wire.",
        "&eTip:&r connectors carry power over long gaps without cables on the ground."]),
    Q("cr_accumulator", 24, -1, [item("createaddition:capacitor", 2), item("createaddition:modular_accumulator")], "Accumulators", subtitle="Store FE in brass and capacitors", deps=["cr_rolling"], xp=100, desc=[
        "&eWhat:&r the Modular Accumulator stores FE, and several placed together merge into one bigger battery.",
        "&eChemistry:&r the capacitor here is zinc over copper, the same pair Volta used in the first battery in 1800.",
        "&eHow:&r needs brass casing, capacitors, copper rods and electrum wire. Electrum is gold + silver mixed hot.",
        "&eTip:&r put it between your alternators and your machines to smooth out spikes."]),
    Q("cr_newage", 22, -3, [item("create_new_age:generator_coil"), item("create_new_age:basic_energiser")], "Create: New Age", subtitle="Magnets, coils and energisers", deps=["cr_alternator"], xp=150, desc=[
        "&eWhat:&r magnet-and-coil generators, and Energisers that charge items with electricity.",
        "&eHow:&r the Generator Coil needs an analog circuit in this pack. Spin it among magnets; the Ponder shows the layout.",
        "&eTip:&r the Basic Energiser is just an andesite casing and a lightning rod."]),
    Q("cr_energiser", 24, -3, [item("create_new_age:overcharged_iron", 4)], "Charging Metal", subtitle="Iron soaked in electricity", deps=["cr_newage"], xp=100, desc=[
        "&eWhat:&r overcharged iron, made by charging an iron ingot in an Energiser.",
        "&eHow:&r power the Energiser with FE and put iron underneath it (on a depot or belt). Each ingot takes 1,000 FE.",
        "&eTip:&r overcharged metals make better wire and magnets."]),
    Q("cr_magnet", 24, -5, [item("create_new_age:layered_magnet", 4)], "Layered Magnets", subtitle="Stronger fields, more power", deps=["cr_energiser"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r stronger magnets for New Age generators.",
        "&eHow:&r overcharged iron and overcharged gold in layers (check JEI).",
        "&eTip:&r a stronger field induces more current in the same coil."]),
    Q("cr_reactor", 26, -3, [item("create_new_age:thorium", 8), item("create_new_age:reactor_rod")], "Thorium Reactor", subtitle="New Age goes nuclear", deps=["cr_energiser", "t6_pu"], xp=400, desc=[
        "&eWhat:&r New Age's nuclear reactor, fuelled by &ethorium&r.",
        "&eChemistry:&r thorium-232 isn't fissile itself; it absorbs a neutron and becomes uranium-233, which is.",
        "&eHow:&r the rods need an &eMI processing unit&r (EV), so it arrives alongside Mekanism fission. Check JEI and the Ponder for the build.",
        "&eTip:&r treat it like any reactor: cooling first, then power."]),

    # --- Experience (y = 3) --------------------------------------------------------------------
    Q("cr_xp", 20, 3, [item("create_enchantment_industry:mechanical_grindstone"), item("create_enchantment_industry:experience_bucket")], "Liquid Experience", subtitle="XP you can pipe", deps=["cr_precision"], xp=100, desc=[
        "&eWhat:&r Enchantment Industry turns experience into a fluid you can store and pipe.",
        "&eHow:&r the Mechanical Grindstone strips enchantments off items; a Grindstone Drain collects the XP as fluid. Check JEI.",
        "&eTip:&r feed it the enchanted junk from your mob farm."]),
    Q("cr_enchant", 22, 3, [item("create_enchantment_industry:blaze_enchanter")], "Automated Enchanting", subtitle="A blaze that reads spellbooks", deps=["cr_xp"], xp=100, desc=[
        "&eWhat:&r the Blaze Enchanter spends liquid XP to enchant items automatically.",
        "&eHow:&r it's a smithing upgrade of a Blaze Burner with an enchanting table (check JEI). Give it an enchanting template and XP.",
        "&eTip:&r put it beside a belt and a deployer for a hands-free enchanting line."]),
    Q("cr_printer", 24, 3, [item("create_enchantment_industry:printer")], "The Printer", subtitle="Copy books with XP", deps=["cr_enchant"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r the Printer copies written and enchanted books, paid for in liquid XP.",
        "&eHow:&r check JEI and the Ponder for the setup.",
        "&eTip:&r find a good enchanted book once, then print it as often as your XP lasts."]),

    # --- More Create: Connected (y=4) ----------------------------------------------------------
    Q("cr_battery", 6, 4, [item("create_connected:kinetic_battery")], "Kinetic Battery", deps=["cr_connected"], xp=40,
      optional=True, tokens=1, subtitle="Optional: store rotation for later", desc=[
        "&eWhat:&r the Kinetic Battery charges from rotation and gives it back later, so a windmill's power isn't wasted when nothing is running.",
        "&eHow:&r check JEI and its Ponder scene (hold W over it). Put it on a shaft line to charge it.",
        "&eTip:&r a charged battery can be picked up and moved, like a wind-up spring."]),

    # --- Biofuel (y=-4) ------------------------------------------------------------------------
    Q("cr_biofuel", 12, -4, [item("createaddition:seed_oil_bucket"), item("createaddition:bioethanol_bucket")], "Bioethanol", deps=["cr_mixer"], xp=75,
      optional=True, tokens=1, subtitle="Optional: fuel from fermented plants", desc=[
        "&eWhat:&r Crafts & Additions makes liquid fuel from plants: seed oil, then biomass, then bioethanol, which burns in a Liquid Blaze Burner.",
        "&eChemistry:&r real bioethanol comes from yeast fermenting sugar: C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂. Plant oils are triglycerides, long carbon chains that store a lot of energy.",
        "&eHow:&r compact seeds in a press and basin for seed oil; mix crops with seed oil over heat for biomass; mix biomass, sugar and cinder flour for bioethanol (check JEI).",
        "&eTip:&r it's a renewable fuel for Create steam engines that never touches your oil wells."]),

    # --- More electricity (x>=22) --------------------------------------------------------------
    Q("cr_tesla", 26, 0.5, [item("createaddition:tesla_coil")], "Tesla Coil", deps=["cr_accumulator"], xp=60,
      optional=True, tokens=1, subtitle="Optional: charge items with lightning", desc=[
        "&eWhat:&r the Tesla Coil charges FE items on belts or depots below it, and zaps anything that walks under it.",
        "&eHow:&r a mechanical crafting recipe with brass, a capacitor, electron tubes and a copper spool (check JEI). Power it with FE.",
        "&eTip:&r put a belt of jetpacks or gadgets under it for an automatic charging station."]),
    Q("cr_stirling", 22, -5, [item("create_new_age:stirling_engine"), item("create_new_age:basic_solar_heating_plate")], "Heat Engines", deps=["cr_newage"], xp=60,
      optional=True, tokens=1, subtitle="Optional: rotation from sunlight and heat", desc=[
        "&eWhat:&r New Age moves heat through heat pipes. Solar heating plates collect it from sunlight; a Stirling Engine turns it into slow rotation, and a Boiler Heater uses it in place of a blaze burner.",
        "&eChemistry:&r a real Stirling engine heats and cools a sealed gas. Hot gas expands and pushes a piston; cooled gas contracts and pulls it back. No fuel burns inside it.",
        "&eHow:&r heat pipes, iron and glass for the plate; a copper block, heat pipes and a shaft for the engine (check JEI and the Ponder scenes)."]),
], links=[("gs_iron", -2, 0), ("t3_analog", 20, -3), ("t6_pu", 26, -5)])
