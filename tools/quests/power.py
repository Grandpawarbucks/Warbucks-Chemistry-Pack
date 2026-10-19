"""Quest chapter: power. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

# Layout: y=-2 combustion, y=-4 nuclear, y=0 storage (Mekanism -> induction -> Flux),
# y=2 MI steam and EU, y=4 Powah, y=6 renewables. Optional quests sit at the row ends / off-row.
CHAPTER = Chapter("power", "Power", "mekanismgenerators:gas_burning_generator",
        ["Energy is chemistry too: combustion, gas burning, fission and fusion."], SIDE, [
    Q("pw_iron_gen", 0, 0, [tick()], "Choosing Your Power", subtitle="A catalogue of every way to make FE and EU", deps=["t1_power"], xp=40,
      size=1.5, shape="hexagon", desc=[
        "&6You remember holding lightning. For now, the generator you built in T1 will do.&r",
        "&eWhat:&r this page lists the pack's power options by row: combustion, storage, MI steam and EU, Powah, renewables and nuclear. Pick the lines that suit your base; most are optional.",
        "&eChemistry:&r every generator turns some stored energy into current: chemical bonds (C + O₂ → CO₂), sunlight, wind, heat, or the nucleus itself.",
        "&eHow:&r start from the Generator Galore generator you made for Forge Energy (FE), the power most mods share. Click the checkmark to open the page.",
        "&eTip:&r MI machines run on EU, Modern Industrialization's own electricity (the MI steam and EU row). Most other mods run on FE."]),

    # --- Combustion (y = -2) -----------------------------------------------------------------
    Q("pw_gold_gen", 2, -2, [item("generatorgalore:gold_generator")], "A Faster Burn", optional=True, tokens=1, subtitle="Optional: same fuel, more FE per tick", deps=["pw_iron_gen"], xp=60, desc=[
        "&eWhat:&r the next Generator Galore tier: it burns fuel faster and makes more FE per tick.",
        "&eHow:&r upgrade from the iron generator (check JEI for the recipe).",
        "&eTip:&r a faster burn needs a steadier fuel supply. Pipe in charcoal from a tree farm."]),
    Q("pw_gg_collection", 2, -4, [item("generatorgalore:diamond_generator"), item("generatorgalore:culinary_generator"), item("generatorgalore:magmatic_generator"), item("generatorgalore:halitosis_generator")],
      "Generator Collector", subtitle="Four odd ways to make FE", deps=["pw_gold_gen"], xp=200, optional=True, tokens=2, desc=[
        "&eWhat:&r a diamond-tier generator plus three that burn strange fuels.",
        "&eHow:&r each one's tooltip and JEI page show what it burns. The Halitosis Generator wants dragon's breath, so plan an End trip.",
        "&eTip:&r the Culinary Generator eats spare food. Hook it to a farm's overflow."]),
    Q("pw_bio", 0, -2, [item("mekanismgenerators:bio_generator")], "Bio Fuel", subtitle="Crops into power", deps=["pw_heat"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r Mekanism's Bio-Generator burns Bio Fuel.",
        "&eChemistry:&r plants store sunlight as sugars and cellulose. Burning them releases it, and the CO₂ is the same CO₂ the plant took in.",
        "&eHow:&r crush seeds and crops into Bio Fuel in a Mekanism Crusher."]),
    Q("pw_gas", 4, -2, [item("mekanismgenerators:gas_burning_generator")], "Burning Hydrogen", optional=True, tokens=1, subtitle="Optional: the cleanest combustion there is", deps=["pw_iron_gen", "t4_separator"], xp=150, desc=[
        "&eWhat:&r the Gas-Burning Generator turns flammable gas into FE.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O + energy. The only exhaust is water.",
        "&eHow:&r pipe hydrogen from your Electrolytic Separator in with pressurized tubes.",
        "&eTip:&r electrolysis costs more energy than burning hydrogen returns. Use it to store spare power, not to make it."]),
    Q("pw_diesel", 6, -2, [item("modern_industrialization:mv_diesel_generator")], "Diesel Generators", optional=True, tokens=1, subtitle="Optional: petrochemical power", deps=["pw_iron_gen", "t5_diesel"], xp=150, desc=[
        "&eWhat:&r MI generators that burn the fuels from your distillation tower.",
        "&eChemistry:&r diesel is a mix of hydrocarbons around C₁₂ to C₂₀. Long chains pack lots of C-H bonds, and lots of energy.",
        "&eHow:&r pipe diesel into the generator and cable it to your machines."]),
    Q("pw_large_diesel", 8, -2, [item("modern_industrialization:large_diesel_generator")], "Large Diesel Generator", optional=True, tokens=1, subtitle="Optional: factory-scale combustion", deps=["pw_diesel", "t5_hv"], xp=250, desc=[
        "&eWhat:&r a multiblock diesel generator for real factories.",
        "&eHow:&r the 3D layout is in JEI and the MI guidebook. It needs fluid input and energy output hatches.",
        "&eTip:&r refined fuels (like boosted diesel) burn for more EU per bucket. Check JEI."]),

    # --- Storage (y = 0) ---------------------------------------------------------------------
    Q("pw_heat", 2, 0, [item("mekanismgenerators:heat_generator")], "Heat Generator", subtitle="Mekanism's starter generator", deps=["pw_iron_gen", "t3_infuser"], xp=60, desc=[
        "&eWhat:&r Mekanism's first generator. It burns fuel and turns heat into FE.",
        "&eHow:&r place lava next to it for a passive bonus, and feed it fuel for more.",
        "&eTip:&r lava from a pump makes this a decent passive generator early on."]),
    Q("pw_cube", 4, 0, [item("mekanism:basic_energy_cube")], "Store It", subtitle="A buffer for your grid", deps=["pw_heat"], xp=60, desc=[
        "&eWhat:&r energy cubes hold FE so short spikes don't stall your machines.",
        "&eHow:&r put one between your generators and machines. Configure its sides with the Configurator.",
        "&eTip:&r cubes upgrade in place: craft the next tier around the old one."]),
    Q("pw_adv_cube", 6, 0, [item("mekanism:advanced_energy_cube")], "Bigger Cubes", subtitle="Alloys and energy tablets around the cube below", deps=["pw_cube", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the Advanced Energy Cube holds and moves much more energy.",
        "&eHow:&r a basic cube with infused alloy, osmium ingots and energy tablets around it (check JEI). Upgrading in place keeps the stored energy.",
        "&eTip:&r Elite and Ultimate cubes follow the same pattern with reinforced and atomic alloys."]),
    Q("pw_brine", 8, 0, [item("mekanism:thermal_evaporation_controller"), item("mekanism:brine_bucket")], "Evaporation Ponds", subtitle="Sunlight and heat concentrate brine", deps=["pw_adv_cube"], xp=150, desc=[
        "&eWhat:&r the Thermal Evaporation Plant boils water down into brine, and brine down into liquid lithium.",
        "&eChemistry:&r real lithium comes from salt flats: brine sits in ponds until the water evaporates and the salts concentrate.",
        "&eHow:&r a multiblock tower of Thermal Evaporation Blocks, Valves and one Controller. See Just Enough Mekanism Multiblocks in JEI.",
        "&eTip:&r taller towers and more heat run faster. Feed it plain water."]),
    Q("pw_lithium", 10, 0, [item("mekanism:dust_lithium", 8)], "Lithium", subtitle="The battery metal", deps=["pw_brine"], xp=150, desc=[
        "&eWhat:&r lithium dust, for induction cells (and later, tritium).",
        "&eChemistry:&r lithium is the lightest metal and gives up its electron easily, which is why lithium-ion batteries store so much energy for their weight.",
        "&eHow:&r run brine through the plant again for liquid lithium. Turn it into gas in a Rotary Condensentrator, then crystallise it in a Chemical Crystallizer.",
        "&eTip:&r check JEI with &eR&r on Lithium Dust to confirm each step."]),
    Q("pw_induction", 12, 0, [item("mekanism:induction_casing", 16), item("mekanism:induction_port"), item("mekanism:basic_induction_cell"), item("mekanism:basic_induction_provider")],
      "Induction Matrix", subtitle="One multiblock battery for the whole base", deps=["pw_lithium"], xp=300, size=1.5, shape="hexagon", desc=[
        "&6Power stored, waiting, obedient. This feels familiar.&r",
        "&eWhat:&r a hollow multiblock battery. Cells inside set how much it stores; providers set how fast it charges and discharges.",
        "&eHow:&r casings form the shell (Structural Glass works for the walls), ports move energy in and out. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r switch one port to output with the Configurator. Start small; you can rebuild it larger later."]),
    Q("pw_flux_storage", 14, 0, [item("fluxnetworks:basic_flux_storage"), item("fluxnetworks:flux_plug"), item("fluxnetworks:flux_point")], "Wireless Grid", optional=True, tokens=1, subtitle="Optional: power anywhere, no cables", deps=["pw_induction", "t6_pu"], xp=300, desc=[
        "&eWhat:&r Flux Networks sends power through the air: Plugs take it in, Points give it out, Storage buffers it.",
        "&eHow:&r the Flux Core needs an &eMI processing unit&r (EV) in this pack. Link all devices to one network in their GUI.",
        "&eTip:&r put a Flux Plug on your induction matrix's output port and every Point on the network draws from it."]),

    # --- MI steam and EU (y = 2) ---------------------------------------------------------------
    Q("pw_mi_storage", 2, 2, [item("modern_industrialization:lv_storage_unit")], "EU Storage", subtitle="A battery for MI's grid", deps=["pw_iron_gen", "t3_hull"], xp=60, desc=[
        "&eWhat:&r MI's storage unit holds EU, Modern Industrialization's electricity.",
        "&eHow:&r built from redstone batteries, battery alloy plates and an LV hull. Put it between your turbine and your machines.",
        "&eTip:&r a buffer lets your steam turbine keep running while machines are idle."]),
    Q("pw_mv_turbine", 4, 2, [item("modern_industrialization:mv_steam_turbine")], "MV Steam Turbine", optional=True, tokens=1, subtitle="Optional: more steam, more EU", deps=["pw_mi_storage", "t4_mv"], xp=100, desc=[
        "&eWhat:&r a bigger steam turbine that outputs MV power.",
        "&eChemistry:&r a turbine converts the energy of hot, expanding steam into rotation, then a generator turns rotation into current.",
        "&eHow:&r assemble it from an MV hull, aluminum rotors and large motors (check JEI)."]),
    Q("pw_transformer", 6, 2, [item("modern_industrialization:lv_mv_transformer")], "Transformers", optional=True, tokens=1, subtitle="Optional: step voltage between tiers", deps=["pw_mv_turbine"], xp=75, desc=[
        "&eWhat:&r a transformer moves energy between two neighbouring voltage tiers (LV and MV here).",
        "&eHow:&r place it between an MV cable and your LV machines (or the other way round). Check which face is which in its tooltip.",
        "&eTip:&r real grids do the same: high voltage for transmission, low voltage at the socket."]),
    Q("pw_hv_turbine", 8, 2, [item("modern_industrialization:hv_steam_turbine")], "HV Steam Turbine", optional=True, tokens=1, subtitle="Optional: high-voltage steam", deps=["pw_transformer", "t5_hv"], xp=150, desc=[
        "&eWhat:&r the HV steam turbine, for HV machine lines.",
        "&eHow:&r check JEI for the recipe. Feed it from a large boiler.",
        "&eTip:&r more steam than one turbine can eat? Add a second turbine on the same steam line."]),
    Q("pw_large_turbine", 10, 2, [item("modern_industrialization:large_steam_turbine")], "Large Steam Turbine", optional=True, tokens=1, subtitle="Optional: power-station scale", deps=["pw_hv_turbine", "t6_pu"], xp=300, desc=[
        "&eWhat:&r MI's multiblock steam turbine. It eats steam by the thousands of mB and makes serious EU.",
        "&eHow:&r the controller needs an HV steam turbine, a processing unit (EV) and a highly advanced hull. Layout: JEI or the MI guidebook.",
        "&eTip:&r pair it with a large boiler or a reactor's steam output."]),

    # --- Powah (y = 4) -------------------------------------------------------------------------
    Q("pw_energized", 2, 4, [item("powah:steel_energized", 8)], "Energized Steel", subtitle="Iron and gold, charged together", deps=["pw_iron_gen", "t4_uraninite"], xp=100, desc=[
        "&eWhat:&r Powah's basic alloy, made by the Energizing Orb.",
        "&eHow:&r place Energizing Rods aimed at the orb and power them. Put 1 iron + 1 gold in the orb for 2 Energized Steel.",
        "&eTip:&r more rods (and better rods) charge faster."]),
    Q("pw_powah_cell", 4, 4, [item("powah:energy_cell_basic")], "Powah Energy Cells", subtitle="Stack your storage", deps=["pw_energized"], xp=100, desc=[
        "&eWhat:&r Powah's energy storage block, with tiers from Starter to Nitro.",
        "&eHow:&r iron, a dielectric casing and Powah capacitors. Higher tiers use better capacitors and crystals (check JEI).",
        "&eTip:&r cells pass power through each other, so a wall of them makes one big buffer."]),
    Q("pw_thermo", 6, 4, [item("powah:thermo_generator_starter")], "Thermo Generator", subtitle="Power from a temperature difference", deps=["pw_powah_cell"], xp=100, desc=[
        "&eWhat:&r a generator that needs a hot block underneath and a coolant fed in.",
        "&eChemistry:&r thermoelectric plates make current from a temperature difference (the Seebeck effect). Hotter below and colder inside means more power.",
        "&eHow:&r place it on lava or magma and pipe water in."]),
    Q("pw_powah", 8, 4, [item("powah:reactor_basic", 36)], "Powah Reactor", subtitle="Uraninite-fuelled multiblock", deps=["pw_thermo"], xp=250, desc=[
        "&eWhat:&r a multiblock reactor fuelled by the uraninite you oxidised yourself.",
        "&eChemistry:&r uraninite is UO₂. Its uranium releases heat as it fissions; the reactor turns that heat into FE.",
        "&eHow:&r place the reactor blocks in a stack and they form one reactor (check JEI). Feed it uraninite.",
        "&eTip:&r fuel, temperature and coolant all show in its GUI. Watch the temperature as you scale up."]),

    # --- Renewables (y = 6) -------------------------------------------------------------------
    Q("pw_solar", 4, 6, [item("mekanismgenerators:solar_generator"), item("powah:solar_panel_starter")], "Photovoltaics", optional=True, tokens=1, subtitle="Optional: light straight into electricity", deps=["pw_iron_gen", "t4_mv"], xp=100, desc=[
        "&eWhat:&r solar panels from Mekanism and Powah.",
        "&eChemistry:&r silicon solar cells use a p-n junction: a photon knocks an electron loose and the junction pushes it into a current.",
        "&eHow:&r place them under open sky. They stop at night and slow in rain.",
        "&eTip:&r pair solar with an energy cube to cover the night."]),
    Q("pw_adv_solar", 6, 6, [item("mekanismgenerators:advanced_solar_generator")], "Advanced Solar", subtitle="A bigger array", deps=["pw_solar"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r Mekanism's Advanced Solar Generator, a larger array with much more output.",
        "&eHow:&r check JEI for the recipe. Give it space: it's bigger than one block.",
        "&eTip:&r like the basic panel, it only works in daylight. Buffer it with a cube."]),
    Q("pw_wind", 8, 6, [item("mekanismgenerators:wind_generator")], "Wind Power", subtitle="Build it high", deps=["pw_solar"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r Mekanism's Wind Generator. It works day and night.",
        "&eHow:&r it makes more power the higher it's placed. Build it on a mountain or a tall tower.",
        "&eTip:&r it needs open space around it, so leave room."]),

    # --- Nuclear (y = -4) ----------------------------------------------------------------------
    Q("pw_fission_safety", 10, -4, [item("mekanismgenerators:fission_reactor_logic_adapter", 2)], "Reactor Safety", subtitle="Build the off-switch first", deps=["pw_iron_gen", "t6_fission"], xp=200, desc=[
        "&eWhat:&r Logic Adapters let redstone read the reactor and switch it off.",
        "&eChemistry:&r a fission reactor makes heat by splitting heavy nuclei. If heat can't escape fast enough, the reactor takes damage; at 100% it melts down.",
        "&eHow:&r set one adapter to emit a signal on damage or high temperature (pick the mode in its GUI) and wire it to another in Activation mode.",
        "&eTip:&r start at a low burn rate (0.1 mB/t), keep coolant flowing, and drain waste and heated coolant constantly."]),
    Q("pw_turbine", 12, -4, [item("mekanismgenerators:turbine_casing", 16)], "Industrial Turbine", subtitle="Steam into enormous power", deps=["pw_fission_safety"], xp=300, desc=[
        "&eWhat:&r Mekanism's multiblock turbine. Feed it steam from fission or a boiler and it makes huge amounts of FE.",
        "&eHow:&r casings, valves, vents, rotors with blades, a rotational complex, a pressure disperser and electromagnetic coils. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r a Saturating Condenser turns spent steam back into water, closing the loop."]),
    Q("pw_dt_fuel", 14, -4, [item("mekanism:solar_neutron_activator"), item("mekanismgenerators:hohlraum")], "D-T Fuel", subtitle="Deuterium and tritium", deps=["pw_turbine", "pw_lithium"], xp=300, desc=[
        "&eWhat:&r fusion fuel: deuterium and tritium, the two heavy isotopes of hydrogen.",
        "&eChemistry:&r deuterium comes from heavy water (D₂O). Tritium is bred from lithium by neutrons: ⁶Li + n → ³H + ⁴He.",
        "&eHow:&r electrolyse heavy water for deuterium; put lithium in the Solar Neutron Activator for tritium. Combine them into D-T fuel in the Chemical Infuser, then fill a Hohlraum with it (a chemical tank's item slot works; see its tooltip).",
        "&eTip:&r heavy water comes from a Mekanism Electric Pump with a Filter Upgrade."]),
    Q("pw_fusion", 16, -4, [item("mekanismgenerators:fusion_reactor_controller")], "Fusion", subtitle="The power of a star", deps=["pw_dt_fuel", "t6_waste"], xp=1000, size=1.75, shape="hexagon", desc=[
        "&6The power of a star, in a box you built. This is what you were.&r",
        "&eWhat:&r Mekanism's fusion reactor, the top of the power tree.",
        "&eChemistry:&r D + T → ⁴He + n + 17.6 MeV, millions of times more energy per kilogram than any chemical reaction.",
        "&eHow:&r a filled Hohlraum in the controller, then a burst from a Laser through a Laser Amplifier to ignite it. Layout: Just Enough Mekanism Multiblocks."]),

    # --- More Generators Galore (y=-4, x=4..8) -------------------------------------------------
    Q("pw_gg_upgrade", 4, -4, [item("generatorgalore:iron_to_gold_upgrade")], "Upgrade in Place", deps=["pw_gold_gen"], xp=30,
      optional=True, tokens=1, subtitle="Optional: upgrade a generator without breaking it", desc=[
        "&eWhat:&r Generators Galore upgrade kits turn a placed generator into the next tier, keeping its fuel and connections.",
        "&eHow:&r gold ingots, an item frame and a redstone block for iron → gold (check JEI for the others). Right-click the placed generator.",
        "&eTip:&r the tree branches: gold leads to diamond or to the food-burning Culinary Generator."]),
    Q("pw_gg_8x", 6, -4, [item("generatorgalore:iron_generator_8x")], "Eight Times the Burn", deps=["pw_gold_gen", "w_ancient"], xp=60,
      optional=True, tokens=1, subtitle="Optional: compressed generators", desc=[
        "&eWhat:&r 8x generators burn fuel eight times as fast and make eight times the FE in one block.",
        "&eHow:&r eight generators of a tier around an echo shard (check JEI). Echo shards come from Ancient City chests.",
        "&eTip:&r a 64x version exists too, for when space matters more than echo shards."]),
    Q("pw_gg_star", 8, -4, [item("generatorgalore:netherstar_generator")], "Burning a Star", deps=["pw_gg_collection"], xp=100,
      secret=True, loot="secret", subtitle="Secret: fuel fit for a god", desc=[
        "&6You remember lighting stars. Burning one feels like a waste, and also like coming home.&r",
        "&eWhat:&r the Nether Star Generator burns Nether Stars for an enormous amount of FE.",
        "&eChemistry:&r real stars run on fusion: hydrogen nuclei fuse into helium (4 ¹H → ⁴He) and a little mass becomes a lot of energy, E = mc²."]),

    # --- More Powah (y=4, x>=10) ---------------------------------------------------------------
    Q("pw_blazing", 10, 4, [item("powah:crystal_blazing", 8), item("powah:energy_cell_blazing")], "Blazing Crystals", deps=["pw_powah", "t2_blaze"], xp=100,
      subtitle="Powah's second tier: energized blaze", desc=[
        "&eWhat:&r every Powah tier is built from a crystal made in the Energizing Orb. Blazing crystals unlock the blazing tier of cells, generators and cables.",
        "&eHow:&r energize a blaze rod (or four blaze powder) with 120,000 FE. Then craft blazing-tier parts (check JEI).",
        "&eTip:&r feed the energizing rods from your biggest power source; crystals charge faster with more rods."]),
    Q("pw_niotic", 12, 4, [item("powah:crystal_niotic", 4), item("powah:energy_cell_niotic")], "Niotic Crystals", deps=["pw_blazing"], xp=125,
      subtitle="Energized diamond", desc=[
        "&eWhat:&r the niotic tier. Reactors and generators get much stronger.",
        "&eChemistry:&r diamond is pure carbon in a rigid lattice where every atom bonds to four others. Pumping energy into it is Powah's magic, but diamond really does conduct heat better than any metal.",
        "&eHow:&r energize a diamond with 300,000 FE (check JEI)."]),
    Q("pw_spirited", 14, 4, [item("powah:crystal_spirited", 4), item("powah:energy_cell_spirited")], "Spirited Crystals", deps=["pw_niotic"], xp=150,
      subtitle="Energized emerald", desc=[
        "&eWhat:&r the spirited tier, one step below the top.",
        "&eChemistry:&r emerald is the mineral beryl, Be₃Al₂Si₆O₁₈. A trace of chromium (Cr³⁺) replacing some aluminum gives it its green colour.",
        "&eHow:&r energize an emerald with 1,000,000 FE (check JEI). A villager trading hall pays off here."]),
    Q("pw_nitro", 15, 5.5, [item("powah:crystal_nitro", 16)], "Nitro Crystals", deps=["pw_spirited"], xp=250,
      optional=True, tokens=2, subtitle="Optional: Powah's top tier", desc=[
        "&eWhat:&r nitro crystals build the strongest Powah reactors and cells.",
        "&eHow:&r energize a Nether Star, two redstone blocks and a blazing crystal block with 20,000,000 FE. One craft makes sixteen.",
        "&eTip:&r save your Nether Stars for this; the Wither is the only reliable source (check JEI for a Hostile Neural Networks wither model)."]),
    Q("pw_ender", 11, 5.5, [item("powah:ender_cell_basic"), item("powah:player_transmitter_basic")], "Ender Power", deps=["pw_powah_cell"], xp=60,
      optional=True, tokens=1, subtitle="Optional: wireless Powah energy", desc=[
        "&eWhat:&r Ender Cells share one energy pool across your base; the Player Transmitter charges the items in your inventory.",
        "&eHow:&r both need an Ender Core (an eye of ender, dielectric casing and a tiny capacitor, energized). Check JEI, and link them with a Binding Card.",
        "&eTip:&r a player transmitter keeps jetpacks and the MekaSuit charged while you work."]),

    # --- More Flux Networks (y=1.5) ------------------------------------------------------------
    Q("pw_flux_big", 13, 1.5, [item("fluxnetworks:herculean_flux_storage")], "Herculean Storage", deps=["pw_flux_storage"], xp=100,
      optional=True, tokens=1, subtitle="Optional: a much bigger flux battery", desc=[
        "&eWhat:&r Herculean (and then Gargantuan) Flux Storage holds far more energy in one block, shared with the whole flux network.",
        "&eHow:&r Basic Flux Storage blocks around glass panes (check JEI). Gargantuan is the same with Herculean blocks.",
        "&eTip:&r flux storage keeps its energy when broken, so you can carry charged batteries to a new base."]),
    Q("pw_flux_controller", 15, 1.5, [item("fluxnetworks:flux_controller"), item("fluxnetworks:flux_configurator")], "Flux Controller", deps=["pw_flux_storage"], xp=100,
      optional=True, tokens=1, subtitle="Optional: charge yourself from the network", desc=[
        "&eWhat:&r the Flux Controller sends network energy wirelessly into players' inventories. The Configurator copies settings between flux devices.",
        "&eHow:&r flux blocks, a Flux Core and flux dust (check JEI). The Flux Core needs an MI processing unit in this pack.",
        "&eTip:&r turn charging off for your armor slots if it fights with other chargers."]),

    # ===== ATM10-aligned round (2026-10-19): the rest of Generator Galore, and flux dust =====
    Q("pw_gg_obsidian", 0, 0, [item("generatorgalore:obsidian_generator")], "Obsidian Generator", deps=["pw_gg_collection", "t2_obsidian"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the hub of the late generator tree", desc=[
        "&eWhat:&r a stronger burner, and the base for the ender, enchantment and magmatic generators.",
        "&eHow:&r a diamond generator in obsidian with a redstone block (or use the diamond to obsidian upgrade kit on a placed one).",
        "&eTip:&r the upgrade kits keep fuel and connections; JEI shows the whole tree."]),
    Q("pw_gg_gems", 0, 0, [item("generatorgalore:emerald_generator"), item("generatorgalore:netherite_generator")], "Emerald and Netherite Generators", deps=["pw_gg_collection", "t2_debris"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the two top solid-fuel burners", desc=[
        "&eWhat:&r the emerald and netherite generators burn ordinary fuel at a much higher rate for much more FE per tick.",
        "&eHow:&r emerald: a diamond generator in emeralds with a redstone block. Netherite: smithing table, template + diamond generator + netherite ingot.",
        "&eTip:&r feed them coal blocks or coke blocks; loose coal won't keep up."]),
    Q("pw_gg_ender", 0, 0, [item("generatorgalore:ender_generator"), item("generatorgalore:enchantment_generator")], "Ender and Enchantment Generators", deps=["pw_gg_obsidian"], xp=80,
      optional=True, tokens=1, subtitle="Optional: burn pearls and enchanted books", desc=[
        "&eWhat:&r the ender generator burns ender pearls; the enchantment generator burns enchanted books. Junk books from fishing finally have a use.",
        "&eHow:&r an obsidian generator in ender pearls with a redstone block, or in enchanted books with an enchanting table (check JEI).",
        "&eTip:&r an enderman farm feeds the ender generator for ever."]),
    Q("pw_gg_sweet", 0, 0, [item("generatorgalore:honey_generator"), item("generatorgalore:potion_generator")], "Honey and Potion Generators", deps=["pw_gg_collection"], xp=80,
      optional=True, tokens=1, subtitle="Optional: burn honey and leftover potions", desc=[
        "&eWhat:&r two branches from the Culinary Generator: one burns honey, the other burns potions.",
        "&eChemistry:&r honey is about 80% sugars (fructose and glucose). Sugar burns well: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O, the same reaction your cells run, only slower.",
        "&eHow:&r a culinary generator in honey blocks with buckets and a redstone block, or in pink dye with brewing stands (check JEI).",
        "&eTip:&r a few beehives with campfires underneath keep the honey generator running."]),
    Q("pw_gg_64x", 0, 0, [anyof([f"generatorgalore:{g}_generator_{n}" for g in ("copper", "iron", "gold", "diamond", "emerald", "obsidian", "netherite", "magmatic", "culinary",
                                                                              "honey", "potion", "ender", "enchantment", "halitosis", "netherstar") for n in ("8x", "64x")
                                 if not (g == "iron" and n == "8x")
                                 and not (n == "64x" and g in ("copper", "iron", "gold", "diamond", "emerald", "obsidian"))])],
      "Compressed Generators", deps=["pw_gg_8x"], xp=100, optional=True, tokens=2, subtitle="Optional: another 8x or a 64x", desc=[
        "&eWhat:&r any compressed generator other than the iron 8x: magmatic, star, gem, food, whatever you run most. 64x generators are eight 8x ones around a conduit.",
        "&eHow:&r 8x: eight generators around an echo shard. 64x: eight 8x generators around a conduit (check JEI).",
        "&eTip:&r a 64x generator eats fuel 64 times as fast. Make sure the fuel line can keep up first."]),
    Q("pw_flux_dust", 0, 0, [item("fluxnetworks:flux_dust", 16), item("fluxnetworks:flux_block")], "Flux Dust", deps=["pw_iron_gen", "t2_nether"], xp=60,
      optional=True, tokens=1, subtitle="Optional: redstone crushed between obsidian and bedrock", desc=[
        "&eWhat:&r flux dust is the base of every Flux Networks device. Nine make a Flux Block.",
        "&eChemistry:&r real redstone doesn't exist, but pressure really does change minerals: graphite squeezed hard enough becomes diamond, and that's the idea here.",
        "&eHow:&r its tooltip says it: redstone compressed with bedrock and obsidian. JEI's Flux Networks page shows the setup. Bedrock is easy to reach at the Nether's floor or roof.",
        "&eTip:&r make a big batch now. The Flux Core still needs an MI processing unit (EV), but the dust doesn't."]),
], links=[("t1_power", -2, 0), ("t6_flux", 14, -2), ("t4_uraninite", 0, 4), ("t6_fission", 8, -6)])
