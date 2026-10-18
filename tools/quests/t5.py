"""Quest chapter: t5. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t5", "VI. Petrochemistry", "modern_industrialization:polyethylene_bucket",
        ["Crude oil is a mixture. Separate it by boiling point, then build polymers from the pieces."], MAIN, [
    Q("t5_oil", 0, 0, [item("modern_industrialization:oil_drilling_rig"), item("modern_industrialization:crude_oil_bucket")], "Black Gold", deps=["t4_mv"], xp=200, desc=[
        "Drill for crude oil: millions of years of compressed life, a soup of hydrocarbons.",
        "How: the Oil Drilling Rig goes on an MI Quarry (check JEI)."]),
    Q("t5_distill", 2, 0, [item("modern_industrialization:distillation_tower")], "Fractional Distillation", deps=["t5_oil"], xp=300, size=1.5, desc=[
        "Heat the crude and each fraction boils off at its own temperature: gases at the top, then naphtha, diesel and heavy oils lower down.",
        "This tower is &ethe refinery&r of the pack. Every other mod gets its fuel and plastic from here."]),
    Q("t5_diesel", 4, -2, [item("modern_industrialization:diesel_bucket"), item("modern_industrialization:lv_diesel_generator")], "Diesel Power", deps=["t5_distill"], xp=150, desc=[
        "Diesel burns in MI generators, and later fuels your rockets (Ad Astra runs on MI diesel)."]),
    Q("t5_ethylene", 4, 0, [item("modern_industrialization:ethylene_bucket")], "Cracking", deps=["t5_distill"], xp=150, desc=[
        "Breaking big hydrocarbon molecules into small ones gives &eethylene&r (C₂H₄), the most important building block in plastics."]),
    Q("t5_pe", 6, 0, [item("modern_industrialization:polyethylene_bucket")], "Polymerisation", deps=["t5_ethylene"], xp=250, desc=[
        "Chain thousands of ethylene molecules together and you get &epolyethylene&r.",
        "MI's ethylene also feeds Mekanism's HDPE plastic."]),
    Q("t5_hdpe", 6, 2, [item("mekanism:hdpe_pellet", 8)], "HDPE", deps=["t5_pe"], xp=150, desc=[
        "High-density polyethylene pellets, made in Mekanism's Pressurized Reaction Chamber."]),
    Q("t5_ebf", 6, -2, [item("modern_industrialization:electric_blast_furnace"), item("modern_industrialization:stainless_steel_ingot", 8)], "Stainless Steel", deps=["t5_distill"], xp=200, desc=[
        "Steel alloyed with chromium and nickel resists corrosion, so it can handle acids and hot fluids.",
        "How: the Electric Blast Furnace makes it. HV parts need it."]),
    Q("t5_hv", 8, 0, [item("modern_industrialization:digital_circuit"), item("modern_industrialization:turbo_machine_hull")], "HV: Digital Circuits", deps=["t5_pe", "t5_ebf"], xp=300, size=1.5, items=[("modern_industrialization:digital_circuit", 2)], desc=[
        "Digital circuit boards are laminated with polyethylene. The &eHV hull&r follows, with a &esodium&r battery made from your salt chemistry."]),
    Q("t5_ae2", 10, 0, [item("ae2:inscriber"), item("ae2:controller")], "The God's Archive", deps=["t5_hv"], xp=400, size=1.75, shape="hexagon", items=[("ae2:drive", 1)], desc=[
        "&6Your memory, rebuilt as a network.&r",
        "Applied Energistics 2 is gated by petrochemistry: the Inscriber needs a Turbo hull and the ME Controller a digital circuit.",
        "How: Tom's Simple Storage was your early network. AE2 takes over from here (see Storage and Logistics)."]),
    Q("t5_twilight", 10, -2, [dim("twilightforest:twilight_forest")], "The Twilight Forest", deps=["t5_hv"], xp=300, desc=[
        "A realm of permanent dusk.",
        "How: dig a 2x2 pool of water ringed with flowers, stand in it, and throw in a diamond."]),
])
