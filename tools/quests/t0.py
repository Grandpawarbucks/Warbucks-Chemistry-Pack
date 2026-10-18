"""Quest chapter: t0. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t0", "I. Fire and Bronze", "modern_industrialization:bronze_ingot",
        ["Heat drives chemistry: reduce ore with carbon, mix metals into alloys, and let steam do the work."], MAIN, [
    Q("t0_charcoal", 0, 0, [item("minecraft:charcoal", 16)], "Pyrolysis", deps=["gs_ready"], xp=25, desc=[
        "Heat wood without enough oxygen to burn and the volatile compounds escape as smoke and tar.",
        "What's left is &echarcoal&r: almost pure carbon. This is &epyrolysis&r.",
        "How: smelt logs in a furnace."]),
    Q("t0_copper", 0, 2, [item("minecraft:copper_ingot", 16)], "Copper", deps=["gs_ready"], xp=20, desc=[
        "Smelting is &ereduction&r: carbon pulls oxygen away from the metal oxide and leaves metal behind.",
        "How: copper ore is common near the surface, especially in dripstone caves."]),
    Q("t0_tin", 2, 2, [item("modern_industrialization:raw_tin", 8), item("modern_industrialization:tin_ingot", 8)], "Tin", deps=["t0_copper"], xp=25, desc=[
        "Tin ore here comes from Modern Industrialization (MI). It's grey with pale specks and fairly common underground.",
        "How: mine it and smelt the raw tin."]),
    Q("t0_hammer", 2, 0, [item("modern_industrialization:forge_hammer")], "The Forge Hammer", deps=["t0_charcoal", "t0_copper"], xp=25, desc=[
        "MI's first workstation. It crushes ore into dust and hammers ingots into plates.",
        "Ores give at most &e2x&r here. Bigger yields come later from &eacids&r, not bigger hammers.",
        "How: craft it (check JEI), place it, and right-click to use."]),
    Q("t0_bronze", 4, 1, [item("modern_industrialization:bronze_ingot", 16)], "The First Alloy", deps=["t0_hammer", "t0_tin"], xp=50, size=1.5, desc=[
        "About 3 parts copper to 1 part tin gives &ebronze&r, which is harder than either metal alone.",
        "Humanity's first engineered material, and the frame of your steam age.",
        "How: crush copper and tin into dust with the Forge Hammer, mix the dusts by crafting, and smelt the bronze dust."]),
    Q("t0_casing", 6, 0, [item("modern_industrialization:bronze_machine_casing")], "Bronze Machine Casing", deps=["t0_bronze"], xp=40, desc=[
        "The block every steam machine is built around. You'll also need one for the Dissolver in Chapter II.",
        "How: bronze plates around a furnace-like core (check JEI)."]),
    Q("t0_boiler", 8, 0, [item("modern_industrialization:bronze_boiler")], "Steam Power", deps=["t0_casing"], xp=75, size=1.5, items=[("minecraft:charcoal", 32), ("modern_industrialization:bronze_furnace", 1)], desc=[
        "Burn fuel, boil water, and the expanding steam does work. Welcome to the industrial revolution.",
        "How: place the boiler, give it water and fuel (coal or charcoal), and place steam machines next to it. Steam flows into adjacent machines or through MI fluid pipes."]),
    Q("t0_pump", 8, 2, [item("modern_industrialization:bronze_water_pump")], "Endless Water", deps=["t0_boiler"], xp=40, desc=[
        "A steam-powered pump that pulls water from the ground, so your boiler never runs dry.",
        "How: place it next to the boiler, or pipe its water into it."]),
    Q("t0_furnace", 10, -2, [item("modern_industrialization:bronze_furnace")], "Steam Furnace", deps=["t0_boiler"], xp=30, desc=[
        "Smelts with steam instead of fuel. Your first automated machine."]),
    Q("t0_macerator", 10, -1, [item("modern_industrialization:bronze_macerator")], "Steam Macerator", deps=["t0_boiler"], xp=30, desc=[
        "Grinds ore and items into dust: 1 ore makes 2 raw ore here (capped at 2x until acids)."]),
    Q("t0_compressor", 10, 0, [item("modern_industrialization:bronze_compressor")], "Steam Compressor", deps=["t0_boiler"], xp=30, desc=[
        "Presses ingots into plates. Machines need lots of plates."]),
    Q("t0_mixer", 10, 1, [item("modern_industrialization:bronze_mixer")], "Steam Mixer", deps=["t0_boiler"], xp=30, desc=[
        "Mixes dusts (like copper + tin into bronze) and fluids."]),
    Q("t0_cutter", 10, 2, [item("modern_industrialization:bronze_cutting_machine")], "Steam Cutting Machine", deps=["t0_boiler"], xp=30, desc=[
        "Cuts ingots into rods and planks into more planks. It uses water as coolant."]),
    Q("t0_pipes", 12, 0, [item("modern_industrialization:item_pipe", 8), item("modern_industrialization:fluid_pipe", 8)], "Pipes", deps=["t0_furnace", "t0_macerator", "t0_compressor", "t0_mixer", "t0_cutter"], xp=50, desc=[
        "Connect your machines. MI pipes carry items or fluids, including steam.",
        "How: right-click a pipe end with an empty hand to set it to insert or extract."]),
])
