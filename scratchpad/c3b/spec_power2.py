FIS, TUR, BOI, FUS, SPS = '"Fission"', '"Turbine"', '"Boiler"', '"Fusion"', '"Antimatter"'
SUIT, MOD, IND, QIO, GEAR = '"MekaSuit"', '"Modules"', '"Induction Matrix"', '"QIO"', '"Robots and Tools"'

EDIT = {
    "mkp_intro": {"mirror": '"078B69E9362A5496"', "section": FIS, "size": "2.0", "shape": '"gear"'},
    "mk2_sodium": {"mirror": '"17E2C05C48B03043"', "section": BOI, "deps": '["mkp_fission_port", "mk2_salt"]'},
    "mk2_boiler": {"mirror": '"6B7E13AB3BF2C5C8"', "section": BOI,
                   "tasks": '[item(MEK + "boiler_casing", 24), item(MEK + "structural_glass", 6), item(MEK + "boiler_valve", 4), item(MEK + "pressure_disperser"), item(MEK + "superheating_element")]',
                   "deps": '["mkp_boiler_valves", "mkp_boiler_core", "t6_fission"]', "size": "1.5", "shape": '"hexagon"'},
    "mk2_waste_barrel": {"mirror": '"593CB120B657126C"', "section": FIS, "tasks": '[item(MEK + "radioactive_waste_barrel")]',
                         "deps": '["mkp_fission"]', "optional": "False", "tokens": "None"},
    "mk2_turbine_shell": {"mirror": '"3E5BE6D6422F682C"', "section": TUR, "tasks": '[item(GEN + "turbine_valve", 2), item(GEN + "turbine_vent")]',
                          "deps": '["mkp_waste_tank", "pw_turbine"]'},
    "mk2_turbine_parts": {"mirror": '"4211F29561F21643"', "section": TUR,
                          "tasks": '[item(GEN + "turbine_rotor", 2), item(GEN + "turbine_blade", 4), item(GEN + "rotational_complex")]',
                          "title": '"Turbine Rotor"', "subtitle": '"Rotor, blades and the complex on top"', "deps": '["mkp_waste_tank", "pw_turbine"]'},
    "mk2_ignition": {"mirror": '"4926C95DD02F1410"', "section": FUS, "tasks": '[item(MEK + "laser")]', "title": '"Laser"',
                     "subtitle": '"Light, focused into a tool"', "deps": '["mkp_intro", "t7_laser"]'},
    "mk2_fusion_build": {"mirror": '"3561A33758A1E8C3"', "section": FUS,
                         "tasks": '[item(GEN + "fusion_reactor_controller"), item(GEN + "laser_focus_matrix"), item(GEN + "fusion_reactor_frame", 36), item(GEN + "reactor_glass", 25), item(GEN + "fusion_reactor_port", 3)]',
                         "title": '"The Fusion Reactor"', "deps": '["mkp_focus", "mkp_hohlraum", "mkp_fusion_port", "pw_dt_fuel"]',
                         "size": "2.0", "shape": '"gear"', "loot": '"t7"'},
    "mk2_fusion_logic": {"deps": '["mk2_fusion_build"]', "section": FUS},
    "mk2_robit": {"mirror": '"05DA7F48E2A1B77F"', "section": GEAR, "deps": '["mk2_refined_obsidian", "mkp_intro"]'},
    "mk2_miner": {"mirror": '"3B936CA3F0F7B26B"', "section": GEAR},
    "mk2_qio": {"mirror": '"5B18676A77CD6069"', "section": QIO, "tasks": '[item(MEK + "qio_drive_array")]', "deps": '["mk2_ult_circuit", "mkp_intro"]',
                "size": "1.5", "shape": '"hexagon"'},
    "mk2_qio_io": {"mirror": '"53E929BF89209CFC"', "section": QIO, "tasks": '[item(MEK + "qio_exporter"), item(MEK + "qio_importer")]',
                   "title": '"QIO Importer and Exporter"', "deps": '["mk2_qio"]'},
    "mk2_qio_drives": {"mirror": '"011D8CADA29C9C70"', "section": QIO,
                       "tasks": '[anyof([MEK + "qio_drive_" + t for t in ("base", "hyper_dense", "time_dilating", "supermassive")])]',
                       "title": '"QIO Drives"', "subtitle": '"Where the items actually live"', "deps": '["mk2_qio"]'},
    "mk2_module_base": {"mirror": '"6A1174845810C7A1"', "section": MOD},
    "mk2_mekatool": {"mirror": '"14385D3D359224BC"', "section": GEAR, "deps": '["mkp_disassembler", "mk2_module_base"]'},
    "mk2_mekasuit_full": {"mirror": '"56DB53F255100136"', "section": SUIT, "tasks": '[item(MEK + "mekasuit_pants")]', "title": '"MekaSuit Pants"',
                          "subtitle": '"Legs for the suit"', "deps": '["mkp_antimatter", "mk2_module_base"]', "size": "1.0", "shape": "None"},
}

