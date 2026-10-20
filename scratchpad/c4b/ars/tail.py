
    # --- Our own side sections: Source logistics, Ars Additions, essences, Wilden, Ars Elemental, armor ----------
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
    Q("ars_storage", 12, -3, [item("ars_nouveau:storage_lectern"), item("ars_nouveau:repository", 2)], "Storage Lectern", deps=["m_apparatus"], xp=50, section="Storage and Additions",
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
    Q("ars_familiar", 16, -3, [anyof(["ars_nouveau:familiar_starbuncle", "ars_nouveau:familiar_wixie", "ars_nouveau:familiar_drygmy",
                                      "ars_nouveau:familiar_whirlisprig", "ars_nouveau:familiar_bookwyrm", "ars_nouveau:familiar_amethyst_golem",
                                      "ars_elemental:firenando_familiar", "ars_elemental:flashjack_familiar", "ars_elemental:siren_familiar"])],
      "A Familiar", deps=["ars_ritual_binding"], xp=75, optional=True, tokens=1,
      subtitle="Optional: a small spirit that follows you", desc=[
        "&eWhat:&r a familiar is a bound creature that rides along and gives a passive bonus: Starbuncles speed you up, Wixies boost potions, Bookwyrms cut spell costs.",
        "&eHow:&r run the Ritual of Binding with the creature's charm nearby to turn it into a familiar item. Use the item to call your familiar.",
        "&eTip:&r Ars Elemental adds elemental familiars (Firenando, Flashjack, Siren) that boost that school of magic."]),
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
    Q("ars_fire_essence", 10, 1.5, [item("ars_nouveau:fire_essence", 2)], "Fire Essence", deps=["ars_source_gem"], xp=40, section="Essences",
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
    Q("ars_wilden", 0, 3, [kill("ars_nouveau:wilden_hunter", 5)], "Wilden Hunt", deps=["m_book"], xp=75, loot="hunt", section="The Wilden",
      subtitle="Kill 5 Wilden Hunters", desc=[
        "&eWhat:&r Wilden are Ars Nouveau's wild magical beasts. Hunters charge, Stalkers fly, Guardians throw spikes.",
        "&eHow:&r they roam the Overworld at night, more often near archwood forests and Wilden dens. Bring a shield.",
        "&eTip:&r keep every horn, spike and wing they drop. Rituals need them."]),
    Q("ars_wings", 2, 3, [item("ars_nouveau:wilden_wing", 3)], "Wilden Wings", deps=["ars_wilden"], xp=50,
      subtitle="The key ingredient for flight", desc=[
        "&eWhat:&r Wilden Wings drop from Wilden Stalkers, the flying ones.",
        "&eHow:&r hunt Stalkers at night. The Ritual of Flight tablet needs three wings (purple archwood log, 3 wings, 2 diamonds, an ender pearl).",
        "&eTip:&r a Ritual of Wilden Summoning will need three more Wilden drops, so keep hunting."]),
    Q("ars_chimera", 4, 3, [kill("ars_nouveau:wilden_boss")], "The Wilden Chimera", deps=["ars_conjuration", "ars_wilden_ritual"], xp=300,
      loot="boss", size=1.5, shape="hexagon", subtitle="Summon and slay Ars Nouveau's boss", desc=[
        "&6You remember beasts that were many beasts at once. You remember winning.&r",
        "&eWhat:&r the Wilden Chimera combines all three Wilden. It drops Wilden Tribute, used for the Archmage book and Ars Elemental's Mark of Mastery.",
        "&eHow:&r run the Ritual of Wilden Summoning (quest above) in a brazier away from your base, and fight.",
        "&eTip:&r it has phases and calls spikes from the ground. Keep moving and bring healing."]),
    Q("ars_mastery", 6, 3, [item("ars_elemental:mark_of_mastery")], "Mark of Mastery", deps=["ars_chimera", "ars_anima"], xp=100, section="Ars Elemental",
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

    Q("ars_armor", 14, 3, [anyof(["ars_nouveau:sorcerer_robes", "ars_nouveau:arcanist_robes", "ars_nouveau:battlemage_robes"])],
      "Mage Armor", deps=["ars_fiber"], xp=75, section="Mage Armor", subtitle="Armor that stores mana", desc=[
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

    Q("ars_flight_note", 20, 1.5, [tick()], "Two Roads to the Sky", deps=["m_ritual"], xp=50, optional=True, tokens=1,
      subtitle="Optional: how Ars flight fits the pack", desc=[
        "&eWhat:&r a note on the Ritual of Flight and the pack's other flight sources.",
        "&eHow:&r read the second page, then click the checkmark.",
        "{@pagebreak}",
        "&eRitual of Flight:&r the tablet is a purple archwood log, 3 Wilden Wings, 2 diamonds, an ender pearl and 2 hydrogen. The hydrogen is this pack's addition: no chemistry, no wings.",
        "&eRange:&r the ritual only grants flight near its brazier and drains Source while you fly. It's base flight, not world flight.",
        "&eNot flight:&r the Belt of Levitation, the Jump Ring and the Glide glyph help you move, but none of them is true flight.",
        "&eElsewhere:&r the Infusion Pylon with a Potion of Flying (hydrogen from the Dissolver), Iron Jetpacks (MI circuits) and the Angel Ring (digital circuit) all work anywhere. See Tools and Comfort."]),
    Q("ars_saplings", 0, 0, [item("ars_nouveau:red_archwood_sapling"), item("ars_nouveau:blue_archwood_sapling"),
                             item("ars_nouveau:green_archwood_sapling"), item("ars_nouveau:purple_archwood_sapling")],
      "Four Archwoods", deps=["ars_archwood"], xp=50, optional=True, tokens=1, subtitle="Optional: one sapling of every colour", desc=[
        "&eWhat:&r Blazing (red), Cascading (blue), Flourishing (green) and Vexing (purple) archwood. Each colour feeds different rituals.",
        "&eHow:&r break archwood leaves in the four kinds of archwood forest. Plant a few of each at home.",
        "&eTip:&r the Ritual of Awakening needs all four saplings at once."]),
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
    Q("ars_greater_discount", 0, 0, [tick()], "Two Ring Slots", deps=["ars_discount"], xp=30,
      optional=True, tokens=1, icon="ars_nouveau:ring_of_greater_discount", subtitle="Optional: how the discounts stack", desc=[
        "&eWhat:&r you can wear two rings at once, and their discounts add up.",
        "&eHow:&r wear a Greater and a Lesser ring together, or two Greater rings once you can afford them. Click the checkmark when both slots are full.",
        "&eTip:&r the rings quest above asks for one of each; this is the reminder to wear both."]),
