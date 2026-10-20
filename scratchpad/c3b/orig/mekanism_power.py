"""Quest chapter: mekanism_power (mod page: Mekanism Generators reactors, Mekanism: More Machine, Mekanism Extras).
See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Split out of mekanism.py (2026-10-18). Quest keys were moved unchanged (mk2_*), so progress is kept.
The first quest, mkp_intro, opens with the Mekanism page (mk2_intro). Each row starts from mkp_intro plus the
main-path quest that gates it (fission, turbine casing, D-T fuel, control circuits, yellowcake), which are linked.
Rows: reactors (boiler, turbine, fusion); every generator; Mekanism: More Machine; Mekanism Extras.
The basic generators, energy cubes, turbine casing, D-T fuel and fusion controller are in power.py and t6/t7.
"""
from questlib import Q, Chapter, item, tick, anyof, SIDE  # noqa: F401

MEK = "mekanism:"
GEN = "mekanismgenerators:"
MM = "mekmm:"
EX = "mekanism_extras:"


def ex_factories(tier):
    kinds = ("smelting", "enriching", "crushing", "compressing", "combining", "purifying", "injecting", "infusing", "sawing",
             "oxidizing", "dissolving", "washing", "crystallizing", "centrifuging")
    return [f"{EX}{tier}_{k}_factory" for k in kinds]


