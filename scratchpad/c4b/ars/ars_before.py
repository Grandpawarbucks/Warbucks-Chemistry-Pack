"""Quest chapter: ars. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, anytag, SIDE  # noqa: F401

# Layout: the main line runs left to right at y=0 (book -> Source -> Apparatus -> brazier -> flight).
# Spells and Source/Apparatus side quests sit above (y<0); essences, Wilden, Ars Elemental and gear below (y>0).
# Recipes checked against ars_nouveau 5.13.3, ars_elemental 0.7.10.4 and ars_additions 21.3.0. The pack's KubeJS
# does not change any Ars recipe; flight stays behind the chemistry-gated Infusion Pylon (t2_pylon) in this book.

CHAPTER = Chapter("ars", "Ars Nouveau", "ars_nouveau:novice_spell_book",
        ["Spellcraft, Source, rituals and the Wilden: magic that runs on stored energy."], SIDE, [
    # --- Main line (y=0) -----------------------------------------------------------------------
    Q("m_book", 0, 0, [item("ars_nouveau:novice_spell_book")], "Novice Spell Book", deps=["t2_ars"], xp=50,
      subtitle="Your first spells", desc=[
        "&6You remember speaking and the world listening. The words come back slowly.&r",
        "&eWhat:&r the Novice Spell Book holds spells built from glyphs: a form (how it's cast), effects, then augments.",
        "&eHow:&r a book with an iron shovel, pickaxe, axe and sword (shapeless). Open it to combine glyphs, e.g. Projectile + Break to mine at range.",
        "&eTip:&r the Worn Notebook explains every glyph. Mana regenerates over time."]),
    Q("ars_archwood", 2, 0, [anytag("c:logs/archwood", 16)], "Archwood Logs", deps=["m_book"], xp=30,
      subtitle="Any colour of magic wood", desc=[
        "&eWhat:&r archwood is the wood Ars Nouveau builds with: the Scribe's Table, Source Jars, the Imbuement Chamber and every ritual tablet.",
        "&eHow:&r find the bright red, blue, green or purple trees in archwood forests and cut any 16 logs. Bring saplings home too.",
        "&eTip:&r ritual tablets ask for a specific colour (purple for Flight and Binding, green for farming rituals), so plant all four."]),
    Q("m_scribe", 4, 0, [item("ars_nouveau:scribes_table")], "Scribe's Table", deps=["ars_archwood"], xp=40,
      subtitle="Write new glyphs into your book", desc=[
        "&eWhat:&r the Scribe's Table crafts new glyphs, which unlock more spell parts.",
        "&eHow:&r archwood slabs, gold nuggets and archwood logs. Put your spell book on it and pick a glyph; each costs items and experience.",
        "&eTip:&r Light and Harvest are cheap early glyphs that pay off right away."]),
    Q("m_jar", 6, 0, [item("ars_nouveau:source_jar"), item("ars_nouveau:imbuement_chamber")], "Source", deps=["m_scribe"], xp=75,
      subtitle="Store magic, then spend it", desc=[
        "&eWhat:&r Source is Ars Nouveau's magical energy. Jars store it; the Imbuement Chamber spends it to make source gems and essences.",
        "&eHow:&r jars are glass and archwood slabs; the chamber is archwood planks and gold. Place jars near the chamber; they share Source within a few blocks.",
        "&eTip:&r empty jars do nothing. The next step is a Sourcelink to fill them."]),
    Q("m_sourcelink", 8, 0, [item("ars_nouveau:volcanic_sourcelink")], "Volcanic Sourcelink", deps=["m_jar"], xp=75,
      subtitle="Turn fuel into Source", desc=[
        "&eWhat:&r the Volcanic Sourcelink burns fuel and pushes the Source into nearby jars.",
        "&eChemistry:&r burning is fast oxidation: C + O₂ → CO₂ plus heat. The sourcelink claims that energy as Source.",
        "&eHow:&r two source gems, two gold ingots and a lava bucket. Feed it logs or coal with a hopper or pipe.",
        "&eTip:&r the other sourcelinks feed on crops (Agronomic), food (Mycelial), mob deaths (Vitalic) and potions (Alchemical)."]),
    Q("ars_source_gem", 10, 0, [item("ars_nouveau:source_gem", 16)], "Source Gems", deps=["m_sourcelink"], xp=50,
      subtitle="Imbue amethyst or lapis", desc=[
        "&eWhat:&r source gems are the currency of Ars Nouveau: sourcestone, pedestals, relays, essences and charms all need them.",
        "&eChemistry:&r amethyst is quartz (SiO₂) tinted purple by iron impurities; lapis owes its blue to lazurite, an aluminosilicate holding sulfur radicals.",
        "&eHow:&r put an amethyst shard or a lapis lazuli in the Imbuement Chamber with Source nearby. Each gem costs 500 Source.",
        "&eTip:&r a budding amethyst geode or an amethyst farm turns into an endless gem supply."]),
    Q("ars_sourcestone", 12, 0, [item("ars_nouveau:sourcestone", 32)], "Sourcestone", deps=["ars_source_gem"], xp=40,
      subtitle="Stone that carries magic", desc=[
        "&eWhat:&r sourcestone is the building block of the Arcane Core, the Arcane Pedestals and the Enchanting Apparatus.",
        "&eHow:&r eight stone around one source gem gives eight sourcestone (any c:stones work). A stonecutter turns it into bricks and tiles.",
        "&eTip:&r make extra; it's a handsome building stone for your magic room."]),
    Q("m_apparatus", 14, 0, [item("ars_nouveau:enchanting_apparatus"), item("ars_nouveau:arcane_core"), item("ars_nouveau:arcane_pedestal", 4)], "Enchanting Apparatus",
      deps=["ars_sourcestone"], xp=100, subtitle="Ars Nouveau's big crafting altar", desc=[
        "&eWhat:&r the Apparatus sits on an Arcane Core and fuses items from surrounding Arcane Pedestals, using Source.",
        "&eHow:&r Core first, Apparatus on top, pedestals within a few blocks. Put the main item in the Apparatus and right-click (check JEI).",
        "&eTip:&r it also applies enchantments to gear: more ways to make divine equipment."]),
    Q("m_brazier", 16, 0, [item("ars_nouveau:ritual_brazier")], "Ritual Brazier", deps=["m_apparatus"], xp=75,
      subtitle="Where rituals happen", desc=[
        "&eWhat:&r rituals are area effects: sunrise, cloudshaping, overgrowth, flight and more. Each needs a brazier and a ritual tablet.",
        "&eHow:&r an Arcane Pedestal, a source gem block and three gold ingots (shapeless). Place it and right-click it with a ritual tablet.",
        "&eTip:&r most rituals draw Source from nearby jars, so build next to your source room."]),
    Q("m_ritual", 18, 0, [item("ars_nouveau:ritual_flight")], "Ritual of Flight", deps=["m_brazier", "t2_pylon"], xp=150,
      size=1.5, shape="hexagon", subtitle="Base flight, after you've earned the sky", desc=[
        "&6You already remember the sky. Now your home remembers it too.&r",
        "&eWhat:&r gives creative flight to players near the brazier, paid for with Source. It's base flight, not world flight.",
        "&eChemistry:&r hydrogen (H₂) is the lightest gas there is, 14 times less dense than air. It lifted the first balloons in 1783.",
        "&eHow:&r a purple archwood log, 3 Wilden Wings, 2 diamonds, an ender pearl and 2 hydrogen from the Dissolver (this pack's recipe). Put the tablet in the Ritual Brazier and keep the jars topped up.",
        "&eTip:&r this opens after the Infusion Pylon on purpose: real flight is a chemistry milestone."]),

    # --- Spells (y=-1.5 .. -4.5) -------------------------------------------------------------
    Q("ars_glyph_t1", 4, -1.5, [tick()], "Tier 1 Glyphs", deps=["m_scribe"], xp=40,
      subtitle="Forms, effects and augments", desc=[
        "&eWhat:&r tier 1 glyphs are the basics: Projectile, Touch and Self (forms); Break, Harm, Ignite, Light, Harvest, Leap and Freeze (effects); Amplify, Delay and Randomize (augments).",
        "&eHow:&r scribe them at the Scribe's Table. Each costs a few common items plus experience; JEI shows the exact list.",
        "&eTip:&r a Touch + Break + Amplify spell is a magic pickaxe. Click the checkmark once you've written five glyphs."]),
    Q("m_apprentice", 4, -3, [item("ars_nouveau:apprentice_spell_book")], "Apprentice Spell Book", deps=["ars_glyph_t1"], xp=100,
      subtitle="More glyphs, bigger spells", desc=[
        "&eWhat:&r the second spell book tier: more mana, more slots and access to tier 2 glyphs.",
        "&eHow:&r a crafting-grid upgrade: your Novice book with obsidian, 3 diamonds, 2 quartz blocks and 2 blaze rods (keeps your spells).",
        "&eTip:&r more mana means longer spells and more casts between rests."]),
    Q("ars_glyph_t2", 6, -3, [tick()], "Tier 2 Glyphs", deps=["m_apprentice"], xp=60,
      subtitle="Explosions, smelting and area spells", desc=[
        "&eWhat:&r tier 2 adds the AOE, Pierce, Fortune, Extract, Extend Time and Dampen augments, and effects like Smelt, Crush, Grow, Exchange, Explosion, Heal and Slowfall.",
        "&eHow:&r scribe them with the Apprentice book. Several want an essence from the Imbuement Chamber (check JEI).",
        "&eTip:&r Crush + AOE grinds cobble to sand and gravel in bulk. Click the checkmark when you've written three."]),
    Q("ars_explosion", 6, -4.5, [item("ars_nouveau:fire_essence"), item("minecraft:tnt", 3)], "Explosion Glyph", deps=["ars_glyph_t2"],
      xp=60, optional=True, tokens=1, subtitle="Optional: the chemistry of a bang", desc=[
        "&eWhat:&r the Explosion glyph needs fire essence, three TNT and a fire charge. Scribe it and your spells can blast.",
        "&eChemistry:&r TNT is trinitrotoluene, C₇H₅N₃O₆: toluene nitrated with HNO₃ and H₂SO₄, the same acids your Ostwald and contact plants make.",
        "&eHow:&r gather the items, then write the glyph at the Scribe's Table.",
        "&eTip:&r Dampen makes the blast smaller and Amplify makes it bigger."]),
    Q("m_archmage", 8, -3, [item("ars_nouveau:archmage_spell_book")], "Archmage Spell Book", deps=["ars_chimera"], xp=250,
      optional=True, tokens=2, subtitle="Optional: the top spell book", desc=[
        "&6You remember when every word you spoke was a spell. This book is a reminder.&r",
        "&eWhat:&r the last book tier, with tier 3 glyphs and the most mana.",
        "&eHow:&r crafting grid: the Apprentice book with 3 ender pearls, 2 emeralds, a Totem of Undying, a Nether Star and a Wilden Tribute.",
        "&eTip:&r the Wither and the Wilden Chimera both stand between you and this book."]),
    Q("ars_glyph_t3", 10, -3, [tick()], "Tier 3 Glyphs", deps=["m_archmage"], xp=100, optional=True, tokens=1,
      subtitle="Optional: Blink, Lightning, Linger, Wall", desc=[
        "&eWhat:&r tier 3 glyphs are the strongest: Blink (teleport), Lightning, Fangs, Linger and Wall (lasting zones), Split, Glide and summons.",
        "&eHow:&r scribe them with the Archmage book; they cost the most experience (check JEI).",
        "&eTip:&r Glide works like an elytra, not like flight. Click the checkmark when you've written one."]),

    # --- Source and Apparatus side quests (y=-1.5 .. -4.5) -------------------------------------
    Q("ars_sourcelinks", 8, -1.5, [anyof(["ars_nouveau:agronomic_sourcelink", "ars_nouveau:mycelial_sourcelink",
                                         "ars_nouveau:vitalic_sourcelink", "ars_nouveau:alchemical_sourcelink"])],
      "Other Sourcelinks", deps=["m_sourcelink"], xp=50, optional=True, tokens=1,
      subtitle="Optional: Source from crops, food, mobs or potions", desc=[
        "&eWhat:&r every sourcelink feeds on a different kind of energy. Agronomic eats crop growth, Mycelial eats food, Vitalic eats mob deaths, Alchemical eats potions.",
        "&eChemistry:&r all of them are the same idea in a costume: stored chemical energy (sugars, fats, potions) released and captured.",
        "&eHow:&r same frame as the Volcanic one (source gems and gold) around wheat, mushroom stew, a glistering melon or a brewing stand.",
        "&eTip:&r an Agronomic Sourcelink next to a crop farm is free Source forever."]),
    Q("ars_relay", 10, -1.5, [item("ars_nouveau:relay", 2)], "Source Relays", deps=["ars_source_gem"], xp=40, optional=True, tokens=1,
      subtitle="Optional: move Source across your base", desc=[
        "&eWhat:&r relays carry Source from one jar to another, so your sourcelinks don't have to sit next to the machines that spend it.",
        "&eHow:&r gold ingots around a source gem block. Link them with a Dominion Wand (the Worn Notebook shows how). A Relay Splitter shares one input between many outputs.",
        "&eTip:&r put noisy sourcelink farms out of sight and relay the Source in."]),
    Q("ars_ender_jar", 12, -1.5, [item("ars_additions:ender_source_jar")], "Ender Source Jar", deps=["ars_storage"], xp=50, optional=True, tokens=1,
      subtitle="Optional: Source that follows you", desc=[
        "&eWhat:&r an Ars Additions jar whose Source is shared with your other Ender Source Jars, wherever they are.",
        "&eHow:&r a Source Jar in the Apparatus with 4 ender pearls and 4 popped chorus fruit.",
        "&eTip:&r one at home and one at an outpost makes a Source network without relays."]),
    Q("ars_storage", 12, -3, [item("ars_nouveau:storage_lectern"), item("ars_nouveau:repository", 2)], "Storage Lectern", deps=["m_apparatus"], xp=50,
      optional=True, tokens=1, subtitle="Optional: Ars Nouveau's own storage network", desc=[
        "&eWhat:&r the Storage Lectern shows the contents of linked Repositories and chests in one searchable screen.",
        "&eHow:&r a lectern with 4 chests in the Apparatus; Repositories are archwood logs and gold nuggets. Link them with a Dominion Wand.",
        "&eTip:&r it's small and cheap; AE2 or Occultism storage scale further."]),
    Q("ars_turret", 12, -4.5, [item("ars_nouveau:spell_turret")], "Spell Turret", deps=["ars_storage"], xp=60, optional=True, tokens=1,
      subtitle="Optional: spells that cast themselves", desc=[
        "&eWhat:&r a turret casts the spell you inscribe into it whenever it gets a redstone signal, using Source from nearby jars.",
        "&eHow:&r the Basic Spell Turret is source gems, gold and a redstone block; upgrade it in the Apparatus with a source gem block and 2 blaze rods.",
        "&eTip:&r a turret with Break or Harvest on a clock is a simple farm."]),
    Q("ars_charm", 14, -1.5, [anyof(["ars_additions:undying_charm", "ars_additions:fall_prevention_charm",
                                     "ars_additions:fire_resistance_charm", "ars_additions:night_vision_charm",
                                     "ars_additions:water_breathing_charm", "ars_additions:void_protection_charm"])],
      "Ars Additions Charms", deps=["ars_discount"], xp=60, optional=True, tokens=1,
      subtitle="Optional: one-shot protections in a bottle", desc=[
        "&eWhat:&r Ars Additions charms save you once from a specific danger: falling, fire, drowning, the void, or death itself.",
        "&eHow:&r made in the Enchanting Apparatus around a glass bottle (the Undying Charm takes a Totem of Undying, crying obsidian and glowstone). Recharge them in the Imbuement Chamber.",
        "&eTip:&r a Void Protection Charm (stable warp scroll and end stone bricks) is cheap insurance in the End."]),
    Q("ars_haversack", 14, -3, [item("ars_additions:handy_haversack")], "Handy Haversack", deps=["ars_storage"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a bag bound to a chest", desc=[
        "&eWhat:&r the Handy Haversack links to a container so items you pick up go straight there.",
        "&eHow:&r craft it (check JEI), then bind it to a chest or your storage as its tooltip says.",
        "&eTip:&r bind it to your AE2 or Occultism storage interface for a bottomless pocket."]),

    # --- Rituals (y=-1.5 .. -4.5) ----------------------------------------------------------------
    Q("ars_ritual_binding", 16, -1.5, [item("ars_nouveau:ritual_binding")], "Ritual of Binding", deps=["m_brazier"], xp=60,
      subtitle="Turn a helper into a familiar", desc=[
        "&eWhat:&r the Ritual of Binding turns a creature charm into its familiar form, a companion that rides along and grants a bonus.",
        "&eHow:&r a purple archwood log, blank parchment, an ender pearl and 3 source gems. Run it in the brazier with the charm nearby.",
        "&eTip:&r the Worn Notebook lists what each familiar gives."]),
    Q("ars_familiar", 16, -3, [anyof(["ars_nouveau:familiar_starbuncle", "ars_nouveau:familiar_wixie", "ars_nouveau:familiar_drygmy",
                                      "ars_nouveau:familiar_whirlisprig", "ars_nouveau:familiar_bookwyrm", "ars_nouveau:familiar_amethyst_golem",
                                      "ars_elemental:firenando_familiar", "ars_elemental:flashjack_familiar", "ars_elemental:siren_familiar"])],
      "A Familiar", deps=["ars_ritual_binding"], xp=75, optional=True, tokens=1,
      subtitle="Optional: a small spirit that follows you", desc=[
        "&eWhat:&r a familiar is a bound creature that rides along and gives a passive bonus: Starbuncles speed you up, Wixies boost potions, Bookwyrms cut spell costs.",
        "&eHow:&r run the Ritual of Binding with the creature's charm nearby to turn it into a familiar item. Use the item to call your familiar.",
        "&eTip:&r Ars Elemental adds elemental familiars (Firenando, Flashjack, Siren) that boost that school of magic."]),
    Q("ars_ritual_time", 18, -1.5, [anyof(["ars_nouveau:ritual_sunrise", "ars_nouveau:ritual_moonfall", "ars_nouveau:ritual_cloudshaping"])],
      "Sky Rituals", deps=["m_brazier"], xp=50, optional=True, tokens=1, subtitle="Optional: command the day and the weather", desc=[
        "&eWhat:&r Sunrise skips to morning, Moonfall to night, and Cloudshaping clears or starts rain.",
        "&eHow:&r Sunrise is a red archwood log, 3 dandelions and a clock; Moonfall a blue log, an ink sac, a coal block and a clock; Cloudshaping a blue log, a feather and a source gem block.",
        "&eTip:&r Moonfall on demand is a quick way to hunt Wilden."]),
    Q("ars_ritual_farm", 18, -3, [anyof(["ars_nouveau:ritual_overgrowth", "ars_nouveau:ritual_fertility", "ars_nouveau:ritual_harvest",
                                         "ars_nouveau:ritual_forestation", "ars_nouveau:ritual_flowering"])],
      "Garden Rituals", deps=["ars_ritual_time"], xp=50, optional=True, tokens=1,
      subtitle="Optional: crops, trees and animals on their own", desc=[
        "&eWhat:&r green-log rituals tend the land: Overgrowth grows plants, Fertility breeds animals, Harvest reaps crops, Forestation plants trees.",
        "&eHow:&r each starts from a green archwood log; Harvest is the log, earth essence and an iron hoe. JEI has the rest.",
        "&eTip:&r a Harvest ritual next to an Agronomic Sourcelink feeds itself."]),
    Q("ars_scrying", 20, -1.5, [item("ars_nouveau:ritual_scrying")], "Ritual of Scrying", deps=["ars_ritual_time"], xp=50, optional=True, tokens=1,
      subtitle="Optional: see ores through the stone", desc=[
        "&eWhat:&r Scrying highlights a chosen block (usually an ore) through walls for a while.",
        "&eHow:&r a purple archwood log, 3 spider eyes, glowstone and a source gem block. The Worn Notebook shows how to pick which block it reveals.",
        "&eTip:&r combine it with the spectrometer and the pack's deposit depths to find rich veins faster."]),
    Q("ars_chunk", 20, -3, [item("ars_additions:ritual_chunk_loading")], "Ritual of Chunk Loading", deps=["ars_scrying"], xp=60,
      optional=True, tokens=1, subtitle="Optional: keep your base running", desc=[
        "&eWhat:&r an Ars Additions ritual that keeps its chunk loaded while it has Source.",
        "&eHow:&r craft the tablet (check JEI) and run it in a Ritual Brazier next to your Source Jars.",
        "&eTip:&r FTB Chunks can also force-load claimed chunks; use whichever you prefer."]),
    Q("ars_warp", 20, -4.5, [item("ars_nouveau:stable_warp_scroll")], "Warp Scrolls", deps=["ars_ender_jar"], xp=60, optional=True, tokens=1,
      subtitle="Optional: go home in one step", desc=[
        "&eWhat:&r a Warp Scroll remembers a spot and takes you back once; the Stable Warp Scroll can be reused.",
        "&eHow:&r Warp Scroll: blank parchment, 4 lapis and 4 source gems. Stabilize it in the Apparatus with 4 blaze powder and 2 ender pearls.",
        "&eTip:&r a Ritual of Warping (purple log + warp scroll) does the same for creatures around the brazier."]),

    # --- Essences (y=1.5 / 3) ----------------------------------------------------------------
    Q("ars_fire_essence", 10, 1.5, [item("ars_nouveau:fire_essence", 2)], "Fire Essence", deps=["ars_source_gem"], xp=40,
      subtitle="A source gem that learned to burn", desc=[
        "&eWhat:&r essences are source gems imbued with one idea. Fire essence goes into fire glyphs, threads and Ars Elemental gear.",
        "&eChemistry:&r gunpowder is about 75% saltpetre (KNO₃), 15% charcoal and 10% sulfur: the nitrate supplies the oxygen, so it burns without air.",
        "&eHow:&r Imbuement Chamber: a source gem, with flint and steel, a torch and gunpowder on nearby pedestals (2,000 Source).",
        "&eTip:&r Arcane Pedestals next to the chamber hold the extra ingredients."]),
    Q("ars_earth_water", 12, 1.5, [item("ars_nouveau:earth_essence"), item("ars_nouveau:water_essence")], "Earth and Water", deps=["ars_fire_essence"], xp=40,
      subtitle="Two more essences", desc=[
        "&eWhat:&r earth essence feeds growth rituals and earth spells; water essence makes Sanctuary, the Everfull Urn and water foci.",
        "&eChemistry:&r burned kelp was once Europe's source of soda ash (Na₂CO₃), and in 1811 the first iodine was isolated from seaweed ash.",
        "&eHow:&r earth: an iron ingot, seeds and dirt on pedestals. Water: a water bucket, a snow block and kelp. Both 2,000 Source.",
        "&eTip:&r keep a stack of source gems ready; essences go fast."]),
    Q("ars_abjuration", 14, 1.5, [item("ars_nouveau:abjuration_essence")], "Abjuration Essence", deps=["ars_earth_water"], xp=40,
      subtitle="The essence of protection", desc=[
        "&eWhat:&r abjuration essence makes Potion Jars, the Potion Melder, Potion Flasks and Restoration.",
        "&eHow:&r Imbuement Chamber: a source gem, with a fermented spider eye, sugar and a milk bucket on pedestals (2,000 Source).",
        "&eTip:&r a Source Jar plus abjuration essence makes a Potion Jar, which stores potions by the litre."]),
    Q("ars_manipulation", 16, 1.5, [item("ars_nouveau:manipulation_essence")], "Manipulation Essence", deps=["ars_abjuration"], xp=40,
      subtitle="The essence of change", desc=[
        "&eWhat:&r manipulation essence goes into the Enchanter's Wand, Spell Bow, Repairing thread, runic chalk and Containment.",
        "&eHow:&r Imbuement Chamber: a source gem, with a stone button, redstone and a clock on pedestals (2,000 Source).",
        "&eTip:&r it also converts some blocks into others, such as stone into granite or tuff (check JEI)."]),
    Q("ars_anima", 18, 1.5, [item("sauce:anima_essence")], "Anima Essence", deps=["ars_manipulation"], xp=50,
      subtitle="Ars Elemental's essence of life and death", desc=[
        "&eWhat:&r anima essence is the eighth essence, used for the Mark of Mastery and necromantic gear.",
        "&eChemistry:&r bone meal comes from bone, which is mostly hydroxyapatite, a calcium phosphate (Ca₅(PO₄)₃OH).",
        "&eHow:&r Imbuement Chamber: a source gem, with a wither skeleton skull, bone meal and a golden apple on pedestals (3,000 Source).",
        "&eTip:&r the skulls come from Nether fortresses, or Occultism's Wild Hunt."]),
    Q("ars_air_essence", 2, 4.5, [item("ars_nouveau:air_essence")], "Air Essence", deps=["ars_wings"], xp=40,
      subtitle="Bottled wind", desc=[
        "&eWhat:&r air essence makes the Jump Ring, the Belt of Levitation, air foci and several threads.",
        "&eHow:&r Imbuement Chamber: a source gem, with a feather, a Wilden Wing and arrows on pedestals (2,000 Source).",
        "&eTip:&r save a few wings for the Ritual of Flight before spending them here."]),
    Q("ars_conjuration", 0, 4.5, [item("ars_nouveau:conjuration_essence")], "Conjuration Essence", deps=["ars_air_essence"], xp=40,
      subtitle="The essence of summoning", desc=[
        "&eWhat:&r conjuration essence feeds summoning glyphs and can also make end stone or soul sand (check JEI).",
        "&eHow:&r Imbuement Chamber: a source gem, with a Wilden Horn, Starbuncle shards and a book on pedestals (2,000 Source).",
        "&eTip:&r the Mark of Mastery needs one of every essence, so make this one early."]),

    # --- Wilden and Ars Elemental (y=3 / 4.5) ------------------------------------------------
    Q("ars_wilden", 0, 3, [kill("ars_nouveau:wilden_hunter", 5)], "Wilden Hunt", deps=["m_book"], xp=75, loot="hunt",
      subtitle="Kill 5 Wilden Hunters", desc=[
        "&eWhat:&r Wilden are Ars Nouveau's wild magical beasts. Hunters charge, Stalkers fly, Guardians throw spikes.",
        "&eHow:&r they roam the Overworld at night, more often near archwood forests and Wilden dens. Bring a shield.",
        "&eTip:&r keep every horn, spike and wing they drop. Rituals need them."]),
    Q("ars_wings", 2, 3, [item("ars_nouveau:wilden_wing", 3)], "Wilden Wings", deps=["ars_wilden"], xp=50,
      subtitle="The key ingredient for flight", desc=[
        "&eWhat:&r Wilden Wings drop from Wilden Stalkers, the flying ones.",
        "&eHow:&r hunt Stalkers at night. The Ritual of Flight tablet needs three wings (purple archwood log, 3 wings, 2 diamonds, an ender pearl).",
        "&eTip:&r a Ritual of Wilden Summoning will need three more Wilden drops, so keep hunting."]),
    Q("ars_chimera", 4, 3, [kill("ars_nouveau:wilden_boss")], "The Wilden Chimera", deps=["ars_conjuration", "m_brazier"], xp=300,
      loot="boss", size=1.5, shape="hexagon", subtitle="Summon and slay Ars Nouveau's boss", desc=[
        "&6You remember beasts that were many beasts at once. You remember winning.&r",
        "&eWhat:&r the Wilden Chimera combines all three Wilden. It drops Wilden Tribute, used for the Archmage book and Ars Elemental's Mark of Mastery.",
        "&eHow:&r craft the Ritual of Wilden Summoning (purple archwood log, 3 Wilden drops, a lapis block), place it in a brazier away from your base, and fight.",
        "&eTip:&r it has phases and calls spikes from the ground. Keep moving and bring healing."]),
    Q("ars_mastery", 6, 3, [item("ars_elemental:mark_of_mastery")], "Mark of Mastery", deps=["ars_chimera", "ars_anima"], xp=100,
      subtitle="Ars Elemental's upgrade token", desc=[
        "&eWhat:&r the Mark of Mastery upgrades elemental foci and turns Arcanist armor into elemental mage armor.",
        "&eHow:&r imbue a Wilden Tribute with all seven essences plus anima essence on the pedestals (check JEI). One tribute gives five marks.",
        "&eTip:&r five marks is a focus plus most of an armor set; plan before you spend them."]),
    Q("ars_focus", 6, 4.5, [anyof(["ars_elemental:lesser_fire_focus", "ars_elemental:lesser_water_focus",
                                   "ars_elemental:lesser_earth_focus", "ars_elemental:lesser_air_focus"])],
      "Lesser Elemental Focus", deps=["ars_anima"], any_dep=True, xp=75,
      subtitle="Pick an element and specialise", desc=[
        "&eWhat:&r an Ars Elemental focus is a curio that strengthens one school of spells (fire, water, earth or air) and lowers its cost.",
        "&eChemistry:&r the four classical elements were the first attempt at a periodic table. You know there are 118, but the spells don't.",
        "&eHow:&r in the Imbuement Chamber: an amethyst shard with 3 matching essences and 3 gold ingots on pedestals (5,000 Source).",
        "&eTip:&r choose the school your favourite spell uses most."]),
    Q("ars_focus_full", 8, 4.5, [anyof(["ars_elemental:fire_focus", "ars_elemental:water_focus",
                                        "ars_elemental:earth_focus", "ars_elemental:air_focus"])],
      "Greater Elemental Focus", deps=["ars_focus", "ars_mastery"], xp=150, subtitle="Master an element", optional=True, tokens=1, desc=[
        "&eWhat:&r the full focus gives a much bigger bonus to its school and protects you from matching hazards.",
        "&eHow:&r put the lesser focus in the Enchanting Apparatus with a Mark of Mastery on a pedestal (5,000 Source).",
        "&eTip:&r a fire focus pairs well with Ignite and Flare; a water focus with Watery Grave."]),
    Q("ars_elem_armor", 10, 3, [anyof(["ars_elemental:fire_hat", "ars_elemental:aqua_hat", "ars_elemental:earth_hat", "ars_elemental:air_hat",
                                       "ars_elemental:fire_robes", "ars_elemental:aqua_robes", "ars_elemental:earth_robes", "ars_elemental:air_robes"])],
      "Elemental Mage Armor", deps=["ars_mastery"], xp=200, optional=True, tokens=2,
      subtitle="Optional: armor of a single element", desc=[
        "&eWhat:&r Ars Elemental turns Arcanist armor into fire, water, earth or air armor, each with resistances and a spell bonus.",
        "&eHow:&r in the Enchanting Apparatus: an Arcanist piece plus a Mark of Mastery, a netherite ingot and two matching essences (7,000 Source).",
        "&eTip:&r a full set matching your focus makes that school very cheap to cast."]),
    Q("ars_urn", 8, 6, [item("ars_elemental:everfull_urn")], "Everfull Urn", deps=["ars_earth_water"], xp=40, optional=True, tokens=1,
      subtitle="Optional: water from nowhere", desc=[
        "&eWhat:&r the Everfull Urn pushes water into adjacent tanks and machines for free.",
        "&eChemistry:&r water is the feedstock for half your chemistry: electrolysis splits 2H₂O → 2H₂ + O₂.",
        "&eHow:&r a flower pot in the Apparatus with a source gem, 2 water essences and 2 prismarine shards.",
        "&eTip:&r one next to an electrolyzer saves a pump."]),
    Q("ars_caster_bag", 10, 6, [item("ars_elemental:caster_bag")], "Caster's Bag", deps=["ars_manipulation"], xp=40, optional=True, tokens=1,
      subtitle="Optional: a bag for books and charms", desc=[
        "&eWhat:&r the Curio Bag holds trinkets and charms; the Caster's Bag is its upgrade that also takes spell books and caster tomes.",
        "&eHow:&r Curio Bag: a chest in magebloom fiber. Then the Apparatus with 2 manipulation essences, 2 blaze powder and 2 gold blocks.",
        "&eTip:&r it frees hotbar slots for tools."]),

    # --- Magebloom, armor and trinkets (y=3 .. 7.5) ------------------------------------------
    Q("ars_magebloom", 16, 3, [item("ars_nouveau:magebloom", 8)], "Magebloom", deps=["m_apparatus"], xp=40,
      subtitle="The magic fiber crop", desc=[
        "&eWhat:&r magebloom is a flower crop; each one gives 4 magebloom fiber for robes, threads, the Alteration Table and runic chalk.",
        "&eHow:&r Magebloom seeds come from the Apparatus (any seeds with 4 source gems). Plant them like wheat.",
        "&eTip:&r a small magebloom field early saves a lot of waiting later."]),
    Q("ars_armor", 14, 3, [anyof(["ars_nouveau:sorcerer_robes", "ars_nouveau:arcanist_robes", "ars_nouveau:battlemage_robes"])],
      "Mage Armor", deps=["ars_magebloom"], xp=75, subtitle="Armor that stores mana", desc=[
        "&eWhat:&r Ars Nouveau armor comes in three styles (Sorcerer, Arcanist, Battlemage). Each piece adds mana and mana regeneration.",
        "&eHow:&r made in the Enchanting Apparatus around a golden armor piece with 4 magebloom fiber (check JEI for each style).",
        "&eTip:&r grow magebloom early; every piece needs fiber."]),
    Q("ars_armor_up", 12, 3, [tick()], "Armor Tiers", deps=["ars_armor"], xp=75,
      subtitle="Upgrade mage armor in the Apparatus", optional=True, tokens=1, desc=[
        "&eWhat:&r mage armor has three tiers. Each tier raises mana and opens more thread slots.",
        "&eHow:&r put the armor in the Apparatus: tier 2 needs 2 blaze rods (2,500 Source), tier 3 needs 2 ender pearls and a chorus fruit (5,000 Source).",
        "&eTip:&r click the checkmark once you've upgraded a piece."]),
    Q("ars_alteration", 14, 4.5, [item("ars_nouveau:alteration_table"), item("ars_nouveau:blank_thread", 2)], "Alteration Table", deps=["ars_armor"], xp=50,
      subtitle="Sew threads into your robes", desc=[
        "&eWhat:&r the Alteration Table holds a piece of mage armor and lets you put threads (perks) into its slots.",
        "&eHow:&r the table is a Scribe's Table with magebloom fiber; blank threads are magebloom fiber and gold nuggets.",
        "&eTip:&r right-click the table with armor, then with threads."]),
    Q("ars_threads", 12, 4.5, [anyof(["ars_nouveau:thread_spellpower", "ars_nouveau:thread_magic_capacity", "ars_nouveau:thread_repairing",
                                      "ars_nouveau:thread_warding", "ars_nouveau:thread_feather", "ars_nouveau:thread_high_step"])],
      "Threads", deps=["ars_alteration"], xp=50, optional=True, tokens=1, subtitle="Optional: perks for your armor", desc=[
        "&eWhat:&r threads add perks: Spellpower, Magic Capacity, Repairing, Warding, Feather Falling, Step Height and more.",
        "&eHow:&r a blank thread in the Apparatus with the thread's ingredients (Repairing: an anvil and 2 manipulation essences; check JEI for the rest).",
        "&eTip:&r Spellpower takes one of every essence; it's worth it for a main spell set."]),
    Q("ars_amulet", 16, 4.5, [anyof(["ars_nouveau:amulet_of_mana_boost", "ars_nouveau:amulet_of_mana_regen"])], "Mana Amulet",
      deps=["m_apparatus"], xp=40, optional=True, tokens=1, subtitle="Optional: more mana around your neck", desc=[
        "&eWhat:&r amulets are curios that raise your maximum mana or how fast it comes back.",
        "&eHow:&r a Dull Trinket (iron nuggets and a source gem) in the Apparatus with diamonds and source gems (Regen also wants gold).",
        "&eTip:&r Regen suits short, frequent spells; Boost suits big ones."]),
    Q("ars_discount", 16, 6, [item("ars_nouveau:ring_of_lesser_discount")], "Ring of Discount", deps=["ars_amulet"], xp=40, optional=True, tokens=1,
      subtitle="Optional: cheaper spells", desc=[
        "&eWhat:&r discount rings cut the mana cost of every spell you cast.",
        "&eHow:&r a Ring of Potential (iron nuggets and a source gem) in the Apparatus with 4 diamonds, 2 ender pearls and 2 source gems. The Greater ring swaps the pearls for blaze rods.",
        "&eTip:&r you have two ring slots; two rings stack."]),
    Q("ars_enchanter_gear", 14, 6, [anyof(["ars_nouveau:enchanters_sword", "ars_nouveau:spell_bow", "ars_nouveau:enchanters_shield"])],
      "Enchanter's Arms", deps=["ars_manipulation"], xp=60, optional=True, tokens=1,
      subtitle="Optional: weapons that cast spells", desc=[
        "&eWhat:&r the Enchanter's Sword casts a spell on hit, the Spell Bow puts spells on arrows, and the Enchanter's Shield is a mana-powered shield.",
        "&eHow:&r the vanilla item in the Apparatus with source gem blocks and gold blocks (the bow also takes manipulation essence, the sword a diamond).",
        "&eTip:&r give them a spell at the Scribe's Table, like a spell book."]),

    # --- Helpers (y=6 .. 9) -------------------------------------------------------------------
    Q("m_starbuncle", 18, 4.5, [item("ars_nouveau:starbuncle_charm")], "Starbuncle", deps=["m_apparatus"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a tiny helper that moves items", desc=[
        "&eWhat:&r a Starbuncle carries items from one chest to another. Cute logistics.",
        "&eHow:&r befriend a wild Starbuncle for its shards (the Worn Notebook explains how), then put the shards in the Apparatus with 4 gold ingots.",
        "&eTip:&r use a Dominion Wand to set where it picks up and where it drops off."]),
    Q("ars_shades", 18, 6, [item("ars_nouveau:starbuncle_shades")], "Too Cool for Logistics", deps=["m_starbuncle"], xp=50,
      secret=True, loot="secret", subtitle="Secret: sunglasses for a Starbuncle", desc=[
        "&6You remember having servants who took themselves very seriously. This one does not.&r",
        "&eWhat:&r Starbuncle Shades: tinted glass and a source gem. Give them to a Starbuncle.",
        "&eTip:&r they do nothing useful. That is the point."]),
    Q("ars_wixie", 20, 4.5, [item("ars_nouveau:wixie_charm")], "Wixie", deps=["m_starbuncle"], xp=60, optional=True, tokens=1,
      subtitle="Optional: a helper that crafts and brews", desc=[
        "&eWhat:&r a Wixie works a cauldron: it repeats a crafting recipe or brews potions from nearby chests.",
        "&eHow:&r cast a Dispel spell on a witch at half health or less for Wixie Shards, then the Apparatus with a sapling, an emerald, a crafting table and a brewing stand.",
        "&eTip:&r pair a brewing Wixie with a Potion Jar to keep your favourite potion stocked."]),
    Q("ars_drygmy", 20, 6, [item("ars_nouveau:drygmy_charm")], "Drygmy", deps=["ars_wixie"], xp=60, optional=True, tokens=1,
      subtitle="Optional: mob drops without killing", desc=[
        "&eWhat:&r a Drygmy at its henge collects drops from nearby mobs without hurting them.",
        "&eHow:&r Drygmy shards (the Worn Notebook explains how to befriend one) in the Apparatus with fish, wheat, an apple, a carrot, seeds and 3 source gems.",
        "&eTip:&r the Worn Notebook shows the henge layout and what the Drygmy needs nearby."]),
    Q("ars_whirlisprig", 20, 7.5, [item("ars_nouveau:whirlisprig_charm")], "Whirlisprig", deps=["ars_drygmy"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a garden spirit", desc=[
        "&eWhat:&r a Whirlisprig speeds up plant growth around it and makes Source from a varied garden.",
        "&eHow:&r Whirlisprig shards in the Apparatus with a source gem, magebloom (seed and flower), a diamond, three saplings and wheat seeds.",
        "&eTip:&r the more different plants nearby, the happier it is."]),

    Q("ars_flight_note", 20, 1.5, [tick()], "Two Roads to the Sky", deps=["m_ritual"], xp=50, optional=True, tokens=1,
      subtitle="Optional: how Ars flight fits the pack", desc=[
        "&eWhat:&r a note on the Ritual of Flight and the pack's other flight sources.",
        "&eHow:&r read the second page, then click the checkmark.",
        "{@pagebreak}",
        "&eRitual of Flight:&r the tablet is a purple archwood log, 3 Wilden Wings, 2 diamonds, an ender pearl and 2 hydrogen. The hydrogen is this pack's addition: no chemistry, no wings.",
        "&eRange:&r the ritual only grants flight near its brazier and drains Source while you fly. It's base flight, not world flight.",
        "&eNot flight:&r the Belt of Levitation, the Jump Ring and the Glide glyph help you move, but none of them is true flight.",
        "&eElsewhere:&r the Infusion Pylon with a Potion of Flying (hydrogen from the Dissolver), Iron Jetpacks (MI circuits) and the Angel Ring (digital circuit) all work anywhere. See Tools and Comfort."]),

    # --- ATM10-aligned additions (2026-10-19): tools, jars, rituals, sets -------------------------
    Q("ars_dowsing", 0, 0, [item("ars_nouveau:dowsing_rod")], "Dowsing Rod", deps=["ars_archwood"], xp=30,
      optional=True, tokens=1, subtitle="Optional: find geodes and magical creatures", desc=[
        "&eWhat:&r a short burst of Scrying for budding amethyst, and magical creatures within 75 blocks start to glow. It has limited uses.",
        "&eChemistry:&r a geode is a hollow rock where silica-rich water slowly deposited SiO₂ crystals inward, layer by layer.",
        "&eHow:&r a gold ingot above two archwood planks.",
        "&eTip:&r a budding amethyst near home means endless source gems."]),
    Q("ars_dominion", 0, 0, [item("ars_nouveau:dominion_wand")], "Dominion Wand", deps=["m_apparatus"], xp=40,
      optional=True, tokens=1, subtitle="Optional: tell things where to go", desc=[
        "&eWhat:&r the Dominion Wand links blocks and creatures: relays to jars, Starbuncles to chests, golems and Weald Walkers to their homes.",
        "&eHow:&r a stick in the Enchanting Apparatus with 2 source gems and a gold ingot on the pedestals.",
        "&eTip:&r click the first thing, then the second. Sneak-click shows what is already linked."]),
    Q("ars_casters", 0, 0, [anyof(["ars_nouveau:wand", "ars_nouveau:enchanters_mirror"])], "Wand or Mirror", deps=["ars_manipulation", "ars_air_essence"],
      xp=60, optional=True, tokens=1, subtitle="Optional: one spell, cast cheaply", desc=[
        "&eWhat:&r the Enchanter's Wand fires one spell as Projectile + Accelerate; the Enchanter's Mirror casts one self spell on you, cheaper and longer.",
        "&eHow:&r wand: an archwood log in the Apparatus with 4 source gems, 2 gold, air and manipulation essence. Mirror: a source gem block with glass, archwood logs, gold and 2 manipulation essence.",
        "&eTip:&r inscribe them at the Scribe's Table with a spell that has no form of its own (e.g. just Break, or Heal + Amplify)."]),
    Q("ars_jars", 0, 0, [anyof(["ars_nouveau:jar_of_light", "ars_nouveau:void_jar", "ars_nouveau:potion_jar"])], "Useful Jars", deps=["ars_abjuration"],
      xp=40, optional=True, tokens=1, subtitle="Optional: light, a trash can or a potion tank", desc=[
        "&eWhat:&r the Jar of Light summons a light that follows you; the Jar of Voiding deletes chosen items on pickup for a little mana; the Potion Jar stores 100 potions.",
        "&eChemistry:&r glowstone light is fiction, but real 'cold light' exists: in a glow stick, a peroxide reaction excites a dye that emits photons instead of heat.",
        "&eHow:&r Potion Jar: a Source Jar and abjuration essence (shapeless). The other two are a glass bottle in the Apparatus (check JEI).",
        "&eTip:&r a Void Jar set to cobblestone and dirt keeps your inventory clean while mining."]),
    Q("ars_belts", 0, 0, [anyof(["ars_nouveau:belt_of_levitation", "ars_nouveau:belt_of_unstable_gifts"])], "Magic Belts", deps=["ars_air_essence", "m_apparatus"],
      xp=40, optional=True, tokens=1, subtitle="Optional: levitate, or gamble on potions", desc=[
        "&eWhat:&r the Belt of Levitation lets you rise by sneaking in mid-air (climbing, not flight). The Belt of Unstable Gifts hands out random good potion effects.",
        "&eHow:&r a Mundane Belt in the Apparatus. Levitation: 4 gold, 3 feathers and air essence. Unstable Gifts: brewing ingredients and a brewing stand.",
        "&eTip:&r levitation also softens falls a little; it doesn't replace real flight."]),
    Q("ars_greater_discount", 0, 0, [item("ars_nouveau:ring_of_greater_discount")], "Greater Discount", deps=["ars_discount"], xp=60,
      optional=True, tokens=1, subtitle="Optional: the better ring", desc=[
        "&eWhat:&r a slightly bigger discount on every spell than the lesser ring.",
        "&eHow:&r the Ring of Lesser Discount in the Apparatus with 4 diamonds, 2 blaze rods and 2 source gems.",
        "&eTip:&r wear it with a lesser ring in the second slot until you can afford two."]),
    Q("ars_saplings", 0, 0, [item("ars_nouveau:red_archwood_sapling"), item("ars_nouveau:blue_archwood_sapling"),
                             item("ars_nouveau:green_archwood_sapling"), item("ars_nouveau:purple_archwood_sapling")],
      "Four Archwoods", deps=["ars_archwood"], xp=50, optional=True, tokens=1, subtitle="Optional: one sapling of every colour", desc=[
        "&eWhat:&r Blazing (red), Cascading (blue), Flourishing (green) and Vexing (purple) archwood. Each colour feeds different rituals.",
        "&eHow:&r break archwood leaves in the four kinds of archwood forest. Plant a few of each at home.",
        "&eTip:&r the Ritual of Awakening needs all four saplings at once."]),
    Q("ars_awakening", 0, 0, [item("ars_nouveau:ritual_awakening")], "Ritual of Awakening", deps=["ars_saplings", "m_brazier"], xp=60,
      optional=True, tokens=1, subtitle="Optional: wake the trees", desc=[
        "&6You remember forests that stood up when you called. Some of them still do.&r",
        "&eWhat:&r awakens nearby archwood trees into Weald Walkers that guard an area, and budding amethyst into an Amethyst Golem charm.",
        "&eHow:&r a green archwood log, one sapling of each colour and 4 source gems (shapeless). Run it next to the tree base or the budding amethyst.",
        "&eTip:&r add Book and Quills to the ritual and it makes Bookwyrm charms instead."]),
    Q("ars_golem", 0, 0, [item("ars_nouveau:amethyst_golem_charm")], "Amethyst Golem", deps=["ars_awakening"], xp=60,
      optional=True, tokens=1, subtitle="Optional: a geode that tends itself", desc=[
        "&eWhat:&r the Amethyst Golem grows and harvests amethyst near its home, turns amethyst blocks into budding amethyst and stores the shards.",
        "&eChemistry:&r amethyst is quartz, SiO₂, coloured purple by Fe³⁺ ions that natural radiation has changed in the crystal.",
        "&eHow:&r run the Ritual of Awakening near budding amethyst. Place the charm, then give the golem a home with the Dominion Wand (a chest makes it store shards).",
        "&eTip:&r golem shards in an Imbuement Chamber are a hands-free source gem line."]),
    Q("ars_rituals_more", 0, 0, [anyof(["ars_nouveau:ritual_burrowing", "ars_nouveau:ritual_disintegration", "ars_nouveau:ritual_restoration",
                                        "ars_nouveau:ritual_warping", "ars_nouveau:ritual_challenge", "ars_nouveau:ritual_wilden_summon"])],
      "Working Rituals", deps=["m_brazier"], xp=50, optional=True, tokens=1, subtitle="Optional: dig, heal, warp or fight", desc=[
        "&eWhat:&r Burrowing digs four holes to bedrock; Disintegration turns monsters into double experience; Restoration heals and cures zombie villagers; Warping moves everyone to a warp scroll; Challenge starts a raid; Wilden Summoning calls the Chimera.",
        "&eHow:&r each tablet is an archwood log plus a few items (Burrowing: green log, iron pickaxe, coal block; Restoration: green log, golden apple, abjuration essence). JEI has them all.",
        "&eTip:&r Burrowing drops ore as raw ore: it saves digging, not processing."]),
    Q("ars_containment", 0, 0, [item("ars_nouveau:mob_jar"), item("ars_nouveau:ritual_containment")], "Containment", deps=["ars_manipulation", "m_brazier"],
      xp=50, optional=True, tokens=1, subtitle="Optional: a mob in a jar", desc=[
        "&eWhat:&r Containment Jars hold a living mob. Chickens still lay, cows can be milked, sheep sheared, and a jarred blaze lights the room.",
        "&eHow:&r the jar is glass and archwood slabs. The Ritual of Containment (purple log, manipulation essence, 3 glass bottles) puts a mob within 3 blocks into a nearby jar.",
        "&eTip:&r a Drygmy counts jarred mobs as if they were roaming free."]),
    Q("ars_source_spawner", 0, 0, [item("ars_additions:source_spawner")], "Source Spawner", deps=["ars_containment", "ars_drygmy"], xp=75,
      optional=True, tokens=1, subtitle="Optional: a spawner that runs on Source", desc=[
        "&eWhat:&r an Ars Additions spawner that reads nearby Containment Jars to decide what to spawn and pays Source for each mob. A redstone signal turns it off.",
        "&eHow:&r a Drygmy charm in the Apparatus with a summon focus and conjuration essence.",
        "&eTip:&r it spawns mobs without their guaranteed drops, so it's for farms of normal drops, not boss loot."]),
    Q("ars_fiber", 0, 0, [item("ars_nouveau:magebloom_fiber", 16), item("ars_nouveau:magebloom_crop", 4)], "Magebloom Fiber", deps=["ars_magebloom"], xp=30,
      optional=True, tokens=1, subtitle="Optional: spin the magic crop", desc=[
        "&eWhat:&r magebloom fiber is the cloth of Ars Nouveau: robes, threads, the Alteration Table, runic chalk and mirrorweave.",
        "&eChemistry:&r real fibres like cotton are cellulose: long chains of glucose (C₆H₁₀O₅)ₙ held together by hydrogen bonds.",
        "&eHow:&r each magebloom flower crafts into fiber. Keep 4 seeds back so the field keeps growing (seeds are any seeds with 4 source gems in the Apparatus).",
        "&eTip:&r a Harvest ritual or a Whirlisprig keeps the field going without you."]),
    Q("ars_chalk_weave", 0, 0, [anyof(["ars_nouveau:runic_chalk", "ars_nouveau:mirrorweave"])], "Runes and Illusions", deps=["ars_fiber", "ars_manipulation"],
      xp=40, optional=True, tokens=1, subtitle="Optional: traps and fake walls", desc=[
        "&eWhat:&r Runic Chalk draws permanent runes that cast a spell on whatever walks over them. Mirrorweave copies the look of any block you use on it.",
        "&eHow:&r runic chalk: manipulation essence, bone meal and magebloom fiber. Mirrorweave: 8 magebloom blocks around conjuration essence (makes 8).",
        "&eTip:&r a mirrorweave wall hides a secret door; Sense Magic reveals it."]),
    Q("ars_mage_set", 0, 0, [anyof(["ars_nouveau:sorcerer_hood", "ars_nouveau:arcanist_hood", "ars_nouveau:battlemage_hood"]),
                             anyof(["ars_nouveau:sorcerer_robes", "ars_nouveau:arcanist_robes", "ars_nouveau:battlemage_robes"]),
                             anyof(["ars_nouveau:sorcerer_leggings", "ars_nouveau:arcanist_leggings", "ars_nouveau:battlemage_leggings"]),
                             anyof(["ars_nouveau:sorcerer_boots", "ars_nouveau:arcanist_boots", "ars_nouveau:battlemage_boots"])],
      "A Full Mage Set", deps=["ars_armor"], xp=100, optional=True, tokens=1, subtitle="Optional: hat, robes, leggings and boots", desc=[
        "&eWhat:&r four pieces of mage armor, any style mixed: every piece adds mana and regeneration, and each one is a thread slot.",
        "&eHow:&r each piece is the matching golden armor piece in the Apparatus with magebloom fiber (check JEI per style).",
        "&eTip:&r Arcanist pieces are needed later for Ars Elemental's elemental armor."]),
    Q("ars_elem_set", 0, 0, [anyof(["ars_elemental:fire_hat", "ars_elemental:aqua_hat", "ars_elemental:earth_hat", "ars_elemental:air_hat"]),
                             anyof(["ars_elemental:fire_robes", "ars_elemental:aqua_robes", "ars_elemental:earth_robes", "ars_elemental:air_robes"]),
                             anyof(["ars_elemental:fire_leggings", "ars_elemental:aqua_leggings", "ars_elemental:earth_leggings", "ars_elemental:air_leggings"]),
                             anyof(["ars_elemental:fire_boots", "ars_elemental:aqua_boots", "ars_elemental:earth_boots", "ars_elemental:air_boots"])],
      "A Full Elemental Set", deps=["ars_elem_armor"], xp=250, optional=True, tokens=2, subtitle="Optional: four pieces of elemental armor", desc=[
        "&6You remember wearing a single element like a cloak. Now you wear it like a lab coat.&r",
        "&eWhat:&r all four slots in Ars Elemental armor. Matching pieces stack their school bonus and resistances.",
        "&eHow:&r each Arcanist piece in the Apparatus with a Mark of Mastery, a netherite ingot and two matching essences.",
        "&eTip:&r that's four marks and four netherite: plan it with your Wilden Tribute."]),
], links=[("t2_ars", -2, 0), ("t2_pylon", 18, 1.5)])
