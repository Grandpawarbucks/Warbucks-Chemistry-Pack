"""Quest chapter: t2. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("t2", "III. Divine Ascent", "pylons:infusion_pylon",
        ["Walk through fire, brew in the dark, and take back the sky.",
         "Flight needs the Nether and your first Alchemistry machine: fire and chemistry together."], MAIN, [
    Q("t2_obsidian", 0, 0, [item("minecraft:obsidian", 10), item("minecraft:flint_and_steel")], "A Door of Fire", deps=["gs_ironpick"], xp=30, desc=[
        "A Nether portal is a 4x5 frame of obsidian, lit with flint and steel.",
        "How: you need a diamond pickaxe to mine obsidian, or pour water over a lava source to make it in place."]),
    Q("t2_nether", 2, 0, [dim("minecraft:the_nether")], "Into the Fire", deps=["t2_obsidian"], xp=100, desc=[
        "The Nether is a chemistry lab: sulfur, quartz (SiO₂) and blaze powder all come from here.",
        "How: bring food, armour and blocks. NetherPortalFix keeps portals linked properly."]),
    Q("t2_blaze", 4, -1, [item("minecraft:blaze_rod", 4)], deps=["t2_nether"], xp=50, desc=[
        "Blaze powder fuels brewing, alchemy's oldest form of applied chemistry.",
        "How: blazes spawn in Nether Fortresses. Explorer's Compass can point you to one."]),
    Q("t2_wart", 4, 1, [item("minecraft:nether_wart", 8)], deps=["t2_nether"], xp=25, desc=[
        "The base reagent for almost every potion. It grows on soul sand in fortresses; replant it at home."]),
    Q("t2_quartz", 8, -2, [item("minecraft:quartz", 16)], "Nether Quartz", deps=["t2_nether"], xp=25, desc=[
        "Silicon dioxide, SiO₂. You'll need it for the Infusion Pylon, and much later for silicon."]),
    Q("t2_brewing", 6, 0, [item("minecraft:brewing_stand")], "The Brewer's Art", deps=["t2_blaze", "t2_wart"], xp=75, desc=[
        "Look up &ePotion of Flying&r in JEI (it comes from Apothic Attributes). That's your road back to the sky.",
        "How: awkward potion first (water bottle + nether wart), then follow the JEI recipe."]),
    Q("t2_filter", 8, 0, [item("pylons:potion_filter")], "Potion Filter", deps=["t2_brewing"], xp=75, desc=[
        "Drink a potion, then right-click a Potion Filter to store the effect.",
        "A filter needs &e1 hour&r of an effect to activate (about 7.5 extended potions). Combine filters with the same effect by holding one in each hand and right-clicking."]),
    Q("t2_hydrogen", 8, 2, [item("chemlib:hydrogen", 8)], "Lighter than Air", deps=["t1_dissolver"], xp=75, desc=[
        "Hydrogen is the lightest element. Balloons filled with it carried the first people into the sky in 1783.",
        "Your flight pylon needs it, and only the &eDissolver&r can pull it out of matter as an item.",
        "How: dissolve water, plants or wood and collect the hydrogen."]),
    Q("t2_pylon", 10, 0, [item("pylons:infusion_pylon")], "Wings of a God", deps=["t2_filter", "t2_quartz", "t2_hydrogen"], xp=500, size=2.0, shape="hexagon", items=[("minecraft:experience_bottle", 32)], desc=[
        "&6The sky is yours again.&r",
        "The &eInfusion Pylon&r needs Nether quartz and blackstone, plus &ehydrogen&r from your Dissolver. Fire and chemistry together.",
        "Put an activated Potion of Flying filter in it and you get creative-style flight anywhere.",
        "How: the pylon's chunk must stay loaded, so force-load it with FTB Chunks (press M, right-click the chunk)."]),
    Q("t2_ars", 2, 2, [item("ars_nouveau:worn_notebook"), item("ars_nouveau:source_gem", 4)], "Whispers of Magic", deps=["t2_nether"], xp=50, desc=[
        "Light magic suits a demigod. The Worn Notebook teaches Ars Nouveau spellcrafting.",
        "Its Ritual of Flight is another way to fly near your base. See the Divine Gifts chapter."]),
])