CHAPTER = Chapter("mekanism_power", "Mekanism: Power and Beyond", "mekanismgenerators:fusion_reactor_controller",
        ["Boilers, turbines and fusion; Mekanism: More Machine; and Mekanism Extras' four tiers beyond ultimate."], SIDE, [
    Q("mkp_intro", 0, 0, [tick()], "Power and Beyond", subtitle="Mekanism's reactors and its two add-ons", deps=["mk2_intro"], xp=50, desc=[
        "&6The machines obey you now. You remember wanting more: more heat, more power, more than the last tier allowed.&r",
        "&eWhat:&r the second Mekanism page. It covers the big power multiblocks (boiler, turbine, fusion), &eMekanism: More Machine&r and &eMekanism Extras&r.",
        "&eHow:&r each row opens when its main-path quest is done: fission for the boiler, the turbine casing, D-T fuel for fusion, yellowcake for Extras. Those quests are linked on the left.",
        "&eTip:&r the machines, factories, circuits and logistics are on the first Mekanism page."]),

    # --- Generators and reactor multiblocks (y = 16 / 17.5) -------------------------------------
    Q("mk2_boiler", 0, 16, [item(MEK + "boiler_casing", 16), item(MEK + "boiler_valve", 2), item(MEK + "superheating_element", 4), item(MEK + "pressure_disperser")],
      "Thermoelectric Boiler", subtitle="Water into steam, by the tank", deps=["mkp_intro", "t6_fission"], xp=150, desc=[
        "&eWhat:&r a multiblock boiler that turns water into steam, heated by Superheating Elements (power) or by hot coolant from a fission reactor.",
        "&eChemistry:&r boiling water takes 2,260 J per gram, far more than heating it. That latent heat is what the turbine later turns back into work.",
        "&eHow:&r the layout is in &eJust Enough Mekanism Multiblocks&r in JEI: casing walls, valves, a layer of pressure dispersers, and elements on the bottom.",
        "&eTip:&r a sodium-cooled fission reactor sends heated sodium here instead of boiling water itself."]),
    Q("mk2_sodium", 2, 16, [tick()], "Sodium Coolant", subtitle="A liquid metal carries the heat", deps=["mk2_boiler", "mk2_salt"], xp=200, desc=[
        "&eWhat:&r cool your fission reactor with sodium instead of water. It returns as superheated sodium, which the Thermoelectric Boiler uses to make steam before sending the sodium back.",
        "&eChemistry:&r sodium melts at 98 °C and boils at 883 °C, so it stays liquid at reactor temperatures without high pressure. Real fast reactors use it, and keep it away from water, which it reacts with violently.",
        "&eHow:&r sodium comes from brine in the Electrolytic Separator (see Salt and Sodium). Pipe it into the reactor, superheated sodium out to a boiler valve, and the cooled sodium back. Click to confirm once it runs.",
        "&eTip:&r one sodium loop feeds a much bigger boiler and turbine than water cooling does."]),
    Q("mk2_turbine_shell", 4, 16, [item(GEN + "turbine_valve", 2), item(GEN + "turbine_vent", 8)], "Turbine Valves and Vents", subtitle="Steam in, spent steam out", deps=["mkp_intro", "pw_turbine"], xp=150, desc=[
        "&eWhat:&r valves feed steam in and take power out; vents let the spent steam leave through the walls above the rotor.",
        "&eChemistry:&r a turbine extracts work as steam expands and cools. The more vent area, the more steam can pass per tick.",
        "&eHow:&r valve: turbine casings around an Advanced Control Circuit (MV). Vent: casings around iron bars (check JEI).",
        "&eTip:&r the turbine GUI shows whether vent flow or blade count is your limit."]),
    Q("mk2_turbine_parts", 6, 16, [item(GEN + "turbine_rotor", 4), item(GEN + "turbine_blade", 8), item(GEN + "rotational_complex"), item(GEN + "electromagnetic_coil", 2), item(GEN + "saturating_condenser", 4)],
      "Turbine Internals", subtitle="Rotor, blades, coils, condensers", deps=["mk2_turbine_shell"], xp=200, desc=[
        "&eWhat:&r the moving parts inside an Industrial Turbine. More blades and coils mean more power from the same steam.",
        "&eChemistry:&r condensers turn spent steam back into water, so the loop reuses the same water over and over.",
        "&eHow:&r stack rotors with two blades each on the centre column, a Rotational Complex on top, then coils and condensers above. See Just Enough Mekanism Multiblocks.",
        "&eTip:&r the turbine's GUI shows whether steam flow or blade count is the limit."]),
    Q("mk2_fusion_build", 8, 16, [item(GEN + "fusion_reactor_frame", 16), item(GEN + "reactor_glass", 4), item(GEN + "fusion_reactor_port", 2), item(GEN + "laser_focus_matrix")],
      "Building the Fusion Reactor", subtitle="Frame, glass, ports and a laser window", deps=["mk2_turbine_parts", "pw_dt_fuel"], xp=300, desc=[
        "&eWhat:&r the shell of the Fusion Reactor: frames, reactor glass, ports for fuel and output, and a Laser Focus Matrix to let the ignition laser in.",
        "&eHow:&r the 3D layout is in &eJust Enough Mekanism Multiblocks&r in JEI. The controller sits on top in the middle.",
        "&eTip:&r ports switch between input and output with a Configurator."]),
    Q("mk2_ignition", 10, 16, [item(MEK + "laser", 3), item(MEK + "laser_amplifier")], "Ignition", subtitle="A laser hot enough to start a star", deps=["mk2_fusion_build"], xp=200, desc=[
        "&eWhat:&r lasers charge a Laser Amplifier, which fires a single huge pulse into the reactor to ignite it.",
        "&eChemistry:&r deuterium and tritium only fuse above about 100 million °C, when the nuclei move fast enough to beat their electric repulsion.",
        "&eHow:&r put a filled Hohlraum in the controller, aim the amplifier at the Laser Focus Matrix and fire it with a redstone signal. Then go to the Fusion quest.",
        "&eTip:&r once lit, the reactor sustains itself as long as fuel keeps coming."]),
    Q("mk2_gen_field", 0, 17.5, [item(GEN + "heat_generator"), item(GEN + "solar_generator"), item(GEN + "advanced_solar_generator"), item(GEN + "wind_generator"), item(GEN + "gas_burning_generator"), item(GEN + "bio_generator")],
      "Challenge: Every Generator", subtitle="Six ways to make FE", deps=["mkp_intro"], xp=300, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each Mekanism generator: heat, solar, advanced solar, wind, gas-burning and bio.",
        "&eChemistry:&r between them: combustion, the photovoltaic effect, kinetic energy of air, and the energy stored in plant sugars by photosynthesis.",
        "&eHow:&r each one has its own quest on the Power page. The wind generator needs an Energy Tablet; the advanced solar is built from four basic solar generators.",
        "&eTip:&r none of these beats fission or fusion, but they never need fuel deliveries."]),
    Q("mk2_waste_barrel", 3, 17.5, [item(MEK + "radioactive_waste_barrel", 2)], "Radioactive Waste Barrel", subtitle="Somewhere safe for the leftovers", deps=["mkp_intro", "t6_fission"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r a barrel that stores spent nuclear waste and other radioactive chemicals, and lets them slowly decay.",
        "&eChemistry:&r radioactive decay can't be sped up by chemistry; you can only wait out the half-life. Real spent fuel spends years in cooling ponds, then decades in dry casks.",
        "&eHow:&r check JEI for the recipe. Pipe waste into it with pressurized tubes; never vent it or break a full tube.",
        "&eTip:&r reprocessing waste into plutonium and polonium (the T6 page) is better than storing it."]),
    Q("mk2_fusion_logic", 10, 17.5, [item(GEN + "fusion_reactor_logic_adapter")], "Fusion Logic Adapter", subtitle="Let redstone watch the star", deps=["mk2_ignition"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r a reactor block that outputs redstone for things like ignition state, plasma temperature or low fuel.",
        "&eHow:&r a fusion reactor frame surrounded by redstone; swap one frame of the shell for it and pick the mode in its GUI.",
        "&eTip:&r wire \"ready for ignition\" to your laser amplifier to relight the reactor automatically."]),

    # --- Bigger energy storage (ATM10-alignment round, 2026-10-19) -----------------------------
    Q("mkp_induction_adv", 0, 0, [item(MEK + "advanced_induction_cell"), item(MEK + "advanced_induction_provider")], "Advanced Induction",
      subtitle="More storage, faster in and out", deps=["mkp_intro", "pw_induction", "mk2_adv_circuit"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r cells set how much an Induction Matrix stores; providers set how fast power goes in and out. Swap basic ones for advanced and the same shell does far more.",
        "&eChemistry:&r the basic cells are lithium: Li has the lowest density of any metal and gives up its electron easily, which is why real batteries use it.",
        "&eHow:&r cell: four basic cells around an Advanced Energy Cube, with Energy Tablets in the corners. Provider: four basic providers around an Advanced Energy Cube, with &eAdvanced Control Circuits&r (MV). Check JEI.",
        "&eTip:&r cells and providers go inside the matrix, not in its walls."]),
    Q("mkp_induction_elite", 0, 0, [item(MEK + "elite_induction_cell"), item(MEK + "elite_induction_provider")], "Elite Induction",
      subtitle="The next tier inside the matrix", deps=["mkp_induction_adv", "mk2_elite_circuit"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r elite cells and providers, each again several times bigger than the advanced ones.",
        "&eHow:&r the same pattern one tier up: advanced cells around an Elite Energy Cube; advanced providers with &eElite Control Circuits&r (HV). Check JEI.",
        "&eTip:&r a fission or fusion plant needs a big buffer for when the turbine spins down. Size the providers to your turbine's output."]),
    Q("mkp_ult_cube", 0, 0, [item(MEK + "ultimate_energy_cube")], "Ultimate Energy Cube",
      subtitle="The biggest single-block battery", deps=["mkp_intro", "mk2_atomic"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the top Energy Cube: a lot of storage in one block you can pick up and carry, contents and all.",
        "&eHow:&r an Elite Energy Cube (Reinforced Alloy, gold) upgraded again with Atomic Alloy, Energy Tablets and diamonds (check JEI).",
        "&eTip:&r it's also the core of the ultimate induction cell and provider."]),
    Q("mkp_induction_ult", 0, 0, [item(MEK + "ultimate_induction_cell"), item(MEK + "ultimate_induction_provider")], "Challenge: Ultimate Induction",
      subtitle="A power bank for a star", deps=["mkp_induction_elite", "mkp_ult_cube", "mk2_ult_circuit"], xp=400, optional=True, tokens=2, desc=[
        "&6You remember holding the energy of a sun and not noticing the weight. This is close.&r",
        "&eWhat:&r the top Induction Matrix parts. A matrix full of these stores more than any other block in base Mekanism.",
        "&eHow:&r elite cells or providers around an Ultimate Energy Cube, with Ultimate Control Circuits for the provider (check JEI).",
        "&eTip:&r a full matrix lets a fusion reactor keep your base running while you refuel or rebuild it."]),

    # --- Mekanism: More Machine (y = 22.5 .. 25.5) ----------------------------------------------
    Q("mk2_mm_cnc", 0, 24, [anyof([MM + "cnc_stamper", MM + "cnc_lathe", MM + "cnc_rolling_mill"])], "CNC Machines", subtitle="More Machine: stamp, turn and roll", deps=["mkp_intro", "t3_mekcircuit"], xp=80, desc=[
        "&eWhat:&r Mekanism: More Machine adds CNC machines: the Stamper presses plates, the Lathe turns rods, the Rolling Mill rolls wire.",
        "&eHow:&r the CNC Stamper needs Basic Control Circuits, Basic Alloy, pistons and a steel casing. The Lathe also needs a Robit (check JEI). Any one counts.",
        "&eTip:&r MI's machines make most plates already. Use CNC machines for the mod recipes that list them in JEI (the stamper also prints AE2 processors)."]),
    Q("mk2_mm_recycler", 2, 24, [item(MM + "recycler"), item(MM + "scrap", 8)], "Recycler", subtitle="Stone and dirt into scrap", deps=["mk2_mm_cnc", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the Recycler grinds cheap blocks (stone, dirt, substrate) and sometimes leaves Scrap.",
        "&eHow:&r a Crusher, Advanced Control Circuits (MV), Infused Alloy and osmium (check JEI). About 1 stone in 6 gives a scrap.",
        "&eTip:&r 64 scrap compress into a Scrap Box, the first step towards UU-Matter. Start stockpiling early."]),
    Q("mk2_mm_large", 2, 22.5, [anyof([MM + "large_heat_generator", MM + "large_gas_burning_generator", MM + "large_wind_generator", MM + "large_chemical_infuser",
                                       MM + "large_electrolytic_separator", MM + "large_rotary_condensentrator", MM + "large_solar_neutron_activator", MM + "large_pigment_mixer"])],
      "Large Machines", subtitle="Big single-block versions", deps=["mk2_mm_cnc", "t6_pu"], xp=250, optional=True, tokens=1, desc=[
        "&eWhat:&r More Machine's large machines do the work of many normal ones, such as the Large Electrolytic Separator or Large Chemical Infuser.",
        "&eHow:&r most need a Robit, steel blocks and ultimate-tier tanks or circuits (EV). Any one counts; check JEI for each.",
        "&eTip:&r the Large Solar Neutron Activator is a big help for polonium and tritium."]),
    Q("mk2_mm_replicator", 4, 24, [item(MM + "replicator"), item(MM + "uu_matter")], "UU-Matter", subtitle="Matter from antimatter", deps=["mk2_mm_recycler", "t7_antimatter"], xp=500, size=1.5, shape="hexagon", desc=[
        "&6Scrap, crystal, antimatter, and then anything. You remember when making matter was just a thought.&r",
        "&eWhat:&r UU-Matter is More Machine's universal matter. The Replicator turns it back into items.",
        "&eHow:&r scrap boxes become Empty Crystals in the PRC (with fusion fuel and a special gas, check JEI). 64 crystals + antimatter in the Antiprotonic Nucleosynthesizer (an optional t7 quest) make one UU-Matter.",
        "&eTip:&r the Replicator needs Ultimate Control Circuits and Atomic Alloy. Check JEI for what it can copy."]),
    Q("mk2_mm_presser", 0, 25.5, [item(MM + "presser")], "Presser", subtitle="An upgraded stamper", deps=["mk2_mm_cnc", "t5_hv"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r the Presser builds on the CNC Stamper and makes processors and other pressed parts (check JEI for its recipes).",
        "&eHow:&r a CNC Stamper with Elite Control Circuits (HV), Reinforced Alloy and pistons.",
        "&eTip:&r press U on the Presser in JEI to see what it makes."]),
    Q("mk2_mm_planting", 2, 25.5, [item(MM + "planting_station")], "Planting Station", subtitle="Grow crops in a box", deps=["mk2_mm_recycler", "t5_hv"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r a machine that grows seeds and saplings indoors and outputs the harvest.",
        "&eChemistry:&r photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂, here powered by electricity instead of sunlight.",
        "&eHow:&r Elite Control Circuits (HV), Reinforced Alloy, bio fuel and a steel casing (check JEI)."]),
    Q("mk2_mm_doll", 4, 25.5, [item(MM + "author_doll")], "A Small Tribute", subtitle="Secret: the author, in doll form", deps=["mk2_mm_replicator"], xp=200, secret=True, loot="secret", desc=[
        "&eWhat:&r a decorative doll of More Machine's author, compressed out of 64 UU-Matter and a breath of antimatter in the Osmium Compressor.",
        "&eTip:&r the mod's modeller has a doll too, made from UU-Matter gas instead. Thank you, modders."]),
    Q("mk2_mm_gas", 6, 25.5, [item(MM + "ambient_gas_collector")], "Ambient Gas Collector", subtitle="Pull gas out of thin air", deps=["mk2_mm_recycler", "t6_pu"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r a machine that collects gas from its surroundings (check JEI and its GUI for what it gathers).",
        "&eChemistry:&r real air is 78% N₂, 21% O₂ and 1% argon; industry separates it by cooling it into a liquid and distilling it.",
        "&eHow:&r Atomic Alloy, an osmium block, an ultimate chemical tank and ultimate tubes (EV)."]),

    # --- Mekanism Extras (y = 28 / 29.5) --------------------------------------------------------
    Q("mk2_ex_radiance", 0, 28, [item(EX + "dust_radiance", 4), item(EX + "alloy_radiance", 2)], "Radiance", subtitle="Mekanism Extras begins", deps=["mkp_intro", "t6_yellowcake"], xp=200, desc=[
        "&eWhat:&r Mekanism Extras adds four tiers beyond ultimate: absolute, supreme, cosmic and infinite. Each needs a new alloy, starting with Radiance.",
        "&eHow:&r Osmium Compressor: glowstone dust + uranium oxide gas → Radiance Dust. Enrich it, then infuse Atomic Alloy with radiance (check JEI).",
        "&eTip:&r uranium oxide comes from oxidising yellowcake in the Chemical Oxidizer."]),
    Q("mk2_ex_absolute", 2, 28, [item(EX + "absolute_control_circuit", 2)], "Absolute Control Circuit", subtitle="Tier five", deps=["mk2_ex_radiance"], xp=250, desc=[
        "&eWhat:&r the first Extras circuit: an Ultimate Control Circuit between two Radiance Alloys.",
        "&eHow:&r craft it, or infuse an ultimate circuit with radiance in the Metallurgic Infuser.",
        "&eTip:&r absolute factories, cubes and tanks all start here."]),
    Q("mk2_ex_supreme", 4, 28, [item(EX + "alloy_thermonuclear", 2), item(EX + "supreme_control_circuit")], "Supreme Control Circuit", subtitle="Thermonuclear alloy", deps=["mk2_ex_absolute"], xp=300, desc=[
        "&eWhat:&r tier six. Its alloy is Thermonuclear: Radiance Alloy infused with thermonuclear material.",
        "&eHow:&r enriched radiance reacts with lava and molten thermonuclear in the PRC (check JEI for the full chain).",
        "&eTip:&r the circuit is an Absolute Control Circuit between two Thermonuclear Alloys."]),
    Q("mk2_ex_cosmic", 6, 28, [item(EX + "alloy_shining", 2), item(EX + "cosmic_control_circuit")], "Cosmic Control Circuit", subtitle="Shining alloy, made with antimatter", deps=["mk2_ex_supreme", "t7_antimatter"], xp=400, desc=[
        "&eWhat:&r tier seven. Its alloy, Shining, needs enriched thermonuclear transmuted with antimatter.",
        "&eHow:&r Antiprotonic Nucleosynthesizer: enriched thermonuclear + antimatter → enriched shining. Then infuse Thermonuclear Alloy with it (check JEI).",
        "&eTip:&r the Nucleosynthesizer is slow; run it on fusion power."]),
    Q("mk2_ex_infinite", 8, 28, [item(EX + "alloy_spectrum", 2), item(EX + "infinite_control_circuit")], "Infinite Control Circuit", subtitle="The last tier", deps=["mk2_ex_cosmic"], xp=600, size=1.5, shape="gear", desc=[
        "&6Infinite, the circuit says. You remember when that word described you.&r",
        "&eWhat:&r tier eight, the top of Mekanism Extras. Its alloy is Spectrum.",
        "&eHow:&r Osmium Compressor: enriched shining + antimatter → enriched spectrum; infuse Shining Alloy with it, then craft the circuit (check JEI)."]),
    Q("mk2_ex_factory", 1, 29.5, [anyof(ex_factories("absolute"))], "Absolute Factory", subtitle="Factories beyond ultimate", deps=["mk2_ex_absolute"], xp=250, optional=True, tokens=1, desc=[
        "&eWhat:&r Extras factories have more slots than ultimate ones, and Extras adds factory types base Mekanism lacks (oxidizing, washing, crystallizing, centrifuging...).",
        "&eHow:&r upgrade an ultimate factory with Absolute Control Circuits and Radiance Alloy, or use an Absolute Tier Installer. Any absolute factory counts.",
        "&eTip:&r the extra factory types are the big win: a washing or crystallizing factory speeds up the whole 5x line."]),
    Q("mk2_ex_naquadah", 4, 29.5, [item(EX + "raw_naquadah", 8)], "Naquadah", subtitle="A metal from science fiction", deps=["mk2_ex_supreme"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r Naquadah ore, added by Mekanism Extras. It is the fuel for the Naquadah Reactor.",
        "&eChemistry:&r naquadah is not real; it comes from the Stargate films. Every other material on this page is real chemistry.",
        "&eHow:&r Naquadah ore generates underground and in the End. Jade shows the block name when you look at it.",
        "&eTip:&r it processes like other Mekanism ores: dissolve, wash and crystallise for the best yield."]),
    Q("mk2_ex_reactor", 8, 29.5, [item(EX + "naquadah_reactor_controller"), item(EX + "naquadah_reactor_casing", 16)], "Naquadah Reactor", subtitle="A fusion reactor on fictional fuel", deps=["mk2_ex_cosmic", "mk2_ex_naquadah"], xp=500, optional=True, tokens=2, desc=[
        "&eWhat:&r a fusion-style power multiblock from Mekanism Extras that runs on naquadah-based fuel.",
        "&eHow:&r casings are lead blocks transmuted with antimatter in the Nucleosynthesizer; the controller needs Cosmic Control Circuits. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r the fuel chain starts with fluorinated naquadah-uranium fuel. Check JEI for each step."]),
], links=[("mk2_intro", -4, 0), ("t6_fission", -4, 2), ("mk2_salt", -6, 2), ("pw_turbine", -4, 4), ("pw_dt_fuel", -6, 4),
          ("pw_fusion", -4, 6), ("t3_mekcircuit", -4, 8), ("t7_opt_nucleo", -6, 8), ("t6_yellowcake", -4, 10), ("t7_antimatter", -6, 10)])
