"""Quest chapter: t1. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t1", "II. Steam and Steel", "modern_industrialization:coke",
        ["Destructive distillation turns coal into coke, and coke turns iron into steel.",
         "At the end of this chapter, matter itself opens up to you."], MAIN, [
    Q("t1_coke_oven", 0, 0, [item("modern_industrialization:coke_oven")], "The Coke Oven", deps=["t0_pipes"], xp=50, desc=[
        "Coal is carbon mixed with many other compounds. Bake it without air and those volatiles are driven off.",
        "This is &edestructive distillation&r.",
        "How: the Coke Oven is a small multiblock. Look at it in JEI or use MI's guidebook to see the shape, then power it with steam."]),
    Q("t1_coke", 2, -1, [item("modern_industrialization:coke", 16)], "Coke", deps=["t1_coke_oven"], xp=40, desc=[
        "Nearly pure carbon that burns hotter than coal. It's exactly what a blast furnace needs."]),
    Q("t1_creosote", 2, 1, [item("modern_industrialization:creosote_bucket")], "Byproduct: Creosote", deps=["t1_coke_oven"], xp=40, desc=[
        "The tar driven out of coal is &ecreosote&r. Nothing is wasted in chemistry: creosote is a fuel for your boilers.",
        "How: pipe it out of the Coke Oven into a tank, or straight into a boiler."]),
    Q("t1_blast", 4, 0, [item("modern_industrialization:steam_blast_furnace")], "The Steam Blast Furnace", deps=["t1_coke"], xp=75, desc=[
        "A multiblock that gets hot enough to melt iron and dissolve carbon into it.",
        "How: check the structure in JEI, then feed it steam."]),
    Q("t1_steel", 6, 0, [item("modern_industrialization:steel_ingot", 16)], "Steel", deps=["t1_blast"], xp=100, size=1.5, items=[("modern_industrialization:steel_ingot", 16)], desc=[
        "Iron with a small, controlled amount of carbon (about 0.2-2%) is &esteel&r: strong, tough, and the backbone of every machine to come.",
        "Too much carbon and you get brittle cast iron. Chemistry is about the right ratio.",
        "How: mix iron dust with coke dust, then melt it in the blast furnace (check JEI for the exact recipe)."]),
    Q("t1_steel_paxel", 6, 2, [item("mekanismtools:steel_paxel")], "Steel Paxel", deps=["t1_steel"], xp=40, desc=[
        "A sturdier paxel."]),
    Q("t1_steel_boiler", 8, -2, [item("modern_industrialization:steel_boiler")], "Steel Boiler", deps=["t1_steel"], xp=60, desc=[
        "More steam per tick. Steel versions of the steam machines (macerator, compressor and others) run faster too."]),
    Q("t1_power", 8, 2, [item("generatorgalore:iron_generator")], "Forge Energy", deps=["t1_steel"], xp=50, desc=[
        "Some machines run on &eFE&r (Forge Energy) instead of steam. You'll need it for the Dissolver.",
        "How: Generator Galore's Iron Generator burns fuel into FE. A Mekanism Heat Generator or Powah Furnator also works."]),
    Q("t1_dissolver", 10, -1, [item("alchemistry:dissolver")], "The Dissolver", deps=["t1_steel", "t1_power"], xp=150, size=1.75, shape="hexagon", items=[("minecraft:experience_bottle", 16)], desc=[
        "&6Your first divine gift returns.&r",
        "The Dissolver breaks any item into the &eelements and compounds&r it's made of.",
        "How: it needs steel plates and a Bronze Machine Casing. Power it with FE, insert anything, and collect the elements."]),
    Q("t1_combiner", 10, 1, [item("alchemistry:combiner")], "The Combiner", deps=["t1_steel", "t1_power"], xp=150, size=1.75, shape="hexagon", desc=[
        "The reverse: arrange elements and the Combiner builds them back into items and blocks.",
        "Taking the world apart and rebuilding it to your design is what this pack is about."]),
    Q("t1_elements", 12, 0, [item("chemlib:hydrogen", 16), item("chemlib:carbon", 16), item("chemlib:oxygen", 16), item("chemlib:iron", 16)],
      "First Entries in the Periodic Table", deps=["t1_dissolver", "t1_combiner"], xp=200, desc=[
        "Dissolve whatever you have lying around and collect your first elements:",
        "&eH&r (1), &eC&r (6), &eO&r (8), &eFe&r (26).",
        "How: wood and plants give carbon, hydrogen and oxygen. Iron ingots give iron."]),
    Q("t1_compound", 14, 0, [item("chemlib:water", 4)], "Your First Synthesis", deps=["t1_elements"], xp=200, desc=[
        "Two hydrogen, one oxygen: H₂O. Build water from its elements in the Combiner.",
        "It's a trivial compound, but you made it from scratch. That's the point.",
        "How: the Combiner shows the recipe once you pick the target item in its GUI."]),
])
