"""Quest chapter: power. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("power", "Power", "mekanismgenerators:gas_burning_generator",
        ["Energy is chemistry too: combustion, gas burning, fission and fusion."], SIDE, [
    Q("pw_iron_gen", 0, 0, [item("generatorgalore:iron_generator")], "First FE", deps=["t1_power"], xp=40, desc=[
        "Generator Galore's generators burn fuel (and, at higher tiers, stranger things) for FE."]),
    Q("pw_gold_gen", 2, -1, [item("generatorgalore:gold_generator")], deps=["pw_iron_gen"], xp=60, desc=["A faster generator."]),
    Q("pw_heat", 2, 1, [item("mekanismgenerators:heat_generator")], "Heat Generator", deps=["pw_iron_gen", "t3_infuser"], xp=60, desc=[
        "Mekanism's starter generator burns fuel, and gets a bonus from lava next to it."]),
    Q("pw_cube", 4, 1, [item("mekanism:basic_energy_cube")], "Store It", deps=["pw_heat"], xp=60, desc=[
        "Energy cubes buffer power. Upgrade them through the circuit tiers."]),
    Q("pw_gas", 4, -1, [item("mekanismgenerators:gas_burning_generator")], "Burning Hydrogen", deps=["t4_separator"], xp=150, desc=[
        "2H₂ + O₂ → 2H₂O + energy. Feed it hydrogen from your electrolysis line: water in, power out, water back. It's the cleanest combustion there is."]),
    Q("pw_solar", 6, 1, [item("mekanismgenerators:solar_generator"), item("powah:solar_panel_starter")], "Photovoltaics", deps=["t4_mv"], xp=100, desc=[
        "Silicon solar cells turn light straight into electricity: semiconductors at work."]),
    Q("pw_diesel", 6, -1, [item("modern_industrialization:mv_diesel_generator")], "Diesel Generators", deps=["t5_diesel"], xp=150, desc=[
        "Burn the diesel from your distillation tower. Scale up to HV and the Large Diesel Generator for real factories."]),
    Q("pw_large_diesel", 8, -1, [item("modern_industrialization:large_diesel_generator")], deps=["pw_diesel", "t5_hv"], xp=250),
    Q("pw_powah", 8, 1, [item("powah:reactor_basic", 36)], "Powah Reactor", deps=["t4_uraninite"], xp=250, desc=[
        "A multiblock reactor fuelled by the uraninite you oxidised yourself."]),
    Q("pw_turbine", 10, -1, [item("mekanismgenerators:turbine_casing", 16)], "Industrial Turbine", deps=["t6_fission"], xp=300, desc=[
        "Fission makes heat; a turbine turns the steam into enormous amounts of power."]),
    Q("pw_fusion", 12, 0, [item("mekanismgenerators:fusion_reactor_controller")], "Fusion", deps=["pw_turbine", "t6_waste"], xp=1000, size=1.75, shape="hexagon", desc=[
        "&6The power of a star.&r Deuterium and tritium fuse into helium, releasing more energy than any chemical reaction.",
        "How: deuterium from heavy water, tritium from lithium (Mekanism). Check JEI and Just Enough Mekanism Multiblocks."]),
])
