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
        "&eTip:&r the machines, factories, circuits and logistics are on the first Mekanism page."], mirror="078B69E9362A5496", section="Fission", size=2.0, shape="gear"),

    # --- Generators and reactor multiblocks (y = 16 / 17.5) -------------------------------------
    Q("mk2_boiler", 0, 16, [item(MEK + "boiler_casing", 24), item(MEK + "structural_glass", 6), item(MEK + "boiler_valve", 4), item(MEK + "pressure_disperser"), item(MEK + "superheating_element")],
      "Thermoelectric Boiler", subtitle="Water into steam, by the tank", deps=["mkp_boiler_valves", "mkp_boiler_core", "t6_fission"], xp=150, desc=[
        "&eWhat:&r a multiblock boiler that turns water into steam, heated by Superheating Elements (power) or by hot coolant from a fission reactor.",
        "&eChemistry:&r boiling water takes 2,260 J per gram, far more than heating it. That latent heat is what the turbine later turns back into work.",
        "&eHow:&r the layout is in &eJust Enough Mekanism Multiblocks&r in JEI: casing walls, valves, a layer of pressure dispersers, and elements on the bottom.",
        "&eTip:&r a sodium-cooled fission reactor sends heated sodium here instead of boiling water itself."], mirror="6B7E13AB3BF2C5C8", section="Boiler", size=1.5, shape="hexagon"),
    Q("mk2_sodium", 2, 16, [tick()], "Sodium Coolant", subtitle="A liquid metal carries the heat", deps=["mkp_fission_port", "mk2_salt"], xp=200, desc=[
        "&eWhat:&r cool your fission reactor with sodium instead of water. It returns as superheated sodium, which the Thermoelectric Boiler uses to make steam before sending the sodium back.",
        "&eChemistry:&r sodium melts at 98 °C and boils at 883 °C, so it stays liquid at reactor temperatures without high pressure. Real fast reactors use it, and keep it away from water, which it reacts with violently.",
        "&eHow:&r sodium comes from brine in the Electrolytic Separator (see Salt and Sodium). Pipe it into the reactor, superheated sodium out to a boiler valve, and the cooled sodium back. Click to confirm once it runs.",
        "&eTip:&r one sodium loop feeds a much bigger boiler and turbine than water cooling does."], mirror="17E2C05C48B03043", section="Boiler"),
    Q("mk2_turbine_shell", 4, 16, [item(GEN + "turbine_valve", 2), item(GEN + "turbine_vent")], "Turbine Valves and Vents", subtitle="Steam in, spent steam out", deps=["mkp_waste_tank", "pw_turbine"], xp=150, desc=[
        "&eWhat:&r valves feed steam in and take power out; vents let the spent steam leave through the walls above the rotor.",
        "&eChemistry:&r a turbine extracts work as steam expands and cools. The more vent area, the more steam can pass per tick.",
        "&eHow:&r valve: turbine casings around an Advanced Control Circuit (MV). Vent: casings around iron bars (check JEI).",
        "&eTip:&r the turbine GUI shows whether vent flow or blade count is your limit."], mirror="3E5BE6D6422F682C", section="Turbine"),
    Q("mk2_turbine_parts", 6, 16, [item(GEN + "turbine_rotor", 2), item(GEN + "turbine_blade", 4), item(GEN + "rotational_complex")],
      "Turbine Rotor", subtitle="Rotor, blades and the complex on top", deps=["mkp_waste_tank", "pw_turbine"], xp=200, desc=[
        "&eWhat:&r the moving parts inside an Industrial Turbine. More blades and coils mean more power from the same steam.",
        "&eChemistry:&r condensers turn spent steam back into water, so the loop reuses the same water over and over.",
        "&eHow:&r stack rotors with two blades each on the centre column, a Rotational Complex on top, then coils and condensers above. See Just Enough Mekanism Multiblocks.",
        "&eTip:&r the turbine's GUI shows whether steam flow or blade count is the limit."], mirror="4211F29561F21643", section="Turbine"),
    Q("mk2_fusion_build", 8, 16, [item(GEN + "fusion_reactor_controller"), item(GEN + "laser_focus_matrix"), item(GEN + "fusion_reactor_frame", 36), item(GEN + "reactor_glass", 25), item(GEN + "fusion_reactor_port", 3)],
      "The Fusion Reactor", subtitle="Frame, glass, ports and a laser window", deps=["mkp_focus", "mkp_hohlraum", "mkp_fusion_port", "pw_dt_fuel"], xp=300, desc=[
        "&eWhat:&r the shell of the Fusion Reactor: frames, reactor glass, ports for fuel and output, and a Laser Focus Matrix to let the ignition laser in.",
        "&eHow:&r the 3D layout is in &eJust Enough Mekanism Multiblocks&r in JEI. The controller sits on top in the middle.",
        "&eTip:&r ports switch between input and output with a Configurator."], mirror="3561A33758A1E8C3", section="Fusion", size=2.0, shape="gear", loot="t7"),
    Q("mk2_ignition", 10, 16, [item(MEK + "laser")], "Laser", subtitle="Light, focused into a tool", deps=["mkp_intro", "t7_laser"], xp=200, desc=[
        "&eWhat:&r lasers charge a Laser Amplifier, which fires a single huge pulse into the reactor to ignite it.",
        "&eChemistry:&r deuterium and tritium only fuse above about 100 million °C, when the nuclei move fast enough to beat their electric repulsion.",
        "&eHow:&r put a filled Hohlraum in the controller, aim the amplifier at the Laser Focus Matrix and fire it with a redstone signal. Then go to the Fusion quest.",
        "&eTip:&r once lit, the reactor sustains itself as long as fuel keeps coming."], mirror="4926C95DD02F1410", section="Fusion"),
    Q("mk2_gen_field", 0, 17.5, [item(GEN + "heat_generator"), item(GEN + "solar_generator"), item(GEN + "advanced_solar_generator"), item(GEN + "wind_generator"), item(GEN + "gas_burning_generator"), item(GEN + "bio_generator")],
      "Challenge: Every Generator", subtitle="Six ways to make FE", deps=["mkp_intro"], xp=300, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each Mekanism generator: heat, solar, advanced solar, wind, gas-burning and bio.",
        "&eChemistry:&r between them: combustion, the photovoltaic effect, kinetic energy of air, and the energy stored in plant sugars by photosynthesis.",
        "&eHow:&r each one has its own quest on the Power page. The wind generator needs an Energy Tablet; the advanced solar is built from four basic solar generators.",
        "&eTip:&r none of these beats fission or fusion, but they never need fuel deliveries."]),
    Q("mk2_waste_barrel", 3, 17.5, [item(MEK + "radioactive_waste_barrel")], "Radioactive Waste Barrel", subtitle="Somewhere safe for the leftovers", deps=["mkp_fission"], xp=100, optional=False, tokens=None, desc=[
        "&eWhat:&r a barrel that stores spent nuclear waste and other radioactive chemicals, and lets them slowly decay.",
        "&eChemistry:&r radioactive decay can't be sped up by chemistry; you can only wait out the half-life. Real spent fuel spends years in cooling ponds, then decades in dry casks.",
        "&eHow:&r check JEI for the recipe. Pipe waste into it with pressurized tubes; never vent it or break a full tube.",
        "&eTip:&r reprocessing waste into plutonium and polonium (the T6 page) is better than storing it."], mirror="593CB120B657126C", section="Fission"),
    Q("mk2_fusion_logic", 10, 17.5, [item(GEN + "fusion_reactor_logic_adapter")], "Fusion Logic Adapter", subtitle="Let redstone watch the star", deps=["mk2_fusion_build"], xp=100, optional=True, tokens=1, desc=[
        "&eWhat:&r a reactor block that outputs redstone for things like ignition state, plasma temperature or low fuel.",
        "&eHow:&r a fusion reactor frame surrounded by redstone; swap one frame of the shell for it and pick the mode in its GUI.",
        "&eTip:&r wire \"ready for ignition\" to your laser amplifier to relight the reactor automatically."], section="Fusion"),

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

    Q("mk2_robit", 8, -1, [item(MEK + "robit")], "Robit", subtitle="A small robot friend", deps=["mk2_refined_obsidian", "mkp_intro"], xp=100, desc=[
        "&eWhat:&r the Robit follows you, picks up items, smelts and crafts. It is also a crafting part for the Digital Miner and several More Machine blocks.",
        "&eHow:&r Atomic Alloy, refined obsidian, steel, an Energy Tablet and a personal chest (check JEI). Place it on a Chargepad to recharge.",
        "&eTip:&r rename it with a name tag. It won't mind."], mirror="05DA7F48E2A1B77F", section="Robots and Tools"),
    Q("mk2_miner", 10, -1, [item(MEK + "digital_miner")], "Digital Miner", subtitle="Mine a whole area by filter", deps=["mk2_robit", "mk2_teleport_core"], xp=200, desc=[
        "&eWhat:&r a machine that mines out a large radius below it, taking only the blocks you filter for.",
        "&eHow:&r Atomic Alloy, a Logistical Sorter, a Robit, a Teleportation Core and a steel casing (check JEI). Set filters (tags like c:ores work), radius and height, then start it.",
        "&eTip:&r it uses a lot of power. Speed upgrades help, but bring Energy upgrades too. Rich deposits sit at metal-specific depths: set its height range to match."], mirror="3B936CA3F0F7B26B", section="Robots and Tools"),
    Q("mk2_qio", 8, 1, [item(MEK + "qio_drive_array")], "QIO", subtitle="Mekanism's digital storage", deps=["mk2_ult_circuit", "mkp_intro"], xp=250, desc=[
        "&eWhat:&r Quantum Item Orchestration: drives in a drive array hold items, and dashboards, importers and exporters reach them wirelessly through a frequency.",
        "&eHow:&r the drive array needs a Teleportation Core and Ultimate Control Circuits (EV); the base drive needs an ultimate circuit too. Give every QIO block the same frequency.",
        "&eTip:&r AE2 is the pack's main storage. QIO is a good wireless add-on for a remote outpost."], mirror="5B18676A77CD6069", section="QIO", size=1.5, shape="hexagon"),
    Q("mk2_qio_io", 10, 1, [item(MEK + "qio_exporter"), item(MEK + "qio_importer")], "QIO Importer and Exporter", subtitle="Importers, exporters and a dashboard to carry", deps=["mk2_qio"], xp=200, desc=[
        "&eWhat:&r importers pull items from the inventory they face into QIO; exporters push chosen items out. The Portable Dashboard opens your QIO from anywhere.",
        "&eHow:&r importer and exporter: lead, ender pearls, a Teleportation Core, an ultimate circuit and a (sticky) piston. The portable dashboard wraps a dashboard and a core in seven polonium pellets (check JEI).",
        "&eTip:&r an exporter with a filter on a machine's input is a tiny autocrafting line."], mirror="53E929BF89209CFC", section="QIO"),
    Q("mk2_qio_drives", 12, 2.5, [anyof([MEK + "qio_drive_" + t for t in ("base", "hyper_dense", "time_dilating", "supermassive")])], "QIO Drives", subtitle="Where the items actually live", deps=["mk2_qio"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r the Hyper-Dense QIO Drive holds far more than a base drive. Time-Dilating and Supermassive drives go further still.",
        "&eHow:&r each tier wraps the one below with a Teleportation Core and rarer materials (check JEI for each).",
        "&eTip:&r drive count matters as much as size: an array holds 12 drives."], mirror="011D8CADA29C9C70", section="QIO"),
    Q("mk2_module_base", 8, 9, [item(MEK + "module_base", 4), item(MEK + "modification_station")], "Modules", subtitle="The Modification Station", deps=["mk2_hdpe_parts", "t6_polonium"], xp=250, desc=[
        "&eWhat:&r module bases are the blank every MekaSuit and Meka-Tool module is built on. The Modification Station installs modules into your gear.",
        "&eHow:&r module base: an HDPE sheet in tin ingots and bronze nuggets (makes 2). Station: HDPE sheets, a chest, Ultimate Control Circuits (EV), a steel casing and a polonium pellet (check JEI).",
        "&eTip:&r press U on a Module Base in JEI to see every module and what each one needs."], mirror="6A1174845810C7A1", section="Modules"),
    Q("mk2_mekatool", 10, 8.25, [item(MEK + "meka_tool")], "Meka-Tool", subtitle="Every tool, upgradable", deps=["mkp_disassembler", "mk2_module_base"], xp=300, desc=[
        "&eWhat:&r the Atomic Disassembler grown up: one FE-powered tool that mines, digs, chops and fights, and takes modules for range, speed, silk touch, veinmining and more.",
        "&eHow:&r an Atomic Disassembler, a Configurator, HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI).",
        "&eTip:&r it drinks power fast with big modules. Carry a charged energy cube or wear the MekaSuit."], mirror="14385D3D359224BC", section="Robots and Tools"),
    Q("mk2_mekasuit_full", 10, 9.75, [item(MEK + "mekasuit_pants")], "MekaSuit Pants", subtitle="Legs for the suit", deps=["mkp_antimatter", "mk2_module_base"], xp=400, size=1.0, shape=None, desc=[
        "&6Four pieces, one will. You remember standing in fire and feeling only warmth.&r",
        "&eWhat:&r the MekaSuit legs and boots, completing the armour started on the Tools page. Legs take movement and locomotion modules; boots take jump and fall protection.",
        "&eHow:&r netherite leggings / boots in HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI).",
        "&eTip:&r the full suit shares one energy pool through its modules. Charge it on a Chargepad or with a charging module."], mirror="56DB53F255100136", section="MekaSuit"),


    # --- ATM10 mirror round (2026-10-20): ATM10's Mekanism Reactors chapter, quest for quest where we have the items -----
    Q("mkp_tips", 0, 0, [tick()], "Reactor Safety", subtitle="Read this before you build a reactor", deps=["mkp_intro"], xp=10, optional=True, tokens=1,
      icon=GEN + "fission_reactor_casing", mirror="066F78936C8F943B", section="Fission", desc=[
        "&eWhat:&r a fission reactor that runs out of coolant heats up, and a hot enough reactor melts down and leaves radiation behind.",
        "&eHow:&r start at a low burn rate, keep coolant and waste flowing, and put a logic adapter on the reactor so redstone can stop it.",
        "&eTip:&r test a new design in creative or at burn rate 0.1 first."]),
    Q("mkp_yellowcake", 0, 0, [item(MEK + "enrichment_chamber"), item(MEK + "yellow_cake_uranium"), item(MEK + "chemical_oxidizer")], "Yellowcake",
      subtitle="Uranium ore, enriched", deps=["mkp_intro", "t6_yellowcake"], xp=100, mirror="302E9BC711779A4A", section="Fission", desc=[
        "&eWhat:&r yellowcake is uranium concentrate. Oxidised, it becomes uranium oxide, the start of fission fuel.",
        "&eChemistry:&r real yellowcake is mostly U₃O₈ and related uranium oxides, leached out of the ore and dried.",
        "&eHow:&r Enrichment Chamber: uranium → yellowcake. Chemical Oxidizer: yellowcake → uranium oxide gas."]),
    Q("mkp_fluorite", 0, 0, [item(MEK + "rotary_condensentrator"), item(MEK + "chemical_infuser"), item(MEK + "chemical_dissolution_chamber"), item(MEK + "fluorite_gem")],
      "Hydrofluoric Acid", subtitle="Fluorite in sulfuric acid", deps=["mkp_intro"], xp=100, mirror="7D279FC39DA5C630", section="Fission", desc=[
        "&eWhat:&r hydrogen fluoride turns uranium oxide into uranium hexafluoride, the gas the centrifuge enriches.",
        "&eChemistry:&r CaF₂ + H₂SO₄ → CaSO₄ + 2HF. HF is one of the most dangerous acids there is: it passes through skin and attacks bone.",
        "&eHow:&r dissolve fluorite in sulfuric acid in the Dissolution Chamber; water vapour comes from the Rotary Condensentrator (check JEI)."]),
    Q("mkp_centrifuge", 0, 0, [item(MEK + "chemical_infuser"), item(MEK + "isotopic_centrifuge")], "Fissile Fuel", subtitle="UF₆, spun until it's enriched",
      deps=["mkp_yellowcake", "mkp_fluorite", "t6_centrifuge"], xp=150, mirror="71766BD7321FCB13", section="Fission", desc=[
        "&eWhat:&r the Chemical Infuser makes uranium hexafluoride; the Isotopic Centrifuge turns it into fissile fuel.",
        "&eChemistry:&r U-235 is only 0.7% of natural uranium. UF₆ is a gas, so centrifuges can separate the slightly lighter ²³⁵UF₆ molecules from ²³⁸UF₆.",
        "&eHow:&r uranium oxide + HF in the Chemical Infuser → UF₆; centrifuge → fissile fuel."]),
    Q("mkp_fission_parts", 0, 0, [item(GEN + "fission_fuel_assembly"), item(GEN + "control_rod_assembly")], "Fuel and Control Rods",
      subtitle="The core of the reactor", deps=["mkp_centrifuge"], xp=150, mirror="09D7D3CF61E156B1", section="Fission", desc=[
        "&eWhat:&r fuel assemblies hold the fissile fuel; control rod assemblies sit on top of each column.",
        "&eChemistry:&r control rods soak up neutrons (boron and cadmium are the real choices), which slows the chain reaction.",
        "&eHow:&r check JEI. The reactor's inside is columns of fuel assemblies, each capped with a control rod."]),
    Q("mkp_fission_logic", 0, 0, [item(GEN + "fission_reactor_logic_adapter")], "Fission Logic Adapter", subtitle="A redstone hand on the reactor",
      deps=["mkp_intro", "t6_fission"], xp=100, mirror="3D2B4D9FD2086B9B", section="Fission", desc=[
        "&eWhat:&r a reactor wall block that sends redstone (for high heat or low coolant) or takes it (to activate or SCRAM the reactor).",
        "&eHow:&r a fission reactor casing with redstone (check JEI). Swap it for one casing in the wall.",
        "&eTip:&r wire it to stop the reactor on high damage. It can save your base."]),
    Q("mkp_fission_port", 0, 0, [item(GEN + "fission_reactor_port", 2)], "Fission Reactor Ports", subtitle="Fuel and coolant in, steam and waste out",
      deps=["mkp_intro", "t6_fission"], xp=100, mirror="5A088F8402230BA5", section="Fission", desc=[
        "&eWhat:&r ports are where pipes meet the reactor. Each one can be set to input, output waste or output coolant.",
        "&eHow:&r fission reactor casings around a chemical tank (check JEI). Switch modes with a Configurator.",
        "&eTip:&r use at least two: one for fuel and coolant in, one for steam and waste out."]),
    Q("mkp_fission", 0, 0, [item(GEN + "fission_reactor_casing", 29), item(GEN + "fission_reactor_port", 4), item(GEN + "fission_reactor_logic_adapter"),
                            item(GEN + "fission_fuel_assembly"), item(GEN + "control_rod_assembly")], "Fission Reactor", subtitle="Splitting atoms for steam",
      deps=["mkp_fission_port", "mkp_fission_logic", "mkp_fission_parts"], xp=300, size=2.0, shape="gear", loot="t6", mirror="7E3C84D7FCEC9D52", section="Fission", desc=[
        "&6The atom yields. You remember the old fire inside every stone.&r",
        "&eWhat:&r a small fission reactor: casings, ports, a logic adapter and one column of fuel and control rods.",
        "&eChemistry:&r a U-235 nucleus that catches a neutron splits into two lighter nuclei, 2-3 neutrons and about 200 MeV of energy. The neutrons split the next nuclei.",
        "&eHow:&r the 3D layout is in Just Enough Mekanism Multiblocks in JEI. Feed it fissile fuel and water (or sodium); take steam and nuclear waste out."]),
    Q("mkp_scram", 0, 0, [item(GEN + "fission_reactor_logic_adapter", 2), item("minecraft:redstone"), item("minecraft:redstone_torch"), item("minecraft:repeater", 2)],
      "Automatic SCRAM", subtitle="Stop the reactor before it stops you", deps=["mkp_fission_logic"], xp=60, optional=True, tokens=1,
      mirror="7B0764DDE94E73D0", section="Fission", desc=[
        "&eWhat:&r one logic adapter watches for damage, the other shuts the reactor down. A torch and repeaters link them.",
        "&eChemistry:&r a real SCRAM drops every control rod at once; the chain reaction stops within seconds.",
        "&eHow:&r set one adapter to 'damage critical' output, the other to SCRAM input, and wire them together."]),
    Q("mkp_daylight", 0, 0, [item("minecraft:daylight_detector"), item("minecraft:redstone")], "Day Shift", subtitle="Run the reactor while you watch it",
      deps=["mkp_fission_logic"], xp=40, optional=True, tokens=1, mirror="5AEA705D6A64A982", section="Fission", desc=[
        "&eWhat:&r a daylight detector on the logic adapter runs the reactor only by day (or only by night, inverted).",
        "&eHow:&r set the adapter to activation input and wire the detector to it.",
        "&eTip:&r a simple timer while you are still learning how your design behaves."]),
    Q("mkp_waste_tank", 0, 0, [item(MEK + "basic_chemical_tank")], "Steam and Waste Tanks", subtitle="Buffers around the reactor", deps=["mkp_fission"], xp=60,
      mirror="7B385FD1CBE02C85", section="Turbine", desc=[
        "&eWhat:&r chemical tanks between the reactor and the rest of the plant hold steam and waste when something downstream stops.",
        "&eHow:&r osmium and redstone (check JEI). Higher tiers hold more.",
        "&eTip:&r a full waste tank stops the reactor safely; an empty one is a warning sign."]),
    Q("mkp_waste_centrifuge", 0, 0, [item(MEK + "isotopic_centrifuge")], "Reprocessing Waste", subtitle="Nuclear waste into plutonium",
      deps=["mk2_waste_barrel", "t6_centrifuge"], xp=150, mirror="5194A067BEA98E79", section="Antimatter", desc=[
        "&eWhat:&r the Isotopic Centrifuge turns nuclear waste into plutonium.",
        "&eChemistry:&r in a reactor, U-238 catches neutrons and turns into Pu-239 over two beta decays. Reprocessing pulls it back out of the spent fuel.",
        "&eHow:&r pipe waste from the reactor into the centrifuge (check JEI)."]),
    Q("mkp_plutonium", 0, 0, [item(MEK + "pellet_plutonium")], "Plutonium Pellet", subtitle="Waste turned into value", deps=["mkp_waste_centrifuge"],
      xp=200, size=2.0, shape="gear", mirror="20054D077AFE3F56", section="Antimatter", desc=[
        "&eWhat:&r plutonium pellets go into the SPS, the Seed's chemistry and late recipes.",
        "&eHow:&r crystallise plutonium in the Chemical Crystallizer (check JEI).",
        "&eTip:&r every pellet started as reactor waste."]),
    Q("mkp_sna", 0, 0, [item(MEK + "solar_neutron_activator")], "Solar Neutron Activator", subtitle="Sunlight, neutrons, new isotopes",
      deps=["mk2_waste_barrel", "t6_sna"], xp=150, mirror="4BAF44FCA0894DE8", section="Antimatter", desc=[
        "&eWhat:&r the SNA uses sunlight to bombard a chemical with neutrons: nuclear waste into polonium, lithium into tritium.",
        "&eChemistry:&r Li-6 + n → He-4 + T (tritium). Bi-209 + n → Bi-210, which decays into Po-210.",
        "&eHow:&r it needs open sky above it (check JEI for the recipe)."]),
    Q("mkp_polonium", 0, 0, [item(MEK + "pellet_polonium")], "Polonium Pellet", subtitle="A fierce little isotope", deps=["mkp_sna"], xp=200, size=2.0,
      shape="gear", mirror="438F734D16DA9638", section="Antimatter", desc=[
        "&eWhat:&r polonium pellets power QIO, the MekaSuit, the SPS and more.",
        "&eChemistry:&r Po-210 is an alpha emitter with a 138-day half-life. Gram for gram it gives off about 140 W of heat.",
        "&eHow:&r SNA: waste → polonium, then crystallise it into pellets (check JEI)."]),
    Q("mkp_hazmat", 0, 0, [item(MEK + "hazmat_mask"), item(MEK + "hazmat_gown"), item(MEK + "hazmat_pants"), item(MEK + "hazmat_boots")], "Hazmat Suit",
      subtitle="Dress for the reactor room", deps=["mk2_waste_barrel"], xp=60, optional=True, tokens=1, mirror="2DC4446A644A4079", section="Fission", desc=[
        "&eWhat:&r a full hazmat set blocks radiation damage while you work near leaks.",
        "&eChemistry:&r most radiation from waste is alpha and beta: a layer of clothing and plastic stops it, but breathing it in does not.",
        "&eHow:&r HDPE and fabric pieces (check JEI). Wear all four."]),
    Q("mkp_turbine_top", 0, 0, [item(MEK + "pressure_disperser"), item(GEN + "electromagnetic_coil"), item(GEN + "saturating_condenser")], "Turbine Upper Deck",
      subtitle="Disperser, coil and condenser", deps=["mkp_waste_tank", "pw_turbine"], xp=150, mirror="02C6132919DEAF2A", section="Turbine", desc=[
        "&eWhat:&r above the rotor sit a layer of pressure dispersers, electromagnetic coils that make the power, and condensers that turn steam back into water.",
        "&eChemistry:&r a coil turning in a magnetic field makes current (Faraday's law). The condenser recovers the water as steam gives up its heat.",
        "&eHow:&r check JEI for each part; the layout is in Just Enough Mekanism Multiblocks."]),
    Q("mkp_turbine", 0, 0, [item(GEN + "turbine_casing", 52), item(MEK + "structural_glass", 64), item(GEN + "turbine_valve", 2), item(GEN + "turbine_rotor", 2),
                            item(GEN + "turbine_blade", 4), item(GEN + "rotational_complex"), item(MEK + "pressure_disperser", 8),
                            item(GEN + "electromagnetic_coil", 9), item(GEN + "saturating_condenser", 9), item(GEN + "turbine_vent", 12)],
      "Industrial Turbine", subtitle="Steam into serious power", deps=["mk2_turbine_shell", "mk2_turbine_parts", "mkp_turbine_top"], xp=300, size=1.5,
      shape="hexagon", loot="t6", mirror="6CCE920735187234", section="Turbine", desc=[
        "&eWhat:&r a full Industrial Turbine: casing and glass walls, valves, vents, a rotor with blades, and the upper deck.",
        "&eHow:&r the parts list above builds a 7x7 turbine; the layout is in Just Enough Mekanism Multiblocks.",
        "&eTip:&r feed it the reactor's steam and send the condensed water back."]),
    Q("mkp_boiler_valves", 0, 0, [item(MEK + "boiler_valve", 4)], "Boiler Valves", subtitle="Pipes into the boiler", deps=["mk2_sodium"], xp=80,
      mirror="141D68BAD039784B", section="Boiler", desc=[
        "&eWhat:&r valves let water, hot coolant and steam in and out of the Thermoelectric Boiler.",
        "&eHow:&r boiler casings around an Advanced Control Circuit (check JEI).",
        "&eTip:&r set each valve's mode with a Configurator."]),
    Q("mkp_boiler_core", 0, 0, [item(MEK + "superheating_element"), item(MEK + "pressure_disperser")], "Boiler Core", subtitle="Heaters and the disperser layer",
      deps=["mkp_intro", "t6_fission"], xp=80, mirror="5B9F3F32AB28A83A", section="Boiler", desc=[
        "&eWhat:&r superheating elements heat the boiler with electricity; the disperser layer splits water from steam.",
        "&eHow:&r check JEI for both.",
        "&eTip:&r with sodium cooling you can skip most of the elements."]),
    Q("mkp_amplifier", 0, 0, [item(MEK + "laser_amplifier")], "Laser Amplifier", subtitle="Store a laser's energy, release it at once",
      deps=["mk2_ignition"], xp=150, mirror="1C87535D3CDCDA5F", section="Fusion", desc=[
        "&eWhat:&r lasers charge the Laser Amplifier, which fires one huge pulse on a redstone signal.",
        "&eHow:&r check JEI. Aim the lasers into it, and it at the reactor's focus matrix."]),
    Q("mkp_focus", 0, 0, [item(GEN + "laser_focus_matrix")], "Laser Focus Matrix", subtitle="A window for the laser", deps=["mkp_amplifier"], xp=100,
      mirror="0306D25C7407FE88", section="Fusion", desc=[
        "&eWhat:&r the reactor wall block the ignition laser fires through.",
        "&eHow:&r reactor glass and redstone (check JEI)."]),
    Q("mkp_deuterium", 0, 0, [item(MEK + "electric_pump"), item(MEK + "upgrade_filter"), item(MEK + "electrolytic_separator")], "Deuterium",
      subtitle="Heavy water, split", deps=["mk2_upgrade_set"], xp=100, mirror="40E8940C92668D4F", section="Fusion", desc=[
        "&eWhat:&r a pump with a Filter upgrade pulls heavy water; the separator splits it into deuterium and oxygen.",
        "&eChemistry:&r 2D₂O → 2D₂ + O₂. Deuterium is hydrogen with one neutron.",
        "&eHow:&r Electric Pump + Filter upgrade over water, into an Electrolytic Separator."]),
    Q("mkp_tritium", 0, 0, [item(MEK + "thermal_evaporation_block", 33), item(MEK + "thermal_evaporation_controller"), item(MEK + "thermal_evaporation_valve"),
                            item(MEK + "rotary_condensentrator"), item(MEK + "solar_neutron_activator")], "Tritium", subtitle="Lithium, hit by neutrons",
      deps=["mkp_sna"], xp=150, mirror="369DADE3B3D8416F", section="Fusion", desc=[
        "&eWhat:&r brine boils down to lithium in the evaporation plant; the SNA turns lithium into tritium.",
        "&eChemistry:&r Li-6 + n → He-4 + T. Tritium is hydrogen with two neutrons and a half-life of about 12 years.",
        "&eHow:&r evaporation plant → liquid lithium → condensentrator → lithium gas → SNA."]),
    Q("mkp_hohlraum", 0, 0, [item(MEK + "chemical_infuser"), item(GEN + "hohlraum")], "D-T Fuel and the Hohlraum", subtitle="Fuel for a star",
      deps=["mkp_tritium", "mkp_deuterium", "pw_dt_fuel"], xp=200, mirror="7177653B736AB10E", section="Fusion", desc=[
        "&eWhat:&r deuterium + tritium in the Chemical Infuser make D-T fuel. A hohlraum filled with it starts the reaction.",
        "&eChemistry:&r D + T → He-4 + n + 17.6 MeV, the easiest fusion reaction to ignite.",
        "&eHow:&r fill the hohlraum with D-T fuel in a chemical tank's slot and place it in the controller (check JEI)."]),
    Q("mkp_fusion_port", 0, 0, [item(GEN + "fusion_reactor_port")], "Fusion Reactor Port", subtitle="Fuel in, power and steam out", deps=["mkp_polonium"],
      xp=150, mirror="4E18E28BDF6B7983", section="Fusion", desc=[
        "&eWhat:&r ports feed fuel in and take power, steam or hot coolant out.",
        "&eHow:&r a reactor frame with circuits and a chemical tank (check JEI). Switch the mode with a Configurator."]),
    Q("mkp_sps_port", 0, 0, [item(MEK + "sps_port")], "SPS Port", subtitle="Polonium in, antimatter out", deps=["mkp_polonium", "mkp_plutonium", "t7_sps"],
      xp=200, mirror="7846B7FFC3DD85C5", section="Antimatter", desc=[
        "&eWhat:&r the Supercritical Phase Shifter's ports: polonium goes in, antimatter comes out.",
        "&eHow:&r SPS casing, a chemical tank and Ultimate Control Circuits (check JEI)."]),
    Q("mkp_coil", 0, 0, [item(MEK + "supercharged_coil")], "Supercharged Coil", subtitle="Power into the SPS", deps=["mkp_polonium", "t7_sps"], xp=200,
      mirror="3CCBE9BBCA8ADA38", section="Antimatter", desc=[
        "&eWhat:&r the coil carries power into the SPS through one of its ports.",
        "&eHow:&r check JEI. Place it against a port, on the outside."]),
    Q("mkp_sps", 0, 0, [item(MEK + "sps_casing", 60), item(MEK + "structural_glass", 64), item(MEK + "sps_port", 4), item(MEK + "supercharged_coil", 2)],
      "Supercritical Phase Shifter", subtitle="The machine that makes antimatter", deps=["mkp_sps_port", "mkp_coil"], xp=400, size=2.0, shape="gear",
      loot="t7", mirror="008E65AF545A706E", section="Antimatter", desc=[
        "&6You remember the moment matter met its mirror. Now you can make it.&r",
        "&eWhat:&r the SPS: a 7x7 shell of casing and glass with ports and coils.",
        "&eHow:&r the layout is in Just Enough Mekanism Multiblocks. It needs a lot of power per tick.",
        "&eTip:&r feed it polonium steadily; it only makes a little antimatter at a time."]),
    Q("mkp_antimatter", 0, 0, [item(MEK + "pellet_antimatter")], "Antimatter Pellet", subtitle="Matter's mirror image", deps=["mkp_sps", "t7_antimatter"],
      xp=400, size=2.0, shape="gear", mirror="50F23B2688D7E699", section="MekaSuit", desc=[
        "&eWhat:&r antimatter pellets: the late-game material for the Nucleosynthesizer and the Seed's chemistry.",
        "&eChemistry:&r every particle has an antiparticle with the opposite charge. When they meet, both turn into energy (E = mc²).",
        "&eHow:&r SPS → antimatter gas → Chemical Crystallizer → pellets (check JEI)."]),
    Q("mkp_nucleo", 0, 0, [item(MEK + "antiprotonic_nucleosynthesizer")], "Antiprotonic Nucleosynthesizer", subtitle="Turn one element into another",
      deps=["mkp_antimatter"], xp=300, hidden=True, mirror="4B2835706B593E9A", section="MekaSuit", desc=[
        "&eWhat:&r uses antimatter to transmute items: one element into another.",
        "&eChemistry:&r real transmutation needs nuclear reactions, not chemistry: you change the number of protons in the nucleus.",
        "&eHow:&r check JEI for the recipe and every transmutation it can do."]),
    Q("mkp_meka_helmet", 0, 0, [item(MEK + "mekasuit_helmet")], "MekaSuit Helmet", subtitle="Sight, air and food", deps=["mkp_antimatter", "mk2_module_base"],
      xp=150, mirror="7864C8F2CBC910CB", section="MekaSuit", desc=[
        "&eWhat:&r the MekaSuit helmet takes breathing, vision and nutrition modules.",
        "&eHow:&r a netherite helmet in HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI)."]),
    Q("mkp_meka_body", 0, 0, [item(MEK + "mekasuit_bodyarmor")], "MekaSuit Bodyarmor", subtitle="Jetpack, elytra, gravity", deps=["mkp_antimatter", "mk2_module_base"],
      xp=150, mirror="6C1F7A0B330B3F42", section="MekaSuit", desc=[
        "&eWhat:&r the chest piece holds the suit's flight modules and shares energy with the rest.",
        "&eHow:&r a netherite chestplate in HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI)."]),
    Q("mkp_meka_boots", 0, 0, [item(MEK + "mekasuit_boots")], "MekaSuit Boots", subtitle="Jumps, falls and frost", deps=["mkp_antimatter", "mk2_module_base"],
      xp=150, mirror="6D7D0A5313284B53", section="MekaSuit", desc=[
        "&eWhat:&r the boots take jump boost, fall protection, frost walker and more.",
        "&eHow:&r netherite boots in HDPE sheets, Ultimate Control Circuits, polonium pellets and a Basic Induction Cell (check JEI)."]),
    Q("mkp_suit_tip", 0, 0, [tick()], "Wearing a Reactor", subtitle="How the MekaSuit spends energy", deps=["mk2_module_base"], xp=10, optional=True, tokens=1,
      icon=MEK + "module_base", mirror="505799C894C771B2", section="MekaSuit", desc=[
        "&eWhat:&r every installed module draws energy. The suit can run dry in a fight if you leave everything on.",
        "&eHow:&r open the module menu (the Mekanism key) to toggle modules, and add Energy Units for more storage.",
        "&eTip:&r a Geothermal or Solar unit keeps a suit topped up between charges."]),
    Q("mkp_disassembler", 0, 0, [item(MEK + "atomic_disassembler")], "Atomic Disassembler", subtitle="One tool for everything", deps=["mkp_intro"], xp=100,
      mirror="16DDAE318535D0F9", section="Robots and Tools", desc=[
        "&eWhat:&r an FE-powered pickaxe, axe, shovel and sword in one, with several dig modes.",
        "&eHow:&r Atomic Alloy, an Energy Tablet and obsidian (check JEI).",
        "&eTip:&r it is the base of the Meka-Tool."]),
    Q("mkp_qio_dashboard", 0, 0, [item(MEK + "qio_dashboard")], "QIO Dashboard", subtitle="A terminal for your drives", deps=["mk2_qio"], xp=100,
      mirror="13A5748DF69D832E", section="QIO", desc=[
        "&eWhat:&r the dashboard shows every item in your QIO and crafts from it.",
        "&eHow:&r check JEI. Give it the same frequency as your drive array."]),
    Q("mkp_qio_portable", 0, 0, [item(MEK + "portable_qio_dashboard")], "Portable QIO Dashboard", subtitle="Your storage, anywhere",
      deps=["mkp_qio_dashboard", "t6_polonium"], xp=150, mirror="7310BBC4A90EDA9D", section="QIO", desc=[
        "&eWhat:&r a hand-held dashboard that opens your QIO from anywhere.",
        "&eHow:&r a dashboard and polonium pellets (check JEI)."]),
    Q("mkp_ind_port", 0, 0, [item(MEK + "induction_port")], "Induction Port", subtitle="Power in and out of the matrix", deps=["mkp_intro", "pw_induction"], xp=100,
      mirror="55702BE0151D33FE", section="Induction Matrix", desc=[
        "&eWhat:&r ports are the matrix's connections. Switch each between input and output with a Configurator.",
        "&eHow:&r induction casing around an Elite Control Circuit (check JEI)."]),
    Q("mkp_ind_cell", 0, 0, [anyof([MEK + t + "_induction_cell" for t in ("basic", "advanced", "elite", "ultimate")])], "Induction Cell",
      subtitle="Sets how much the matrix holds", deps=["mkp_intro", "pw_induction"], xp=100, mirror="298A7BED5C2C7582", section="Induction Matrix", desc=[
        "&eWhat:&r cells inside the matrix store the energy. Any tier counts.",
        "&eChemistry:&r the basic cell is built on lithium dust: lithium gives up its electron easily, which is why real batteries use it.",
        "&eHow:&r check JEI."]),
    Q("mkp_ind_provider", 0, 0, [anyof([MEK + t + "_induction_provider" for t in ("basic", "advanced", "elite", "ultimate")])], "Induction Provider",
      subtitle="Sets how fast power moves", deps=["mkp_intro", "pw_induction"], xp=100, mirror="6B3BD54A34EB02C2", section="Induction Matrix", desc=[
        "&eWhat:&r providers set how much power the matrix can take in or give out per tick. Any tier counts.",
        "&eHow:&r check JEI."]),
    Q("mkp_matrix", 0, 0, [item(MEK + "induction_casing", 32), item(MEK + "induction_port", 2)], "Induction Matrix", subtitle="The big battery",
      deps=["mkp_ind_port", "mkp_ind_cell", "mkp_ind_provider"], xp=200, size=1.5, shape="hexagon", loot="t5", mirror="54E0B946BAC13654",
      section="Induction Matrix", desc=[
        "&eWhat:&r a multiblock battery of any size from 3x3x3: casing walls, two ports, and cells and providers inside.",
        "&eHow:&r the layout is in Just Enough Mekanism Multiblocks in JEI.",
        "&eTip:&r size the providers to your biggest generator, and the cells to a night's worth of use."]),
    Q("mkp_mod_energy", 0, 0, [item("mekanism:module_energy_unit")], "Energy Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="5AC68C8A4024F4C9", section="Modules", desc=[
        "&eWhat:&r this module adds energy storage to the suit or tool, and is a part of other modules.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_color", 0, 0, [item("mekanism:module_color_modulation_unit")], "Colour Modulation Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="4869D9DBDD1A15CD", section="Modules", desc=[
        "&eWhat:&r this module lets you paint the MekaSuit any colour.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_laser", 0, 0, [item("mekanism:module_laser_dissipation_unit")], "Laser Dissipation Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="4447EEEB8D762721", section="Modules", desc=[
        "&eWhat:&r this module spreads incoming laser energy over the suit so lasers stop hurting you.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_radiation", 0, 0, [item("mekanism:module_radiation_shielding_unit")], "Radiation Shielding Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="35D9CD19EAADED6C", section="Modules", desc=[
        "&eWhat:&r this module blocks radiation, so a leaking reactor hall is survivable.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_excavation", 0, 0, [item("mekanism:module_excavation_escalation_unit")], "Excavation Escalation Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="0F97EFAFD6E68F8D", section="Modules", desc=[
        "&eWhat:&r this module makes the Meka-Tool dig faster, at a higher energy cost.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_attack", 0, 0, [item("mekanism:module_attack_amplification_unit")], "Attack Amplification Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="3526D444F81AD6D9", section="Modules", desc=[
        "&eWhat:&r this module raises the Meka-Tool's melee damage.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_farming", 0, 0, [item("mekanism:module_farming_unit")], "Farming Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="6518480251F0565A", section="Modules", desc=[
        "&eWhat:&r this module lets the Meka-Tool till, strip and flatten like a hoe, axe and shovel.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_shearing", 0, 0, [item("mekanism:module_shearing_unit")], "Shearing Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      optional=True, tokens=1, mirror="00E19377BAE5DD6A", section="Modules", desc=[
        "&eWhat:&r this module lets the Meka-Tool shear sheep and cut leaves and vines.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_silk", 0, 0, [item("mekanism:module_silk_touch_unit")], "Silk Touch Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      optional=True, tokens=1, mirror="7ECE00D12CFC50A4", section="Modules", desc=[
        "&eWhat:&r this module gives the Meka-Tool silk touch.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_fortune", 0, 0, [item("mekanism:module_fortune_unit")], "Fortune Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      optional=True, tokens=1, mirror="40B24676E11D9410", section="Modules", desc=[
        "&eWhat:&r this module gives the Meka-Tool fortune.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_blasting", 0, 0, [item("mekanism:module_blasting_unit")], "Blasting Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      optional=True, tokens=1, mirror="52B3955A80DB0B4A", section="Modules", desc=[
        "&eWhat:&r this module makes the Meka-Tool break an area around each block.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_vein", 0, 0, [item("mekanism:module_vein_mining_unit")], "Vein Mining Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      optional=True, tokens=1, mirror="77B6A7151B3E5980", section="Modules", desc=[
        "&eWhat:&r this module mines a whole connected vein of ore or a whole tree at once.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_teleport", 0, 0, [item("mekanism:module_teleportation_unit")], "Teleportation Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      optional=True, tokens=1, mirror="18EB2170CAC48E99", section="Modules", desc=[
        "&eWhat:&r this module teleports you to the block you look at.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_breathing", 0, 0, [item("mekanism:module_electrolytic_breathing_unit")], "Electrolytic Breathing Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="0133DA323E24A455", section="Modules", desc=[
        "&eWhat:&r this module splits the water around you into oxygen to breathe underwater.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_purification", 0, 0, [item("mekanism:module_inhalation_purification_unit")], "Inhalation Purification Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="27195E9A3482C158", section="Modules", desc=[
        "&eWhat:&r this module clears harmful potion effects from what you breathe.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_vision", 0, 0, [item("mekanism:module_vision_enhancement_unit")], "Vision Enhancement Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="459AEC4C2A611824", section="Modules", desc=[
        "&eWhat:&r this module gives night vision.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_nutrition", 0, 0, [item("mekanism:module_nutritional_injection_unit")], "Nutritional Injection Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="63B0E39CA4B25A7E", section="Modules", desc=[
        "&eWhat:&r this module feeds you nutritional paste from the helmet.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_dosimeter", 0, 0, [item("mekanism:module_dosimeter_unit")], "Dosimeter Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="43DB0CFC5F5B0967", section="Modules", desc=[
        "&eWhat:&r this module shows the radiation dose you have taken.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_geiger", 0, 0, [item("mekanism:module_geiger_unit")], "Geiger Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="24E800EEC2CAD626", section="Modules", desc=[
        "&eWhat:&r this module shows the radiation level around you.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_jetpack", 0, 0, [item("mekanism:module_jetpack_unit")], "Jetpack Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="58B5EF8EB72934C2", section="Modules", desc=[
        "&eWhat:&r this module a hydrogen jetpack built into the chest piece.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_charge", 0, 0, [item("mekanism:module_charge_distribution_unit")], "Charge Distribution Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="22171982D22CE15F", section="Modules", desc=[
        "&eWhat:&r this module shares the chest piece's energy with the rest of the suit.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_gravity", 0, 0, [item("mekanism:module_gravitational_modulating_unit")], "Gravitational Modulating Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="7C7BD54624ED9AC2", section="Modules", desc=[
        "&eWhat:&r this module creative-style flight, at a steep energy cost.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_elytra", 0, 0, [item("mekanism:module_elytra_unit")], "Elytra Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="32ABE5D734703B9C", section="Modules", desc=[
        "&eWhat:&r this module an elytra built into the chest piece.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_locomotive", 0, 0, [item("mekanism:module_locomotive_boosting_unit")], "Locomotive Boosting Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="2747AEE1F7F97848", section="Modules", desc=[
        "&eWhat:&r this module makes you sprint faster.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_gyro", 0, 0, [item("mekanism:module_gyroscopic_stabilization_unit")], "Gyroscopic Stabilization Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="23B68F19A04AF5D7", section="Modules", desc=[
        "&eWhat:&r this module removes the mining slowdown while you float or swim.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_hydrostatic", 0, 0, [item("mekanism:module_hydrostatic_repulsor_unit")], "Hydrostatic Repulsor Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="4F9C8D90ACF563F5", section="Modules", desc=[
        "&eWhat:&r this module lets you walk on the sea floor as if on land.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_servo", 0, 0, [item("mekanism:module_motorized_servo_unit")], "Motorized Servo Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="1FC88A3BFCE6C9D7", section="Modules", desc=[
        "&eWhat:&r this module raises your step height so you walk up blocks.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_hydraulic", 0, 0, [item("mekanism:module_hydraulic_propulsion_unit")], "Hydraulic Propulsion Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="0EBE20E44A7AEC7E", section="Modules", desc=[
        "&eWhat:&r this module raises your jump height and step assist.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_magnet", 0, 0, [item("mekanism:module_magnetic_attraction_unit")], "Magnetic Attraction Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="48F496BD0FFE5A34", section="Modules", desc=[
        "&eWhat:&r this module pulls nearby items to you.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_frost", 0, 0, [item("mekanism:module_frost_walker_unit")], "Frost Walker Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="795B80BF12D23897", section="Modules", desc=[
        "&eWhat:&r this module freezes water under your feet as you walk.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_soul", 0, 0, [item("mekanism:module_soul_surfer_unit")], "Soul Surfer Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="5CE7756D80E051CC", section="Modules", desc=[
        "&eWhat:&r this module speeds you up on soul sand and soul soil.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_geothermal", 0, 0, [item("mekanismgenerators:module_geothermal_generator_unit")], "Geothermal Generator Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="62B29AEF8468750E", section="Modules", desc=[
        "&eWhat:&r this module charges the suit while you stand in lava or fire.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
    Q("mkp_mod_solar", 0, 0, [item("mekanismgenerators:module_solar_recharging_unit")], "Solar Recharging Unit", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      mirror="123C0417D85B9DB2", section="Modules", desc=[
        "&eWhat:&r this module charges the suit in sunlight.",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),
], links=[("mk2_intro", -4, 0), ("t6_fission", -4, 2), ("mk2_salt", -6, 2), ("pw_turbine", -4, 4), ("pw_dt_fuel", -6, 4),
          ("pw_fusion", -4, 6), ("t3_mekcircuit", -4, 8), ("t7_opt_nucleo", -6, 8), ("t6_yellowcake", -4, 10), ("t7_antimatter", -6, 10)], mirror="mekanism_reactors")
