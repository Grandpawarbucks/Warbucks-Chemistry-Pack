"""Quest chapter: periodic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("periodic", "The Periodic Table", "chemlib:hydrogen",
        ["Rebuild the table, group by group. Each column shares a chemistry, because each shares an outer-electron arrangement."], SIDE, [
    Q("pt_alkali", 0, 0, [item("chemlib:lithium", 8), item("chemlib:sodium", 8), item("chemlib:potassium", 8)], "Alkali Metals", deps=["t1_elements"], xp=100, desc=[
        "Group 1: one outer electron they're desperate to lose. Sodium fizzes on water; potassium bursts into lilac flame.",
        "How: dissolve salt (sodium), potatoes and plants (potassium), and lithium-bearing minerals in the Dissolver."]),
    Q("pt_alkaline", 2, 0, [item("chemlib:beryllium", 4), item("chemlib:magnesium", 8), item("chemlib:calcium", 8)], "Alkaline Earth Metals", deps=["pt_alkali"], xp=100, desc=[
        "Group 2: two outer electrons. Calcium builds bones and limestone; magnesium burns with a blinding white light."]),
    Q("pt_transition", 4, 0, [item("chemlib:iron", 16), item("chemlib:copper", 16), item("chemlib:nickel", 8), item("chemlib:zinc", 8), item("chemlib:gold", 4)], "Transition Metals", deps=["pt_alkaline"], xp=150, desc=[
        "The wide middle block: hard, conductive, often colourful compounds, and the backbone of every machine you've built."]),
    Q("pt_metalloids", 0, 2, [item("chemlib:boron", 4), item("chemlib:silicon", 16), item("chemlib:arsenic", 4)], "Metalloids", deps=["t1_elements"], xp=150, desc=[
        "Half metal, half non-metal. Silicon's in-between conductivity is exactly what makes semiconductors (and AE2) possible."]),
    Q("pt_nonmetals", 2, 2, [item("chemlib:nitrogen", 16), item("chemlib:phosphorus", 8), item("chemlib:sulfur", 16)], "Non-Metals", deps=["pt_metalloids"], xp=150, desc=[
        "Nitrogen, phosphorus and sulfur: fertilisers, matches and acids. Life and industry both run on them."]),
    Q("pt_halogens", 4, 2, [item("chemlib:fluorine", 4), item("chemlib:chlorine", 8), item("chemlib:bromine", 4), item("chemlib:iodine", 4)], "Halogens", deps=["pt_nonmetals"], xp=200, desc=[
        "Group 17: one electron short of full, so fiercely reactive. 'Halogen' means 'salt-maker': chlorine plus sodium is table salt."]),
    Q("pt_noble", 6, 1, [item("chemlib:helium", 8), item("chemlib:neon", 8), item("chemlib:argon", 8)], "Noble Gases", deps=["pt_halogens", "pt_transition"], xp=200, desc=[
        "Group 18: a full outer shell, so they barely react with anything. Argon shields welding; neon lights up signs."]),
    Q("pt_liquid", 6, 3, [item("chemlib:mercury", 4), item("chemlib:gallium", 4)], "Liquid Metals", deps=["pt_transition"], xp=150, desc=[
        "Mercury is liquid at room temperature; gallium melts in your hand (29.8 °C)."]),
    Q("pt_rare_earth", 8, 0, [item("chemlib:lanthanum", 4), item("chemlib:cerium", 4), item("chemlib:neodymium", 4)], "Rare Earths", deps=["pt_noble", "t6_pu"], xp=300, desc=[
        "The lanthanides aren't actually rare, just hard to separate: they're chemically almost identical. Neodymium makes the strongest permanent magnets."]),
    Q("pt_actinides", 8, 2, [item("chemlib:thorium", 4), item("chemlib:uranium", 8), item("chemlib:plutonium", 4)], "Actinides", deps=["pt_noble", "t6_waste"], xp=400, desc=[
        "Every actinide is radioactive. Plutonium barely exists in nature: you made it in a reactor."]),
    Q("pt_complete", 10, 1, [item("chemlib:oganesson")], "Element 118", deps=["pt_rare_earth", "pt_actinides", "t6_table"], xp=1000, size=2.0, shape="gear", desc=[
        "&6The last box on the table.&r Oganesson, the heaviest element ever made, lasts under a millisecond in reality.",
        "Every group, every period: the whole periodic table, rebuilt by your hand."]),
])
