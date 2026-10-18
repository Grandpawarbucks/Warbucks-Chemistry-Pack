"""Quest chapter: ars. See tools/quests/STYLE.md. Build: python3 tools/build_quests.py"""
from questlib import Q, Chapter, item, dim, tick, kill, anyof, SIDE  # noqa: F401

CHAPTER = Chapter("ars", "Ars Nouveau", "ars_nouveau:novice_spell_book",
        ["Spellcraft, Source, rituals and the Wilden: magic that runs on stored energy."], SIDE, [
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

    # --- More Source (y=-1.5 / -3) ------------------------------------------------------------
    Q("ars_sourcelinks", 7, -1.5, [anyof(["ars_nouveau:agronomic_sourcelink", "ars_nouveau:mycelial_sourcelink",
                                         "ars_nouveau:vitalic_sourcelink", "ars_nouveau:alchemical_sourcelink"])],
      "Other Sourcelinks", deps=["m_sourcelink"], xp=50, optional=True, tokens=1,
      subtitle="Optional: Source from crops, food, mobs or potions", desc=[
        "&eWhat:&r every sourcelink feeds on a different kind of energy. Agronomic eats crop growth, Mycelial eats food, Vitalic eats mob deaths, Alchemical eats potions.",
        "&eChemistry:&r all of them are the same idea in a costume: stored chemical energy (sugars, fats, potions) released and captured.",
        "&eHow:&r craft any one of them (check JEI) and place it near your Source Jars.",
        "&eTip:&r an Agronomic Sourcelink next to a crop farm is free Source forever."]),
    Q("ars_charm", 9, -3, [anyof(["ars_additions:undying_charm", "ars_additions:fall_prevention_charm",
                                  "ars_additions:fire_resistance_charm", "ars_additions:night_vision_charm",
                                  "ars_additions:water_breathing_charm", "ars_additions:void_protection_charm"])],
      "Ars Additions Charms", deps=["m_apparatus"], xp=60, optional=True, tokens=1,
      subtitle="Optional: one-shot protections in a bottle", desc=[
        "&eWhat:&r Ars Additions charms save you once from a specific danger: falling, fire, drowning, the void, or death itself.",
        "&eHow:&r made in the Enchanting Apparatus around a glass bottle (the Undying Charm takes a Totem of Undying, crying obsidian and glowstone). Recharge them in the Imbuement Chamber.",
        "&eTip:&r a Void Protection Charm is cheap insurance before your first trip to the End."]),
    Q("ars_haversack", 11, -3, [item("ars_additions:handy_haversack")], "Handy Haversack", deps=["m_apparatus"], xp=50,
      optional=True, tokens=1, subtitle="Optional: a bag bound to a chest", desc=[
        "&eWhat:&r the Handy Haversack links to a container so items you pick up go straight there.",
        "&eHow:&r craft it (check JEI), then bind it to a chest or your storage as its tooltip says.",
        "&eTip:&r bind it to your AE2 or Occultism storage interface for a bottomless pocket."]),
    Q("ars_familiar", 13, -3, [anyof(["ars_nouveau:familiar_starbuncle", "ars_nouveau:familiar_wixie", "ars_nouveau:familiar_drygmy",
                                      "ars_nouveau:familiar_whirlisprig", "ars_nouveau:familiar_bookwyrm", "ars_nouveau:familiar_amethyst_golem",
                                      "ars_elemental:firenando_familiar", "ars_elemental:flashjack_familiar", "ars_elemental:siren_familiar"])],
      "A Familiar", deps=["m_brazier"], xp=75, optional=True, tokens=1,
      subtitle="Optional: a small spirit that follows you", desc=[
        "&eWhat:&r a familiar is a bound creature that rides along and gives a passive bonus: Starbuncles speed you up, Wixies boost potions, Bookwyrms cut spell costs.",
        "&eHow:&r run the Ritual of Binding with the creature's charm nearby to turn it into a familiar item (the Worn Notebook has the details). Use the item to call your familiar.",
        "&eTip:&r Ars Elemental adds elemental familiars (Firenando, Flashjack, Siren) that boost that school of magic."]),
    Q("ars_chunk", 13, -1.5, [item("ars_additions:ritual_chunk_loading")], "Ritual of Chunk Loading", deps=["m_brazier"], xp=60,
      optional=True, tokens=1, subtitle="Optional: keep your base running", desc=[
        "&eWhat:&r an Ars Additions ritual that keeps its chunk loaded while it has Source.",
        "&eHow:&r craft the tablet (check JEI) and run it in a Ritual Brazier next to your Source Jars.",
        "&eTip:&r FTB Chunks can also force-load claimed chunks; use whichever you prefer."]),
    Q("ars_shades", 5, -3, [item("ars_nouveau:starbuncle_shades")], "Too Cool for Logistics", deps=["m_starbuncle"], xp=50,
      secret=True, loot="secret", subtitle="Secret: sunglasses for a Starbuncle", desc=[
        "&6You remember having servants who took themselves very seriously. This one does not.&r",
        "&eWhat:&r Starbuncle Shades: tinted glass and a source gem. Give them to a Starbuncle.",
        "&eTip:&r they do nothing useful. That is the point."]),

    # --- Wilden and Ars Elemental (y=2.5) -----------------------------------------------------
    Q("ars_wilden", 0, 2.5, [kill("ars_nouveau:wilden_hunter", 5)], "Wilden Hunt", deps=["m_book"], xp=75, loot="hunt",
      subtitle="Kill 5 Wilden Hunters", desc=[
        "&eWhat:&r Wilden are Ars Nouveau's wild magical beasts. Hunters charge, Stalkers fly, Guardians throw spikes.",
        "&eHow:&r they roam the Overworld at night, more often near archwood forests and Wilden dens. Bring a shield.",
        "&eTip:&r keep every horn, spike and wing they drop. Rituals need them."]),
    Q("ars_wings", 2, 2.5, [item("ars_nouveau:wilden_wing", 3)], "Wilden Wings", deps=["ars_wilden"], xp=50,
      subtitle="The key ingredient for flight", desc=[
        "&eWhat:&r Wilden Wings drop from Wilden Stalkers, the flying ones.",
        "&eHow:&r hunt Stalkers at night. The Ritual of Flight tablet needs three wings (purple archwood log, 3 wings, 2 diamonds, an ender pearl).",
        "&eTip:&r a Ritual of Wilden Summoning will need three more Wilden drops, so keep hunting."]),
    Q("ars_chimera", 4, 2.5, [kill("ars_nouveau:wilden_boss")], "The Wilden Chimera", deps=["ars_wings", "m_brazier"], xp=300,
      loot="boss", size=1.5, shape="hexagon", subtitle="Summon and slay Ars Nouveau's boss", desc=[
        "&6You remember beasts that were many beasts at once. You remember winning.&r",
        "&eWhat:&r the Wilden Chimera combines all three Wilden. It drops Wilden Tribute, used for Ars Elemental's Mark of Mastery.",
        "&eHow:&r craft the Ritual of Wilden Summoning (purple archwood log, 3 Wilden drops, a lapis block), place it in a brazier away from your base, and fight.",
        "&eTip:&r it has phases and calls spikes from the ground. Keep moving and bring healing."]),
    Q("ars_mastery", 6, 2.5, [item("ars_elemental:mark_of_mastery")], "Mark of Mastery", deps=["ars_chimera"], xp=100,
      subtitle="Ars Elemental's upgrade token", desc=[
        "&eWhat:&r the Mark of Mastery upgrades elemental foci and turns Arcanist armor into elemental mage armor.",
        "&eHow:&r imbue a Wilden Tribute with all seven essences plus anima essence (check JEI). One tribute gives five marks.",
        "&eTip:&r anima essence comes from imbuing a source gem with a wither skeleton skull, bone meal and a golden apple."]),
    Q("ars_focus", 6, 4, [anyof(["ars_elemental:lesser_fire_focus", "ars_elemental:lesser_water_focus",
                                 "ars_elemental:lesser_earth_focus", "ars_elemental:lesser_air_focus"])],
      "Lesser Elemental Focus", deps=["m_jar"], xp=75, subtitle="Pick an element and specialise", desc=[
        "&eWhat:&r an Ars Elemental focus is a curio that strengthens one school of spells (fire, water, earth or air) and lowers its cost.",
        "&eChemistry:&r the four classical elements were the first attempt at a periodic table. You know there are 118, but the spells don't.",
        "&eHow:&r in the Imbuement Chamber: an amethyst shard with 3 matching essences and 3 gold ingots on pedestals.",
        "&eTip:&r choose the school your favourite spell uses most."]),
    Q("ars_focus_full", 8, 2.5, [anyof(["ars_elemental:fire_focus", "ars_elemental:water_focus",
                                        "ars_elemental:earth_focus", "ars_elemental:air_focus"])],
      "Greater Elemental Focus", deps=["ars_focus", "ars_mastery"], xp=150, subtitle="Master an element", desc=[
        "&eWhat:&r the full focus gives a much bigger bonus to its school and protects you from matching hazards.",
        "&eHow:&r put the lesser focus in the Enchanting Apparatus with a Mark of Mastery on a pedestal (5,000 Source).",
        "&eTip:&r a fire focus pairs well with Ignite and Flare; a water focus with Watery Grave."]),
    Q("ars_armor", 8, 4, [anyof(["ars_nouveau:sorcerer_robes", "ars_nouveau:arcanist_robes", "ars_nouveau:battlemage_robes"])],
      "Mage Armor", deps=["m_apparatus"], xp=75, subtitle="Armor that stores mana", desc=[
        "&eWhat:&r Ars Nouveau armor comes in three styles (Sorcerer, Arcanist, Battlemage). Each piece adds mana and mana regeneration.",
        "&eHow:&r made in the Enchanting Apparatus around a golden armor piece with magebloom fiber (check JEI for each style).",
        "&eTip:&r grow magebloom early; every piece needs fiber."]),
    Q("ars_armor_up", 10, 4, [tick()], "Armor Tiers", deps=["ars_armor"], xp=75,
      subtitle="Upgrade mage armor in the Apparatus", desc=[
        "&eWhat:&r mage armor has three tiers. Each tier raises mana and opens more thread slots.",
        "&eHow:&r place the armor in the Enchanting Apparatus with the upgrade items on pedestals: tier 2 needs blaze rods, tier 3 needs more (check JEI under 'armor upgrade').",
        "&eTip:&r threads go into the Alteration Table: Spellpower, Magic Capacity, Repairing and more. Click the checkmark once you've upgraded a piece."]),
    Q("ars_elem_armor", 10, 2.5, [anyof(["ars_elemental:fire_hat", "ars_elemental:aqua_hat", "ars_elemental:earth_hat", "ars_elemental:air_hat",
                                         "ars_elemental:fire_robes", "ars_elemental:aqua_robes", "ars_elemental:earth_robes", "ars_elemental:air_robes"])],
      "Elemental Mage Armor", deps=["ars_mastery", "ars_armor"], xp=200, optional=True, tokens=2,
      subtitle="Optional: armor of a single element", desc=[
        "&eWhat:&r Ars Elemental turns Arcanist armor into fire, water, earth or air armor, each with resistances and a spell bonus.",
        "&eHow:&r in the Enchanting Apparatus: an Arcanist piece plus a Mark of Mastery, a netherite ingot and two matching essences (7,000 Source).",
        "&eTip:&r a full set matching your focus makes that school very cheap to cast."]),
    Q("ars_flight_note", 14, 0, [tick()], "Two Roads to the Sky", deps=["m_ritual"], xp=50, optional=True, tokens=1,
      subtitle="Optional: how Ars flight fits the pack", desc=[
        "&eWhat:&r a note on the Ritual of Flight and the pack's other flight sources.",
        "&eHow:&r read the second page, then click the checkmark.",
        "{@pagebreak}",
        "&eRitual of Flight:&r the tablet is a purple archwood log, 3 Wilden Wings, 2 diamonds and an ender pearl. Ars Elemental adds a second recipe: a flashing (yellow) archwood log, 1 wing, 2 diamonds and a feather.",
        "&eRange:&r the ritual only grants flight near its brazier and drains Source while you fly. It's base flight, not world flight.",
        "&eElsewhere:&r the Infusion Pylon with a Potion of Flying (hydrogen from the Dissolver), Iron Jetpacks (MI circuits) and the Angel Ring (digital circuit) all work anywhere. See Tools and Comfort."]),
], links=[("t2_ars", -2, 0)])
