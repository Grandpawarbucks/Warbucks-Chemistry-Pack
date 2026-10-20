
S_START, S_SOURCE, S_APP, S_BLOOM, S_HELP, S_GEAR, S_RIT = (
    "First Steps", "Source", "The Apparatus", "Magebloom", "Helpers", "Enchanter's Gear", "Rituals")

CHAPTER = Chapter("ars", "Ars Nouveau", "ars_nouveau:novice_spell_book",
        ["Spellcraft, Source, rituals and the Wilden: magic that runs on stored energy."], SIDE, [
    # --- First steps and spell books (ATM10: welcome, books, two info quests, archwood, dowsing) ---------------
    Q("ars_welcome", 0, 0, [item("minecraft:book")], "Words with Weight", deps=["t2_ars"], xp=30, size=1.5, shape="hexagon",
      section=S_START, mirror="6E0E13806F388D7E", subtitle="Every spellbook starts as a plain book", desc=[
        "&6You remember that a word, said the right way, was once enough. A book will have to do for now.&r",
        "&eWhat:&r Ars Nouveau is spellcraft you design yourself: glyphs written into a book, powered by mana, plus Source, a stored magic that runs machines and rituals.",
        "&eHow:&r hold a plain book (paper and leather). The Worn Notebook from Chapter II explains every block and glyph.",
        "&eTip:&r this page runs book, archwood, Scribe's Table, Source, Apparatus, rituals. Glyphs fill the three tiers above."]),
    Q("m_book", 0, 0, [item("ars_nouveau:novice_spell_book")], "Novice Spell Book", deps=["ars_welcome"], xp=50,
      mirror="64D0E66CB4FBEC82", subtitle="Your first spells", desc=[
        "&eWhat:&r the Novice Spell Book holds spells built from glyphs: a form (how it's cast), effects, then augments. It can use tier 1 glyphs.",
        "&eHow:&r a book with an iron shovel, pickaxe, axe and sword (shapeless). Open it to combine glyphs, e.g. Projectile + Break to mine at range.",
        "&eTip:&r the Worn Notebook explains every glyph. Mana regenerates over time."]),
    Q("ars_spellcraft", 0, 0, [tick()], "Building a Spell", deps=["m_book"], xp=20, optional=True, tokens=1,
      mirror="5CFBA24B3E0CDEDD", icon="ars_nouveau:spell_parchment", subtitle="Optional: form, effect, augment", desc=[
        "&eWhat:&r a spell is a row of glyphs read left to right: one form first (Projectile, Touch, Self, Underfoot...), then effects, each followed by the augments that change it.",
        "&eHow:&r open the book's spell screen (the key is in Controls, C by default), drag glyphs into a slot, name it and save. Click the checkmark when you have saved one.",
        "&eTip:&r augments only touch the glyph right before them: Break, Amplify mines harder; Amplify, Break does nothing."]),
    Q("ars_mana", 0, 0, [tick()], "Mana", deps=["m_book"], xp=20, optional=True, tokens=1,
      mirror="6B511C8B572E8940", icon="ars_nouveau:source_gem", subtitle="Optional: the fuel in your head", desc=[
        "&eWhat:&r every cast spends mana from the bar above your hotbar; it refills on its own. Longer spells cost more.",
        "&eHow:&r raise your maximum and regeneration with better spell books, mage armor, mana amulets and threads. Click the checkmark when you've read this.",
        "&eTip:&r mana is personal. Source is the separate, stored energy that machines and rituals use."]),
    Q("ars_archwood", 2, 0, [anytag("c:logs/archwood", 16)], "Archwood Logs", deps=["m_book"], xp=30,
      mirror="33682F4B44950123", subtitle="Any colour of magic wood", desc=[
        "&eWhat:&r archwood is the wood Ars Nouveau builds with: the Scribe's Table, Source Jars, the Imbuement Chamber and every ritual tablet.",
        "&eHow:&r find the bright red, blue, green or purple trees in archwood forests and cut any 16 logs. Bring saplings home too.",
        "&eTip:&r ritual tablets ask for a specific colour (purple for Flight and Binding, green for farming rituals), so plant all four."]),
    Q("ars_dowsing", 0, 0, [item("ars_nouveau:dowsing_rod")], "Dowsing Rod", deps=["ars_archwood"], xp=30,
      optional=True, tokens=1, mirror="3142A40E1EAEBAA3", subtitle="Optional: find geodes and magical creatures", desc=[
        "&eWhat:&r a short burst of Scrying for budding amethyst, and magical creatures within 75 blocks start to glow. It has limited uses.",
        "&eChemistry:&r a geode is a hollow rock where silica-rich water slowly deposited SiO₂ crystals inward, layer by layer.",
        "&eHow:&r a gold ingot above two archwood planks.",
        "&eTip:&r a budding amethyst near home means endless source gems."]),
    Q("m_apprentice", 4, -3, [item("ars_nouveau:apprentice_spell_book")], "Apprentice Spell Book", deps=["m_book"], xp=100,
      mirror="0D330FAD6C993DBC", subtitle="More glyphs, bigger spells", desc=[
        "&eWhat:&r the second spell book tier: more mana, more slots and access to tier 2 glyphs.",
        "&eHow:&r a crafting-grid upgrade: your Novice book with obsidian, 3 diamonds, 2 quartz blocks and 2 blaze rods (keeps your spells).",
        "&eTip:&r more mana means longer spells and more casts between rests."]),
    Q("m_archmage", 8, -3, [item("ars_nouveau:archmage_spell_book")], "Archmage Spell Book", deps=["m_apprentice", "ars_chimera"], xp=250,
      optional=True, tokens=2, mirror="17D7D34F519F7E5F", subtitle="Optional: the top spell book", desc=[
        "&6You remember when every word you spoke was a spell. This book is a reminder.&r",
        "&eWhat:&r the last book tier, with tier 3 glyphs and the most mana.",
        "&eHow:&r crafting grid: the Apprentice book with 3 ender pearls, 2 emeralds, a Totem of Undying, a Nether Star and a Wilden Tribute.",
        "&eTip:&r the Wither and the Wilden Chimera both stand between you and this book."]),

    # --- Scribe's Table and the three glyph tiers ---------------------------------------------------------------
    Q("m_scribe", 4, 0, [item("ars_nouveau:scribes_table")], "Scribe's Table", deps=["ars_archwood"], xp=40,
      size=1.5, shape="hexagon", mirror="3D4D88B8BE881351", subtitle="Write new glyphs into your book", desc=[
        "&6You remember an alphabet older than any language. Each letter you recover is a new glyph.&r",
        "&eWhat:&r the Scribe's Table crafts new glyphs, which unlock more spell parts.",
        "&eHow:&r archwood slabs, gold nuggets and archwood logs. Use your spell book on it, pick a glyph, then throw the items on the table; each glyph also costs experience.",
        "&eTip:&r it pulls ingredients from nearby chests, which saves a lot of throwing."]),
    Q("ars_glyph_t1", 4, -1.5, [tick()], "Tier 1 Glyphs", deps=["m_scribe"], xp=40, section="Tier 1 Glyphs",
      mirror="441C0659ED28D935", icon="ars_nouveau:glyph_break", subtitle="Forms, effects and augments", desc=[
        "&eWhat:&r tier 1 glyphs are the basics: Break, Harm, Ignite, Light, Harvest, Leap, Freeze and more, plus augments like Amplify and Delay. The Novice book can hold them.",
        "&eHow:&r scribe them at the Scribe's Table. Each costs a few common items plus 27 experience points; the quests around this one list each recipe.",
        "&eTip:&r a Touch + Break + Amplify spell is a magic pickaxe. Click the checkmark to open the tier."]),
    Q("ars_glyph_t2", 6, -3, [tick()], "Tier 2 Glyphs", deps=["m_scribe", "m_apprentice"], xp=60, section="Tier 2 Glyphs",
      mirror="63DD7F5A4441ACE7", icon="ars_nouveau:glyph_aoe", subtitle="Explosions, smelting and area spells", desc=[
        "&eWhat:&r tier 2 adds the AOE, Pierce, Fortune, Extract, Extend Time and Dampen augments, and effects like Smelt, Crush, Grow, Exchange, Explosion and Heal.",
        "&eHow:&r scribe them with the Apprentice book (a Novice book can't hold them). Most want an essence from the Imbuement Chamber and 55 experience points.",
        "&eTip:&r Crush + AOE grinds cobble to sand and gravel in bulk. Click the checkmark to open the tier."]),
    Q("ars_glyph_t3", 10, -3, [tick()], "Tier 3 Glyphs", deps=["m_scribe", "m_archmage"], xp=100, optional=True, tokens=1,
      section="Tier 3 Glyphs", mirror="6F3602F5600A6221", icon="ars_nouveau:glyph_lightning",
      subtitle="Optional: Blink, Lightning, Linger, Fangs", desc=[
        "&eWhat:&r tier 3 glyphs are the strongest: Blink (teleport), Lightning, Fangs, Linger (a lasting zone), Split, Glide and the bigger summons.",
        "&eHow:&r scribe them with the Archmage book; each costs 160 experience points and rare items.",
        "&eTip:&r Glide works like an elytra, not like flight. Click the checkmark to open the tier."]),
    *glyphs(1, GLYPHS_T1),
    *glyphs(2, GLYPHS_T2),
    Q("ars_explosion", 6, -4.5, [item("ars_nouveau:glyph_explosion")], "Explosion", deps=["ars_glyph_t2"], xp=30,
      mirror="5DE36D1C9F29F931", subtitle="The chemistry of a bang", desc=[
        "&eWhat:&r causes an explosion where the spell lands. Amplify makes it a bit bigger and harder; AOE makes it much wider but not harder.",
        "&eChemistry:&r TNT is trinitrotoluene, C₇H₅N₃O₆: toluene nitrated with HNO₃ and H₂SO₄, the same acids your Ostwald and contact plants make.",
        "&eHow:&r at the Scribe's Table: fire essence, 3 TNT and a fire charge, plus 55 experience points.",
        "&eTip:&r add Extract and the blast stops destroying the blocks it breaks."]),
    *glyphs(3, GLYPHS_T3),

    # --- Source (ATM10: chamber, gems, jar, sourcelinks, potion jar) -------------------------------------------
    Q("ars_imbuement", 0, 0, [item("ars_nouveau:imbuement_chamber")], "Imbuement Chamber", deps=["ars_archwood"], xp=40,
      section=S_SOURCE, mirror="5766C8B9E850C186", subtitle="Where plain things soak up magic", desc=[
        "&eWhat:&r the Imbuement Chamber turns amethyst or lapis into source gems, and source gems into essences.",
        "&eHow:&r archwood planks and gold (check JEI). It slowly gathers Source by itself; Source Jars within 2 blocks make it much faster.",
        "&eTip:&r essence recipes want Arcane Pedestals with items right next to the chamber."]),
    Q("ars_source_gem", 10, 0, [item("ars_nouveau:source_gem", 16)], "Source Gems", deps=["ars_imbuement"], xp=50,
      size=1.5, shape="hexagon", mirror="40BC67BDEE15D1DE", subtitle="Imbue amethyst or lapis", desc=[
        "&eWhat:&r source gems are the currency of Ars Nouveau: sourcestone, pedestals, relays, essences and charms all need them.",
        "&eChemistry:&r amethyst is quartz (SiO₂) tinted purple by iron impurities; lapis owes its blue to lazurite, an aluminosilicate holding sulfur radicals.",
        "&eHow:&r put an amethyst shard or a lapis lazuli in the Imbuement Chamber and wait; Source Jars nearby speed it up.",
        "&eTip:&r a budding amethyst geode or an amethyst farm turns into an endless gem supply."]),
    Q("m_jar", 6, 0, [item("ars_nouveau:source_jar")], "Source Jar", deps=["ars_source_gem"], xp=75,
      size=1.5, shape="hexagon", mirror="227DBA8836021B0B", subtitle="Store magic, then spend it", desc=[
        "&6You remember power you could pour from one vessel to another. Here it is again, in a jar.&r",
        "&eWhat:&r Source is Ars Nouveau's stored magical energy. Jars hold it, and machines, rituals and helpers draw from jars nearby.",
        "&eHow:&r glass and archwood slabs. Place jars next to whatever spends Source; a comparator reads how full they are.",
        "&eTip:&r empty jars do nothing. The next step is a Sourcelink to fill them."]),
    Q("m_sourcelink", 8, 0, [item("ars_nouveau:volcanic_sourcelink")], "Volcanic Sourcelink", deps=["m_jar"], xp=75,
      mirror="19D02325579F2AA8", subtitle="Turn fuel into Source", desc=[
        "&eWhat:&r the Volcanic Sourcelink burns fuel and pushes the Source into nearby jars.",
        "&eChemistry:&r burning is fast oxidation: C + O₂ → CO₂ plus heat. The sourcelink claims that energy as Source.",
        "&eHow:&r two source gems, two gold ingots and a lava bucket. Feed it logs or coal with a hopper or pipe.",
        "&eTip:&r the other sourcelinks feed on crops (Agronomic), food (Mycelial), mob deaths (Vitalic) and potions (Alchemical)."]),
    Q("ars_vitalic", 0, 0, [item("ars_nouveau:vitalic_sourcelink")], "Vitalic Sourcelink", deps=["m_jar"], xp=40,
      optional=True, tokens=1, mirror="295C77EEC89000FC", subtitle="Optional: Source from life and death", desc=[
        "&eWhat:&r the Vitalic Sourcelink gathers Source when creatures nearby die or age.",
        "&eHow:&r 2 source gems, 2 gold ingots and a glistering melon slice.",
        "&eTip:&r put it beside a mob farm's kill floor."]),
    Q("ars_mycelial", 0, 0, [item("ars_nouveau:mycelial_sourcelink")], "Mycelial Sourcelink", deps=["m_jar"], xp=40,
      optional=True, tokens=1, mirror="77145113CD5B26FB", subtitle="Optional: Source from food", desc=[
        "&eWhat:&r the Mycelial Sourcelink consumes food dropped nearby and turns it into Source; richer food gives more.",
        "&eChemistry:&r food energy is chemical energy: respiration runs C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O, slowly instead of in a flame.",
        "&eHow:&r 2 source gems, 2 gold ingots and a bowl of mushroom stew.",
        "&eTip:&r feed it from a crop farm's surplus with a hopper."]),
    Q("ars_sourcelinks", 8, -1.5, [item("ars_nouveau:agronomic_sourcelink")], "Agronomic Sourcelink", deps=["m_jar"], xp=40,
      optional=True, tokens=1, mirror="2D0CF18C8B2ABB7D", subtitle="Optional: Source from growing plants", desc=[
        "&eWhat:&r the Agronomic Sourcelink makes Source whenever plants around it grow.",
        "&eChemistry:&r plants store sunlight as sugar: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. The sourcelink sips some of that energy.",
        "&eHow:&r 2 source gems, 2 gold ingots and wheat.",
        "&eTip:&r an Agronomic Sourcelink next to a crop farm is free Source forever."]),
    Q("ars_potion_jar", 0, 0, [item("ars_nouveau:potion_jar")], "Potion Jar", deps=["m_jar", "ars_abjuration"], xp=40,
      optional=True, tokens=1, mirror="04D9F6587EF8D9B7", subtitle="Optional: a tank for potions", desc=[
        "&eWhat:&r a Potion Jar stores a large amount of one potion, and pours it back into bottles.",
        "&eHow:&r a Source Jar and abjuration essence (shapeless).",
        "&eTip:&r a brewing Wixie can fill it for you."]),
    Q("ars_alchemical", 0, 0, [item("ars_nouveau:alchemical_sourcelink")], "Alchemical Sourcelink", deps=["ars_potion_jar"], xp=40,
      optional=True, tokens=1, mirror="41A0BE357C8A74E1", subtitle="Optional: Source from potions", desc=[
        "&eWhat:&r the Alchemical Sourcelink drinks potions from nearby Potion Jars and turns them into Source; stronger potions give more.",
        "&eHow:&r 2 source gems, 2 gold ingots and a brewing stand.",
        "&eTip:&r a Wixie brewing into a jar beside it makes a hands-free Source line."]),

    # --- The Apparatus (ATM10: sourcestone, pedestals, apparatus) ------------------------------------------------
    Q("ars_sourcestone", 12, 0, [item("ars_nouveau:sourcestone", 32)], "Sourcestone", deps=["ars_source_gem"], xp=40,
      section=S_APP, mirror="5C3FF43CF16BCF30", subtitle="Stone that carries magic", desc=[
        "&eWhat:&r sourcestone is the building block of the Arcane Core, the Arcane Pedestals and the Enchanting Apparatus.",
        "&eHow:&r eight stone around one source gem gives eight sourcestone (any c:stones work). A stonecutter turns it into bricks and tiles.",
        "&eTip:&r make extra; it's a handsome building stone for your magic room."]),
    Q("ars_pedestals", 0, 0, [item("ars_nouveau:arcane_pedestal", 8)], "Arcane Pedestals", deps=["ars_sourcestone"], xp=50,
      size=1.5, shape="hexagon", mirror="18A2FBE2D4133FA2", subtitle="Eight places to set things down", desc=[
        "&eWhat:&r pedestals hold the side ingredients for the Apparatus, the Imbuement Chamber and the Ritual Brazier.",
        "&eHow:&r sourcestone, gold nuggets and a source gem each (check JEI). Set them around the Apparatus, within a few blocks.",
        "&eTip:&r a hopper under a pedestal won't pull from it; load pedestals by hand or with a Starbuncle."]),
    Q("m_apparatus", 14, 0, [item("ars_nouveau:enchanting_apparatus"), item("ars_nouveau:arcane_core")], "Enchanting Apparatus",
      deps=["ars_pedestals"], xp=100, size=1.5, shape="hexagon", mirror="3D862A3D3F83CA26",
      subtitle="Ars Nouveau's big crafting altar", desc=[
        "&6You remember forging with more hands than two. The pedestals will have to stand in for them.&r",
        "&eWhat:&r the Apparatus sits on an Arcane Core and fuses items from the surrounding Arcane Pedestals, using Source.",
        "&eHow:&r the core is sourcestone, gold and a source gem; the Apparatus is sourcestone, gold and a diamond. Core first, Apparatus on top, then put the main item in it and right-click (check JEI).",
        "&eTip:&r it also applies enchantments to gear: more ways to make divine equipment."]),

    # --- Magebloom (ATM10: seeds, fiber, parchment, chalk) -------------------------------------------------------
    Q("ars_magebloom", 16, 3, [item("ars_nouveau:magebloom_crop", 3)], "Magebloom Seeds", deps=["m_apparatus"], xp=40,
      section=S_BLOOM, mirror="58EC47584C773B82", subtitle="The magic fiber crop", desc=[
        "&eWhat:&r magebloom is a flower crop; each flower gives 4 magebloom fiber for robes, threads, parchment and runic chalk.",
        "&eHow:&r in the Apparatus: any seeds in the middle, 4 source gems on the pedestals. Plant them like wheat.",
        "&eTip:&r a small magebloom field early saves a lot of waiting later."]),
    Q("ars_fiber", 0, 0, [item("ars_nouveau:magebloom_fiber", 16)], "Magebloom Fiber", deps=["ars_magebloom"], xp=30,
      mirror="542C6D76B579886C", subtitle="Spin the magic crop", desc=[
        "&eWhat:&r magebloom fiber is the cloth of Ars Nouveau: robes, threads, the Alteration Table, parchment and runic chalk.",
        "&eChemistry:&r real fibres like cotton are cellulose: long chains of glucose (C₆H₁₀O₅)ₙ held together by hydrogen bonds.",
        "&eHow:&r each magebloom flower crafts into 4 fiber. Keep some seeds back so the field keeps growing.",
        "&eTip:&r a Harvest ritual or a Whirlisprig keeps the field going without you."]),
    Q("ars_parchment", 0, 0, [item("ars_nouveau:spell_parchment")], "Spell Parchment", deps=["ars_fiber"], xp=30,
      mirror="0E2AD156E5EF263A", subtitle="A spell written down", desc=[
        "&eWhat:&r Spell Parchment carries one spell. Turrets, runes and other casters read their spell from it.",
        "&eHow:&r Blank Parchment is paper ringed with magebloom fiber. Put it on the Scribe's Table, pick the spell in your book, then sneak and use the book on the table.",
        "&eTip:&r label your parchments with the spell's name; they all look alike."]),
    Q("ars_chalk_weave", 0, 0, [item("ars_nouveau:runic_chalk")], "Runic Chalk", deps=["ars_parchment", "ars_manipulation"], xp=40,
      optional=True, tokens=1, mirror="151648179684B088", subtitle="Optional: traps drawn on the floor", desc=[
        "&eWhat:&r Runic Chalk draws permanent runes that cast a spell on whatever walks over them; they can be recharged.",
        "&eHow:&r manipulation essence, bone meal and magebloom fiber (shapeless). Draw a rune, then use parchment or your book on it to give it a spell.",
        "&eTip:&r Mirrorweave (magebloom blocks around conjuration essence) hides a rune or a secret door; Sense Magic reveals both."]),

    # --- Helpers (ATM10: dominion wand, then the five charms) ---------------------------------------------------
    Q("ars_dominion", 0, 0, [item("ars_nouveau:dominion_wand")], "Dominion Wand", deps=["m_apparatus"], xp=40,
      optional=True, tokens=1, section=S_HELP, mirror="1D86B2E553503E53", subtitle="Optional: tell things where to go", desc=[
        "&eWhat:&r the Dominion Wand links blocks and creatures: relays to jars, Starbuncles to chests, golems and Weald Walkers to their homes.",
        "&eHow:&r a stick in the Enchanting Apparatus with 2 source gems and a gold ingot on the pedestals.",
        "&eTip:&r click the first thing, then the second. Sneak-click shows what is already linked."]),
    Q("m_starbuncle", 18, 4.5, [item("ars_nouveau:starbuncle_charm")], "Starbuncle", deps=["ars_dominion"], xp=50,
      optional=True, tokens=1, mirror="48D5D9D9AD98409F", subtitle="Optional: a tiny helper that moves items", desc=[
        "&eWhat:&r a Starbuncle carries items from one chest to another. Cute logistics.",
        "&eHow:&r befriend a wild Starbuncle for its shards (the Worn Notebook explains how), then put the shards in the Apparatus with 4 gold ingots.",
        "&eTip:&r use a Dominion Wand to set where it picks up and where it drops off."]),
    Q("ars_shades", 18, 6, [item("ars_nouveau:starbuncle_shades")], "Too Cool for Logistics", deps=["m_starbuncle"], xp=50,
      secret=True, loot="secret", subtitle="Secret: sunglasses for a Starbuncle", desc=[
        "&6You remember having servants who took themselves very seriously. This one does not.&r",
        "&eWhat:&r Starbuncle Shades: tinted glass and a source gem. Give them to a Starbuncle.",
        "&eTip:&r they do nothing useful. That is the point."]),
    Q("ars_wixie", 20, 4.5, [item("ars_nouveau:wixie_charm")], "Wixie", deps=["ars_dominion"], xp=60, optional=True, tokens=1,
      mirror="34A173721735401B", subtitle="Optional: a helper that crafts and brews", desc=[
        "&eWhat:&r a Wixie works a cauldron: it repeats a crafting recipe or brews potions from nearby chests.",
        "&eHow:&r cast a Dispel spell on a witch at half health or less for Wixie Shards, then the Apparatus with a sapling, an emerald, a crafting table and a brewing stand.",
        "&eTip:&r pair a brewing Wixie with a Potion Jar to keep your favourite potion stocked."]),
    Q("ars_whirlisprig", 20, 7.5, [item("ars_nouveau:whirlisprig_charm")], "Whirlisprig", deps=["ars_dominion"], xp=60,
      optional=True, tokens=1, mirror="2C47C9B566A63135", subtitle="Optional: a garden spirit", desc=[
        "&eWhat:&r a Whirlisprig speeds up plant growth around it and makes Source from a varied garden.",
        "&eHow:&r Whirlisprig shards in the Apparatus with a source gem, magebloom (seed and flower), a diamond, three saplings and wheat seeds.",
        "&eTip:&r the more different plants nearby, the happier it is."]),
    Q("ars_drygmy", 20, 6, [item("ars_nouveau:drygmy_charm")], "Drygmy", deps=["ars_dominion"], xp=60, optional=True, tokens=1,
      mirror="04987E54ADC2C057", subtitle="Optional: mob drops without killing", desc=[
        "&eWhat:&r a Drygmy at its henge collects drops from nearby mobs without hurting them.",
        "&eHow:&r Drygmy shards (the Worn Notebook explains how to befriend one) in the Apparatus with fish, wheat, an apple, a carrot, seeds and 3 source gems.",
        "&eTip:&r the Worn Notebook shows the henge layout and what the Drygmy needs nearby."]),
    Q("ars_golem", 0, 0, [item("ars_nouveau:amethyst_golem_charm")], "Amethyst Golem", deps=["ars_dominion", "ars_awakening"], xp=60,
      optional=True, tokens=1, mirror="6CEAA86EEAAC1203", subtitle="Optional: a geode that tends itself", desc=[
        "&eWhat:&r the Amethyst Golem grows and harvests amethyst near its home, turns amethyst blocks into budding amethyst and stores the shards.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured purple by Fe³⁺ ions that natural radiation has changed in the crystal.",
        "&eHow:&r run the Ritual of Awakening near budding amethyst. Place the charm, then give the golem a home with the Dominion Wand (a chest makes it store shards).",
        "&eTip:&r golem shards in an Imbuement Chamber are a hands-free source gem line."]),

    # --- Enchanter's gear (ATM10: ten Apparatus crafts) ---------------------------------------------------------
    Q("ars_enchanter_gear", 14, 6, [item("ars_nouveau:enchanters_sword")], "Enchanter's Sword", deps=["m_apparatus"], xp=60,
      optional=True, tokens=1, section=S_GEAR, mirror="14DB8A515CA50932", subtitle="Optional: a sword that casts on hit", desc=[
        "&eWhat:&r the Enchanter's Sword casts its stored spell on whatever it hits, paid with your mana.",
        "&eHow:&r a diamond sword in the Apparatus with a diamond, 2 gold blocks and 2 source gem blocks. Give it a spell at the Scribe's Table, like a spell book.",
        "&eTip:&r a short Hex or Snare spell makes every hit count."]),
    Q("ars_shield", 0, 0, [item("ars_nouveau:enchanters_shield")], "Enchanter's Shield", deps=["m_apparatus"], xp=60,
      optional=True, tokens=1, section=S_GEAR, mirror="3182E8AF755104E4", subtitle="Optional: a shield fed by mana", desc=[
        "&eWhat:&r a shield that repairs itself with your mana and grants a little protection while you block.",
        "&eHow:&r a shield in the Apparatus with 2 gold blocks and 2 source gem blocks.",
        "&eTip:&r it keeps enchantments from the shield you put in."]),
    Q("ars_mirror", 0, 0, [item("ars_nouveau:enchanters_mirror")], "Enchanter's Mirror", deps=["m_apparatus", "ars_manipulation"], xp=60,
      optional=True, tokens=1, section=S_GEAR, mirror="632BC46928CC9A8C", subtitle="Optional: one self spell, cheaper", desc=[
        "&eWhat:&r the mirror casts one spell on you, cheaper and longer than from the book.",
        "&eHow:&r a source gem block in the Apparatus with 2 glass, 2 manipulation essences, 2 archwood logs and 2 gold ingots.",
        "&eTip:&r inscribe it with a spell that has no form, such as Night Vision (Light) with Extend Time."]),
    Q("ars_spell_bow", 0, 0, [item("ars_nouveau:spell_bow")], "Spell Bow", deps=["m_apparatus", "ars_manipulation"], xp=60,
      optional=True, tokens=1, section=S_GEAR, mirror="51162B9185A45BB1", subtitle="Optional: arrows that carry spells", desc=[
        "&eWhat:&r the Spell Bow puts its stored spell on every arrow, and can fire mana arrows when you have none.",
        "&eHow:&r a bow in the Apparatus with a source gem block, a gold block and manipulation essence.",
        "&eTip:&r Ars also has Pierce and Split arrows for it (check JEI)."]),
    Q("ars_jars", 0, 0, [item("ars_nouveau:jar_of_light"), item("ars_nouveau:void_jar")], "Light and Void", deps=["m_apparatus"],
      xp=40, optional=True, tokens=1, section=S_GEAR, mirror="6DAA82B5F94AF9F8", subtitle="Optional: a lamp that follows you, and a bin", desc=[
        "&eWhat:&r the Jar of Light summons a light that follows you; the Jar of Voiding deletes chosen items as you pick them up, for a little mana.",
        "&eChemistry:&r real 'cold light' exists: in a glow stick, a peroxide reaction excites a dye that gives off light instead of heat.",
        "&eHow:&r both are a glass bottle in the Apparatus. Light: 4 glowstone, 2 redstone lamps and 2 glass. Voiding: a lava bucket, a bucket, an Allow Scroll and an ender pearl.",
        "&eTip:&r a Void Jar set to cobblestone and dirt keeps your inventory clean while mining."]),
    Q("ars_discount", 16, 6, [item("ars_nouveau:ring_of_lesser_discount"), item("ars_nouveau:ring_of_greater_discount")],
      "Rings of Discount", deps=["m_apparatus"], xp=60, optional=True, tokens=1, section=S_GEAR, mirror="0A1ABE9CF7740AAA",
      subtitle="Optional: cheaper spells, twice", desc=[
        "&eWhat:&r discount rings cut the mana cost of every spell you cast. You have two ring slots.",
        "&eHow:&r a Ring of Potential (iron nuggets and a source gem) in the Apparatus with 4 diamonds, 2 ender pearls and 2 source gems. The Greater ring is the lesser one with 4 diamonds, 2 blaze rods and 2 source gems.",
        "&eTip:&r make the lesser ring twice and upgrade one; the two stack."]),
    Q("ars_unstable_belt", 0, 0, [item("ars_nouveau:belt_of_unstable_gifts")], "Belt of Unstable Gifts", deps=["m_apparatus"], xp=40,
      optional=True, tokens=1, section=S_GEAR, mirror="088FCB5267CB7A89", subtitle="Optional: random good potions", desc=[
        "&eWhat:&r the belt hands you a random helpful potion effect every so often.",
        "&eHow:&r a Mundane Belt in the Apparatus with sugar, nether wart, a blaze rod, glowstone dust, a fermented spider eye, redstone, a brewing stand and a feather.",
        "&eTip:&r you can't choose the effect; it's a bonus, not a plan."]),
    Q("ars_belts", 0, 0, [item("ars_nouveau:belt_of_levitation")], "Belt of Levitation", deps=["m_apparatus", "ars_air_essence"],
      xp=40, optional=True, tokens=1, section=S_GEAR, mirror="3FD702B5AB006402", subtitle="Optional: rise by sneaking in mid-air", desc=[
        "&eWhat:&r the Belt of Levitation lets you rise by sneaking in mid-air. It is climbing, not flight.",
        "&eHow:&r a Mundane Belt in the Apparatus with 4 gold ingots, 3 feathers and air essence.",
        "&eTip:&r it also softens falls a little; real flight is still a chemistry milestone."]),
    Q("ars_amulet", 16, 4.5, [item("ars_nouveau:amulet_of_mana_boost"), item("ars_nouveau:amulet_of_mana_regen")], "Mana Amulets",
      deps=["m_apparatus"], xp=40, optional=True, tokens=1, section=S_GEAR, mirror="6A1C0B17B22CE50F",
      subtitle="Optional: more mana, or faster mana", desc=[
        "&eWhat:&r amulets are curios that raise your maximum mana (Boost) or how fast it comes back (Regen). You wear one at a time.",
        "&eHow:&r a Dull Trinket (iron nuggets and a source gem) in the Apparatus. Boost: 3 diamonds and 5 source gems. Regen: 2 diamonds, 2 gold and 4 source gems.",
        "&eTip:&r Regen suits short, frequent spells; Boost suits big ones."]),
    Q("ars_casters", 0, 0, [item("ars_nouveau:wand")], "Enchanter's Wand", deps=["m_apparatus", "ars_manipulation", "ars_air_essence"],
      xp=60, optional=True, tokens=1, section=S_GEAR, mirror="111649D7E16D869F", subtitle="Optional: one spell, fired fast", desc=[
        "&eWhat:&r the wand fires its one stored spell as an accelerated projectile.",
        "&eHow:&r an archwood log in the Apparatus with 4 source gems, 2 gold ingots, air essence and manipulation essence.",
        "&eTip:&r inscribe it with a spell that has no form of its own, e.g. just Break, or Harm + Amplify."]),

    # --- Rituals (ATM10: brazier, then fifteen tablets) ---------------------------------------------------------
    Q("m_brazier", 16, 0, [item("ars_nouveau:ritual_brazier")], "Ritual Brazier", deps=["ars_pedestals"], xp=75,
      size=1.5, shape="hexagon", section=S_RIT, mirror="457DE8C154641437", subtitle="Where rituals happen", desc=[
        "&6You remember rites that changed the weather and the seasons. The brazier remembers them too.&r",
        "&eWhat:&r rituals are area effects: sunrise, cloudshaping, overgrowth, flight and more. Each needs a brazier and a ritual tablet.",
        "&eHow:&r an Arcane Pedestal, a source gem block and three gold ingots (shapeless). Place it and right-click it with a ritual tablet.",
        "&eTip:&r most rituals draw Source from nearby jars, so build next to your source room."]),
    Q("ars_ritual_time", 18, -1.5, [item("ars_nouveau:ritual_sunrise")], "Ritual of Sunrise", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="43784C83C8A76E8B", subtitle="Optional: morning, now", desc=[
        "&eWhat:&r skips the night to sunrise.",
        "&eHow:&r a red archwood log, 3 dandelions and a clock (shapeless).",
        "&eTip:&r on a server it saves waiting for everyone to sleep."]),
    Q("ars_warping", 0, 0, [item("ars_nouveau:ritual_warping")], "Ritual of Warping", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="21EC1A577B4E2FC4", subtitle="Optional: move everyone at once", desc=[
        "&eWhat:&r teleports everything around the brazier to the spot stored in a Warp Scroll.",
        "&eHow:&r a purple archwood log and a Warp Scroll (shapeless). The scroll is blank parchment with lapis and source gems (check JEI).",
        "&eTip:&r a team trip to a far base in one step."]),
    Q("ars_ritual_farm", 18, -3, [item("ars_nouveau:ritual_overgrowth")], "Ritual of Overgrowth", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="07DE3A966516EA8B", subtitle="Optional: everything grows at once", desc=[
        "&eWhat:&r makes plants around the brazier grow, again and again, as if bone-mealed.",
        "&eHow:&r a green archwood log, 3 magebloom and 2 earth essences (shapeless).",
        "&eTip:&r the farming rituals Harvest, Forestation and Flowering also start from a green log (check JEI)."]),
    Q("ars_moonfall", 0, 0, [item("ars_nouveau:ritual_moonfall")], "Ritual of Moonfall", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="34DC34EA5ED7C96D", subtitle="Optional: night, now", desc=[
        "&eWhat:&r skips the day to nightfall.",
        "&eHow:&r a blue archwood log, an ink sac, a coal block and a clock (shapeless).",
        "&eTip:&r night on demand is a quick way to hunt Wilden."]),
    Q("ars_fertility", 0, 0, [item("ars_nouveau:ritual_fertility")], "Ritual of Fertility", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="08803844E52178AA", subtitle="Optional: animals breed on their own", desc=[
        "&eWhat:&r breeds the animals around the brazier without feeding them by hand.",
        "&eHow:&r a green archwood log, 3 wheat, a golden apple and 2 blaze powder (shapeless).",
        "&eTip:&r cap your pens; it doesn't know when to stop."]),
    Q("ars_rituals_more", 0, 0, [item("ars_nouveau:ritual_burrowing")], "Ritual of Burrowing", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="4E0976E1DAF65FC9", subtitle="Optional: a hole straight down", desc=[
        "&eWhat:&r digs holes straight down from the brazier.",
        "&eHow:&r a green archwood log, an iron pickaxe and a coal block (shapeless).",
        "&eTip:&r ore it digs comes out as ore: it saves digging, not processing."]),
    Q("ars_challenge", 0, 0, [item("ars_nouveau:ritual_challenge")], "Ritual of Challenge", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="6D8C9D7D9DF9A6DD", subtitle="Optional: start a raid on purpose", desc=[
        "&eWhat:&r calls a raid to the brazier, the way Bad Omen does.",
        "&eHow:&r a purple archwood log, an emerald block and an ink sac (shapeless).",
        "&eTip:&r a raid farm without hunting pillager captains."]),
    Q("ars_cloudshaping", 0, 0, [item("ars_nouveau:ritual_cloudshaping")], "Ritual of Cloudshaping", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="4F8119B6298EA753", subtitle="Optional: rain on or off", desc=[
        "&eWhat:&r clears the sky, or starts rain or a storm.",
        "&eHow:&r a blue archwood log, a feather and a source gem block (shapeless).",
        "&eChemistry:&r rain forms when water vapour condenses on tiny particles; cloud seeding uses silver iodide, AgI, for the same job.",
        "&eTip:&r a storm on demand makes charged creepers and tridents easier."]),
    Q("ars_disintegration", 0, 0, [item("ars_nouveau:ritual_disintegration")], "Ritual of Disintegration", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="40407D2CDC660866", subtitle="Optional: monsters into experience", desc=[
        "&eWhat:&r destroys hostile creatures near the brazier and leaves extra experience.",
        "&eHow:&r a red archwood log, 3 golden swords and 3 books (shapeless).",
        "&eTip:&r useful for glyph experience, which adds up fast in tier 3."]),
    Q("ars_restoration", 0, 0, [item("ars_nouveau:ritual_restoration")], "Ritual of Restoration", deps=["m_brazier"], xp=40,
      optional=True, tokens=1, mirror="251C9E4B29A29728", subtitle="Optional: heal and cure around you", desc=[
        "&eWhat:&r heals and cures the creatures near the brazier, zombie villagers included.",
        "&eHow:&r a green archwood log, a golden apple and abjuration essence (shapeless).",
        "&eTip:&r curing zombie villagers gives you the best trade prices."]),
    Q("ars_awakening", 0, 0, [item("ars_nouveau:ritual_awakening")], "Ritual of Awakening", deps=["m_brazier"], xp=60,
      optional=True, tokens=1, mirror="0E88FDAE4CB5561B", subtitle="Optional: wake the trees", desc=[
        "&6You remember forests that stood up when you called. Some of them still do.&r",
        "&eWhat:&r awakens nearby archwood trees into Weald Walkers that guard an area, and budding amethyst into an Amethyst Golem charm.",
        "&eHow:&r a green archwood log, one sapling of each colour and 4 source gems (shapeless). Run it next to the tree base or the budding amethyst.",
        "&eTip:&r add Book and Quills to the ritual and it makes Bookwyrm charms instead."]),
    Q("m_ritual", 18, 0, [item("ars_nouveau:ritual_flight")], "Ritual of Flight", deps=["m_brazier", "t2_pylon"], xp=150,
      mirror="7471CDF5166D38F0", subtitle="Base flight, after you've earned the sky", desc=[
        "&6You already remember the sky. Now your home remembers it too.&r",
        "&eWhat:&r gives creative flight to players near the brazier, paid for with Source. It's base flight, not world flight.",
        "&eChemistry:&r hydrogen (H₂) is the lightest gas there is, 14 times less dense than air. It lifted the first balloons in 1783.",
        "&eHow:&r a purple archwood log, 3 Wilden Wings, 2 diamonds, an ender pearl and 2 hydrogen from the Dissolver (this pack's recipe). Put the tablet in the Ritual Brazier and keep the jars topped up.",
        "&eTip:&r this opens after the Infusion Pylon on purpose: real flight is a chemistry milestone."]),
    Q("ars_wilden_ritual", 0, 0, [item("ars_nouveau:ritual_wilden_summon")], "Ritual of Wilden Summoning", deps=["m_brazier", "ars_wilden"],
      xp=60, mirror="28D9ED74EBBC9818", subtitle="Call the Chimera", desc=[
        "&eWhat:&r summons the Wilden Chimera, Ars Nouveau's boss, at the brazier.",
        "&eHow:&r a purple archwood log, 3 Wilden drops (horns, spikes or wings, mixed is fine) and a lapis block (shapeless).",
        "&eTip:&r build a separate brazier away from your base for this one."]),
    Q("ars_scrying", 20, -1.5, [item("ars_nouveau:ritual_scrying")], "Ritual of Scrying", deps=["m_brazier"], xp=50, optional=True, tokens=1,
      mirror="26D2183E27E1273A", subtitle="Optional: see ores through the stone", desc=[
        "&eWhat:&r Scrying highlights a chosen block (usually an ore) through walls for a while.",
        "&eHow:&r a purple archwood log, 3 spider eyes, glowstone and a source gem block. The Worn Notebook shows how to pick which block it reveals.",
        "&eTip:&r combine it with the spectrometer and the pack's deposit depths to find rich veins faster."]),
    Q("ars_ritual_binding", 16, -1.5, [item("ars_nouveau:ritual_binding")], "Ritual of Binding", deps=["m_brazier"], xp=60,
      mirror="634B477861AC9162", subtitle="Turn a helper into a familiar", desc=[
        "&eWhat:&r the Ritual of Binding turns a creature charm into its familiar form, a companion that rides along and grants a bonus.",
        "&eHow:&r a purple archwood log, blank parchment, an ender pearl and 3 source gems. Run it in the brazier with the charm nearby.",
        "&eTip:&r the Worn Notebook lists what each familiar gives."]),
