"""Quest chapter: t4. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t4", "V. Electrochemistry and Acids", "modern_industrialization:sulfuric_acid_bucket",
        ["Electricity splits compounds into elements. Acids dissolve what fire can't.",
         "Ore processing becomes chemistry."], MAIN, [
    Q("t4_electrolyzer", 0, 0, [item("modern_industrialization:electrolyzer")], "Electrolysis", deps=["t3_assembler"], xp=150, desc=[
        "Pass current through a compound and it splits: water into &eH₂ + O₂&r, salt water into &eCl₂&r and sodium.",
        "This is &eelectrochemistry&r, and its gases drive everything in this chapter."]),
    Q("t4_salt", 2, -2, [item("modern_industrialization:salt_dust", 16)], "Salt", deps=["t4_electrolyzer"], xp=40, desc=[
        "Sodium chloride, NaCl. MI salt ore is found underground; macerate it into dust.",
        "Electrolysed, it gives &esodium&r and &echlorine&r, the start of the chlor-alkali industry."]),
    Q("t4_separator", 0, 2, [item("mekanism:electrolytic_separator")], "Mekanism Gases", deps=["t3_mekcircuit"], xp=100, desc=[
        "Mekanism's Electrolytic Separator makes hydrogen and oxygen as gases you can pipe and store.",
        "How: feed it water and FE. Use Mekanism pressurized tubes and chemical tanks for the gases."]),
    Q("t4_reactor", 2, 0, [item("modern_industrialization:chemical_reactor")], "The Chemical Reactor", deps=["t4_electrolyzer"], xp=100, desc=[
        "MI's general-purpose reaction vessel. It combines items and fluids into new compounds. You'll use it constantly."]),
    Q("t4_oxidizer", 2, 2, [item("mekanism:chemical_oxidizer"), item("mekanism:chemical_infuser")], "The Contact Process, Part 1", deps=["t4_separator"], xp=150, desc=[
        "Burn sulfur into &eSO₂&r in the Chemical Oxidizer, then combine it with oxygen into &eSO₃&r in the Chemical Infuser.",
        "How: sulfur comes from the Nether, or from macerating lignite coal."]),
    Q("t4_acid", 4, 1, [item("modern_industrialization:sulfuric_acid_bucket")], "Sulfuric Acid", deps=["t4_oxidizer", "t4_reactor"], xp=250, size=1.75, shape="hexagon", items=[("modern_industrialization:sulfuric_acid_bucket", 2)], desc=[
        "SO₃ + H₂O → &eH₂SO₄&r. Sulfuric acid is the most-produced chemical on Earth for a reason.",
        "How: make it in Mekanism or MI and fill one bucket."]),
    Q("t4_ore3", 6, -1, [item("mekanism:purification_chamber")], "3x Ore: Oxygen", deps=["t4_acid"], xp=150, desc=[
        "Before acids, every route caps out at &e2x&r per ore. Purifying ore with oxygen gives &e3x&r."]),
    Q("t4_ore4", 8, -1, [item("mekanism:chemical_injection_chamber")], "4x Ore: Hydrogen Chloride", deps=["t4_ore3"], xp=200, desc=[
        "H₂ + Cl₂ → &eHCl&r. Injecting hydrogen chloride splits ore into shards: &e4x&r.",
        "How: combine hydrogen and chlorine in the Chemical Infuser."]),
    Q("t4_ore5", 10, -1, [item("mekanism:chemical_dissolution_chamber"), item("mekanism:chemical_washer"), item("mekanism:chemical_crystallizer")], "5x Ore: Dissolution", deps=["t4_ore4"], xp=300, size=1.5, desc=[
        "Dissolve ore in sulfuric acid into a slurry, wash it, and crystallise it: &e5x&r.",
        "This is &ehydrometallurgy&r, the way most of the world's copper is really refined."]),
    Q("t4_mv", 6, 2, [item("modern_industrialization:electronic_circuit"), item("modern_industrialization:advanced_machine_hull")], "MV: Aluminum", deps=["t4_electrolyzer"], xp=250, size=1.5, items=[("modern_industrialization:electronic_circuit", 4)], desc=[
        "Aluminum is the most common metal in the crust, but it's locked tightly to oxygen in bauxite. It only became cheap once electrolysis could free it.",
        "How: process bauxite (MI ore) into aluminum (check JEI), then build electronic circuits and the &eMV hull&r."]),
    Q("t4_uraninite", 8, 2, [item("powah:energizing_orb"), item("powah:uraninite", 4)], "Uranium Dioxide", deps=["t4_mv", "t4_reactor"], xp=150, desc=[
        "Uraninite is UO₂. Make it by oxidising uranium dust with oxygen in MI's &eChemical Reactor&r.",
        "Powah's reactors run on it, and Powah's Energizing Orb needs an MV circuit."]),
    Q("t4_byproduct", 12, -1, [item("modern_industrialization:centrifuge"), item("modern_industrialization:silver_dust", 4)], "Ore Byproducts", deps=["t4_ore5"], xp=200, desc=[
        "Real ores are never pure. Send Mekanism's &edirty dust&r through MI's &eCentrifuge&r instead of the Enrichment Chamber and you get the same dust plus a chance at a bonus metal:",
        "iron → nickel, copper → gold, gold → silver, &elead → silver&r (galena is the world's main silver ore), tin → tungsten, osmium → iridium, uranium → lead (decay).",
        "How: route dirty dust to a Centrifuge. Rare metals start arriving as a bonus."]),
    Q("t4_undergarden", 4, 4, [item("undergarden:catalyst"), dim("undergarden:undergarden")], "The Undergarden", deps=["t4_acid"], xp=300, desc=[
        "A realm beneath the world. Its portal catalyst needs a bucket of sulfuric acid.",
        "How: build a stone-brick portal frame and right-click it with the catalyst."]),
])