M = [  # (suffix, module id, title, what, ATM10 id, optional)
    ("energy", "mekanism:module_energy_unit", "Energy Unit", "adds energy storage to the suit or tool, and is a part of other modules.", "5AC68C8A4024F4C9", False),
    ("color", "mekanism:module_color_modulation_unit", "Colour Modulation Unit", "lets you paint the MekaSuit any colour.", "4869D9DBDD1A15CD", False),
    ("laser", "mekanism:module_laser_dissipation_unit", "Laser Dissipation Unit", "spreads incoming laser energy over the suit so lasers stop hurting you.", "4447EEEB8D762721", False),
    ("radiation", "mekanism:module_radiation_shielding_unit", "Radiation Shielding Unit", "blocks radiation, so a leaking reactor hall is survivable.", "35D9CD19EAADED6C", False),
    ("excavation", "mekanism:module_excavation_escalation_unit", "Excavation Escalation Unit", "makes the Meka-Tool dig faster, at a higher energy cost.", "0F97EFAFD6E68F8D", False),
    ("attack", "mekanism:module_attack_amplification_unit", "Attack Amplification Unit", "raises the Meka-Tool's melee damage.", "3526D444F81AD6D9", False),
    ("farming", "mekanism:module_farming_unit", "Farming Unit", "lets the Meka-Tool till, strip and flatten like a hoe, axe and shovel.", "6518480251F0565A", False),
    ("shearing", "mekanism:module_shearing_unit", "Shearing Unit", "lets the Meka-Tool shear sheep and cut leaves and vines.", "00E19377BAE5DD6A", True),
    ("silk", "mekanism:module_silk_touch_unit", "Silk Touch Unit", "gives the Meka-Tool silk touch.", "7ECE00D12CFC50A4", True),
    ("fortune", "mekanism:module_fortune_unit", "Fortune Unit", "gives the Meka-Tool fortune.", "40B24676E11D9410", True),
    ("blasting", "mekanism:module_blasting_unit", "Blasting Unit", "makes the Meka-Tool break an area around each block.", "52B3955A80DB0B4A", True),
    ("vein", "mekanism:module_vein_mining_unit", "Vein Mining Unit", "mines a whole connected vein of ore or a whole tree at once.", "77B6A7151B3E5980", True),
    ("teleport", "mekanism:module_teleportation_unit", "Teleportation Unit", "teleports you to the block you look at.", "18EB2170CAC48E99", True),
    ("breathing", "mekanism:module_electrolytic_breathing_unit", "Electrolytic Breathing Unit", "splits the water around you into oxygen to breathe underwater.", "0133DA323E24A455", False),
    ("purification", "mekanism:module_inhalation_purification_unit", "Inhalation Purification Unit", "clears harmful potion effects from what you breathe.", "27195E9A3482C158", False),
    ("vision", "mekanism:module_vision_enhancement_unit", "Vision Enhancement Unit", "gives night vision.", "459AEC4C2A611824", False),
    ("nutrition", "mekanism:module_nutritional_injection_unit", "Nutritional Injection Unit", "feeds you nutritional paste from the helmet.", "63B0E39CA4B25A7E", False),
    ("dosimeter", "mekanism:module_dosimeter_unit", "Dosimeter Unit", "shows the radiation dose you have taken.", "43DB0CFC5F5B0967", False),
    ("geiger", "mekanism:module_geiger_unit", "Geiger Unit", "shows the radiation level around you.", "24E800EEC2CAD626", False),
    ("jetpack", "mekanism:module_jetpack_unit", "Jetpack Unit", "a hydrogen jetpack built into the chest piece.", "58B5EF8EB72934C2", False),
    ("charge", "mekanism:module_charge_distribution_unit", "Charge Distribution Unit", "shares the chest piece's energy with the rest of the suit.", "22171982D22CE15F", False),
    ("gravity", "mekanism:module_gravitational_modulating_unit", "Gravitational Modulating Unit", "creative-style flight, at a steep energy cost.", "7C7BD54624ED9AC2", False),
    ("elytra", "mekanism:module_elytra_unit", "Elytra Unit", "an elytra built into the chest piece.", "32ABE5D734703B9C", False),
    ("locomotive", "mekanism:module_locomotive_boosting_unit", "Locomotive Boosting Unit", "makes you sprint faster.", "2747AEE1F7F97848", False),
    ("gyro", "mekanism:module_gyroscopic_stabilization_unit", "Gyroscopic Stabilization Unit", "removes the mining slowdown while you float or swim.", "23B68F19A04AF5D7", False),
    ("hydrostatic", "mekanism:module_hydrostatic_repulsor_unit", "Hydrostatic Repulsor Unit", "lets you walk on the sea floor as if on land.", "4F9C8D90ACF563F5", False),
    ("servo", "mekanism:module_motorized_servo_unit", "Motorized Servo Unit", "raises your step height so you walk up blocks.", "1FC88A3BFCE6C9D7", False),
    ("hydraulic", "mekanism:module_hydraulic_propulsion_unit", "Hydraulic Propulsion Unit", "raises your jump height and step assist.", "0EBE20E44A7AEC7E", False),
    ("magnet", "mekanism:module_magnetic_attraction_unit", "Magnetic Attraction Unit", "pulls nearby items to you.", "48F496BD0FFE5A34", False),
    ("frost", "mekanism:module_frost_walker_unit", "Frost Walker Unit", "freezes water under your feet as you walk.", "795B80BF12D23897", False),
    ("soul", "mekanism:module_soul_surfer_unit", "Soul Surfer Unit", "speeds you up on soul sand and soul soil.", "5CE7756D80E051CC", False),
    ("geothermal", "mekanismgenerators:module_geothermal_generator_unit", "Geothermal Generator Unit", "charges the suit while you stand in lava or fire.", "62B29AEF8468750E", False),
    ("solar", "mekanismgenerators:module_solar_recharging_unit", "Solar Recharging Unit", "charges the suit in sunlight.", "123C0417D85B9DB2", False),
]
mods = []
for suf, mid, title, what, aid, opt in M:
    mods.append(f'''    Q("mkp_mod_{suf}", 0, 0, [item("{mid}")], "{title}", subtitle="A MekaSuit or Meka-Tool module", deps=["mk2_module_base"], xp=60,
      {"optional=True, tokens=1, " if opt else ""}mirror="{aid}", section="Modules", desc=[
        "&eWhat:&r this module {what}",
        "&eHow:&r built on a Module Base (check JEI for the rest). Install it in the Modification Station; several stack for a stronger effect.",
        "&eTip:&r every module draws from the suit's or tool's energy. Toggle it in the module menu when you don't need it."]),''')

INSERT = r'''
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
''' + "\n".join(mods) + "\n"
