"""Quest chapter: t6. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t6", "VII. Materials and Nuclear", "mekanism:pellet_polonium",
        ["Purity and precision: semiconductors, PVC, isotopes.",
         "Then transmutation: any element from any other."], MAIN, [
    Q("t6_silicon", 0, -2, [item("modern_industrialization:monocrystalline_silicon"), item("modern_industrialization:silicon_wafer", 4)], "Semiconductor Silicon", deps=["t5_hv"], xp=250, desc=[
        "Computer chips need silicon purer than 99.9999999%. A single crystal is grown from molten silicon and sliced into wafers."]),
    Q("t6_pvc", 0, 0, [item("modern_industrialization:polyvinyl_chloride_bucket")], "PVC", deps=["t5_hv", "t4_salt"], xp=250, desc=[
        "Ethylene plus chlorine makes vinyl chloride, which polymerises into &ePVC&r. Petrochemistry meets chlor-alkali chemistry."]),
    Q("t6_pu", 2, -1, [item("modern_industrialization:processing_unit"), item("modern_industrialization:highly_advanced_machine_hull")], "EV: Processing Units", deps=["t6_pvc", "t6_silicon"], xp=400, size=1.5, items=[("modern_industrialization:processing_unit", 2)], desc=[
        "Processing units are insulated with PVC and built on silicon. The &eEV hull&r follows."]),
    Q("t6_centrifuge", 4, -2, [item("mekanism:isotopic_centrifuge")], "Isotope Separation", deps=["t6_pu"], xp=300, desc=[
        "Uranium-235 and uranium-238 behave identically in reactions. Only mass tells them apart.",
        "How: turn uranium into gaseous &eUF₆&r using hydrofluoric acid (fluorite + H₂SO₄), then spin it."]),
    Q("t6_fission", 6, -2, [item("mekanismgenerators:fission_reactor_casing", 16)], "Fission", deps=["t6_centrifuge"], xp=400, desc=[
        "Split heavy nuclei and release enormous energy. Mind the temperature, and the waste.",
        "How: Just Enough Mekanism Multiblocks shows the reactor layout in JEI."]),
    Q("t6_waste", 8, -2, [item("mekanism:pellet_plutonium"), item("mekanism:pellet_polonium")], "Transmutation by Neutron", deps=["t6_fission"], xp=500, size=1.5, desc=[
        "Reprocess nuclear waste: neutron capture has turned some of it into &eplutonium&r and &epolonium&r.",
        "Real alchemy. Lead to gold was never the hard part."]),
    Q("t6_haber", 0, 2, [item("chemlib:ammonia_bucket")], "Haber-Bosch", deps=["t4_reactor", "t5_hv"], xp=250, desc=[
        "N₂ + 3H₂ → 2NH₃. The &eHaber-Bosch&r process makes ammonia from air and hydrogen. It feeds half the world's food through fertiliser.",
        "How: nitrogen + hydrogen in MI's Chemical Reactor. Fill a bucket from the output tank."]),
    Q("t6_ostwald", 2, 3, [item("chemlib:nitric_acid_bucket")], "Ostwald Process", deps=["t6_haber"], xp=250, desc=[
        "NH₃ + 2O₂ → HNO₃ + H₂O. Burning ammonia over a catalyst gives &enitric acid&r."]),
    Q("t6_pgm", 4, 3, [item("kubejs:pgm_sludge", 4), item("kubejs:chloroplatinic_acid", 2), item("modern_industrialization:platinum_dust", 4)], "The Platinum Line", deps=["t6_ostwald"], xp=500, size=1.5, desc=[
        "Platinum-group metals hide in the sludge left by refining nickel and copper.",
        "1. &eElectrolyzer&r: nickel or copper dust → dust + PGM sludge (25%).",
        "2. &eAqua regia&r (3 HCl : 1 HNO₃) in the Chemical Reactor dissolves platinum as chloroplatinic acid. Iridium, osmium, rhodium and ruthenium don't dissolve: they're left as residue.",
        "3. &eAmmonium chloride&r (NH₃ + HCl) precipitates ammonium hexachloroplatinate. 4. Heat it in the &eBlast Furnace&r: pure platinum.",
        "5. Centrifuge the residue for iridium, osmium, rhodium and ruthenium."]),
    Q("t6_flux", 4, 1, [item("fluxnetworks:flux_core")], "Wireless Power", deps=["t6_pu"], xp=200, desc=[
        "Flux Networks moves energy without cables. The Flux Core needs a processing unit."]),
    Q("t6_chambers", 6, 0, [item("alchemistry:fission_chamber_controller"), item("alchemistry:fusion_chamber_controller")], "Element Transmutation", deps=["t6_pu"], xp=500, size=1.5, desc=[
        "Alchemistry's fission chamber splits one element into two lighter ones; the fusion chamber merges two into a heavier one.",
        "With both, &eevery element&r is within reach."]),
    Q("t6_table", 8, 0, [item("chemlib:uranium", 16), item("chemlib:oganesson")], "The Complete Periodic Table", deps=["t6_chambers"], xp=1000, size=2.0, shape="gear", items=[("kubejs:energy_core_empty", 1)], desc=[
        "&6Element 118, oganesson.&r It barely exists in reality, but you made one.",
        "Every block in this world can now be built from chemicals. You're close to what you once were."]),
])
