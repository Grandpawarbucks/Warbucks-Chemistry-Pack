"""Quest chapter: mekanism (mod page: Mekanism, Mekanism Generators, Mekanism: More Machine, Mekanism Extras).
See tools/quests/STYLE.md. Build: python3 tools/build_quests.py

Main-path Mekanism quests live in t3..t7 and power.py; this page LINKS to them (column x = -4) instead of
duplicating them. Mekanism control circuits need the same-tier MI circuit (phase4_integration.js):
basic = LV analog (t3_mekcircuit), advanced = MV electronic (t4_mv), elite = HV digital (t5_hv),
ultimate = EV processing unit (t6_pu).
"""
from questlib import Q, Chapter, item, dim, tick, anyof, MAIN, SIDE  # noqa: F401

MEK = "mekanism:"
GEN = "mekanismgenerators:"
MM = "mekmm:"
EX = "mekanism_extras:"


def factories(tier, kinds=("smelting", "enriching", "crushing", "compressing", "combining", "purifying", "injecting", "infusing", "sawing")):
    return [f"{MEK}{tier}_{k}_factory" for k in kinds]


def ex_factories(tier):
    kinds = ("smelting", "enriching", "crushing", "compressing", "combining", "purifying", "injecting", "infusing", "sawing",
             "oxidizing", "dissolving", "washing", "crystallizing", "centrifuging")
    return [f"{EX}{tier}_{k}_factory" for k in kinds]


