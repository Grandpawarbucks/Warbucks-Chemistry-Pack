"""Quest chapter: t3. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t3", "IV. The Electric Age", "modern_industrialization:basic_machine_hull",
        ["Electricity is the tool that splits compounds apart. First you have to make it, and build the circuits that use it."], MAIN, [
    Q("t3_rubber", 0, -1, [item("modern_industrialization:rubber_sheet", 8)], "Rubber", deps=["t1_steel"], xp=40, desc=[
        "Insulation for cables. Without it, current goes everywhere.",
        "How: check JEI for MI's rubber recipes (from plant matter or, later, synthetic rubber)."]),
    Q("t3_wire", 0, 1, [item("modern_industrialization:copper_wire", 8), item("modern_industrialization:tin_cable", 8)], "Wires and Cables", deps=["t1_steel"], xp=40, desc=[
        "Copper conducts. Rubber-coated wire becomes cable.",
        "How: the Steel Wiremill pulls plates into wire. Cables combine wire with rubber."]),
    Q("t3_components", 2, 0, [item("modern_industrialization:resistor", 2), item("modern_industrialization:capacitor", 2), item("modern_industrialization:inductor", 2)], "Electronic Components", deps=["t3_rubber", "t3_wire"], xp=60, desc=[
        "Resistors limit current, capacitors store charge, inductors resist changes in current. Every circuit needs them.",
        "How: check JEI for each. They're small crafts from wire, plates and rubber."]),
    Q("t3_battery", 2, 2, [item("modern_industrialization:redstone_battery", 2)], "Redstone Battery", deps=["t3_wire"], xp=40, desc=[
        "A simple battery. The LV hull needs two."]),
    Q("t3_analog", 4, 0, [item("modern_industrialization:analog_circuit", 2)], "Analog Circuit", deps=["t3_components"], xp=75, desc=[
        "Your first circuit. Mekanism's Basic Control Circuit also needs one, so MI and Mekanism advance together."]),
    Q("t3_hull", 6, 1, [item("modern_industrialization:basic_machine_hull")], "LV Machine Hull", deps=["t3_analog", "t3_battery"], xp=150, size=1.5, items=[("modern_industrialization:analog_circuit", 4), ("modern_industrialization:electric_macerator", 1)], desc=[
        "&eLV&r (Low Voltage) is the first electric tier. Every LV machine is built on this hull.",
        "How: steel machine casing + analog circuit + 2 redstone batteries + tin cable."]),
    Q("t3_turbine", 8, -1, [item("modern_industrialization:lv_steam_turbine")], "Steam to Electricity", deps=["t3_hull"], xp=100, desc=[
        "A turbine turns your boiler's steam into &eEU&r, MI's electricity. Your steam setup becomes a power plant.",
        "How: pipe steam in, and connect tin cable from the turbine to your machines."]),
    Q("t3_efurnace", 10, -3, [item("modern_industrialization:electric_furnace")], deps=["t3_turbine"], xp=40, desc=["Faster, fuel-free smelting."]),
    Q("t3_emacerator", 10, -2, [item("modern_industrialization:electric_macerator")], deps=["t3_turbine"], xp=40, desc=["Still capped at 2x per ore until acids."]),
    Q("t3_assembler", 10, -1, [item("modern_industrialization:assembler")], "Assembler", deps=["t3_turbine"], xp=60, desc=[
        "Makes circuits and machine parts automatically. This is where MI automation really starts."]),
    Q("t3_ecompressor", 10, 0, [item("modern_industrialization:electric_compressor")], deps=["t3_turbine"], xp=40, desc=["Plates, faster."]),
    Q("t3_ewiremill", 10, 1, [item("modern_industrialization:electric_wiremill")], deps=["t3_turbine"], xp=40, desc=["Wire, faster."]),
    Q("t3_polarizer", 10, 2, [item("modern_industrialization:polarizer")], "Polarizer", deps=["t3_turbine"], xp=40, desc=["Magnetises steel rods, which motors need."]),
    Q("t3_infuser", 8, 3, [item("mekanism:metallurgic_infuser")], "Mekanism: Metallurgic Infuser", deps=["t3_hull"], xp=60, desc=[
        "Mekanism's entry machine. It infuses metals with carbon, redstone and more.",
        "How: you'll need osmium (a blue-grey ore found deep underground; it's unique to Mekanism)."]),
    Q("t3_mekcircuit", 10, 4, [item("mekanism:basic_control_circuit", 2), item("mekanism:steel_casing")], "Mekanism Circuits", deps=["t3_infuser", "t3_analog"], xp=75, desc=[
        "In this pack, a Basic Control Circuit is &eMI Analog Circuit + osmium&r. Each Mekanism circuit tier needs the matching MI circuit.",
        "The Steel Casing is the frame for most Mekanism machines."]),
    Q("t3_enrich", 12, 4, [item("mekanism:enrichment_chamber")], "Enrichment Chamber", deps=["t3_mekcircuit"], xp=60, desc=[
        "Mekanism's 2x ore processing. 3x, 4x and 5x need gases and acids: that's the next chapter."]),
])
