"""Quest chapter: apotheosis. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

CHAPTER = Chapter("apotheosis", "Apotheosis", "apotheosis:gem_dust",
        ["Affix loot, gems, enchanting beyond level 30, spawners and Gateways."], SIDE, [
    # --- Apotheosis (y=3) ----------------------------------------------------------------------
    Q("m_gems", 0, 3, [item("apotheosis:gem_dust", 4)], "Gem Dust", deps=["gs_iron"], xp=30,
      subtitle="The currency of Apotheosis", desc=[
        "&6You remember gear that remembered you back. Mortal gear can learn, if you teach it.&r",
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

    # --- ATM10-aligned additions (2026-10-19): sigils, cases, runes, shelves, tomes --------------
    Q("ap_slate", 0, 0, [item("apotheosis:gem_fused_slate", 8)], "Gem-Fused Slate", deps=["m_gems"], xp=30,
      optional=True, tokens=1, subtitle="Optional: the base of every sigil", desc=[
        "&eWhat:&r gem-fused slate is the backing for sigils and spawner runes.",
        "&eChemistry:&r deepslate is metamorphic rock: older stone squeezed and heated deep underground until its minerals recrystallised.",
        "&eHow:&r 8 deepslate around 1 gem dust makes 8."]),
    Q("ap_sigils", 0, 0, [anyof(["apotheosis:sigil_of_rebirth", "apotheosis:sigil_of_unnaming"])], "Working Sigils", deps=["ap_slate"], xp=40,
      optional=True, tokens=1, subtitle="Optional: fuel reforging, or clear a name", desc=[
        "&eWhat:&r the Sigil of Rebirth fuels the Reforging Table; the Sigil of Unnaming removes an item's affix name.",
        "&eHow:&r Rebirth: 6 slate around 3 gem dust. Unnaming: 6 slate around 3 flint. Each makes 6.",
        "&eTip:&r the rarer sigils (Malice, Supremacy) come from Gateways, not the crafting grid."]),
    Q("ap_gem_case", 0, 0, [item("apotheosis:gem_case")], "Gem Case", deps=["m_gem_cut"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a display case that upgrades gems", desc=[
        "&eWhat:&r a cabinet that stores gems by type and purity and can combine two of a kind into the next purity.",
        "&eChemistry:&r a ruby is corundum (Al₂O₃) with about 1% chromium. Less chromium and it's a pink sapphire.",
        "&eHow:&r glass on top, basalt around a Gem Cutting Table, and an ender chest below.",
        "&eTip:&r infused at the enchanting table it becomes the Gem Case of House Fabergé, which keeps the gems inside."]),
    Q("ap_faberge", 0, 0, [item("apotheosis:ender_gem_case")], "House Fabergé", deps=["ap_gem_case", "ap_infused"], xp=100,
      optional=True, tokens=1, subtitle="Optional: the best gem case", desc=[
        "&eWhat:&r the infused Gem Case. It keeps everything stored in the old one.",
        "&eHow:&r infuse a Gem Case at an enchanting table with very high stats (JEI's infusion page: 100 Eterna and Quanta).",
        "&eTip:&r you'll need endshelves or deepshelves to reach those numbers."]),
    Q("ap_rarity_all", 0, 0, [item("apotheosis:mysterious_scrap_metal"), item("apotheosis:timeworn_fabric"), item("apotheosis:arcane_sands"),
                              item("apotheosis:godforged_pearl")], "Every Rarity", deps=["ap_rarity"], xp=150,
      optional=True, tokens=2, subtitle="Optional: scrap, fabric, sands and a pearl", desc=[
        "&eWhat:&r one material of each other rarity: common scrap metal, uncommon timeworn fabric, epic arcane sands and a mythic godforged pearl.",
        "&eHow:&r salvage gear of each colour. The pearl only comes from mythic gear: tiered Gateways and the toughest elites.",
        "&eTip:&r Divine Reforging, upgrade runes and the strongest sigils all spend these."]),
    Q("ap_god_pearl", 0, 0, [item("apotheosis:god_fused_pearl")], "God-Fused Pearl", deps=["ap_rarity_all", "ap_infused"], xp=200,
      optional=True, tokens=2, subtitle="Optional: infuse a mythic pearl", desc=[
        "&6You remember something like this sitting in your crown. It was warmer then.&r",
        "&eWhat:&r a godforged pearl infused at a maxed-out enchanting table, used for the Raven's table.",
        "&eHow:&r an enchanting table at 100 Eterna, about 59 Arcana and 10 Quanta (JEI's infusion page has the exact window)."]),
    Q("ap_raven", 0, 0, [item("apothic_enchanting:raven_enchanting_table")], "Enchanting Table of the Raven", deps=["ap_god_pearl"], xp=250,
      optional=True, tokens=2, subtitle="Optional: set the enchanting stats yourself", desc=[
        "&eWhat:&r an enchanting table where you set the core stats by hand instead of building shelves.",
        "&eHow:&r an Apothic enchanting table, 2 god-fused pearls, 3 obsidian and a perfect Royalty gem (check JEI).",
        "&eTip:&r a late luxury: a good shelf room already does most of this."]),
    Q("ap_chain", 0, 0, [item("apotheosis:spawner_chain")], "Spawner Chains", deps=["ap_spawner"], xp=40,
      optional=True, tokens=1, subtitle="Optional: blow up a spawner", desc=[
        "&eWhat:&r spawner chains are the binding for spawner runes. They only come from a monster spawner destroyed by an explosion.",
        "&eChemistry:&r TNT (C₇H₅N₃O₆) carries its own oxygen in its nitro groups, so it burns in microseconds and makes a shock wave.",
        "&eHow:&r find a spawner you don't want to keep and blow it up with TNT. Pick up the chains.",
        "&eTip:&r keep the good spawners: Silk Touch them home instead."]),
    Q("ap_rune_more", 0, 0, [anyof(["apotheosis:ignore_light_spawner_rune", "apotheosis:ignore_conditions_spawner_rune", "apotheosis:initial_health_spawner_rune",
                                    "apotheosis:no_ai_spawner_rune", "apotheosis:spawn_range_spawner_rune", "apotheosis:echoing_spawner_rune",
                                    "apotheosis:infused_spawner_rune"])],
      "Stranger Runes", deps=["ap_rune", "ap_chain"], xp=60, optional=True, tokens=1, subtitle="Optional: rewrite more spawner rules", desc=[
        "&eWhat:&r more runes: spawn in daylight, ignore spawn conditions, weaken mobs, freeze their AI, change the range. Some need an Infused Spawner Rune.",
        "&eHow:&r a basic Spawner Rune plus the rune's item (Perpetual Twilight: 4 soul lanterns). The infused rune is a spawner rune infused at the table, or ringed with gem dust and bottles o' enchanting.",
        "&eTip:&r Stupor (no AI) makes a mob farm that can't fight back."]),
    Q("ap_rune_upgrade", 0, 0, [anyof(["apotheosis:frontier_spawner_upgrade_rune", "apotheosis:ascent_spawner_upgrade_rune",
                                       "apotheosis:summit_spawner_upgrade_rune", "apotheosis:pinnacle_spawner_upgrade_rune"])],
      "Spawner Upgrade Runes", deps=["ap_rune", "ap_rarity"], xp=75, optional=True, tokens=1, subtitle="Optional: faster, bigger spawners", desc=[
        "&eWhat:&r four tiers of upgrade rune, from Frontiersman's (slightly better) to Thundering (the maximum).",
        "&eHow:&r Frontiersman's: a spawner rune with timeworn fabric, clocks and flint. Higher tiers use rarer materials; Thundering needs godforged pearls and a Nether Star.",
        "&eTip:&r save Nether Stars: the Seed of a New World needs them too."]),
    Q("ap_odd_shelves", 0, 0, [anyof(["apothic_enchanting:stoneshelf", "apothic_enchanting:beeshelf", "apothic_enchanting:melonshelf",
                                      "apothic_enchanting:geode_shelf", "apothic_enchanting:basic_bookshelf"])],
      "Curious Shelves", deps=["m_shelves"], xp=30, optional=True, tokens=1, subtitle="Optional: shelves that bend the rules", desc=[
        "&eWhat:&r the Stoneshelf, Beeshelf, Melonshelf, Geode shelf and Basic Bookshelf each nudge the table's stats in an odd direction.",
        "&eChemistry:&r a geode's calcite rind is CaCO₃, the same compound as chalk and limestone.",
        "&eHow:&r Stoneshelf: polished andesite and books. Geode shelf: calcite around a bookshelf and a budding amethyst. JEI has the rest.",
        "&eTip:&r every shelf's tooltip lists its Eterna, Quanta and Arcana: read them before you build."]),
    Q("ap_hellshelf_up", 0, 0, [anyof(["apothic_enchanting:blazing_hellshelf", "apothic_enchanting:glowing_hellshelf",
                                       "apothic_enchanting:sightshelf", "apothic_enchanting:sightshelf_t2"])],
      "Hellshelf Upgrades", deps=["ap_infused"], xp=60, optional=True, tokens=1, subtitle="Optional: blazing, glowing or all-seeing", desc=[
        "&eWhat:&r the Infused Hellshelf upgrades into Blazing (fire charges), Glowing (glowstone) or the Hellshelf of Sight, which shows more enchantment clues.",
        "&eHow:&r an Infused Hellshelf in the grid with the upgrade items (check JEI). Masterful Sight needs netherite and emerald blocks.",
        "&eTip:&r one Sightshelf shows much more of what the table will roll."]),
    Q("ap_seashelf", 0, 0, [item("apothic_enchanting:seashelf", 4)], "Seashelves", deps=["m_shelves"], xp=40,
      optional=True, tokens=1, subtitle="Optional: the ocean's shelf family", desc=[
        "&eWhat:&r seashelves are the second shelf family, with different stats from hellshelves.",
        "&eChemistry:&r sea water is about 3.5% dissolved salts, mostly NaCl with magnesium and sulfate ions.",
        "&eHow:&r prismarine bricks, a bookshelf, a water bottle and a pufferfish."]),
    Q("ap_seashelf_up", 0, 0, [anyof(["apothic_enchanting:infused_seashelf", "apothic_enchanting:crystal_seashelf",
                                      "apothic_enchanting:heart_seashelf", "apothic_enchanting:filtering_shelf"])],
      "Seashelf Upgrades", deps=["ap_seashelf", "ap_infused"], xp=60, optional=True, tokens=1, subtitle="Optional: infuse a seashelf", desc=[
        "&eWhat:&r an Infused Seashelf, then Crystalline, Heart-Forged or the Seashelf of Aquatic Filtration, which keeps chosen enchantments out of the pool.",
        "&eHow:&r infuse a seashelf at the table, then craft it with prismarine crystals, a heart of the sea, or prismarine bricks and slabs (check JEI).",
        "&eTip:&r the filtering shelf is how you stop a table rolling the enchantment you never want."]),
    Q("ap_deepshelf", 0, 0, [item("apothic_enchanting:dormant_deepshelf"), item("apothic_enchanting:deepshelf")], "Deepshelves", deps=["ap_infused"], xp=75,
      optional=True, tokens=1, subtitle="Optional: shelves from the deep dark", desc=[
        "&eWhat:&r the deepshelf family pushes the stats high. It starts dormant and wakes with infusion.",
        "&eHow:&r Dormant Deepshelf: cracked deepslate tiles and books. Infuse it at the table to wake it.",
        "&eTip:&r upgrade it with echo shards or soul lanterns; the Deepshelf of Arcane Treasures allows treasure enchantments."]),
    Q("ap_deepshelf_up", 0, 0, [anyof(["apothic_enchanting:echoing_deepshelf", "apothic_enchanting:soul_touched_deepshelf",
                                       "apothic_enchanting:treasure_shelf"])],
      "Deepshelf Upgrades", deps=["ap_deepshelf"], xp=75, optional=True, tokens=1, subtitle="Optional: echoing, soul-touched or treasure", desc=[
        "&eWhat:&r Echoing and Soul-Touched deepshelves raise the stats further; the treasure shelf lets the table roll treasure enchantments.",
        "&eHow:&r a Deepshelf with an echo shard and candles, or a soul lantern and sculk. Treasure: 2 deepshelves, gold blocks, diamonds and an emerald block.",
        "&eTip:&r echo shards come from Ancient City chests."]),
    Q("ap_sculkshelf", 0, 0, [item("apothic_enchanting:warden_tendril"), anyof(["apothic_enchanting:echoing_sculkshelf", "apothic_enchanting:soul_touched_sculkshelf"])],
      "Sculkshelves", deps=["ap_deepshelf_up"], xp=150, optional=True, tokens=2, subtitle="Optional: take a tendril from the Warden", desc=[
        "&eWhat:&r the strongest deepshelves need a Warden Tendril, which drops from a Warden.",
        "&eHow:&r kill a Warden (Ancient City; don't make a sound), then craft the tendril over an upgraded deepshelf with sculk and a sculk catalyst.",
        "&eTip:&r a Warden has 500 health and its sonic boom ignores armor. Plan the fight, or plan the escape."]),
    Q("ap_endshelf_up", 0, 0, [item("apothic_enchanting:infused_breath"), anyof(["apothic_enchanting:pearl_endshelf", "apothic_enchanting:draconic_endshelf"])],
      "Endshelf Upgrades", deps=["ap_endshelf"], xp=150, optional=True, tokens=2, subtitle="Optional: pearlescent or draconic", desc=[
        "&eWhat:&r the top of the shelf ladder. The Pearlescent Endshelf adds end rods; the Draconic one is crowned with a dragon head.",
        "&eHow:&r infuse dragon's breath for Infused Breath (3 per bottle), then craft an Endshelf with end rods and ender pearls, or a dragon head and pearls.",
        "&eTip:&r dragon heads hang on End Ship bows. Bring the elytra home too."]),
    Q("ap_tomes", 0, 0, [anyof(["apothic_enchanting:other_tome", "apothic_enchanting:improved_scrap_tome", "apothic_enchanting:extraction_tome"])],
      "Better Tomes", deps=["ap_tome", "ap_infused"], xp=50, optional=True, tokens=1, subtitle="Optional: books with a single job", desc=[
        "&eWhat:&r the Tome of the Others enchants like a tool no other tome covers; Superior Scrapping and Extraction strip enchantments more gently (Extraction keeps the item).",
        "&eHow:&r Tome of the Others: 6 books and a blaze rod (makes 6). Infuse a Scrap Tome for Superior Scrapping, and that for Extraction.",
        "&eTip:&r Extraction tomes are the cleanest way to move a good enchantment to new gear."]),
    Q("ap_alexandria", 0, 0, [item("apothic_enchanting:ender_library")], "Library of Alexandria", deps=["ap_library"], xp=150,
      optional=True, tokens=2, subtitle="Optional: the library, infused", desc=[
        "&eWhat:&r the infused Enchantment Library stores more and gives back higher levels.",
        "&eHow:&r infuse an Enchantment Library at the enchanting table; it keeps the enchantments already inside (check JEI for the stats).",
        "&eTip:&r the real Library of Alexandria burned; keep this one away from your blaze farm."]),
    Q("ap_leads", 0, 0, [anyof(["apothic_enchanting:flimsy_ender_lead", "apothic_enchanting:ender_lead", "apothic_enchanting:occult_ender_lead"])],
      "Ender Leads", deps=["m_shelves"], xp=40, optional=True, tokens=1, subtitle="Optional: carry a mob in your pocket", desc=[
        "&eWhat:&r the Flimsy Ender Lead captures animals; the infused Ender Lead captures most mobs; the Occult one can bind a mob to a spawner.",
        "&eHow:&r flimsy: an ender pearl, a lead and a gold ingot (shapeless). Infuse it for the Ender Lead; infuse that holding a witch for the Occult lead.",
        "&eTip:&r the easy way to move a villager across the world."]),
    Q("ap_trident", 0, 0, [item("apothic_enchanting:inert_trident")], "Inert Trident", deps=["ap_infused"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a trident without a drowned", desc=[
        "&eWhat:&r an inert trident infuses into a real trident at the enchanting table.",
        "&eHow:&r 3 nautilus shells, a heart of the sea and an iron ingot. Then infuse it (check JEI for the stats).",
        "&eTip:&r a Channeling trident in a thunderstorm calls lightning where it lands."]),
], links=[("gs_iron", -2, 3)])
