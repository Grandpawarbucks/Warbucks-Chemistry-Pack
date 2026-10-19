"""Quest chapter: apotheosis. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

CHAPTER = Chapter("apotheosis", "Apotheosis", "apotheosis:gem_dust",
        ["Affix loot, gems, enchanting beyond level 30, spawners and Gateways."], SIDE, [
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

    # --- Spawners (y=0) ------------------------------------------------------------------------
    Q("ap_spawner", 0, 0, [item("minecraft:spawner")], "Bottled Monsters", deps=["gs_iron"], xp=60, optional=True, tokens=1,
      subtitle="Optional: mine a spawner with Silk Touch", desc=[
        "&eWhat:&r with Apothic Spawners a monster spawner can be picked up with a Silk Touch pickaxe and moved home.",
        "&eHow:&r find one in a dungeon or mineshaft, light it up, then mine it with Silk Touch. Check its tooltip after placing.",
        "&eTip:&r spawners are mob farms for drops you can't make chemically: bones, string, ender pearls, blaze rods."]),
    Q("ap_rune", 2, 0, [anyof(["apotheosis:spawner_rune", "apotheosis:burning_spawner_rune", "apotheosis:redstone_control_spawner_rune",
                               "apotheosis:ignore_players_spawner_rune", "apotheosis:silent_spawner_rune", "apotheosis:youthful_spawner_rune"])],
      "Spawner Runes", deps=["ap_spawner", "m_gems"], xp=75, optional=True, tokens=1,
      subtitle="Optional: rewrite a spawner's rules", desc=[
        "&eWhat:&r spawner runes change a spawner when you right-click it: spawn without players nearby, obey redstone, set mobs on fire, stay silent, and more.",
        "&eHow:&r a basic Spawner Rune is gem dust, gem-fused slate and spawner chains (check JEI for where chains come from). Each modifier rune adds one item, like campfires for Burning.",
        "&eTip:&r Redstone Control first, so you can switch the farm off when you don't need it."]),

    # --- Affix loot and Gateways (y=1.5) -------------------------------------------------------
    Q("ap_hunt", 0, 1.5, [kill("minecraft:zombie", 50)], "Elite Hunting", deps=["gs_iron"], xp=75, loot="hunt",
      subtitle="Kill 50 zombies and watch for affix gear", optional=True, tokens=1, desc=[
        "&eWhat:&r Apotheosis gives some monsters affixed gear and makes rare elites with a coloured name. Their drops can roll affixes and sockets.",
        "&eHow:&r kill 50 zombies. Pick up any named or glowing item they drop and read its tooltip.",
        "&eTip:&r elites hit hard. Gear up before poking one with a stick."]),
    Q("ap_charm", 2, 1.5, [item("apotheosis:potion_charm")], "Potion Charm", deps=["m_gems", "t2_brewing"], xp=60, optional=True, tokens=1,
      subtitle="Optional: a potion that never runs out (almost)", desc=[
        "&eWhat:&r a Potion Charm holds a potion effect and applies it while switched on, using durability.",
        "&eChemistry:&r blaze powder is a reactive powder; here it fixes the potion so it lasts, a bit like a preservative.",
        "&eHow:&r three identical potions in the middle row and six blaze powder around them. Infusing it later makes it permanent (check JEI).",
        "&eTip:&r Night Vision or Haste charms are the most useful early."]),
    Q("ap_rarity", 4, 1.5, [item("apotheosis:luminous_crystal_shard", 4)], "Rarity Materials", deps=["m_salvage"], xp=60,
      subtitle="Scrap, fabric, crystal, sand, pearl", optional=True, tokens=1, desc=[
        "&eWhat:&r each rarity salvages into its own material: common scrap metal, uncommon timeworn fabric, rare luminous crystal, epic arcane sands, mythic godforged pearls.",
        "&eHow:&r salvage rare (blue) gear in the Salvaging Table until you have 4 luminous crystal shards.",
        "&eTip:&r reforging uses the material of that rarity, so sort your loot by colour before salvaging."]),
    Q("ap_gate", 6, 1.5, [item("gateways:gate_pearl")], "Gate Pearl", deps=["t2_nether"], xp=75,
      subtitle="Gateways to Eternity: a wave-based arena", desc=[
        "&eWhat:&r a Gate Pearl opens a Gateway that releases waves of a chosen mob. Beat every wave for rewards.",
        "&eHow:&r the Blaze gate is five blaze rods, an ender pearl and three nether bricks. Apotheosis adds tiered gates (Frontier and up); JEI shows them all.",
        "&eTip:&r a gate is a controlled mob farm: blaze rods, ender pearls and XP on demand."]),
    Q("ap_gate_close", 8, 1.5, [tick()], "Close a Gateway", deps=["ap_gate"], xp=100, loot="hunt",
      subtitle="Survive every wave", optional=True, tokens=1, desc=[
        "&eWhat:&r the gateway closes when every wave is defeated and pays out its reward.",
        "&eHow:&r throw the pearl in an open area, stay close (leaving fails the gate) and kill each wave. Click the checkmark when it closes.",
        "&eTip:&r tiered Apotheosis gates hand out affix gear and rarity materials."]),

    # --- Gems and sigils (y=6) ----------------------------------------------------------------
    Q("ap_withdraw", 7, 6, [item("apotheosis:sigil_of_withdrawal")], "Sigil of Withdrawal", deps=["m_socket"], xp=50,
      optional=True, tokens=1, subtitle="Optional: get your gems back", desc=[
        "&eWhat:&r pulls every gem out of an item without destroying them, so a good gem can move to new gear.",
        "&eHow:&r gem-fused slate, blaze rods, ender pearls, a lava bucket and gem dust (makes 4).",
        "&eTip:&r withdraw gems before salvaging or reforging old gear."]),
    Q("ap_enhance", 11, 4.5, [item("apotheosis:sigil_of_enhancement")], "Sigil of Enhancement", deps=["m_apoth"], xp=200,
      optional=True, tokens=2, subtitle="Optional: raise a gem's rarity", desc=[
        "&eWhat:&r upgrades a socketed gem to the next rarity at the Reforging Table.",
        "&eHow:&r gem-fused slate, gem dust and a godforged pearl (makes 4). Godforged pearls come from salvaging mythic gear.",
        "&eTip:&r save these for gems you'll keep: a mythic gem in endgame gear is worth it."]),

    # --- Enchanting (y=7 / 8.5) ----------------------------------------------------------------
    Q("ap_infused", 2, 7, [item("apothic_enchanting:infused_hellshelf")], "Infusion", deps=["m_shelves"], xp=75,
      subtitle="Enchant a block instead of a tool", optional=True, desc=[
        "&eWhat:&r Apothic Enchanting can 'infuse' items: enchanting a hellshelf at the right power makes an Infused Hellshelf.",
        "&eHow:&r put a hellshelf in the enchanting table with enough shelves around it. JEI's infusion page shows the exact Eterna, Quanta and Arcana it needs.",
        "&eTip:&r the table's three stats are shown on the screen: power, randomness and how many extra enchantments you get."]),
    Q("ap_library", 4, 7, [item("apothic_enchanting:library")], "Enchantment Library", deps=["ap_infused"], xp=100,
      subtitle="Store every enchanted book", optional=True, tokens=1, desc=[
        "&eWhat:&r the Library absorbs enchanted books and stores their enchantments as points, then pulls out any level you've collected.",
        "&eHow:&r four ender chests, four infused shelves and an enchanting table.",
        "&eTip:&r it only gives back levels up to the highest single book you fed it, so feed it every spare book."]),
    Q("ap_endshelf", 6, 7, [item("apothic_enchanting:endshelf", 4)], "Endshelves", deps=["ap_infused", "w_end"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the strongest shelf family", desc=[
        "&eWhat:&r endshelves push enchanting power past what hellshelves and seashelves allow.",
        "&eHow:&r end stone bricks, a bookshelf, an ender pearl and Infused Breath (dragon's breath infused at the enchanting table).",
        "&eTip:&r collect dragon's breath in glass bottles during the Ender Dragon fight."]),
    Q("ap_tome", 2, 8.5, [item("apothic_enchanting:scrap_tome")], "Scrap Tome", deps=["m_shelves"], xp=40,
      optional=True, tokens=1, subtitle="Optional: recycle enchanted gear", desc=[
        "&eWhat:&r a Scrap Tome in an anvil with enchanted gear strips off some of its enchantments into a book (the gear is destroyed).",
        "&eHow:&r eight books around an anvil makes eight tomes.",
        "&eTip:&r the Extraction Tome (infused) keeps the item; check JEI's infusion page."]),
], links=[("gs_iron", -2, 3)])