# Layout: y=-1/1 alloys and circuits, y=3 factories, y=5/6 chemical machines, y=8 utilities,
# y=10 generators and multiblocks, y=12/13 More Machine, y=15/17 Mekanism Extras. Links at x = -4.
CHAPTER = Chapter("mekanism", "Mekanism", "mekanism:metallurgic_infuser",
        ["Osmium, infusion and gases: Mekanism's machines, generators and its two big add-ons."], SIDE, [
    # --- Alloys and circuits (y = -1 / 1) -------------------------------------------------------
    Q("mk2_intro", 0, 0, [tick()], "The Mekanism Way", subtitle="Infuse, tier up, process", deps=["t3_infuser"], xp=50, desc=[
        "&6Osmium hums in your hand. You remember metals that drank other substances and grew stronger.&r",
        "&eWhat:&r Mekanism is a machine mod built on infusion: soak a metal in carbon, redstone, diamond or refined obsidian and it becomes an alloy.",
        "&eHow:&r every machine comes in tiers (basic, advanced, elite, ultimate). In this pack each tier's control circuit needs the matching &eMI circuit&r.",
        "&eTip:&r this page is a side path. The main-path Mekanism quests are linked on the left; click one to jump there."]),
    Q("mk2_reinforced", 2, -1, [item(MEK + "alloy_reinforced", 4)], "Reinforced Alloy", subtitle="Infused alloy plus diamond", deps=["mk2_intro", "t3_infused"], xp=60, desc=[
        "&eWhat:&r the second Mekanism alloy, used in elite circuits, lasers and the Solar Neutron Activator.",
        "&eChemistry:&r real alloys work the same way: a few percent of a second element (carbon in steel, chromium in stainless) changes the metal's properties.",
        "&eHow:&r Metallurgic Infuser: Infused Alloy + diamond infusion (from diamonds or diamond dust; check JEI)."]),
    Q("mk2_atomic", 4, -1, [item(MEK + "alloy_atomic", 4)], "Atomic Alloy", subtitle="Reinforced alloy plus refined obsidian", deps=["mk2_reinforced"], xp=80, desc=[
        "&eWhat:&r the top Mekanism alloy, needed for ultimate circuits, teleportation cores and the Robit.",
        "&eHow:&r first infuse obsidian dust with diamond to get refined obsidian dust, then infuse Reinforced Alloy with refined obsidian.",
        "&eTip:&r crush obsidian in the Crusher or an MI macerator for obsidian dust."]),
    Q("mk2_refined_obsidian", 6, -1, [item(MEK + "osmium_compressor"), item(MEK + "ingot_refined_obsidian", 4)], "Refined Obsidian", subtitle="The Osmium Compressor's speciality", deps=["mk2_atomic", "mk2_adv_circuit"], xp=100, desc=[
        "&eWhat:&r refined obsidian ingots: very hard, blast-proof metal for teleporters, the Robit and endgame tools.",
        "&eHow:&r the Osmium Compressor presses refined obsidian dust with liquid osmium into ingots. It needs an Advanced Control Circuit (MV).",
        "&eTip:&r refined glowstone ingots come from the same machine: glowstone dust plus osmium."]),
    Q("mk2_adv_circuit", 2, 1, [item(MEK + "advanced_control_circuit", 2)], "Advanced Control Circuit", subtitle="Mekanism's MV tier", deps=["t3_mekcircuit", "t4_mv"], xp=100, desc=[
        "&eWhat:&r the circuit for every advanced-tier Mekanism block: factories, cubes, tanks, the Purification Chamber.",
        "&eHow:&r an &eMI electronic circuit&r between two Infused Alloys and a Basic Control Circuit (check JEI).",
        "&eTip:&r the old infuser shortcut for circuits is removed in this pack. Circuits follow MI's voltage tiers."]),
    Q("mk2_elite_circuit", 4, 1, [item(MEK + "elite_control_circuit", 2)], "Elite Control Circuit", subtitle="Mekanism's HV tier", deps=["mk2_adv_circuit", "mk2_reinforced", "t5_hv"], xp=150, desc=[
        "&eWhat:&r the circuit for elite-tier blocks, the Chemical Injection Chamber and the Solar Neutron Activator.",
        "&eHow:&r an &eMI digital circuit&r with Reinforced Alloys and an Advanced Control Circuit (check JEI)."]),
    Q("mk2_ult_circuit", 6, 1, [item(MEK + "ultimate_control_circuit", 2)], "Ultimate Control Circuit", subtitle="Mekanism's EV tier", deps=["mk2_elite_circuit", "mk2_atomic", "t6_pu"], xp=250, desc=[
        "&eWhat:&r the circuit behind Mekanism's best machines: the Chemical Washer, Crystallizer, Dissolution Chamber, Isotopic Centrifuge and QIO.",
        "&eHow:&r an &eMI processing unit&r with Atomic Alloys and an Elite Control Circuit (check JEI).",
        "&eTip:&r this unlocks the rest of the page: ultimate factories, QIO, More Machine's big machines and Mekanism Extras."]),

    # --- Factories (y = 3) ----------------------------------------------------------------------
    Q("mk2_basic_factory", 2, 3, [anyof(factories("basic"))], "Basic Factory", subtitle="Three jobs at once", deps=["t3_mekcircuit"], xp=80, desc=[
        "&eWhat:&r a factory is a machine with several slots that work in parallel. A basic factory runs 3 operations at once.",
        "&eHow:&r craft any single machine (Energized Smelter, Enrichment Chamber, Crusher...) with Basic Control Circuits and Basic Alloy. Any factory type counts.",
        "&eTip:&r factories sort their own inputs with auto-sort in the GUI, so one input pipe is enough."]),
    Q("mk2_adv_factory", 4, 3, [anyof(factories("advanced"))], "Advanced Factory", subtitle="Five jobs at once", deps=["mk2_basic_factory", "mk2_adv_circuit"], xp=120, desc=[
        "&eWhat:&r 5 parallel slots, and faster with upgrades.",
        "&eHow:&r upgrade a basic factory in the crafting grid with Advanced Control Circuits, Infused Alloy and osmium, or use a Tier Installer on a placed one."]),
    Q("mk2_elite_factory", 6, 3, [anyof(factories("elite"))], "Elite Factory", subtitle="Seven jobs at once", deps=["mk2_adv_factory", "mk2_elite_circuit"], xp=180, desc=[
        "&eWhat:&r 7 parallel slots. Pair an Elite Purifying or Injecting Factory with your ore line and the bottleneck moves elsewhere.",
        "&eHow:&r upgrade an advanced factory with Elite Control Circuits and Reinforced Alloy (check JEI)."]),
    Q("mk2_ult_factory", 8, 3, [anyof(factories("ultimate"))], "Ultimate Factory", subtitle="Nine jobs at once", deps=["mk2_elite_factory", "mk2_ult_circuit"], xp=300, size=1.5, shape="hexagon", desc=[
        "&6Nine tasks in one box, all at once. You remember doing many things at once without effort.&r",
        "&eWhat:&r 9 parallel slots, the top of base Mekanism. Mekanism Extras goes further (see the bottom row).",
        "&eHow:&r upgrade an elite factory with Ultimate Control Circuits and Atomic Alloy (check JEI).",
        "&eTip:&r add Speed and Energy upgrades: speed raises power use, energy upgrades bring it back down."]),
    Q("mk2_installer", 0, 3, [item(MEK + "basic_tier_installer"), item(MEK + "advanced_tier_installer")], "Tier Installers", subtitle="Upgrade without breaking", deps=["mk2_basic_factory"], xp=60, optional=True, tokens=1, desc=[
        "&eWhat:&r right-click a placed machine with a Tier Installer to turn it into the next tier, keeping its contents and settings.",
        "&eHow:&r the basic installer needs a Basic Control Circuit; the advanced one needs an Advanced Control Circuit (MV).",
        "&eTip:&r a plain machine plus a basic installer becomes a basic factory."]),

    # --- Chemical machines (y = 5 / 6) --------------------------------------------------------
    # Infuser, oxidizer, separator, washer, crystallizer, dissolution chamber, centrifuge, SPS and SNA
    # are main-path quests (linked at x = -4); the PRC and the plant overview are new here.
    Q("mk2_prc", 0, 6, [item(MEK + "pressurized_reaction_chamber")], "Pressurized Reaction Chamber", subtitle="Solid, liquid and gas in, products out", deps=["t4_separator"], xp=120, desc=[
        "&eWhat:&r the PRC reacts an item, a fluid and a gas together under pressure. It makes substrate, HDPE's ethylene route and more.",
        "&eChemistry:&r pressure pushes gas molecules closer together so they collide with the other reactants more often. Le Chatelier: a reaction that shrinks gas volume is favoured by high pressure.",
        "&eHow:&r Basic Control Circuits, Infused Alloy, steel, an Enrichment Chamber, a Dynamic Tank and chemical tanks (check JEI). Press &eU&r on it in JEI for every recipe.",
        "&eTip:&r it often makes two products at once (an item and a gas). Give each output side its own pipe."]),
    Q("mk2_pigment", 2, 7, [item(MEK + "pigment_extractor"), item(MEK + "painting_machine")], "Pigments", subtitle="Colour as a chemical", deps=["mk2_prc", "mk2_adv_circuit"], xp=80, optional=True, tokens=1, desc=[
        "&eWhat:&r the Pigment Extractor pulls coloured pigment out of dyes; the Painting Machine applies it to blocks and items.",
        "&eChemistry:&r a pigment's colour comes from the light its molecules absorb: indigo absorbs orange-red light, so it looks blue.",
        "&eHow:&r the extractor needs Basic Circuits; the Painting Machine needs an Advanced Control Circuit (MV)."]),
    Q("mk2_chem_plant", 2, 5, [item(MEK + "chemical_infuser"), item(MEK + "chemical_oxidizer"), item(MEK + "electrolytic_separator"), item(MEK + "pressurized_reaction_chamber"),
                               item(MEK + "chemical_washer"), item(MEK + "chemical_crystallizer"), item(MEK + "chemical_dissolution_chamber"),
                               item(MEK + "isotopic_centrifuge"), item(MEK + "solar_neutron_activator"), item(MEK + "sps_port")],
      "Challenge: The Full Chemical Plant", subtitle="One of every Mekanism chemical machine", deps=["mk2_prc", "t7_sps"], xp=500, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each of Mekanism's ten chemical machines, from the Chemical Infuser to an SPS port.",
        "&eChemistry:&r together they cover the unit operations of a real chemical plant: reaction, oxidation, electrolysis, washing, crystallisation, dissolution and isotope separation.",
        "&eHow:&r most are on the main path (see the links on the left). The washer, crystallizer, dissolution chamber and centrifuge need Ultimate Control Circuits (EV).",
        "&eTip:&r an optional collection. Keep spares in a chest as you build each one."]),

    # --- Utilities (y = 8) --------------------------------------------------------------------
    Q("mk2_teleporter", 0, 9, [item(MEK + "teleporter"), item(MEK + "teleporter_frame", 9)], "Teleporter", subtitle="Step through a frame, arrive elsewhere", deps=["mk2_refined_obsidian"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r a frame-and-controller portal that links to other teleporters, even across dimensions.",
        "&eHow:&r the controller needs a Teleportation Core (Atomic Alloy, gold, diamond, ender pearl). Frames are refined obsidian and refined glowstone. Build a 3x4 frame with the controller in it (check JEI).",
        "&eTip:&r the Portable Teleporter does the same from your inventory."]),
    Q("mk2_robit", 2, 9, [item(MEK + "robit")], "Robit", subtitle="A small robot friend", deps=["mk2_refined_obsidian"], xp=100, desc=[
        "&eWhat:&r the Robit follows you, picks up items, smelts and crafts. It is also a crafting part for the Digital Miner and several More Machine blocks.",
        "&eHow:&r Atomic Alloy, refined obsidian, steel, an Energy Tablet and a personal chest (check JEI). Place it on a Chargepad to recharge.",
        "&eTip:&r rename it with a name tag. It won't mind."]),
    Q("mk2_miner", 4, 9, [item(MEK + "digital_miner")], "Digital Miner", subtitle="Mine a whole area by filter", deps=["mk2_robit"], xp=200, desc=[
        "&eWhat:&r a machine that mines out a large radius below it, taking only the blocks you filter for.",
        "&eHow:&r Atomic Alloy, a Logistical Sorter, a Robit, a Teleportation Core and a steel casing (check JEI). Set filters (tags like c:ores work), radius and height, then start it.",
        "&eTip:&r it uses a lot of power. Speed upgrades help, but bring Energy upgrades too."]),
    Q("mk2_qio", 6, 9, [item(MEK + "qio_drive_array"), item(MEK + "qio_dashboard"), item(MEK + "qio_drive_base")], "QIO", subtitle="Mekanism's digital storage", deps=["mk2_ult_circuit"], xp=250, desc=[
        "&eWhat:&r Quantum Item Orchestration: drives in a drive array hold items, and dashboards, importers and exporters reach them wirelessly through a frequency.",
        "&eHow:&r the drive array and the base drive need Ultimate Control Circuits (EV). Set one frequency and give every QIO block the same one.",
        "&eTip:&r AE2 is the pack's main storage. QIO is a good wireless add-on for a remote outpost."]),

    # --- Generators and multiblocks (y = 11) ----------------------------------------------------
    # Heat, gas-burning, turbine, fission and fusion are in power.py and t6 (linked at x = -4).
    Q("mk2_boiler", 0, 11, [item(MEK + "boiler_casing", 16), item(MEK + "boiler_valve", 2), item(MEK + "superheating_element", 4), item(MEK + "pressure_disperser")],
      "Thermoelectric Boiler", subtitle="Water into steam, by the tank", deps=["mk2_intro"], xp=150, desc=[
        "&eWhat:&r a multiblock boiler that turns water into steam, heated by Superheating Elements (power) or by hot coolant from a fission reactor.",
        "&eChemistry:&r boiling water takes 2,260 J per gram, far more than heating it. That latent heat is what the turbine later turns back into work.",
        "&eHow:&r the layout is in &eJust Enough Mekanism Multiblocks&r in JEI: casing walls, valves, a layer of pressure dispersers, and elements on the bottom.",
        "&eTip:&r a sodium-cooled fission reactor sends heated sodium here instead of boiling water itself."]),
    Q("mk2_turbine_parts", 2, 11, [item(GEN + "turbine_rotor", 4), item(GEN + "turbine_blade", 8), item(GEN + "rotational_complex"), item(GEN + "electromagnetic_coil", 2), item(GEN + "saturating_condenser", 4)],
      "Turbine Internals", subtitle="Rotor, blades, coils, condensers", deps=["pw_turbine"], xp=200, desc=[
        "&eWhat:&r the moving parts inside an Industrial Turbine. More blades and coils mean more power from the same steam.",
        "&eChemistry:&r condensers turn spent steam back into water, so the loop reuses the same water over and over.",
        "&eHow:&r stack rotors with two blades each on the centre column, a Rotational Complex on top, then coils and condensers above. See Just Enough Mekanism Multiblocks.",
        "&eTip:&r the turbine's GUI shows whether steam flow or blade count is the limit."]),
    Q("mk2_fusion_build", 4, 11, [item(GEN + "fusion_reactor_frame", 16), item(GEN + "reactor_glass", 4), item(GEN + "fusion_reactor_port", 2), item(GEN + "laser_focus_matrix")],
      "Building the Fusion Reactor", subtitle="Frame, glass, ports and a laser window", deps=["pw_dt_fuel"], xp=300, desc=[
        "&eWhat:&r the shell of the Fusion Reactor: frames, reactor glass, ports for fuel and output, and a Laser Focus Matrix to let the ignition laser in.",
        "&eHow:&r the 3D layout is in &eJust Enough Mekanism Multiblocks&r in JEI. The controller sits on top in the middle.",
        "&eTip:&r ports switch between input and output with a Configurator."]),
    Q("mk2_ignition", 6, 11, [item(MEK + "laser", 3), item(MEK + "laser_amplifier")], "Ignition", subtitle="A laser hot enough to start a star", deps=["mk2_fusion_build"], xp=200, desc=[
        "&eWhat:&r lasers charge a Laser Amplifier, which fires a single huge pulse into the reactor to ignite it.",
        "&eChemistry:&r deuterium and tritium only fuse above about 100 million °C, when the nuclei move fast enough to beat their electric repulsion.",
        "&eHow:&r put a filled Hohlraum in the controller, aim the amplifier at the Laser Focus Matrix and fire it with a redstone signal. Then go to the Fusion quest.",
        "&eTip:&r once lit, the reactor sustains itself as long as fuel keeps coming."]),

    # --- Mekanism: More Machine (y = 13 / 14) -------------------------------------------------
    Q("mk2_mm_cnc", 0, 13, [anyof([MM + "cnc_stamper", MM + "cnc_lathe", MM + "cnc_rolling_mill"])], "CNC Machines", subtitle="More Machine: stamp, turn and roll", deps=["t3_mekcircuit"], xp=80, desc=[
        "&eWhat:&r Mekanism: More Machine adds CNC machines: the Stamper presses plates, the Lathe turns rods, the Rolling Mill rolls wire.",
        "&eHow:&r the CNC Stamper needs Basic Control Circuits, Basic Alloy, pistons and a steel casing. The Lathe also needs a Robit (check JEI). Any one counts.",
        "&eTip:&r MI's machines make most plates already. Use CNC machines for the mod recipes that list them in JEI (the stamper also prints AE2 processors)."]),
    Q("mk2_mm_recycler", 2, 13, [item(MM + "recycler"), item(MM + "scrap", 8)], "Recycler", subtitle="Stone and dirt into scrap", deps=["mk2_mm_cnc", "mk2_adv_circuit"], xp=100, desc=[
        "&eWhat:&r the Recycler grinds cheap blocks (stone, dirt, substrate) and sometimes leaves Scrap.",
        "&eHow:&r a Crusher, Advanced Control Circuits (MV), Infused Alloy and osmium (check JEI). About 1 stone in 6 gives a scrap.",
        "&eTip:&r 64 scrap compress into a Scrap Box, the first step towards UU-Matter. Start stockpiling early."]),
    Q("mk2_mm_presser", 4, 13, [item(MM + "presser")], "Presser", subtitle="An upgraded stamper", deps=["mk2_mm_cnc", "mk2_elite_circuit"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r the Presser builds on the CNC Stamper and makes processors and other pressed parts (check JEI for its recipes).",
        "&eHow:&r a CNC Stamper with Elite Control Circuits (HV), Reinforced Alloy and pistons."]),
    Q("mk2_mm_planting", 6, 13, [item(MM + "planting_station")], "Planting Station", subtitle="Grow crops in a box", deps=["mk2_elite_circuit"], xp=120, optional=True, tokens=1, desc=[
        "&eWhat:&r a machine that grows seeds and saplings indoors and outputs the harvest.",
        "&eChemistry:&r photosynthesis: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂, here powered by electricity instead of sunlight.",
        "&eHow:&r Elite Control Circuits (HV), Reinforced Alloy, bio fuel and a steel casing (check JEI)."]),
    Q("mk2_mm_large", 8, 13, [anyof([MM + "large_heat_generator", MM + "large_gas_burning_generator", MM + "large_wind_generator", MM + "large_chemical_infuser",
                                     MM + "large_electrolytic_separator", MM + "large_rotary_condensentrator", MM + "large_solar_neutron_activator", MM + "large_pigment_mixer"])],
      "Large Machines", subtitle="Big single-block versions", deps=["mk2_ult_circuit", "mk2_robit"], xp=250, desc=[
        "&eWhat:&r More Machine's large machines do the work of many normal ones, such as the Large Electrolytic Separator or Large Chemical Infuser.",
        "&eHow:&r most need a Robit, steel blocks and ultimate-tier tanks or circuits (EV). Any one counts; check JEI for each.",
        "&eTip:&r the Large Solar Neutron Activator is a big help for polonium and tritium."]),
    Q("mk2_mm_gas", 10, 13, [item(MM + "ambient_gas_collector")], "Ambient Gas Collector", subtitle="Pull gas out of thin air", deps=["mk2_ult_circuit"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r a machine that collects gas from its surroundings (check JEI and its GUI for what it gathers).",
        "&eChemistry:&r real air is 78% N₂, 21% O₂ and 1% argon; industry separates it by cooling it into a liquid and distilling it.",
        "&eHow:&r Atomic Alloy, an osmium block, an ultimate chemical tank and ultimate tubes (EV)."]),
    Q("mk2_mm_replicator", 12, 13, [item(MM + "replicator"), item(MM + "uu_matter")], "UU-Matter", subtitle="Matter from antimatter", deps=["mk2_mm_recycler", "t7_antimatter"], xp=500, size=1.5, shape="hexagon", desc=[
        "&6Scrap, crystal, antimatter, and then anything. You remember when making matter was just a thought.&r",
        "&eWhat:&r UU-Matter is More Machine's universal matter. The Replicator turns it back into items.",
        "&eHow:&r scrap boxes become Empty Crystals in the PRC (with fusion fuel and a special gas, check JEI). 64 crystals + antimatter in the Antiprotonic Nucleosynthesizer (an optional t7 quest) make one UU-Matter.",
        "&eTip:&r the Replicator needs Ultimate Control Circuits and Atomic Alloy. Check JEI for what it can copy."]),
    Q("mk2_mm_doll", 12, 15, [item(MM + "author_doll")], "A Small Tribute", subtitle="Secret: the author, in doll form", deps=["mk2_mm_replicator"], xp=200, secret=True, loot="secret", desc=[
        "&eWhat:&r a doll of More Machine's author, compressed out of 64 UU-Matter and a breath of antimatter in the Osmium Compressor.",
        "&eTip:&r the mod's modeller has a doll too, made from UU-Matter gas instead. Thank you, modders."]),

    # --- Mekanism Extras (y = 15 / 17) --------------------------------------------------------
    Q("mk2_ex_radiance", 0, 15, [item(EX + "dust_radiance", 4), item(EX + "alloy_radiance", 2)], "Radiance", subtitle="Mekanism Extras begins", deps=["mk2_ult_circuit", "t6_yellowcake"], xp=200, desc=[
        "&eWhat:&r Mekanism Extras adds four tiers beyond ultimate: absolute, supreme, cosmic and infinite. Each needs a new alloy, starting with Radiance.",
        "&eHow:&r Osmium Compressor: glowstone dust + uranium oxide gas → Radiance Dust. Enrich it, then infuse Atomic Alloy with radiance (check JEI).",
        "&eTip:&r uranium oxide comes from oxidising yellowcake in the Chemical Oxidizer."]),
    Q("mk2_ex_absolute", 2, 15, [item(EX + "absolute_control_circuit", 2)], "Absolute Control Circuit", subtitle="Tier five", deps=["mk2_ex_radiance"], xp=250, desc=[
        "&eWhat:&r the first Extras circuit: an Ultimate Control Circuit between two Radiance Alloys.",
        "&eHow:&r craft it, or infuse an ultimate circuit with radiance in the Metallurgic Infuser.",
        "&eTip:&r absolute factories, cubes and tanks all start here."]),
    Q("mk2_ex_supreme", 4, 15, [item(EX + "alloy_thermonuclear", 2), item(EX + "supreme_control_circuit")], "Supreme Control Circuit", subtitle="Thermonuclear alloy", deps=["mk2_ex_absolute"], xp=300, desc=[
        "&eWhat:&r tier six. Its alloy is Thermonuclear: Radiance Alloy infused with thermonuclear material.",
        "&eHow:&r enriched radiance reacts with lava and molten thermonuclear in the PRC (check JEI for the full chain).",
        "&eTip:&r the circuit is an Absolute Control Circuit between two Thermonuclear Alloys."]),
    Q("mk2_ex_cosmic", 6, 15, [item(EX + "alloy_shining", 2), item(EX + "cosmic_control_circuit")], "Cosmic Control Circuit", subtitle="Shining alloy, made with antimatter", deps=["mk2_ex_supreme", "t7_antimatter"], xp=400, desc=[
        "&eWhat:&r tier seven. Its alloy, Shining, needs enriched thermonuclear transmuted with antimatter.",
        "&eHow:&r Antiprotonic Nucleosynthesizer: enriched thermonuclear + antimatter → enriched shining. Then infuse Thermonuclear Alloy with it (check JEI)."]),
    Q("mk2_ex_infinite", 8, 15, [item(EX + "alloy_spectrum", 2), item(EX + "infinite_control_circuit")], "Infinite Control Circuit", subtitle="The last tier", deps=["mk2_ex_cosmic"], xp=600, size=1.5, shape="gear", desc=[
        "&6Infinite, the circuit says. You remember when that word described you.&r",
        "&eWhat:&r tier eight, the top of Mekanism Extras. Its alloy is Spectrum.",
        "&eHow:&r Osmium Compressor: enriched shining + antimatter → enriched spectrum; infuse Shining Alloy with it, then craft the circuit (check JEI)."]),
    Q("mk2_ex_factory", 2, 17, [anyof(ex_factories("absolute"))], "Absolute Factory", subtitle="Factories beyond ultimate", deps=["mk2_ex_absolute", "mk2_ult_factory"], xp=250, optional=True, tokens=1, desc=[
        "&eWhat:&r Extras factories have more slots than ultimate ones, and Extras adds factory types base Mekanism lacks (oxidizing, washing, crystallizing, centrifuging...).",
        "&eHow:&r upgrade an ultimate factory with Absolute Control Circuits and Radiance Alloy, or use an Absolute Tier Installer. Any absolute factory counts."]),
    Q("mk2_ex_naquadah", 0, 17, [item(EX + "raw_naquadah", 8)], "Naquadah", subtitle="A metal from science fiction", deps=["mk2_ex_radiance"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r Naquadah ore, added by Mekanism Extras. It is the fuel for the Naquadah Reactor.",
        "&eChemistry:&r naquadah is not real; it comes from the Stargate films. Every other material on this page is real chemistry.",
        "&eHow:&r Naquadah ore generates underground and in the End. Jade shows the block name when you look at it.",
        "&eTip:&r it processes like other Mekanism ores: dissolve, wash and crystallise for the best yield."]),
    Q("mk2_ex_reactor", 8, 17, [item(EX + "naquadah_reactor_controller"), item(EX + "naquadah_reactor_casing", 16)], "Naquadah Reactor", subtitle="A fusion reactor on fictional fuel", deps=["mk2_ex_cosmic", "mk2_ex_naquadah"], xp=500, optional=True, tokens=2, desc=[
        "&eWhat:&r a fusion-style power multiblock from Mekanism Extras that runs on naquadah-based fuel.",
        "&eHow:&r casings are lead blocks transmuted with antimatter in the Nucleosynthesizer; the controller needs Cosmic Control Circuits. Layout: Just Enough Mekanism Multiblocks.",
        "&eTip:&r the fuel chain starts with fluorinated naquadah-uranium fuel. Check JEI for each step."]),
], links=[("t3_infuser", -4, 0), ("t3_mekcircuit", -4, 2), ("t4_separator", -4, 4), ("t4_ore5", -4, 6), ("t6_centrifuge", -4, 8),
          ("t7_sps", -4, 10), ("pw_turbine", -4, 12), ("pw_fusion", -4, 14), ("t7_opt_nucleo", -4, 16)])
