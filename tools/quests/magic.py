"""Quest chapter: magic. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, MAIN, SIDE  # noqa: F401

CHAPTER = Chapter("magic", "Divine Gifts", "ars_nouveau:novice_spell_book",
        ["Light magic, relics, and the enchanter's craft."], SIDE, [
    # --- Ars Nouveau (y=0) ---------------------------------------------------------------------
    Q("m_book", 0, 0, [item("ars_nouveau:novice_spell_book")], "Novice Spell Book", deps=["t2_ars"], xp=50,
      subtitle="Your first spells", desc=[
        "&6You remember speaking and the world listening. The words come back slowly.&r",
        "&eWhat:&r the Novice Spell Book holds spells built from glyphs: a form (how it's cast), effects, then augments.",
        "&eHow:&r craft it (check JEI), then open it to combine glyphs, e.g. Projectile + Break to mine at range.",
        "&eTip:&r the Worn Notebook explains every glyph. Mana regenerates over time."]),
    Q("m_scribe", 2, 0, [item("ars_nouveau:scribes_table")], "Scribe's Table", deps=["m_book"], xp=40,
      subtitle="Write new glyphs into your book", desc=[
        "&eWhat:&r the Scribe's Table crafts new glyphs, which unlock more spell parts.",
        "&eHow:&r place it, put your spell book on it, and pick a glyph. JEI and the table show each glyph's cost.",
        "&eTip:&r Light and Harvest are cheap early glyphs that pay off right away."]),
    Q("m_jar", 4, 0, [item("ars_nouveau:source_jar"), item("ars_nouveau:imbuement_chamber")], "Source", deps=["m_scribe"], xp=75,
      subtitle="Store magic, then spend it", desc=[
        "&eWhat:&r Source is Ars Nouveau's magical energy. Jars store it; the Imbuement Chamber spends it to make source gems and essences.",
        "&eHow:&r craft both (check JEI). Place jars near the chamber; they share Source within a few blocks.",
        "&eTip:&r empty jars do nothing. The next step is a Sourcelink to fill them."]),
    Q("m_sourcelink", 6, 0, [item("ars_nouveau:volcanic_sourcelink")], "Volcanic Sourcelink", deps=["m_jar"], xp=75,
      subtitle="Turn fuel into Source", desc=[
        "&eWhat:&r the Volcanic Sourcelink burns fuel and pushes the Source into nearby jars.",
        "&eChemistry:&r burning is fast oxidation: C + O₂ → CO₂ plus heat. The sourcelink claims that energy as Source.",
        "&eHow:&r check JEI. Feed it logs or coal with a hopper or pipe; archwood logs give more.",
        "&eTip:&r the other sourcelinks feed on crops (Agronomic), food (Mycelial), mob deaths (Vitalic) and potions (Alchemical)."]),
    Q("m_apparatus", 8, 0, [item("ars_nouveau:enchanting_apparatus"), item("ars_nouveau:arcane_core"), item("ars_nouveau:arcane_pedestal", 4)], "Enchanting Apparatus",
      deps=["m_sourcelink"], xp=100, subtitle="Ars Nouveau's big crafting altar", desc=[
        "&eWhat:&r the Apparatus sits on an Arcane Core and fuses items from surrounding Arcane Pedestals, using Source.",
        "&eHow:&r Core first, Apparatus on top, pedestals within a few blocks. Put the main item in the Apparatus and right-click (check JEI).",
        "&eTip:&r it also applies enchantments to gear: more ways to make divine equipment."]),
    Q("m_brazier", 10, 0, [item("ars_nouveau:ritual_brazier")], "Ritual Brazier", deps=["m_apparatus"], xp=75,
      subtitle="Where rituals happen", desc=[
        "&eWhat:&r rituals are area effects: sunrise, cloudshaping, overgrowth, flight and more. Each needs a brazier and a ritual tablet.",
        "&eHow:&r craft the brazier (check JEI), place it, and right-click it with a ritual tablet.",
        "&eTip:&r most rituals draw Source from nearby jars, so build next to your source room."]),
    Q("m_ritual", 12, 0, [item("ars_nouveau:ritual_flight")], "Ritual of Flight", deps=["m_brazier"], xp=150,
      size=1.5, shape="hexagon", subtitle="Creative flight around your base", desc=[
        "&6You remember the ground being optional. Around your home, it is again.&r",
        "&eWhat:&r gives creative flight to players nearby, paid for with Source. Good for base flight.",
        "&eHow:&r craft the Flight tablet (check JEI), put it in the Ritual Brazier and keep the jars topped up.",
        "&eTip:&r for flight everywhere, see the Angel Ring and jetpacks in Tools and Comfort."]),
    Q("m_starbuncle", 5, -1.5, [item("ars_nouveau:starbuncle_charm")], "Starbuncle", deps=["m_jar"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a tiny helper that moves items", desc=[
        "&eWhat:&r a Starbuncle carries items from one chest to another. Cute logistics.",
        "&eHow:&r befriend a wild Starbuncle in an Archwood forest for its charm, or check JEI. The Worn Notebook explains binding it to chests.",
        "&eTip:&r Starbuncles are great for carrying Botany Pot harvests to storage."]),
    Q("m_apprentice", 9, -1.5, [item("ars_nouveau:apprentice_spell_book")], "Apprentice Spell Book", deps=["m_apparatus"], xp=100,
      optional=True, tokens=1, subtitle="Optional: more glyphs, bigger spells", desc=[
        "&eWhat:&r the second spell book tier: more mana, more slots and access to tier 2 glyphs.",
        "&eHow:&r upgrade your Novice book in the Enchanting Apparatus (check JEI).",
        "&eTip:&r more mana means longer spells and more casts between rests."]),
    Q("m_archmage", 11, -1.5, [item("ars_nouveau:archmage_spell_book")], "Archmage Spell Book", deps=["m_apprentice"], xp=250,
      optional=True, tokens=2, subtitle="Optional: the top spell book", desc=[
        "&eWhat:&r the last book tier, with tier 3 glyphs.",
        "&eHow:&r upgrade the Apprentice book in the Apparatus (check JEI).",
        "&eTip:&r tier 3 glyphs include some of the strongest effects in the mod."]),

    # --- Apotheosis (y=3) ----------------------------------------------------------------------
    Q("m_gems", 0, 3, [item("apotheosis:gem_dust", 4)], "Gem Dust", deps=["gs_iron"], xp=30,
      subtitle="The currency of Apotheosis", desc=[
        "&eWhat:&r Apotheosis gear can roll affixes and sockets. Gems drop from mobs and chests; gem dust builds its tables.",
        "&eHow:&r crush spare gems into gem dust (JEI shows how).",
        "&eTip:&r keep good gems for sockets and crush the rest."]),
    Q("m_simple_reforge", 2, 3, [item("apotheosis:simple_reforging_table")], "Simple Reforging", deps=["m_gems"], xp=40,
      subtitle="Reroll an item's affixes", desc=[
        "&eWhat:&r the Simple Reforging Table rerolls affixes on gear of lower rarities.",
        "&eHow:&r an enchanting table, iron, smooth stone and gem dust.",
        "&eTip:&r reforging costs rarity materials; salvage junk gear to get them."]),
    Q("m_salvage", 4, 3, [item("apotheosis:salvaging_table")], "Salvaging", deps=["m_simple_reforge"], xp=40,
      subtitle="Junk gear into rarity materials", desc=[
        "&eWhat:&r the Salvaging Table breaks affixed gear into materials of its rarity.",
        "&eHow:&r a smithing table, iron tools, copper, a lava bucket and gem dust (check JEI).",
        "&eTip:&r every affixed sword you don't want is a reforge for one you do."]),
    Q("m_gem_cut", 6, 3, [item("apotheosis:gem_cutting_table")], "Gem Cutting", deps=["m_salvage"], xp=50,
      subtitle="Combine gems into higher purities", desc=[
        "&eWhat:&r the Gem Cutting Table upgrades gems to higher purity using matching gems and dust.",
        "&eChemistry:&r real gems are cut along cleavage planes, flat directions where the crystal's bonds are weakest.",
        "&eHow:&r planks, smooth stone, shears and gem dust."]),
    Q("m_apoth", 8, 3, [item("apotheosis:reforging_table")], "Divine Reforging", deps=["m_gem_cut", "t2_nether"], xp=100,
      size=1.5, subtitle="Reforge any rarity, up to mythic", desc=[
        "&6You remember weapons that chose their wielders. These at least choose good affixes.&r",
        "&eWhat:&r the full Reforging Table handles every rarity, up to mythic gear.",
        "&eHow:&r the Simple Reforging Table, netherite, nether bricks and arcane sands (check JEI)."]),
    Q("m_shelves", 1, 4.5, [item("apothic_enchanting:hellshelf", 4)], "Better Bookshelves", deps=["m_gems", "t2_nether"], xp=40,
      optional=True, tokens=1, subtitle="Optional: push enchanting past level 30", desc=[
        "&eWhat:&r Apothic Enchanting adds shelves that raise enchanting power, quanta and arcana. Hellshelves are the first step.",
        "&eHow:&r bookshelves, nether bricks and a blaze rod. Create: Enchantment Industry can automate enchanting later.",
        "&eTip:&r enchanting power above 30 unlocks enchantments beyond vanilla levels."]),
    Q("m_socket", 7, 4.5, [item("apotheosis:sigil_of_socketing")], "Sigil of Socketing", deps=["m_gem_cut"], xp=60,
      optional=True, tokens=1, subtitle="Optional: add a socket to any gear", desc=[
        "&eWhat:&r adds a socket to gear in a smithing table, so you can slot in a gem.",
        "&eHow:&r gem-fused slate, amethyst, gunpowder and gem dust (check JEI).",
        "&eTip:&r a Sigil of Withdrawal pulls gems back out later."]),
    Q("m_augment", 9, 4.5, [item("apotheosis:augmenting_table")], "Augmenting", deps=["m_apoth"], xp=200,
      optional=True, tokens=2, subtitle="Optional: upgrade and reroll single affixes", desc=[
        "&eWhat:&r the Augmenting Table improves or rerolls one affix at a time.",
        "&eHow:&r an enchanting table, a Nether Star, a godforged pearl and polished blackstone (check JEI).",
        "&eTip:&r save it for gear you plan to keep for the rest of the game."]),

    # --- Relics (y=6.5) ------------------------------------------------------------------------
    Q("m_reliquary", 0, 6.5, [item("reliquary:mob_charm_fragment")], "Relics", deps=["gs_iron"], xp=50,
      subtitle="Reliquary, Relics and Artifacts", desc=[
        "&eWhat:&r three mods of found and crafted treasures. Reliquary items are crafted from mob parts; Relics and Artifacts hide in chests and structures.",
        "&eHow:&r mob charm fragments drop from mobs. JEI shows the charm they build.",
        "&eTip:&r a Mob Charm stops that mob type attacking you."]),
    Q("m_alkahest", 2, 6.5, [item("reliquary:alkahestry_tome")], "Alkahestry Tome", deps=["m_reliquary"], xp=75,
      subtitle="The alchemists' dream, in book form", desc=[
        "&eWhat:&r charged with redstone, the tome duplicates common items in a crafting grid.",
        "&eChemistry:&r alchemists searched for alkahest, a universal solvent. None exists (what would you keep it in?), but aqua regia, HCl + HNO₃, dissolves even gold.",
        "&eHow:&r check JEI for the tome and its recipes. Recharge it with redstone."]),
    Q("m_relic_hunt", 1, 8, [tick()], "Relic Hunter", deps=["m_reliquary"], xp=50,
      optional=True, tokens=1, subtitle="Optional: find a relic or an artifact", desc=[
        "&eWhat:&r find any Relics or Artifacts item: a cloud in a bottle, running shoes, a leafy mantle, a mimic's treasure.",
        "&eHow:&r loot chests in dungeons, mineshafts and towers, and beware chests that bite. Click the checkmark when you have one.",
        "&eTip:&r Relics items level up as you use them; check their tooltips."]),
    Q("m_fortune", 3, 8, [item("reliquary:fortune_coin")], "Fortune Coin", deps=["m_alkahest"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a magnet in your pocket", desc=[
        "&eWhat:&r pulls nearby items and XP toward you while active.",
        "&eHow:&r check JEI. Right-click to toggle it.",
        "&eTip:&r turn it off near your sorting system or it'll grab the items."]),

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
])
