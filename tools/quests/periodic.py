"""Quest chapter: periodic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

# Layout: y=0 metals, y=2 non-metals, y=4 compounds (Combiner), y=-2 / y=6 optional side quests.
CHAPTER = Chapter("periodic", "The Periodic Table", "chemlib:hydrogen",
        ["Rebuild the table, group by group. Each column shares a chemistry, because each shares an outer-electron arrangement."], SIDE, [
    Q("pt_intro", 0, 1, [tick()], "Reading the Table", subtitle="Rows, columns, and why they matter", deps=["t1_elements"], xp=50, desc=[
        "&6You remember this chart. You used to know every box by heart.&r",
        "&eWhat:&r the periodic table orders the elements by proton number. Rows are periods; columns are groups.",
        "&eChemistry:&r elements in the same group have the same number of outer (valence) electrons, so they react alike.",
        "&eHow:&r press &eU&r on any element in JEI to see which blocks the Dissolver turns into it.",
        "&eTip:&r this chapter is a side path. Nothing in the main story waits on it, but it pays well."]),

    # --- Metals (y = 0) ---------------------------------------------------------------------
    Q("pt_alkali", 2, 0, [item("chemlib:lithium", 8), item("chemlib:sodium", 8), item("chemlib:potassium", 8)], "Alkali Metals", subtitle="Group 1: one electron to give away", deps=["pt_intro"], xp=100, desc=[
        "&eWhat:&r lithium, sodium and potassium, the softest and most reactive metals.",
        "&eChemistry:&r one valence electron, easily lost. Sodium fizzes on water (2Na + 2H₂O → 2NaOH + H₂); potassium burns lilac.",
        "&eHow:&r end stone gives lithium; lapis lazuli gives sodium (the mineral lazurite is a sodium aluminosilicate). Plants give potassium.",
        "&eTip:&r check JEI with &eU&r on each element. Many common blocks hide small amounts."]),
    Q("pt_alkaline", 4, 0, [item("chemlib:beryllium", 4), item("chemlib:magnesium", 8), item("chemlib:calcium", 8)], "Alkaline Earth Metals", subtitle="Group 2: two electrons, still eager", deps=["pt_alkali"], xp=100, desc=[
        "&eWhat:&r beryllium, magnesium and calcium: lighter structural metals and the stuff of bones and limestone.",
        "&eChemistry:&r two valence electrons, so they form 2+ ions. Calcium carbonate (CaCO₃) is limestone; magnesium burns blinding white.",
        "&eHow:&r andesite and bone give calcium (bone via hydroxylapatite, the mineral in teeth). Beryllium and magnesium come out of their compounds: check JEI."]),
    Q("pt_transition", 6, 0, [item("chemlib:iron", 16), item("chemlib:copper", 16), item("chemlib:nickel", 8), item("chemlib:zinc", 8), item("chemlib:gold", 4)], "Transition Metals", subtitle="The wide middle block", deps=["pt_alkaline"], xp=150, desc=[
        "&eWhat:&r the hard, conductive metals behind every machine you've built.",
        "&eChemistry:&r their d-orbitals fill across the row. That's why they form coloured compounds and make good catalysts.",
        "&eHow:&r dissolve ingots, nuggets or dusts of each metal.",
        "&eTip:&r ore you already process gives nuggets and dust. Dissolve the spares, not your ingots."]),
    Q("pt_post_transition", 8, 0, [item("chemlib:aluminum", 8), item("chemlib:tin", 8), item("chemlib:lead", 8), item("chemlib:indium", 4)], "Post-Transition Metals", subtitle="Soft metals on the metal side of the line", deps=["pt_transition"], xp=150, desc=[
        "&eWhat:&r aluminum, tin, lead and indium: softer, lower-melting metals just right of the transition block.",
        "&eChemistry:&r indium tin oxide is the clear conductor in every touchscreen. Lead is dense enough to stop X-rays.",
        "&eHow:&r diorite dissolves into tin and indium. Aluminum and lead come from their ingots, dusts and minerals (check JEI)."]),
    Q("pt_liquid", 6, -2, [item("chemlib:mercury", 4), item("chemlib:gallium", 4)], "Liquid Metals", subtitle="Metals that melt in your hand", deps=["pt_transition"], xp=150, desc=[
        "&eWhat:&r mercury and gallium, the two metals you can pour (almost) at room temperature.",
        "&eChemistry:&r mercury melts at −38.8 °C; gallium at 29.8 °C, below body temperature.",
        "&eHow:&r ender pearls and end stone dissolve into mercury. Cobblestone gives a little gallium."]),
    Q("pt_first20", 12, -2, [item("chemlib:hydrogen"), item("chemlib:helium"), item("chemlib:lithium"), item("chemlib:beryllium"), item("chemlib:boron"),
                            item("chemlib:carbon"), item("chemlib:nitrogen"), item("chemlib:oxygen"), item("chemlib:fluorine"), item("chemlib:neon"),
                            item("chemlib:sodium"), item("chemlib:magnesium"), item("chemlib:aluminum"), item("chemlib:silicon"), item("chemlib:phosphorus"),
                            item("chemlib:sulfur"), item("chemlib:chlorine"), item("chemlib:argon"), item("chemlib:potassium"), item("chemlib:calcium")],
      "Challenge: The First Twenty", subtitle="Hydrogen to calcium, one of each", deps=["pt_noble"], xp=300, optional=True, tokens=2, desc=[
        "&eWhat:&r one of each of elements 1 to 20, the four shortest rows of the table.",
        "&eChemistry:&r these twenty make up almost all of your body, the oceans and the air.",
        "&eHow:&r most come from the groups in this chapter. Boron and the noble gases need the Fusion Chamber (boron is 5: try H + Be).",
        "&eTip:&r an optional collection. Keep one of each in a chest as you go."]),
    Q("pt_coinage", 8, -2, [item("chemlib:copper", 8), item("chemlib:silver", 8), item("chemlib:gold", 8)], "The Coinage Metals", subtitle="Group 11: copper, silver, gold", deps=["pt_transition"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r the three metals humans have minted into money for thousands of years.",
        "&eChemistry:&r they're unreactive enough to keep their shine. Silver is the best electrical conductor of any element.",
        "&eHow:&r deepslate dissolves into a little silver. Check JEI for richer sources."]),

    # --- Non-metals (y = 2) ------------------------------------------------------------------
    Q("pt_metalloids", 2, 2, [item("chemlib:germanium", 4), item("chemlib:silicon", 16), item("chemlib:arsenic", 4)], "Metalloids", subtitle="Half metal, half non-metal", deps=["pt_intro"], xp=150, desc=[
        "&eWhat:&r germanium, silicon and arsenic sit on the staircase between metals and non-metals.",
        "&eChemistry:&r silicon conducts a little, and a trace of arsenic (doping) controls how much. The first transistor (1947) was germanium.",
        "&eHow:&r sand dissolves into silicon dioxide, which dissolves again into silicon and oxygen. Blaze powder and Nether bricks give germanium.",
        "&eTip:&r you'll need a lot of silicon later, for circuits and AE2."]),
    Q("pt_nonmetals", 4, 2, [item("chemlib:nitrogen", 16), item("chemlib:phosphorus", 8), item("chemlib:sulfur", 16)], "Non-Metals", subtitle="Fertilisers, matches and acids", deps=["pt_metalloids"], xp=150, desc=[
        "&eWhat:&r nitrogen, phosphorus and sulfur. Life and industry both run on them.",
        "&eChemistry:&r nitrogen and phosphorus feed every crop; sulfur becomes sulfuric acid, the most-made chemical on Earth.",
        "&eHow:&r check JEI with &eU&r. Nether blocks are a good place to look for sulfur."]),
    Q("pt_chalcogens", 6, 2, [item("chemlib:oxygen", 16), item("chemlib:sulfur", 16), item("chemlib:selenium", 4)], "Chalcogens", subtitle="Group 16: the ore-formers", deps=["pt_nonmetals"], xp=150, desc=[
        "&eWhat:&r oxygen, sulfur and selenium. 'Chalcogen' means 'ore-former'.",
        "&eChemistry:&r two electrons short of a full shell, so they grab metals: most ores are oxides or sulfides (Fe₂O₃, ZnS, PbS).",
        "&eHow:&r fish and crimson fungus dissolve into selenium. Oxygen comes from nearly everything.",
        "&eTip:&r selenium is a trace nutrient: you need a little, and too much is poisonous."]),
    Q("pt_halogens", 8, 2, [item("chemlib:fluorine", 4), item("chemlib:chlorine", 8), item("chemlib:bromine", 4), item("chemlib:iodine", 4)], "Halogens", subtitle="Group 17: the salt-makers", deps=["pt_chalcogens"], xp=200, desc=[
        "&eWhat:&r fluorine, chlorine, bromine and iodine, the most reactive non-metals.",
        "&eChemistry:&r one electron short of full. 'Halogen' means 'salt-maker': Na + Cl → NaCl, table salt.",
        "&eHow:&r magma blocks give fluorine and bromine. Horn coral gives iodine (via lead iodide). Chlorine comes out of salts: check JEI."]),
    Q("pt_noble", 10, 1, [item("chemlib:helium", 8), item("chemlib:neon", 8), item("chemlib:argon", 8)], "Noble Gases", subtitle="Group 18: the full shell", deps=["pt_halogens", "pt_post_transition", "t6_pu"], xp=200, desc=[
        "&6Two halves of the table, joined. More of the old knowledge settles into place.&r",
        "&eWhat:&r helium, neon and argon, the gases that refuse to react.",
        "&eChemistry:&r a full outer shell means nothing to gain or lose. Argon shields welds from air; neon glows red in a discharge tube.",
        "&eHow:&r nothing dissolves into them, so build them: the Alchemistry Fusion Chamber (EV) adds proton numbers, so H + H → He. Check JEI for neon and argon.",
        "&eTip:&r real stars fuse hydrogen into helium too, though it takes them four protons, not two."]),
    Q("pt_heavy_noble", 10, -1, [item("chemlib:xenon", 2), item("chemlib:radon", 2)], "Heavy Noble Gases", subtitle="Even the 'inert' ones have limits", deps=["pt_post_transition"], xp=250, optional=True, tokens=1, desc=[
        "&eWhat:&r xenon and radon, the heaviest natural noble gases.",
        "&eChemistry:&r in 1962 xenon was made to react (with platinum hexafluoride), ending the idea that noble gases never react. Radon is radioactive.",
        "&eHow:&r dragon's breath dissolves into both. That means a trip to the End."]),

    # --- Late table ---------------------------------------------------------------------------
    Q("pt_rare_earth", 12, 0, [item("chemlib:lanthanum", 4), item("chemlib:cerium", 4), item("chemlib:neodymium", 4)], "Rare Earths", subtitle="Not rare, just hard to separate", deps=["pt_noble", "t6_pu"], xp=300, desc=[
        "&eWhat:&r the lanthanides: lanthanum, cerium, neodymium and their near-identical neighbours.",
        "&eChemistry:&r they differ only in an inner (4f) shell, so their chemistry is almost the same. Neodymium makes the strongest permanent magnets.",
        "&eHow:&r check JEI for sources. The Alchemistry Fusion Chamber can also build them from lighter elements."]),
    Q("pt_actinides", 12, 2, [item("chemlib:thorium", 4), item("chemlib:uranium", 8), item("chemlib:plutonium", 4)], "Actinides", subtitle="Every one of them radioactive", deps=["pt_noble", "t6_waste"], xp=400, desc=[
        "&eWhat:&r thorium, uranium and plutonium, the fuels of the nuclear age.",
        "&eChemistry:&r every actinide is radioactive. Plutonium barely exists in nature: you made it by firing neutrons at uranium.",
        "&eHow:&r dissolve uranium and thorium materials. Plutonium comes from your fission reactor's waste."]),
    Q("pt_isotopes", 4, -2, [item("mekanism:electric_pump"), item("mekanism:upgrade_filter"), item("mekanism:heavy_water_bucket")], "Isotopes: Heavy Water", subtitle="Same element, different weight", deps=["pt_alkali", "t3_infuser"], xp=200, optional=True, tokens=1, desc=[
        "&eWhat:&r heavy water, D₂O: water made with deuterium, hydrogen with an extra neutron.",
        "&eChemistry:&r isotopes have the same protons (so the same chemistry) but different neutrons. About 1 in 6,400 hydrogen atoms is deuterium.",
        "&eHow:&r put a Filter Upgrade in a Mekanism Electric Pump and pump from water. It pulls out heavy water instead.",
        "&eTip:&r deuterium is half of fusion fuel. You'll want this again in the Power chapter."]),
    Q("pt_superheavy", 14, 1, [item("chemlib:tennessine")], "Superheavy Elements", subtitle="Element 117, built by fusion", deps=["pt_rare_earth", "pt_actinides"], xp=500, desc=[
        "&eWhat:&r tennessine, element 117. Nothing in the world dissolves into it; you have to build it.",
        "&eChemistry:&r real labs make superheavy elements by smashing nuclei together; only a handful of atoms have ever existed.",
        "&eHow:&r the Alchemistry Fusion Chamber joins two elements, adding their proton numbers. Check JEI for the pairs that reach 117.",
        "&eTip:&r one more step after this: add hydrogen (1) to tennessine (117) and you get 118."]),
    Q("pt_complete", 16, 1, [item("chemlib:oganesson")], "Element 118", subtitle="The last box on the table", deps=["pt_superheavy", "t6_table"], xp=1000, size=2.0, shape="gear", desc=[
        "&6The last box on the table. You remember now: you once named these.&r",
        "&eWhat:&r oganesson, the heaviest element ever made.",
        "&eChemistry:&r in reality it lasts under a millisecond. Here it sits in your inventory, which is the kind of thing demigods can do.",
        "&eHow:&r fuse tennessine with hydrogen (or any pair adding to 118) in the Fusion Chamber."]),

    # --- Compounds in the Combiner (y = 4) ------------------------------------------------------
    Q("pt_co2", 4, 4, [item("chemlib:carbon_dioxide", 4)], "Covalent Bonds: CO₂", subtitle="Non-metals share electrons", deps=["pt_nonmetals"], xp=100, desc=[
        "&eWhat:&r carbon dioxide, your first compound in this chapter.",
        "&eChemistry:&r C + O₂ → CO₂. Non-metals don't hand electrons over; they share them in covalent bonds (O=C=O).",
        "&eHow:&r in the Combiner, pick Carbon Dioxide and supply 1 carbon + 2 oxygen.",
        "&eTip:&r the Combiner GUI shows each recipe once you select its output."]),
    Q("pt_methane", 6, 4, [item("chemlib:methane", 4), item("chemlib:ethylene", 4)], "Hydrocarbons", subtitle="Carbon chains and hydrogen", deps=["pt_co2"], xp=125, desc=[
        "&eWhat:&r methane (natural gas) and ethylene (the building block of polyethylene).",
        "&eChemistry:&r CH₄ has four single bonds. C₂H₄ has a C=C double bond, which is what lets it link into plastic chains.",
        "&eHow:&r Combiner: methane = 1 C + 4 H; ethylene = 2 C + 4 H."]),
    Q("pt_ammonia", 8, 4, [item("chemlib:ammonia", 4)], "Ammonia", subtitle="Nitrogen made useful", deps=["pt_methane"], xp=125, desc=[
        "&eWhat:&r ammonia, NH₃, the base of nearly all fertiliser.",
        "&eChemistry:&r N₂ + 3H₂ → 2NH₃. Breaking nitrogen's triple bond is hard; the Haber-Bosch process needs heat, pressure and an iron catalyst.",
        "&eHow:&r Combiner: 1 nitrogen + 3 hydrogen. Later you'll run real Haber-Bosch in an MI machine."]),
    Q("pt_salt", 10, 4, [item("chemlib:sodium_chloride", 8)], "Ionic Bonds: Salt", subtitle="A metal gives, a non-metal takes", deps=["pt_ammonia", "pt_halogens"], xp=125, desc=[
        "&eWhat:&r sodium chloride, NaCl: table salt.",
        "&eChemistry:&r sodium gives its one electron to chlorine. Na⁺ and Cl⁻ then hold together in a cubic crystal: an ionic bond.",
        "&eHow:&r Combiner: 1 sodium + 1 chlorine.",
        "&eTip:&r a reactive metal plus a poisonous gas makes something you sprinkle on food. Chemistry is strange."]),
    Q("pt_acids", 12, 4, [item("chemlib:hydrochloric_acid", 4), item("chemlib:nitric_acid", 4)], "Strong Acids", subtitle="Hydrochloric and nitric acid", deps=["pt_salt"], xp=150, desc=[
        "&eWhat:&r hydrochloric acid (HCl) and nitric acid (HNO₃).",
        "&eChemistry:&r acids give up H⁺ ions in water. Mixed 3:1, HCl and HNO₃ make aqua regia, which dissolves gold and platinum.",
        "&eHow:&r Combiner: HCl = 1 H + 1 Cl; HNO₃ = 1 H + 1 N + 3 O."]),
    Q("pt_sulfuric", 14, 4, [item("chemlib:sulfuric_acid", 8)], "King of Chemicals", subtitle="H₂SO₄ from its elements", deps=["pt_acids"], xp=250, size=1.5, desc=[
        "&6Built atom by atom. The old craft is coming back faster now.&r",
        "&eWhat:&r sulfuric acid, H₂SO₄, built straight from elements.",
        "&eChemistry:&r industry makes it by the contact process: S → SO₂ → SO₃ → H₂SO₄. Here you skip the plant and place the atoms yourself.",
        "&eHow:&r Combiner: 2 hydrogen + 1 sulfur + 4 oxygen."]),
    Q("pt_sugar", 4, 6, [item("chemlib:sucrose", 2), item("chemlib:cellulose", 2)], "Sugar and Wood", subtitle="Carbohydrates from scratch", deps=["pt_co2"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r sucrose (table sugar) and cellulose (what wood and paper are made of).",
        "&eChemistry:&r plants make both from CO₂ and water using sunlight. Cellulose is a chain of glucose rings: C₆H₁₀O₅ per unit.",
        "&eHow:&r Combiner: sucrose = 12 C + 22 H + 11 O; cellulose = 6 C + 10 H + 5 O.",
        "&eTip:&r that's a lot of atoms. Stock up on carbon, hydrogen and oxygen first."]),
    Q("pt_ethanol", 6, 6, [item("chemlib:hydroxide", 4), item("chemlib:ethanol", 2)], "Alcohol", subtitle="Add an OH group", deps=["pt_methane"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r ethanol, C₂H₅OH, made by attaching a hydroxide (OH) group to a two-carbon chain.",
        "&eChemistry:&r the -OH group is what makes it an alcohol and lets it mix with water.",
        "&eHow:&r Combiner: hydroxide = 1 O + 1 H, then ethanol = 2 C + 5 H + 1 hydroxide."]),
    Q("pt_lye", 10, 6, [item("chemlib:sodium_hydroxide", 4)], "Lye", subtitle="The base that balances the acid", deps=["pt_salt"], xp=150, optional=True, tokens=1, desc=[
        "&eWhat:&r sodium hydroxide, NaOH: lye, a strong base.",
        "&eChemistry:&r industry makes it by electrolysing salt water: 2NaCl + 2H₂O → 2NaOH + Cl₂ + H₂. Acid + base → salt + water.",
        "&eHow:&r Combiner: 1 sodium + 1 hydroxide (make hydroxide from 1 O + 1 H)."]),
    Q("pt_rust", 12, 6, [item("chemlib:iron_oxide", 4)], "Rust", subtitle="Iron, slowly returning to ore", deps=["pt_acids"], xp=125, optional=True, tokens=1, desc=[
        "&eWhat:&r iron(III) oxide, Fe₂O₃: rust, and also hematite, the most common iron ore.",
        "&eChemistry:&r 4Fe + 3O₂ → 2Fe₂O₃. A blast furnace runs this backwards, using carbon to pull the oxygen off.",
        "&eHow:&r Combiner: 2 iron + 3 oxygen."]),
])
