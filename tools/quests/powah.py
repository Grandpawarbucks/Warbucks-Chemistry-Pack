"""Quest chapter: powah (side page). See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

P = "powah:"

# Layout: y=0 spine (dielectric parts -> starter tier -> Energizing Orb -> rods and crystal gear),
# y=-2 generators and the hardened tier, y=2 early utilities and (from x=20) links to the crystal
# quests in the Power chapter, y=4 ender network, y=-6 reactor. Optional quests sit off those rows.
# Starter and basic Powah blocks need no Orb, so they are available early (Furnator for FE at t1).
# Everything from energized steel up goes through the Orb, which the pack gates on the MV circuit.
CHAPTER = Chapter("powah", "Powah!", P + "energizing_orb",
        ["Powah: dielectric parts, the Energizing Orb, crystal tiers, generators, cells and wireless power. "
         "The starter tier is open early; the Orb needs an MI electronic circuit (MV)."], SIDE, [

    # --- Dielectric parts and the starter tier (y = 0) -------------------------------------------
    Q("pw_paste", 0, 0, [item(P + "dielectric_paste", 16)], "Dielectric Paste", subtitle="Coal, clay and heat", deps=["t1_power"], xp=40, desc=[
        "&6Insulators and conductors. You remember that power is mostly about where it is not allowed to go.&r",
        "&eWhat:&r the base of every Powah block: rods, casings, capacitors and cables.",
        "&eChemistry:&r a dielectric is an insulator that polarises in an electric field. Fired clay (aluminosilicates such as kaolinite, Alâ‚‚Siâ‚‚Oâ‚…(OH)â‚„) is the porcelain on real power-line insulators.",
        "&eHow:&r shapeless: 3 coal or charcoal + 2 clay balls + a lava bucket makes 24. Or 2 coal + 1 clay ball + 1 blaze powder for 16.",
        "&eTip:&r the lava recipe gives more per craft and keeps the bucket. Make a stack."]),
    Q("pw_rods", 2, 0, [item(P + "dielectric_rod", 8), item(P + "dielectric_rod_horizontal", 8)], "Dielectric Rods", subtitle="Paste set around iron bars", deps=["pw_paste"], xp=40, desc=[
        "&eWhat:&r insulated rods, upright and horizontal. Both go into casings, the Orb, cables and cards.",
        "&eHow:&r 6 paste around 3 iron bars: a vertical line of bars for the upright rod, a horizontal line for the horizontal one. 8 per craft.",
        "&eTip:&r you'll need far more horizontal rods than upright ones; every cable craft eats six."]),
    Q("pw_casing", 4, 0, [item(P + "dielectric_casing", 2)], "Dielectric Casing", subtitle="The shell of every Powah block", deps=["pw_rods"], xp=40, desc=[
        "&eWhat:&r the frame inside almost every Powah machine, cell and generator.",
        "&eHow:&r 4 iron ingots in the corners, horizontal rods top and bottom, upright rods in the middle row (check JEI)."]),
    Q("pw_capacitor", 6, 0, [item(P + "capacitor_basic", 4), item(P + "capacitor_basic_tiny", 2)], "Capacitors", subtitle="Two plates and an insulator", deps=["pw_casing"], xp=50, desc=[
        "&eWhat:&r capacitors set a block's tier. The tiny ones go into starter blocks, the basic ones into basic blocks.",
        "&eChemistry:&r a capacitor is two conductors separated by a dielectric. It stores E = Â½CVÂ², and a better dielectric raises the capacitance C.",
        "&eHow:&r iron ingots, paste and a redstone block make 4 basic capacitors. One basic capacitor splits into 2 tiny ones.",
        "&eTip:&r two basic capacitors combine into a large one, which the hardened tier needs later."]),
    Q("pw_cable", 8, 0, [item(P + "energy_cable_starter", 12)], "Energy Cables", subtitle="Wires that know their tier", deps=["pw_capacitor"], xp=40, desc=[
        "&eWhat:&r Powah's cables. Each tier carries more FE per tick.",
        "&eHow:&r 6 horizontal rods, 2 iron nuggets and a tiny capacitor make 12 starter cables.",
        "&eTip:&r cables connect to any FE block, not just Powah ones. Use the Powah wrench to configure sides."]),
    Q("pw_cell_starter", 10, 0, [item(P + "energy_cell_starter")], "Starter Energy Cell", subtitle="A first Powah battery block", deps=["pw_cable"], xp=50, desc=[
        "&eWhat:&r the smallest Powah cell. Enough to smooth out a furnator's output.",
        "&eHow:&r iron ingots in the corners, tiny capacitors on the sides, a dielectric casing in the middle.",
        "&eTip:&r the basic cell is the same recipe with basic capacitors. The bigger tiers come with energized steel and crystals."]),

    # --- Starter generators (y = -2) ---------------------------------------------------------------
    Q("pw_wrench", 2, -2, [item(P + "wrench")], "Powah Wrench", subtitle="Rotate, configure, link", deps=["pw_paste"], xp=30, optional=True, tokens=1, desc=[
        "&eWhat:&r Powah's wrench. It has Rotate, Config and Link modes; the mode shows on the item.",
        "&eHow:&r iron ingots and dielectric paste (check JEI).",
        "&eTip:&r Config mode sets which sides of a cell or generator push or take power."]),
    Q("pw_furnator", 8, -2, [item(P + "furnator_starter")], "Furnator", subtitle="Burn fuel, make FE", deps=["pw_capacitor"], xp=50, desc=[
        "&eWhat:&r a Powah generator that burns furnace fuel for FE. It's an early way to run the Dissolver.",
        "&eChemistry:&r burning oxidises carbon. Coke burns cleaner and longer than coal because its volatile tars were already driven off.",
        "&eHow:&r paste, 2 tiny capacitors, a dielectric casing and a furnace.",
        "&eTip:&r feed it coke from your coke ovens for long runs."]),
    Q("pw_magmator", 10, -2, [item(P + "magmator_starter")], "Magmator", subtitle="Power from molten rock", deps=["pw_furnator"], xp=50, desc=[
        "&eWhat:&r a generator that burns lava (and other hot fluids) instead of solid fuel.",
        "&eChemistry:&r lava is molten silicate rock at roughly 700 to 1,200 Â°C. The Magmator draws that stored heat off as FE.",
        "&eHow:&r like the Furnator, but with a bucket in place of the furnace. JEI's Magmatic Fluids list shows what it accepts.",
        "&eTip:&r a Nether lava lake and a pump give endless fuel."]),
    Q("pw_gen_basic", 12, -2, [anyof([P + "furnator_basic", P + "magmator_basic", P + "thermo_generator_basic", P + "solar_panel_basic"])], "Basic Generators", subtitle="Upgrade a starter generator", deps=["pw_furnator", "pw_magmator"], any_dep=True, xp=60, desc=[
        "&eWhat:&r every Powah block upgrades by crafting the lower tier into the next one. Basic is the first step.",
        "&eHow:&r a starter generator in the bottom middle, iron ingots, 2 basic capacitors and a dielectric casing (check JEI).",
        "&eTip:&r upgrading keeps the old block's cost, so you never waste a starter."]),

    # --- Early utilities (y = 2) -------------------------------------------------------------------
    Q("pw_pearl", 2, 2, [item(P + "player_aerial_pearl")], "Player Aerial Pearl", subtitle="A pearl that remembers someone", deps=["pw_paste"], xp=40, desc=[
        "&eWhat:&r the core of the Player Transmitter.",
        "&eHow:&r craft an Aerial Pearl (an ender pearl in iron bars and paste), then use it on a Zombie or a Husk.",
        "&eTip:&r trap a zombie near your base so you can make more later."]),
    Q("pw_transmitter", 4, 2, [item(P + "player_transmitter_starter"), item(P + "binding_card")], "Player Transmitter", subtitle="Charge your gear wirelessly", deps=["pw_pearl", "pw_capacitor"], xp=60, desc=[
        "&eWhat:&r a block that charges the FE items carried by the player bound to it.",
        "&eHow:&r Player Aerial Pearl on top, tiny capacitors and a casing in the middle, an upright rod below. The Binding Card is a blank card (2 horizontal rods) with redstone and rotten flesh; right-click to bind it to yourself.",
        "&eTip:&r power it from a cell and your jetpack never runs dry at home."]),
    Q("pw_photo", 6, 2, [item(P + "photoelectric_pane", 3), item(P + "thermoelectric_plate", 3)], "Panes and Plates", subtitle="The parts of solar and thermo generators", deps=["pw_capacitor"], xp=50, desc=[
        "&eWhat:&r photoelectric panes go into Powah solar panels; thermo plates go into thermo generators (both in the Power chapter).",
        "&eChemistry:&r light can knock electrons out of a material: the photoelectric effect Einstein explained in 1905. Lapis gets its blue from trisulfur radical ions (Sâ‚ƒâ») trapped in the mineral lazurite.",
        "&eHow:&r pane: a glass pane in lapis and paste. Plate: a tiny capacitor in redstone and blaze powder.",
        "&eTip:&r blaze powder means a trip to the Nether first."]),
    Q("pw_hopper", 8, 2, [item(P + "energy_hopper_starter"), item(P + "energy_discharger_starter")], "Hopper and Discharger", subtitle="Charge items, drain items", deps=["pw_cell_starter"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r the Energy Hopper charges FE items in the container it faces; the Energy Discharger pulls FE back out of items put in it.",
        "&eHow:&r both are a dielectric casing, tiny capacitors and paste; the hopper also takes a vanilla hopper (check JEI).",
        "&eTip:&r a hopper on a chest of tools makes a charging station."]),
    Q("pw_battery", 10, 2, [item(P + "battery_starter")], "Batteries", subtitle="FE you can carry", deps=["pw_cell_starter"], xp=40, optional=True, tokens=1, desc=[
        "&eWhat:&r Powah batteries are items that hold FE. Higher tiers hold more.",
        "&eHow:&r basic capacitors, a redstone block and paste. Check its tooltip for how it charges your gear.",
        "&eTip:&r fill it from an Energy Hopper, empty it in a Discharger."]),
    Q("pw_dim_card", 6, 4, [item(P + "binding_card_dim")], "Dimensional Binding Card", subtitle="A card touched by the End", deps=["pw_transmitter"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r the dimensional version of the Binding Card, for transmitters and other Powah blocks that take a card.",
        "&eHow:&r use a Binding Card on an Enderman or an Endermite.",
        "&eTip:&r read its tooltip to see what it does differently from the plain card."]),

    # --- The Energizing Orb and rods (y = 0) -------------------------------------------------------
    Q("pw_orb", 14, 0, [item(P + "energizing_orb"), item(P + "energizing_rod_starter", 2)], "The Energizing Orb", subtitle="Pack gate: needs an MV electronic circuit", deps=["pw_cell_starter", "t4_circuit"], xp=150, size=1.5, shape="hexagon", desc=[
        "&6A glass sphere that fills with light. You remember charging things just by holding them.&r",
        "&eWhat:&r the Orb turns FE into new materials: energized steel, crystals, ender cores. Every Powah tier above basic needs it.",
        "&eHow:&r in this pack: glass on top and sides, an MI &eelectronic circuit&r on each side of a dielectric casing in the middle, and 3 horizontal rods on the bottom. Rods: quartz, tiny capacitors, a casing and an upright rod.",
        "&eHow:&r place the orb, aim Energizing Rods at it from nearby, feed the rods FE and put the ingredients in the orb. JEI's Energizing tab shows each recipe and its FE cost.",
        "&eTip:&r the first job is uraninite and energized steel: see the Main Path and Power chapter links."]),
    Q("pw_snowball", 12, 2, [item(P + "charged_snowball", 4)], "Charged Snowball", subtitle="A pocket thunderstorm", deps=["pw_orb"], xp=50, optional=True, tokens=1, desc=[
        "&eWhat:&r a snowball charged with 500,000 FE. Throw it and lightning strikes where it lands.",
        "&eChemistry:&r a lightning channel heats air to around 30,000 K, hotter than the Sun's surface. It splits Nâ‚‚ and Oâ‚‚, and the nitrogen oxides it makes fertilise the soil.",
        "&eHow:&r one snowball in the Energizing Orb.",
        "&eTip:&r lightning turns a pig into a zombified piglin and a villager into a witch. Aim carefully."]),
    Q("pw_rod_up", 16, 0, [item(P + "energizing_rod_basic", 2)], "Better Rods", subtitle="Quartz focuses the charge", deps=["pw_orb"], xp=75, desc=[
        "&eWhat:&r higher-tier rods pour FE into the orb faster. Several rods stack.",
        "&eChemistry:&r quartz is crystalline SiOâ‚‚ and is piezoelectric: squeeze it and it makes a voltage. Every quartz watch keeps time with a vibrating crystal.",
        "&eHow:&r a block of quartz on top, basic capacitors and a casing in the middle, a starter rod below.",
        "&eTip:&r crystals cost hundreds of thousands of FE. More and better rods matter more than anything else here."]),
    Q("pw_rod_hardened", 18, 0, [item(P + "energizing_rod_hardened", 2)], "Hardened Rods", subtitle="Energized steel capacitors in a rod", deps=["pw_rod_up", "pw_cap_hardened"], xp=75, desc=[
        "&eWhat:&r the hardened rod, another step in charging speed.",
        "&eHow:&r a block of quartz, hardened capacitors, a casing and a basic rod below.",
        "&eTip:&r every rod tier is built from the one before, so keep upgrading the same rods."]),

    # --- Hardened tier and generators (y = -2) -----------------------------------------------------
    Q("pw_cap_hardened", 18, -2, [item(P + "capacitor_basic_large", 2), item(P + "capacitor_hardened", 2)], "Hardened Capacitors", subtitle="The first capacitor that needs the Orb", deps=["pw_energized"], xp=75, desc=[
        "&eWhat:&r hardened capacitors unlock the hardened tier of everything.",
        "&eHow:&r 2 basic capacitors make a large one. A large capacitor in energized steel and paste makes 2 hardened capacitors.",
        "&eTip:&r large capacitors go into every crystal capacitor too. Craft spares."]),
    Q("pw_cable_hardened", 20, -2, [item(P + "energy_cable_basic", 6), item(P + "energy_cable_hardened", 12)], "Hardened Cables", subtitle="More FE per tick", deps=["pw_cap_hardened"], xp=60, desc=[
        "&eWhat:&r faster cables for your growing grid.",
        "&eHow:&r basic: 6 rods, 2 starter cables, a basic capacitor. Hardened: 6 rods, 2 energized steel, a hardened capacitor makes 12 (check JEI).",
        "&eTip:&r a cable is only as fast as its slowest segment. Upgrade the trunk line first."]),
    Q("pw_cell_hardened", 22, -2, [item(P + "energy_cell_hardened")], "Hardened Energy Cell", subtitle="A real buffer", deps=["pw_cap_hardened", "pw_powah_cell"], xp=100, desc=[
        "&eWhat:&r the next storage step after the basic cell.",
        "&eHow:&r 2 basic cells, energized steel, hardened capacitors and a dielectric casing.",
        "&eTip:&r the crystal cells in the Power chapter each start from the cell below them."]),
    Q("pw_gen_hardened", 24, -2, [anyof([P + "furnator_hardened", P + "magmator_hardened", P + "thermo_generator_hardened", P + "solar_panel_hardened"])], "Hardened Generators", subtitle="Energized steel around a generator", deps=["pw_cap_hardened", "pw_gen_basic"], xp=100, desc=[
        "&eWhat:&r a hardened Furnator, Magmator, Thermo Generator or Solar Panel. Any one counts.",
        "&eHow:&r the basic generator plus energized steel, hardened capacitors and a casing (check JEI).",
        "&eTip:&r a hardened thermo generator on lava with water fed in is quiet, fuel-free power."]),
    Q("pw_gen_blazing", 26, -2, [anyof([P + "furnator_blazing", P + "magmator_blazing", P + "thermo_generator_blazing", P + "solar_panel_blazing"])], "Blazing Generators", subtitle="Crystal-tier power", deps=["pw_gen_hardened", "pw_blazing_gear"], xp=125, desc=[
        "&eWhat:&r any blazing-tier generator. Output takes a big jump here.",
        "&eHow:&r the hardened generator plus blazing crystals, blazing capacitors and a casing.",
        "&eTip:&r feed the orb's rods from these and the next crystal tier comes quicker."]),
    Q("pw_gen_niotic", 28, -2, [anyof([P + "furnator_niotic", P + "magmator_niotic", P + "thermo_generator_niotic", P + "solar_panel_niotic"])], "Niotic Generators", subtitle="Optional: diamond-tier power", deps=["pw_gen_blazing", "pw_niotic_gear"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r any niotic-tier generator. Spirited and nitro follow the same pattern.",
        "&eHow:&r the blazing generator plus niotic crystals, niotic capacitors and a casing (check JEI)."]),

    # --- Crystal gear (y = 0); the crystals themselves are in the Power chapter (links at y = 2) -----
    Q("pw_blazing_gear", 22, 0, [item(P + "capacitor_blazing", 2), item(P + "energizing_rod_blazing")], "Blazing Gear", subtitle="Capacitor and rod from blazing crystals", deps=["pw_blazing", "pw_rod_hardened"], xp=100, desc=[
        "&eWhat:&r the blazing capacitor is the key part of every blazing block; the blazing rod charges the orb faster still.",
        "&eHow:&r capacitor: a large capacitor in blazing crystals and paste (makes 2). Rod: quartz block, blazing capacitors, a casing and a hardened rod.",
        "&eTip:&r a blaze farm (or a Hostile Neural Networks blaze model) keeps the crystals coming."]),
    Q("pw_niotic_gear", 26, 0, [item(P + "capacitor_niotic", 2), item(P + "energizing_rod_niotic")], "Niotic Gear", subtitle="Diamond in the capacitor", deps=["pw_niotic", "pw_blazing_gear"], xp=125, desc=[
        "&eWhat:&r niotic capacitors and the niotic rod.",
        "&eChemistry:&r diamond is an excellent electrical insulator but conducts heat better than copper, because its stiff carbon lattice carries vibrations so well.",
        "&eHow:&r capacitor: a large capacitor in niotic crystals and paste. Rod: quartz block, niotic capacitors, a casing and a blazing rod.",
        "&eTip:&r niotic cables (6 rods, 2 niotic crystals, a niotic capacitor) carry far more FE."]),
    Q("pw_spirited_gear", 30, 0, [item(P + "capacitor_spirited", 2), item(P + "energizing_rod_spirited")], "Spirited Gear", subtitle="Emerald in the capacitor", deps=["pw_spirited", "pw_niotic_gear"], xp=150, desc=[
        "&eWhat:&r spirited capacitors and the spirited rod, one step below the top.",
        "&eHow:&r capacitor: a large capacitor in spirited crystals and paste. Rod: quartz block, spirited capacitors, a casing and a niotic rod.",
        "&eTip:&r each spirited crystal costs 1,000,000 FE. Run several spirited rods before you try for nitro."]),
    Q("pw_nitro_gear", 34, 3.5, [item(P + "energizing_rod_nitro"), item(P + "energy_cell_nitro")], "Nitro", subtitle="Optional: the top of the Powah ladder", deps=["pw_nitro", "pw_spirited_gear"], xp=300, optional=True, tokens=2, size=1.5, shape="gear", desc=[
        "&6Twenty million FE poured into a star. You remember power like this; it used to be yours.&r",
        "&eWhat:&r the nitro rod and nitro energy cell, the strongest Powah blocks.",
        "&eHow:&r nitro capacitor: a large capacitor in nitro crystals and paste. Rod: quartz block, nitro capacitors, a casing and a spirited rod. Cell: nitro crystals, nitro capacitors, 2 spirited cells and a casing.",
        "&eTip:&r the nitro crystal recipe needs a block of 9 blazing crystals, so save some blazing crystals for it."]),

    # --- Ender network (y = 4) ---------------------------------------------------------------------
    Q("pw_ender_core", 14, 4, [item(P + "ender_core", 2)], "Ender Core", subtitle="An eye of ender, energized", deps=["pw_orb"], xp=75, desc=[
        "&eWhat:&r the heart of Ender Cells and Ender Gates.",
        "&eHow:&r Energizing Orb: an eye of ender, a dielectric casing and a tiny capacitor, 50,000 FE.",
        "&eTip:&r one core per ender block, at every tier."]),
    Q("pw_ender_gate", 16, 4, [item(P + "ender_gate_starter", 4)], "Ender Gates", subtitle="Small taps on the ender network", deps=["pw_ender_core"], xp=75, desc=[
        "&eWhat:&r ender gates connect to the same ender energy network as your Ender Cells, without storing much themselves.",
        "&eHow:&r obsidian, 2 starter cables and an ender core make 4. Set the channel in the GUI to match your cells.",
        "&eTip:&r put a gate next to each remote machine and one Ender Cell at your main bank."]),

    # --- Reactor (y = -6) --------------------------------------------------------------------------
    Q("pw_coolant", 20, -6, [item(P + "dry_ice", 4)], "Dry Ice", subtitle="A solid coolant for the reactor", deps=["pw_powah"], xp=75, desc=[
        "&eWhat:&r a strong solid coolant for the Powah reactor. Cooler reactors waste less fuel.",
        "&eChemistry:&r real dry ice is solid COâ‚‚, which sublimes straight to gas at -78.5 Â°C. Powah's is made from energized blue ice, which is Hâ‚‚O, so take the name loosely.",
        "&eHow:&r Energizing Orb: 2 blue ice, 10,000 FE. JEI's Coolants and Solid Coolants tabs list every option and its strength.",
        "&eTip:&r the reactor also takes carbon and redstone to boost it. Check its GUI slots."]),
    Q("pw_reactor_hardened", 22, -6, [item(P + "reactor_hardened", 36)], "Hardened Reactor", subtitle="Optional: rebuild the reactor a tier up", deps=["pw_coolant", "pw_cap_hardened"], xp=200, optional=True, tokens=2, desc=[
        "&eWhat:&r a hardened reactor, much stronger than the basic one.",
        "&eChemistry:&r uraninite (UOâ‚‚) holds U-235, which splits when it absorbs a neutron and releases more neutrons and heat.",
        "&eHow:&r 4 basic reactor blocks, 4 hardened capacitors and 1 uraninite make 4 hardened blocks. Every block in the stack must be the same tier.",
        "&eTip:&r blazing, niotic, spirited and nitro reactors follow the same recipe with that tier's capacitor."]),

], links=[("t1_power", -2, 0), ("t4_circuit", 14, -2), ("t4_uraninite", 16, -4), ("pw_energized", 16, -2),
          ("pw_powah_cell", 22, -4), ("pw_powah", 18, -6), ("pw_blazing", 20, 2), ("pw_niotic", 24, 2),
          ("pw_spirited", 28, 2), ("pw_nitro", 32, 2), ("pw_ender", 18, 4), ("pw_solar", 6, 6), ("pw_thermo", 8, 6)])
