"""Quest chapter: occultism. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

CHAPTER = Chapter("occultism", "Occultism", "occultism:datura",
        ["Spirits, pentacles, otherworld storage and miners that dig where you can't."], SIDE, [
    # --- Occultism (y=10) ----------------------------------------------------------------------
    Q("m_datura", 0, 10, [item("occultism:datura", 4)], "Demon's Dream", deps=["gs_iron"], xp=40,
      subtitle="Eat it and see the Otherworld", desc=[
        "&6You remember seeing everything at once. One bite, and some of it comes back.&r",
        "&eWhat:&r eating Demon's Dream Fruit gives the Third Eye: you see Otherworld blocks hidden behind normal ones.",
        "&eHow:&r break grass for Demon's Dream seeds, grow them, and eat a fruit. The Dictionary of Spirits explains the rest.",
        "&eTip:&r with the Third Eye active, otherworld trees appear among normal oaks."]),
    Q("m_chalk", 2, 10, [item("occultism:chalk_white"), item("occultism:golden_sacrificial_bowl"), item("occultism:sacrificial_bowl", 4)], "Your First Pentacle",
      deps=["m_datura"], xp=60, subtitle="Chalk, bowls and a circle", desc=[
        "&eWhat:&r rituals happen on chalk pentacles, with a Golden Ritual Bowl at the centre and Sacrificial Bowls holding the ingredients.",
        "&eChemistry:&r real chalk is calcium carbonate, CaCO₃: the shells of tiny sea creatures, pressed into rock.",
        "&eHow:&r impure chalk from otherstone and otherworld wood dust, purified in Spiritfire. The Dictionary shows each pentacle's layout."]),
    Q("m_foliot", 4, 10, [item("occultism:book_of_binding_bound_foliot")], "Bind a Foliot", deps=["m_chalk"], xp=75,
      subtitle="Learn a spirit's true name", desc=[
        "&eWhat:&r a bound Book of Binding holds a spirit's name and starts its rituals. Foliots are the weakest spirits.",
        "&eHow:&r craft the Book of Binding (taboo book, purified ink, awakened feather), then bind it as the Dictionary describes.",
        "&eTip:&r foliots can sort items, chop trees or farm for you."]),
    Q("m_iesnium", 6, 10, [item("occultism:iesnium_ingot", 2)], "Iesnium", deps=["m_foliot", "t2_nether"], xp=75,
      subtitle="An Otherworld metal from the Nether", desc=[
        "&eWhat:&r iesnium ore hides in the Nether and only shows up with the Third Eye. You need an infused pickaxe to mine it.",
        "&eHow:&r spirit-attuned gems (a diamond in Spiritfire) make the infused pickaxe. Smelt the ore.",
        "&eTip:&r iesnium tools and the miner spirits come next."]),
    Q("m_miner", 8, 10, [item("occultism:dimensional_mineshaft"), item("occultism:miner_foliot_unspecialized")], "Spirit Miners", deps=["m_iesnium"], xp=150,
      size=1.5, subtitle="A spirit digs in a world you can't see", desc=[
        "&eWhat:&r the Dimensional Mineshaft holds a miner spirit that pulls ores from the Otherworld over time.",
        "&eHow:&r both come from rituals (check the Dictionary and JEI). The miner needs an iesnium pickaxe and a magic lamp.",
        "&eTip:&r in this pack miners &ccan't&r produce chemistry-milestone ores: uranium, uraninite, osmium, fluorite, platinum, iridium or tungsten. Those still come from real processing."]),

    # --- Foliot helpers and the Wild Hunt (y=8.5) ----------------------------------------------
    Q("oc_satchel", 4, 8.5, [item("occultism:satchel")], "Surprisingly Large Bag", deps=["m_foliot"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a foliot lives in your backpack", desc=[
        "&eWhat:&r a satchel with a bound foliot inside that keeps it bigger on the inside.",
        "&eHow:&r a foliot crafting ritual: a chest, two leather, string and a silver ingot around the golden bowl (check the Dictionary for the pentacle).",
        "&eTip:&r the Dictionary lists the other foliot rituals: lumberjack, farmer, cleaner and item transporter."]),
    Q("oc_wildhunt", 6, 8.5, [kill("occultism:wild_hunt_wither_skeleton", 5)], "The Wild Hunt", deps=["m_chalk", "t2_nether"], xp=150, loot="hunt",
      subtitle="Kill 5 Wild Hunt wither skeletons", desc=[
        "&eWhat:&r the Wild Hunt ritual calls a pack of wither skeletons with a good chance of dropping wither skeleton skulls.",
        "&eHow:&r activated with a skeleton skull; it needs copper, silver and gold blocks, a diamond, netherrack and soul sand, plus a sacrifice (check the Dictionary). Then fight.",
        "&eTip:&r this is the easiest way to collect three skulls for the Wither."]),

    # --- Djinni and dimensional storage (y=11.5) -----------------------------------------------
    Q("oc_djinni", 4, 11.5, [item("occultism:book_of_binding_bound_djinni")], "Bind a Djinni", deps=["m_foliot"], xp=100,
      subtitle="A stronger spirit for bigger rituals", desc=[
        "&6You remember spirits who bowed when you passed. This one only negotiates.&r",
        "&eWhat:&r djinn are the second rank of spirits. Their rituals make storage, soul gems, familiar rings and better miners.",
        "&eHow:&r craft a Book of Binding (Djinni), then bind it with the spirit's name, the same way as the foliot (the Dictionary explains it).",
        "&eTip:&r djinni pentacles are bigger; check each layout in the Dictionary before placing chalk."]),
    Q("oc_matrix", 6, 11.5, [item("occultism:dimensional_matrix")], "Dimensional Matrix", deps=["oc_djinni"], xp=75,
      subtitle="The heart of Occultism storage", desc=[
        "&eWhat:&r the Dimensional Matrix binds a djinni to hold items in a pocket dimension.",
        "&eChemistry:&r the quartz it needs is SiO₂, the same crystal that keeps time in a real watch by vibrating at a fixed frequency.",
        "&eHow:&r a djinni crafting ritual with three quartz blocks and an ender pearl."]),
    Q("oc_storage", 8, 11.5, [item("occultism:storage_controller")], "Storage Actuator", deps=["oc_matrix"], xp=150, size=1.5,
      subtitle="A whole warehouse in one block", desc=[
        "&eWhat:&r the Dimensional Storage Actuator stores thousands of items and shows them in one searchable screen.",
        "&eHow:&r a foliot ritual makes the Storage Actuator Base (otherstone pedestal, copper, gold). Put the matrix on top of the base in a crafting grid.",
        "&eTip:&r it's an alternative to AE2 for early storage. Stabilizers expand it."]),
    Q("oc_stabilizer", 10, 11.5, [item("occultism:storage_stabilizer_tier1", 2)], "Storage Stabilizers", deps=["oc_storage"], xp=75,
      subtitle="More room for the warehouse", desc=[
        "&eWhat:&r stabilizers pointed at the Actuator raise how many items and item types it holds.",
        "&eHow:&r tier 1 is a foliot ritual: a tier 0 stabilizer, a copper block, blaze dust and a spirit-attuned gem. Higher tiers need stronger spirits.",
        "&eTip:&r place them within a few blocks, facing the Actuator."]),
    Q("oc_remote", 10, 13, [item("occultism:storage_remote")], "Storage Remote", deps=["oc_storage"], xp=75,
      optional=True, tokens=1, subtitle="Optional: your storage in your pocket", desc=[
        "&eWhat:&r opens your Storage Actuator from anywhere.",
        "&eHow:&r a djinni ritual with an inert remote, two ender pearls and quartz. Link it to the Actuator by clicking it.",
        "&eTip:&r one remote per player saves a lot of walking back to base."]),
    Q("oc_soulgem", 4, 13, [item("occultism:soul_gem")], "Soul Gem", deps=["oc_djinni"], xp=75,
      optional=True, tokens=1, subtitle="Optional: carry a mob around", desc=[
        "&eWhat:&r a Soul Gem traps a living creature so you can move it and release it elsewhere.",
        "&eHow:&r a djinni ritual: a diamond, copper, silver and gold ingots, a fragile soul gem and soul sand.",
        "&eTip:&r it's the easy way to move villagers or animals to your base."]),
    Q("oc_ring", 6, 13, [item("occultism:familiar_ring")], "Familiar Ring", deps=["oc_soulgem"], xp=100,
      optional=True, tokens=1, subtitle="Optional: wear your familiar", desc=[
        "&eWhat:&r familiars are summoned with rituals (greedy, bat, beaver, deer, blacksmith...). The ring stores one so it travels with you.",
        "&eHow:&r a djinni ritual with a soul gem, two gold and two silver ingots. Capture your familiar with it.",
        "&eTip:&r the Greedy Familiar picks up items for you. The Dictionary lists what each familiar does."]),

    # --- Stronger miners and the Afrit (y=10 / 11.5) -------------------------------------------
    Q("oc_miner_djinni", 10, 10, [item("occultism:miner_djinni_ores")], "Djinni Miner", deps=["m_miner", "oc_djinni"], xp=150,
      subtitle="A faster miner that only brings ores", desc=[
        "&eWhat:&r the djinni miner skips the stone and pulls only ores, much faster than a foliot.",
        "&eHow:&r a djinni ritual with the foliot miner, an iesnium pickaxe, gold, lapis and a spirit-attuned crystal.",
        "&eTip:&r the pack's ban list still applies: no uranium, uraninite, osmium, fluorite, platinum, iridium or tungsten."]),
    Q("oc_afrit", 12, 11.5, [item("occultism:book_of_binding_bound_afrit")], "Bind an Afrit", deps=["oc_djinni"], xp=150,
      subtitle="A spirit of fire", desc=[
        "&eWhat:&r afrits are the third rank of spirits. They power stronger rituals and the deep-mining miner.",
        "&eHow:&r craft a Book of Binding (Afrit) and bind it with the spirit's name (see the Dictionary).",
        "&eTip:&r afrit rituals often need afrit essence, which only an unbound afrit drops."]),
    Q("oc_afrit_wild", 14, 11.5, [kill("occultism:afrit_wild")], "Unbound Afrit", deps=["oc_afrit"], xp=300, loot="boss",
      size=1.5, shape="hexagon", subtitle="Summon a wild afrit and defeat it", desc=[
        "&6You remember fire that obeyed. This one remembers being free.&r",
        "&eWhat:&r the Summon Unbound Afrit ritual calls a hostile afrit. It drops afrit essence when killed.",
        "&eHow:&r netherrack, an iesnium ingot, flint and steel and gunpowder, plus a cow as the sacrifice. Build the pentacle far from anything flammable.",
        "&eTip:&r fire resistance potions turn this from a disaster into a fair fight."]),
], links=[("gs_iron", -2, 10)])
