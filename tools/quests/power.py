"""Quest chapter: power. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Mirror of ATM10's "Basic Power" chapter (user decision 2026-10-20: quest for quest where we have the mod; same items,
order, clusters and sizes; the text is ours). ATM10's "Generators" chapter (Iron Furnaces and
Generator Galore) is its own page now (generators.py, split out 2026-10-20 with the keys unchanged).

ATM10 Basic Power quests skipped (mod not in the pack): Extreme Reactors, RFTools Power cells, Industrial Foregoing's
Mycelial Reactor, Dyson Cube, Draconic energy core, and the two Productive Bees / XyCraft flux-dust automations.
The Powah quests that used to live here (pw_energized, pw_powah_cell, pw_thermo, pw_powah, pw_blazing, pw_niotic,
pw_spirited, pw_nitro, pw_ender) moved to powah.py, keys unchanged. Our own quests ATM10 doesn't have (Mekanism power
plant, MI steam and diesel, extra renewables) stay as side quests; the ones other pages build on stay required.
"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, MAIN, SIDE  # noqa: F401

OPT = dict(optional=True, tokens=1)
MEK, GEN, GG, FLUX = "mekanism:", "mekanismgenerators:", "generatorgalore:", "fluxnetworks:"
S_HUB, S_EARLY, S_MOVE, S_FLUX, S_STORE = "Power Basics", "Early Power", "Moving Power", "Flux Networks", "Storing Power"
S_MID, S_END, S_MEKP, S_MI = "Mid-Game Power", "End-Game Power", "Mekanism Power Plant", "Steam and Diesel"

CHAPTER = Chapter("power", "Power", GEN + "gas_burning_generator",
        ["Energy is chemistry too: combustion, gas burning, fission and fusion."], SIDE, mirror="basic_power", quests=[
    # ===== Power Basics (ATM10 centre) ======================================================
    Q("pw_iron_gen", 0, 0, [item("minecraft:redstone")], "Choosing Your Power", section=S_HUB, deps=["t1_power"], xp=40,
      size=2.0, shape="gear", mirror="4AB0DD227471FDBF", subtitle="A catalogue of every way to make, move and store FE", desc=[
        "&6You remember holding lightning. For now, the generator you built in T1 will do.&r",
        "&eWhat:&r this page lists the pack's power options by stage: early burners, moving power, storing it, mid-game and end-game plants. Furnaces and Generator Galore have their own page, Generators.",
        "&eChemistry:&r every generator turns some stored energy into current: chemical bonds (C + O₂ → CO₂), sunlight, wind, heat, or the nucleus itself.",
        "&eHow:&r a little redstone opens the page. Most lines are optional; pick the ones that suit your base.",
        "&eTip:&r MI machines run on EU, Modern Industrialization's own electricity. Most other mods run on FE (Forge Energy)."]),

    # ===== Early Power ======================================================================
    Q("pw_early", 0, 0, [item("minecraft:coal")], "Early Power", section=S_EARLY, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="42D173B9FF8D16E4", subtitle="Burn something", desc=[
        "&eWhat:&r early power comes from burning fuel or catching heat and light.",
        "&eChemistry:&r coal is mostly carbon; burning it releases about 33 kJ per gram as it becomes CO₂.",
        "&eHow:&r a lump of coal starts this section. Charcoal works in every burner too."]),
    Q("pw_heat", 0, 0, [item(GEN + "heat_generator")], "Heat Generator", section=S_EARLY, deps=["pw_early", "t3_infuser"], xp=60,
      mirror="11D09E918015355C", subtitle="Mekanism's starter generator", desc=[
        "&eWhat:&r Mekanism's first generator. It burns fuel and turns heat into FE.",
        "&eHow:&r place lava next to it for a passive bonus, and feed it fuel for more.",
        "&eTip:&r lava from a pump makes this a decent passive generator early on."]),
    Q("pw_coal_gens", 0, 0, [anyof(["justdirethings:generatort1", "integrateddynamics:coal_generator", GG + "iron_generator"])],
      "Coal Generators", section=S_EARLY, deps=["pw_early"], xp=40, mirror="0BB367839D28607D", subtitle="Any simple burner counts", desc=[
        "&eWhat:&r a plain fuel-burning generator from any mod: Just Dire Things, Integrated Dynamics or Generator Galore.",
        "&eHow:&r check JEI for each. Feed it coal, charcoal or coke.",
        "&eTip:&r coke from your coke oven burns twice as long as coal in most burners."]),
    Q("pw_solar", 0, 0, [anyof([GEN + "solar_generator", GEN + "advanced_solar_generator", GEN + "wind_generator"])], "Renewables",
      section=S_EARLY, deps=["pw_early", "t4_mv"], xp=100, mirror="48DC9E8E9D21A2FA", subtitle="Light and wind, no fuel", desc=[
        "&eWhat:&r Mekanism's solar panels and wind generator: free power once built. Any one counts.",
        "&eChemistry:&r silicon solar cells use a p-n junction: a photon knocks an electron loose and the junction pushes it into a current.",
        "&eHow:&r solar under open sky; wind as high as you can build it (check JEI).",
        "&eTip:&r pair them with an energy cube to cover the night or a calm spell."]),
    Q("pw_adv_solar", 0, 0, [tick()], "Advanced Solar", section=S_EARLY, deps=['pw_solar'], optional=True, tokens=0, xp=0, icon="mekanismgenerators:advanced_solar_generator", subtitle="Moved: see Advanced Solar Generator", desc=["&eMoved:&r this step is now \"Advanced Solar Generator\" on the Mekanism page. Click to dismiss."]),
    Q("pw_wind", 0, 0, [tick()], "Wind Power", section=S_EARLY, deps=['pw_solar'], optional=True, tokens=0, xp=0, icon="mekanismgenerators:wind_generator", subtitle="Moved: see Wind Generator", desc=["&eMoved:&r this step is now \"Wind Generator\" on the Mekanism page. Click to dismiss."]),
    Q("pw_bio", 0, 0, [tick()], "Bio Fuel", section=S_EARLY, deps=['pw_heat'], optional=True, tokens=0, xp=0, icon="mekanismgenerators:bio_generator", subtitle="Moved: see Bio-Generator", desc=["&eMoved:&r this step is now \"Bio-Generator\" on the Mekanism page. Click to dismiss."]),

    # ===== Moving Power =====================================================================
    Q("pw_transfer", 0, 0, [item("minecraft:iron_ingot")], "Moving Power", section=S_MOVE, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="1F81EA5E45424308", subtitle="From generator to machine", desc=[
        "&eWhat:&r power is useless where it's made. This section is cables, pipes and the ways to skip them.",
        "&eChemistry:&r copper and aluminium carry real grids because their electrons move freely; iron conducts about six times worse than copper.",
        "&eHow:&r an iron ingot opens the section."]),
    Q("pw_pipez", 0, 0, [item("pipez:energy_pipe"), item("pipez:wrench")], "Energy Pipes", section=S_MOVE, deps=["pw_transfer"], xp=30,
      mirror="4EEAB467C722ECE7", subtitle="The cheapest FE line", desc=[
        "&eWhat:&r Pipez energy pipes carry FE, and the Pipe Wrench sets which ends pull.",
        "&eHow:&r iron and redstone with a redstone block for the pipe (check JEI). Sneak-click the generator end to extract.",
        "&eTip:&r the Automation and Logic page has the rest of Pipez."]),
    Q("pw_pipez_up", 0, 0, [anyof([f"pipez:{t}_upgrade" for t in ("basic", "improved", "advanced", "ultimate")])], "Pipe Upgrades",
      section=S_MOVE, deps=["pw_pipez"], xp=30, mirror="1409C17773B6A131", subtitle="More FE per tick through one pipe", desc=[
        "&eWhat:&r an upgrade in the extracting end raises how much a pipe moves. Any tier counts.",
        "&eHow:&r each tier is the one before plus better materials (check JEI).",
        "&eTip:&r one upgrade at the generator end is enough for the whole line."]),
    Q("pw_cables", 0, 0, [tick()], "Universal Cables", section=S_MOVE, deps=['pw_transfer', 't3_infuser'], optional=True, tokens=0, xp=0, mirror="5C47935A3B2877FF", icon="mekanism:basic_universal_cable", subtitle="Moved: see Universal Cable", desc=["&eMoved:&r this step is now \"Universal Cable\" on the Mekanism page. Click to dismiss."]),
    Q("pw_entangle", 0, 0, [tick()], "Quantum Entangloporter", section=S_MOVE, deps=['pw_transfer', 't6_pu'], optional=True, tokens=0, xp=0, mirror="7FE969CB4B419FC6", icon="mekanism:quantum_entangloporter", subtitle="Moved: see Quantum Entangloporter", desc=["&eMoved:&r this step is now \"Quantum Entangloporter\" on the Mekanism page. Click to dismiss."]),

    # ===== Flux Networks ====================================================================
    Q("pw_flux_dust", 0, 0, [item(FLUX + "flux_dust", 4)], "Flux Networks", section=S_FLUX, deps=["pw_transfer", "t2_nether"], xp=60,
      size=1.5, mirror="35CC898E0E49FE58", subtitle="Redstone crushed between obsidian and bedrock", desc=[
        "&eWhat:&r flux dust is the base of every Flux Networks device.",
        "&eChemistry:&r real redstone doesn't exist, but pressure really does change minerals: graphite squeezed hard enough becomes diamond, and that's the idea here.",
        "&eHow:&r its tooltip says it: redstone compressed with bedrock and obsidian. JEI's Flux Networks page shows the setup. Bedrock is easy to reach at the Nether's floor or roof.",
        "&eTip:&r make a big batch now. The Flux Core needs an MI processing unit (EV), but the dust doesn't."]),
    Q("pw_flux_core", 0, 0, [item(FLUX + "flux_core", 4), item(FLUX + "flux_block")], "Flux Cores", section=S_FLUX,
      deps=["pw_flux_dust", "t6_pu"], xp=150, mirror="1BE26A00A420DAE3", subtitle="Pack gate: an MI processing unit in each", desc=[
        "&eWhat:&r Flux Cores are the heart of every flux device; nine flux dust make a Flux Block.",
        "&eHow:&r in this pack: flux dust and obsidian around an MI &eprocessing unit&r (EV). Check JEI.",
        "&eTip:&r a plug, a point and a storage block each eat cores. Make four at once."]),
    Q("pw_flux_plug", 0, 0, [item(FLUX + "flux_plug")], "Flux Plug", section=S_FLUX, deps=["pw_flux_core"], xp=60,
      mirror="5F078A574A783B02", subtitle="Where power enters the network", desc=[
        "&eWhat:&r a Flux Plug takes power from whatever it touches and puts it on a flux network.",
        "&eHow:&r flux blocks and a flux core (check JEI). Open it and create a network.",
        "&eTip:&r put one on your biggest battery's output."]),
    Q("pw_flux_net", 0, 0, [tick()], "Set Up a Network", section=S_FLUX, deps=["pw_flux_plug"], xp=40, icon=FLUX + "flux_configurator",
      mirror="36DEA17CBB696CC7", subtitle="Name it, colour it, lock it", desc=[
        "&eWhat:&r every flux device joins one named network. The network decides who may connect.",
        "&eHow:&r open the plug, make a network, give it a colour and set its security (public, encrypted or private). Click the checkmark when it's set.",
        "&eTip:&r private networks stop a teammate's machine draining your reactor by accident."]),
    Q("pw_flux_point", 0, 0, [item(FLUX + "flux_point")], "Flux Point", section=S_FLUX, deps=["pw_flux_net"], xp=60,
      mirror="56B6ABF3D6EA0D84", subtitle="Where power leaves the network", desc=[
        "&eWhat:&r a Flux Point gives network power to whatever it touches.",
        "&eHow:&r like the plug (check JEI). Join it to the same network.",
        "&eTip:&r set a priority so the most important machines fill first."]),
    Q("pw_flux_storage", 0, 0, [item(FLUX + "basic_flux_storage")], "Flux Storage", section=S_FLUX, deps=["pw_flux_net"], xp=80,
      mirror="79AD74A863EA43CB", subtitle="A battery the whole network shares", desc=[
        "&eWhat:&r Basic Flux Storage buffers energy for the network.",
        "&eHow:&r flux blocks and glass around a flux core (check JEI).",
        "&eTip:&r flux storage keeps its energy when broken, so you can carry charged batteries to a new base."]),
    Q("pw_flux_tip", 0, 0, [tick()], "Note: Priorities", section=S_FLUX, deps=["pw_flux_net"], xp=20, **OPT, icon=FLUX + "flux_point",
      mirror="2EB7784D5296F410", subtitle="Optional: who gets fed first", desc=[
        "&eWhat:&r each plug and point has a priority and a transfer limit. High-priority points fill first; storage fills last.",
        "&eHow:&r open a point, set its priority and limit. Click the checkmark when you've set one.",
        "&eTip:&r give the reactor coolant pumps the top priority. Everything else can wait a tick."]),
    Q("pw_flux_controller", 0, 0, [item(FLUX + "flux_controller")], "Flux Controller", section=S_FLUX, deps=["pw_flux_net"], xp=100,
      mirror="27A4FA38992448A0", subtitle="Charge yourself from the network", desc=[
        "&eWhat:&r the Flux Controller sends network energy wirelessly into players' inventories.",
        "&eHow:&r flux blocks, a flux core and flux dust (check JEI).",
        "&eTip:&r turn charging off for your armour slots if it fights with other chargers. The Flux Configurator copies settings between devices."]),
    Q("pw_flux_big", 0, 0, [item(FLUX + "herculean_flux_storage")], "Herculean Storage", section=S_FLUX, deps=["pw_flux_storage"], xp=100,
      **OPT, subtitle="Optional: a much bigger flux battery", desc=[
        "&eWhat:&r Herculean (and then Gargantuan) Flux Storage holds far more energy in one block, shared with the whole network.",
        "&eHow:&r Basic Flux Storage blocks around glass panes (check JEI). Gargantuan is the same with Herculean blocks.",
        "&eTip:&r one Herculean block can carry a small base through a night with no solar."]),

    # ===== Storing Power ====================================================================
    Q("pw_storing", 0, 0, [item("minecraft:iron_ingot")], "Storing Power", section=S_STORE, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="76EA017B12E8F01B", subtitle="A buffer between making and using", desc=[
        "&eWhat:&r a battery keeps machines running when the generator stalls, and catches power you'd otherwise waste.",
        "&eChemistry:&r a lead-acid battery stores energy in a reversible reaction: Pb + PbO₂ + 2H₂SO₄ ⇌ 2PbSO₄ + 2H₂O.",
        "&eHow:&r an iron ingot opens the section."]),
    Q("pw_cube", 0, 0, [anyof([f"{MEK}{t}_energy_cube" for t in ("basic", "advanced", "elite", "ultimate")])], "Energy Cubes",
      section=S_STORE, deps=["pw_storing", "t3_infuser"], xp=60, mirror="477B411F84342EEA", subtitle="Mekanism's block battery", desc=[
        "&eWhat:&r energy cubes hold FE so short spikes don't stall your machines. Any tier counts.",
        "&eHow:&r put one between your generators and machines. Configure its sides with the Configurator.",
        "&eTip:&r cubes upgrade in place: craft the next tier around the old one."]),
    Q("pw_id_battery", 0, 0, [item("integrateddynamics:energy_battery")], "Energy Battery", section=S_STORE, deps=["pw_storing"], xp=40,
      mirror="72EA25D05C46D39A", subtitle="Integrated Dynamics' battery", desc=[
        "&eWhat:&r a small FE battery made of crystalized Menril. It stacks power with others placed next to it.",
        "&eHow:&r Menril chunks and blocks around a redstone block (check JEI). The resin line is on the Automation and Logic page.",
        "&eTip:&r it fits on a logic network, where cables can carry its power."]),
    Q("pw_induction", 0, 0, [anyof([f"{MEK}{t}_induction_provider" for t in ("basic", "advanced", "elite", "ultimate")]),
                             anyof([f"{MEK}{t}_induction_cell" for t in ("basic", "advanced", "elite", "ultimate")])],
      "Induction Matrix", section=S_STORE, deps=["pw_cube", "pw_lithium"], xp=300, size=1.5, mirror="682034C680FDEDC2",
      subtitle="One multiblock battery for the whole base", desc=[
        "&6Power stored, waiting, obedient. This feels familiar.&r",
        "&eWhat:&r a hollow multiblock battery. Cells inside set how much it stores; providers set how fast it charges and discharges.",
        "&eHow:&r casings form the shell (Structural Glass works for the walls), ports move energy in and out. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r switch one port to output with the Configurator. Start small; you can rebuild it larger later."]),

    # ===== Mid-Game Power ===================================================================
    Q("pw_mid", 0, 0, [item("minecraft:diamond")], "Mid-Game Power", section=S_MID, deps=["pw_iron_gen"], xp=30, size=1.5,
      mirror="5E41363F9AE243F3", subtitle="Gases and uranium", desc=[
        "&eWhat:&r the mid game is about chemistry you've built yourself: burning hydrogen, and fission fuel.",
        "&eChemistry:&r diamond is carbon too, but burning one for power would be a terrible trade.",
        "&eHow:&r a diamond opens the section."]),
    Q("pw_gas", 0, 0, [item(GEN + "gas_burning_generator")], "Burning Hydrogen", section=S_MID, deps=["pw_mid", "t4_separator"], xp=150,
      mirror="0AEC181F5E21A299", subtitle="The cleanest combustion there is", desc=[
        "&eWhat:&r the Gas-Burning Generator turns flammable gas into FE.",
        "&eChemistry:&r 2H₂ + O₂ → 2H₂O + energy. The only exhaust is water.",
        "&eHow:&r pipe hydrogen from your Electrolytic Separator in with pressurized tubes.",
        "&eTip:&r electrolysis costs more energy than burning hydrogen returns. Use it to store spare power, not to make it."]),
    Q("pw_more_powah", 0, 0, [item("powah:uraninite")], "More Powah", section=S_MID, deps=["pw_mid", "t4_uraninite"], xp=80,
      mirror="35ABB0DEE70DF7FD", subtitle="Uranium dioxide for Powah's reactors", desc=[
        "&eWhat:&r uraninite fuels Powah's reactors. The Powah! page has the whole mod, tier by tier.",
        "&eChemistry:&r uraninite is UO₂. In this pack you make it the real way: uranium dust oxidised in MI's Chemical Reactor.",
        "&eHow:&r uranium dust and oxygen in the Chemical Reactor (MV). Powah's own shortcut is removed.",
        "&eTip:&r a Powah reactor takes uraninite, coolant, and carbon or redstone to boost it."]),

    # ===== End-Game Power ===================================================================
    Q("pw_end", 0, 0, [item("minecraft:netherite_ingot")], "End-Game Power", section=S_END, deps=["pw_iron_gen", "t2_nether"], xp=40,
      size=1.5, mirror="3BDB94F17765EE77", subtitle="Fusion, and nothing less", desc=[
        "&eWhat:&r end-game power means fusion: more energy than everything else on this page together.",
        "&eHow:&r a netherite ingot opens the section.",
        "&eTip:&r the Mekanism: Power page walks through fission and fusion step by step."]),
    Q("pw_fusion", 0, 0, [item(GEN + "fusion_reactor_controller")], "Fusion", section=S_END, deps=["pw_end", "pw_dt_fuel", "t6_waste"],
      xp=1000, mirror="43D83CFA824B0A70", subtitle="The power of a star", desc=[
        "&6The power of a star, in a box you built. This is what you were.&r",
        "&eWhat:&r Mekanism's fusion reactor, the top of the power tree.",
        "&eChemistry:&r D + T → ⁴He + n + 17.6 MeV, millions of times more energy per kilogram than any chemical reaction.",
        "&eHow:&r a filled Hohlraum in the controller, then a burst from a Laser through a Laser Amplifier to ignite it. Layout: Just Enough Mekanism Multiblocks."]),

    # ===== Mekanism Power Plant (ours; the Mekanism pages build on these) ====================
    Q("pw_adv_cube", 0, 0, [item(MEK + "advanced_energy_cube")], "Bigger Cubes", section=S_MEKP,
      subtitle="Alloys and energy tablets around the cube below", deps=["pw_cube", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the Advanced Energy Cube holds and moves much more energy.",
        "&eHow:&r a basic cube with infused alloy, osmium ingots and energy tablets around it (check JEI). Upgrading in place keeps the stored energy.",
        "&eTip:&r Elite and Ultimate cubes follow the same pattern with reinforced and atomic alloys."]),
    Q("pw_brine", 0, 0, [item(MEK + "thermal_evaporation_controller"), item(MEK + "brine_bucket")], "Evaporation Ponds", section=S_MEKP,
      subtitle="Sunlight and heat concentrate brine", deps=["pw_adv_cube"], xp=150, desc=[
        "&eWhat:&r the Thermal Evaporation Plant boils water down into brine, and brine down into liquid lithium.",
        "&eChemistry:&r real lithium comes from salt flats: brine sits in ponds until the water evaporates and the salts concentrate.",
        "&eHow:&r a multiblock tower of Thermal Evaporation Blocks, Valves and one Controller. See Just Enough Mekanism Multiblocks in JEI.",
        "&eTip:&r taller towers and more heat run faster. Feed it plain water."]),
    Q("pw_lithium", 0, 0, [item(MEK + "dust_lithium", 8)], "Lithium", section=S_MEKP, subtitle="The battery metal", deps=["pw_brine"], xp=150, desc=[
        "&eWhat:&r lithium dust, for induction cells (and later, tritium).",
        "&eChemistry:&r lithium is the lightest metal and gives up its electron easily, which is why lithium-ion batteries store so much energy for their weight.",
        "&eHow:&r run brine through the plant again for liquid lithium. Turn it into gas in a Rotary Condensentrator, then crystallise it in a Chemical Crystallizer.",
        "&eTip:&r check JEI with &eR&r on Lithium Dust to confirm each step."]),
    Q("pw_fission_safety", 0, 0, [tick()], "Reactor Safety", section=S_MEKP, deps=['pw_mid', 't6_fission'], optional=True, tokens=0, xp=0, icon="mekanismgenerators:fission_reactor_logic_adapter", subtitle="Moved: see Fission Logic Adapter", desc=["&eMoved:&r this step is now \"Fission Logic Adapter\" on the Mekanism: Power page. Click to dismiss."]),
    Q("pw_turbine", 0, 0, [item(GEN + "turbine_casing", 16)], "Industrial Turbine", section=S_MEKP, subtitle="Steam into enormous power",
      deps=["mkp_fission_logic"], xp=300, desc=[
        "&eWhat:&r Mekanism's multiblock turbine. Feed it steam from fission or a boiler and it makes huge amounts of FE.",
        "&eHow:&r casings, valves, vents, rotors with blades, a rotational complex, a pressure disperser and electromagnetic coils. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r a Saturating Condenser turns spent steam back into water, closing the loop."]),
    Q("pw_dt_fuel", 0, 0, [item(MEK + "solar_neutron_activator"), item(GEN + "hohlraum")], "D-T Fuel", section=S_MEKP,
      subtitle="Deuterium and tritium", deps=["pw_turbine", "pw_lithium"], xp=300, desc=[
        "&eWhat:&r fusion fuel: deuterium and tritium, the two heavy isotopes of hydrogen.",
        "&eChemistry:&r deuterium comes from heavy water (D₂O). Tritium is bred from lithium by neutrons: ⁶Li + n → ³H + ⁴He.",
        "&eHow:&r electrolyse heavy water for deuterium; put lithium in the Solar Neutron Activator for tritium. Combine them into D-T fuel in the Chemical Infuser, then fill a Hohlraum with it (a chemical tank's item slot works; see its tooltip).",
        "&eTip:&r heavy water comes from a Mekanism Electric Pump with a Filter Upgrade."]),

    # ===== Steam and Diesel (ours) ===========================================================
    Q("pw_mi_storage", 0, 0, [item("modern_industrialization:lv_storage_unit")], "EU Storage", section=S_MI,
      subtitle="Optional: a battery for MI's grid", deps=["pw_storing", "t3_hull"], xp=60, **OPT, desc=[
        "&eWhat:&r MI's storage unit holds EU, Modern Industrialization's electricity.",
        "&eHow:&r built from redstone batteries, battery alloy plates and an LV hull. Put it between your turbine and your machines.",
        "&eTip:&r a buffer lets your steam turbine keep running while machines are idle."]),
    Q("pw_mv_turbine", 0, 0, [item("modern_industrialization:mv_steam_turbine")], "MV Steam Turbine", section=S_MI,
      subtitle="Optional: more steam, more EU", deps=["pw_mi_storage", "t4_mv"], xp=100, **OPT, desc=[
        "&eWhat:&r a bigger steam turbine that outputs MV power.",
        "&eChemistry:&r a turbine converts the energy of hot, expanding steam into rotation, then a generator turns rotation into current.",
        "&eHow:&r assemble it from an MV hull, aluminum rotors and large motors (check JEI)."]),
    Q("pw_transformer", 0, 0, [item("modern_industrialization:lv_mv_transformer")], "Transformers", section=S_MI,
      subtitle="Optional: step voltage between tiers", deps=["pw_mv_turbine"], xp=75, **OPT, desc=[
        "&eWhat:&r a transformer moves energy between two neighbouring voltage tiers (LV and MV here).",
        "&eHow:&r place it between an MV cable and your LV machines (or the other way round). Check which face is which in its tooltip.",
        "&eTip:&r real grids do the same: high voltage for transmission, low voltage at the socket."]),
    Q("pw_hv_turbine", 0, 0, [item("modern_industrialization:hv_steam_turbine")], "HV Steam Turbine", section=S_MI,
      subtitle="Optional: high-voltage steam", deps=["pw_transformer", "t5_hv"], xp=150, **OPT, desc=[
        "&eWhat:&r the HV steam turbine, for HV machine lines.",
        "&eHow:&r check JEI for the recipe. Feed it from a large boiler.",
        "&eTip:&r more steam than one turbine can eat? Add a second turbine on the same steam line."]),
    Q("pw_large_turbine", 0, 0, [item("modern_industrialization:large_steam_turbine")], "Large Steam Turbine", section=S_MI,
      subtitle="Optional: power-station scale", deps=["pw_hv_turbine", "t6_pu"], xp=300, **OPT, desc=[
        "&eWhat:&r MI's multiblock steam turbine. It eats steam by the thousands of mB and makes serious EU.",
        "&eHow:&r the controller needs an HV steam turbine, a processing unit (EV) and a highly advanced hull. Layout: JEI or the MI guidebook.",
        "&eTip:&r pair it with a large boiler or a reactor's steam output."]),
    Q("pw_diesel", 0, 0, [item("modern_industrialization:mv_diesel_generator")], "Diesel Generators", section=S_MI,
      subtitle="Optional: petrochemical power", deps=["pw_mid", "t5_diesel"], xp=150, **OPT, desc=[
        "&eWhat:&r MI generators that burn the fuels from your distillation tower.",
        "&eChemistry:&r diesel is a mix of hydrocarbons around C₁₂ to C₂₀. Long chains pack lots of C-H bonds, and lots of energy.",
        "&eHow:&r pipe diesel into the generator and cable it to your machines."]),
    Q("pw_large_diesel", 0, 0, [item("modern_industrialization:large_diesel_generator")], "Large Diesel Generator", section=S_MI,
      subtitle="Optional: factory-scale combustion", deps=["pw_diesel", "t5_hv"], xp=250, **OPT, desc=[
        "&eWhat:&r a multiblock diesel generator for real factories.",
        "&eHow:&r the 3D layout is in JEI and the MI guidebook. It needs fluid input and energy output hatches.",
        "&eTip:&r refined fuels (like boosted diesel) burn for more EU per bucket. Check JEI."]),
], links=[("t1_power", 0, 0), ("gs_furnace", 0, 0), ("t6_fission", 0, 0), ("t4_uraninite", 0, 0)])
