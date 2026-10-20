"""Quest chapter: allthemodium (Allthemodium 3.2.1: three legendary metals, the Teleport Pad and three realms).
See tools/quests/STYLE.md. Build: python3 tools/build_quests.py. Prefix atm_.

Tiers (design / quest chapter): allthemodium T3 / t4, vibranium T4-T5 / t5-t6, unobtainium T5-T6 / t6-t7.
Gates are in pack/kubejs/server_scripts/phase5_allthemodium.js: no furnace smelting (MI EBF reductions instead),
alloys in the MI Mixer + EBF, and the Teleport Pad needs MI steel plates and an analog circuit.
Facts from the 3.2.1 jar: ores are hand-mined only (a FakePlayer break deletes the ore); pick ladder netherite ->
allthemodium -> vibranium -> unobtainium; templates: allthemodium = suspicious clay in Ancient Cities, vibranium =
suspicious soul sand in Bastion treasure rooms, unobtainium = the library chest of The Other's dungeon.
Pads pair Overworld<->Mining, Nether<->The Other, End<->The Beyond.
"""
from questlib import Q, Chapter, item, dim, tick, kill, structure, biome, anyof, MAIN, SIDE  # noqa: F401

A = "allthemodium:"

CHAPTER = Chapter("allthemodium", "Metals of Legend", A + "allthemodium_ingot",
        ["Allthemodium, vibranium and unobtainium: metals no fire can win.",
         "A pad of steel and pearl opens three more worlds."], SIDE, [
    # ============================ the way in (ATM10: netherite, the guide, the Ancient City) ============================
    Q("atm_start", 0, 0, [item("minecraft:netherite_ingot")], "Beyond Netherite", deps=["hv_netherite_pick"], xp=200, size=2.0,
      mirror="4B2146C9527C54E7", section="The First Legend", subtitle="Netherite is where this story starts", desc=[
        "&6There were metals you once named yourself. The first of them is waiting under the sculk.&r",
        "&eWhat:&r netherite is the strongest ordinary metal. Every legendary metal on this page is mined with, or forged onto, netherite first.",
        "&eHow:&r four netherite scrap and four gold ingots make one ingot (check JEI). Hold one.",
        "&eTip:&r keep your netherite gear: each legendary template upgrades it rather than replacing it."]),
    Q("atm_guide", 0, 0, [tick()], "Three Metals, Three Realms", deps=[], xp=10, optional=True, tokens=0, mirror="552F0B9B00F4F914",
      icon="allthemodium:teleport_pad", subtitle="How this page works", desc=[
        "&eWhat:&r allthemodium, vibranium and unobtainium form a ladder: each pickaxe mines the next ore. The Teleport Pad opens three more worlds.",
        "&eHow:&r none of these metals melts in a furnace here. Each one is refined in the MI Electric Blast Furnace by a real industrial route.",
        "&eTip:&r click the checkmark once you've read this."]),
    Q("atm_city", 0, 0, [structure("minecraft:ancient_city")], "Under the Sculk", deps=["atm_start"], xp=150, mirror="111E4ACF7D570EE8",
      subtitle="Find an Ancient City", desc=[
        "&eWhat:&r Ancient Cities lie in the Deep Dark, and the Deep Dark is where allthemodium grows. The cities also hide its template.",
        "&eHow:&r the Explorer's Compass can find one. Sneak in and stand inside.",
        "&eTip:&r shriekers summon the Warden; break them quietly or go around."]),

    # --- allthemodium (design T3) -----------------------------------------------------------------
    Q("atm_raw", 0, 0, [item(A + "raw_allthemodium", 4)], "Allthemodium Ore", deps=["t4_separator", "atm_city"], xp=150,
      subtitle="Yellow seams on the ceiling of the Deep Dark", desc=[
        "&eWhat:&r the first of three legendary metals. It only grows in the Deep Dark biome, below Y 10, on cave ceilings (plain and deepslate ore).",
        "&eHow:&r a netherite pickaxe or better. Look up, not down. Sneak: the Deep Dark has shriekers and a Warden.",
        "&eTip:&r these ores must be mined by hand. A quarry, miner or other machine that breaks one destroys it and gets nothing. Ultimine is fine."]),
    Q("atm_ingot", 0, 0, [item(A + "allthemodium_ingot")], "Reduce It", deps=["atm_raw", "t3_ebf"], xp=200, size=1.5,
      mirror="201EE3566D4D3123", subtitle="Coke and a cupronickel EBF", desc=[
        "&eWhat:&r allthemodium won't melt in any furnace. Raw ore or dust has to be reduced in the Electric Blast Furnace.",
        "&eChemistry:&r carbothermic reduction, MO + C → M + CO: carbon pulls the oxygen off the metal. It's how iron, and MI's silicon, are made.",
        "&eHow:&r EBF with cupronickel coils, 32 EU/t: 1 raw allthemodium (or dust) + 1 coke dust → 1 ingot."]),
    Q("atm_mek", 0, 0, [item(A + "allthemodium_crystal", 4)], "Five from One", deps=["atm_raw", "t4_ore5"], xp=150,
      optional=True, tokens=1, subtitle="Optional: the acid chain works here too", desc=[
        "&eWhat:&r the mod comes with full Mekanism processing: oxygen 3x, hydrogen chloride 4x, sulfuric acid 5x, like every other ore.",
        "&eChemistry:&r sulfuric acid dissolves the ore into a slurry, water washes it, and crystals grow out as the solution concentrates.",
        "&eHow:&r Dissolution Chamber → Washer → Crystallizer → Injection → Purification → Crusher → Enrichment, then reduce the dust in the EBF.",
        "&eTip:&r without Fortune, silk-touch the ore: an ore block gives 5 crystals, a raw ore 3⅓. With Fortune III, mine it normally."]),
    Q("atm_pad", 0, 0, [item(A + "teleport_pad")], "The Teleport Pad", deps=["atm_ingot", "t3_analog"], xp=250, size=1.5,
      mirror="07FDA46D83F8360D", section="The Teleport Pad", subtitle="Steel, a pearl and a circuit", desc=[
        "&eWhat:&r one block that links two worlds. Placed in the Overworld it leads to the Mining dimension, in the Nether to The Other, in the End to The Beyond.",
        "&eHow:&r an ender pearl, 4 allthemodium nuggets, 4 MI steel plates and an analog circuit (check JEI).",
        "&eTip:&r stand on it, empty both hands and sneak + right-click. A return pad appears on the far side; it doesn't drop if broken, so leave it."]),
    Q("atm_pad_overworld", 0, 0, [dim("minecraft:overworld")], "A Pad at Home", deps=["atm_pad"], xp=50, mirror="2C4299D33D419AA0",
      icon="minecraft:grass_block", subtitle="Overworld pads lead to the Mining dimension", desc=[
        "&eWhat:&r a Teleport Pad placed in the Overworld opens the way to the Mining dimension.",
        "&eHow:&r you're probably here already: place a pad somewhere you'll find again.",
        "&eTip:&r put it inside your base; the return pad appears where you arrive."]),
    Q("atm_pad_nether", 0, 0, [dim("minecraft:the_nether")], "A Pad in the Nether", deps=["atm_pad"], xp=50, mirror="0CC0632E8276C787",
      icon="minecraft:netherrack", subtitle="Nether pads lead to The Other", desc=[
        "&eWhat:&r a Teleport Pad placed in the Nether opens the way to The Other.",
        "&eHow:&r carry a pad through a Nether portal and place it.",
        "&eTip:&r build a little shelter round it: ghasts don't respect machinery."]),
    Q("atm_pad_end", 0, 0, [dim("minecraft:the_end")], "A Pad in the End", deps=["atm_pad"], xp=50, mirror="2EDE91023F7924FB",
      icon="minecraft:end_stone", subtitle="End pads lead to The Beyond", desc=[
        "&eWhat:&r a Teleport Pad placed in the End opens the way to The Beyond.",
        "&eHow:&r carry a pad through the End portal and place it.",
        "&eTip:&r the End's outer islands are also where unobtainium grows."]),
    Q("atm_mining", 0, 0, [dim(A + "mining")], "The Mining Dimension", deps=["atm_pad_overworld"], xp=300,
      mirror="6D738730B371B152", subtitle="A flat world made of ore", desc=[
        "&6You built a world once just to dig in it. You kept the key.&r",
        "&eWhat:&r a flat world in layers: grass and stone on top, deepslate from Y 128 down to 65, netherrack to Y 1, end stone, bedrock. The layers are packed with ore.",
        "&eHow:&r place a Teleport Pad in the Overworld and use it. Iron, emerald, diamond, gold and redstone are far richer here than at home, and ancient debris sits in the netherrack.",
        "&eTip:&r allthemodium grows here too (about one vein per chunk, in the deepslate layer). It is still hand-mined only. Light your tunnels: mobs spawn in the dark."]),
    Q("atm_debris", 0, 0, [item("minecraft:ancient_debris", 16)], "Rich Seams", deps=["atm_mining"], xp=150,
      optional=True, tokens=1, mirror="18FAD56CDE05646A", subtitle="Optional: debris in the netherrack layer", desc=[
        "&eWhat:&r the Mining dimension's netherrack layer (Y 1 to 64) carries veins of ancient debris.",
        "&eHow:&r strip-mine the netherrack layer. A Mekanism or MI tool with a wide area helps.",
        "&eTip:&r every netherite pick and armour piece is an allthemodium upgrade waiting to happen."]),
    Q("atm_template", 0, 0, [item(A + "allthemodium_upgrade_smithing_template")], "Brush the City", deps=["atm_city"], xp=200, size=1.5,
      mirror="71E4FD61787DE299", subtitle="Archaeology in the Ancient City", desc=[
        "&eWhat:&r the smithing template that upgrades netherite gear to allthemodium.",
        "&eHow:&r Ancient Cities hide Suspicious Clay where polished basalt would be. Brush it (vanilla brush) for the template.",
        "&eTip:&r copy it before you use it: template + 7 netherite ingots + deepslate makes 2."]),
    Q("atm_pick", 0, 0, [item(A + "allthemodium_pickaxe")], "Allthemodium Pickaxe", deps=["atm_template", "atm_ingot"], xp=200,
      mirror="6E0624750DF8CD18", section="Allthemodium Gear", subtitle="The pick that breaks vibranium", desc=[
        "&eWhat:&r the next rung of the ladder: netherite pick → allthemodium ore, allthemodium pick → vibranium ore.",
        "&eHow:&r smithing table: allthemodium template + netherite pickaxe + allthemodium ingot. Enchantments carry over."]),
    Q("atm_sword", 0, 0, [item(A + "allthemodium_sword")], "Allthemodium Sword", deps=["atm_template", "atm_ingot"], xp=150,
      optional=True, tokens=1, mirror="1F6C8117F3CED939", subtitle="Optional: a netherite sword, raised a rung", desc=[
        "&eWhat:&r the allthemodium sword, the first legendary blade.",
        "&eHow:&r smithing table: allthemodium template + netherite sword + allthemodium ingot. Enchantments carry over."]),
    Q("atm_mace", 0, 0, [item(A + "allthemodium_mace")], "Allthemodium Mace", deps=["atm_template", "atm_ingot"], xp=150,
      mirror="44D5EDB8711EC7A0", subtitle="A mace that falls even harder", desc=[
        "&eWhat:&r the vanilla mace, upgraded with allthemodium.",
        "&eChemistry:&r a falling mace turns height into energy: E = mgh, so doubling the drop doubles what it delivers on impact.",
        "&eHow:&r smithing table: allthemodium template + mace + a block of allthemodium (nine ingots; check JEI). A mace needs a heavy core from a Trial Chamber vault and a breeze rod.",
        "&eTip:&r pair it with a jump or a fall from a height; that's where a mace earns its keep."]),
    Q("atm_armor", 0, 0, [anyof([A + "allthemodium_helmet", A + "allthemodium_chestplate", A + "allthemodium_leggings", A + "allthemodium_boots"])],
      "Allthemodium Armour", deps=["atm_template", "atm_ingot"], xp=250, mirror="6ECDD26CCCBC07C3", subtitle="Any piece, upgraded from netherite", desc=[
        "&eWhat:&r the boots cancel fall damage, the helmet refills your air underwater, the chestplate halves magic damage, and the set puts out fire on you.",
        "&eHow:&r smithing table, one template and one allthemodium ingot per netherite piece. Any one piece completes this quest.",
        "&eTip:&r no flight here. Your wings still come from chemistry."]),

    # --- The Other ---------------------------------------------------------------------------------
    Q("atm_other", 0, 0, [dim(A + "the_other")], "The Other", deps=["atm_pad_nether"], xp=250,
      mirror="15FEA03A2CDBA33B", section="The Other", subtitle="A pad in the Nether leads somewhere older", desc=[
        "&6A world of endless night, with your old trees still standing. You remember planting them.&r",
        "&eWhat:&r a dark, Nether-like realm of soul sand valleys, deserts and crimson and warped forests, with ancient, demonic and soul trees. Allthemodium and vibranium ores grow here.",
        "&eHow:&r place a Teleport Pad in the Nether and use it.",
        "&eTip:&r blocks inside The Other's structures can't be broken. Explore them; don't tunnel through them."]),
    Q("atm_pyramid", 0, 0, [structure(A + "ancient_pyramid")], "The Ancient Pyramid", deps=["atm_other"], xp=200,
      mirror="24934231538B6492", subtitle="In the soul sand valleys", desc=[
        "&eWhat:&r the pyramids of the soul sand valleys hold loot rooms and treasure chests (allthemodium and vibranium nuggets among them) and the Piglich.",
        "&eHow:&r an Explorer's Compass or a long walk through soul sand. Click once you're inside.",
        "&eTip:&r bring fire resistance; the soul sand valleys of The Other are no kinder than the Nether's."]),
    Q("atm_piglich", 0, 0, [item(A + "piglich_heart")], "Piglich Heart", deps=["atm_pyramid"], xp=250,
      mirror="5BA986D7928BF09F", subtitle="The pyramid's undead lord", desc=[
        "&eWhat:&r the Piglich spawns inside the Ancient Pyramid and drops one heart. Every alloy in this chapter needs one.",
        "&eHow:&r fight it in the pyramid; it keeps spawning inside the structure.",
        "&eTip:&r a Hostile Neural Networks data model for the Piglich farms hearts once you have the Simulation Chamber."]),
    Q("atm_dungeon", 0, 0, [structure(A + "dungeon")], "The Dungeon", deps=["atm_other"], xp=200,
      optional=True, tokens=1, subtitle="Optional: in the warped forests", desc=[
        "&eWhat:&r a sprawling dungeon of halls, a forge, a treasure room and a library. The library's chest holds the unobtainium template.",
        "&eHow:&r search The Other's warped forests. Click once you're inside.",
        "&eTip:&r Apotheosis bosses spawn in The Other. Gear up before you go deep."]),

    # --- vibranium (design T4-T5) -------------------------------------------------------------------
    Q("atm_vib_raw", 0, 0, [item(A + "raw_vibranium", 4)], "Vibranium Ore", deps=["atm_pick", "atm_pad_nether"], xp=200,
      section="Vibranium", subtitle="Hanging from the Nether's ceilings", desc=[
        "&eWhat:&r the second legendary metal. It grows on cave ceilings in the Nether, from Y 64 up to the roof, and in The Other.",
        "&eHow:&r an allthemodium pickaxe or better. Hand-mined only, like allthemodium.",
        "&eTip:&r fly along the Nether ceiling with a light source; the ore shows up against the netherrack."]),
    Q("atm_vib_ingot", 0, 0, [item(A + "vibranium_ingot")], "The Kroll Route", deps=["atm_vib_raw", "t6_kanthal_coil", "t6_argon"], xp=300,
      size=1.5, mirror="144BB025516E0994", subtitle="Chlorine, magnesium, argon, kanthal", desc=[
        "&eWhat:&r vibranium is refined like titanium and zirconium: through its chloride, never by melting the ore.",
        "&eChemistry:&r the Kroll process: MO₂ + 2Cl₂ + 2C → MCl₄ + 2CO, then MCl₄ + 2Mg → M + 2MgCl₂, under argon because the hot metal steals oxygen and nitrogen from air.",
        "&eHow:&r EBF with kanthal coils, 128 EU/t: raw vibranium (or dust) + coke dust + 2 magnesium dust + 500 mB chlorine + 50 mB argon → 1 ingot + 2 magnesium chloride dust.",
        "&eTip:&r the Alchemistry Compactor turns magnesium elements into magnesium dust. Keep the MgCl₂: the Dissolver splits it back into Mg and Cl."]),
    Q("atm_vib_template", 0, 0, [item(A + "vibranium_upgrade_smithing_template")], "Brush the Bastion", deps=["atm_pad_nether"], xp=200,
      size=1.5, mirror="226B8B60AF864FEF", subtitle="Archaeology in a treasure room", desc=[
        "&eWhat:&r the template that upgrades allthemodium gear to vibranium.",
        "&eHow:&r the treasure-room variant of a Bastion Remnant hides Suspicious Soul Sand among its blackstone. Brush it.",
        "&eTip:&r copy it: template + 7 allthemodium ingots + ancient stone (from The Other) makes 2."]),
    Q("atm_vib_pick", 0, 0, [item(A + "vibranium_pickaxe")], "Vibranium Pickaxe", deps=["atm_vib_ingot", "atm_vib_template"], xp=250,
      mirror="5AAF6CA41209B365", subtitle="The pick that breaks unobtainium", desc=[
        "&eWhat:&r the only kind of pick (besides unobtainium) that can mine unobtainium ore.",
        "&eHow:&r smithing table: vibranium template + allthemodium pickaxe + vibranium ingot."]),
    Q("atm_vib_sword", 0, 0, [item(A + "vibranium_sword")], "Vibranium Sword", deps=["atm_vib_ingot", "atm_vib_template"], xp=200,
      optional=True, tokens=1, mirror="151D836C7B0E6FAF", subtitle="Optional: the second legendary blade", desc=[
        "&eWhat:&r the vibranium sword.",
        "&eHow:&r smithing table: vibranium template + allthemodium sword + vibranium ingot."]),
    Q("atm_vib_mace", 0, 0, [item(A + "vibranium_mace")], "Vibranium Mace", deps=["atm_vib_ingot", "atm_vib_template"], xp=200,
      mirror="68E6AE1B9EBCEFFF", subtitle="The mace, another rung up", desc=[
        "&eWhat:&r the allthemodium mace, upgraded with vibranium.",
        "&eHow:&r smithing table: vibranium template + allthemodium mace + a block of vibranium (check JEI)."]),
    Q("atm_vib_armor", 0, 0, [anyof([A + "vibranium_helmet", A + "vibranium_chestplate", A + "vibranium_leggings", A + "vibranium_boots"])],
      "Vibranium Armour", deps=["atm_vib_ingot", "atm_vib_template"], xp=300, mirror="7DE2154159D273C3", subtitle="Any piece, upgraded again", desc=[
        "&eWhat:&r the same perks as allthemodium armour, and the chestplate cuts magic damage to a quarter.",
        "&eHow:&r one vibranium template and ingot per allthemodium piece. Any one piece completes this quest."]),
    Q("atm_va_alloy", 0, 0, [item(A + "vibranium_allthemodium_alloy_ingot")], "Vibranium-Allthemodium Alloy", deps=["atm_vib_ingot", "atm_piglich"], xp=300,
      mirror="66039B738CF0718A", section="The Legendary Alloys", subtitle="Powder metallurgy, with a heart in it", desc=[
        "&6Two metals that refuse each other. You remember how to make them agree.&r",
        "&eWhat:&r the first of the three legendary alloys.",
        "&eChemistry:&r refractory alloys melt too hot for any crucible, so industry blends the metal powders and consolidates them by sintering or arc-melting under argon.",
        "&eHow:&r Mixer: allthemodium dust + vibranium dust + Piglich Heart → 2 alloy dust. EBF (kanthal, 128 EU/t): 1 alloy dust + 100 mB argon → 1 ingot.",
        "&eTip:&r crush ingots to dust in the Mekanism Crusher."]),

    # --- unobtainium (design T5-T6) ------------------------------------------------------------------
    Q("atm_unob_raw", 0, 0, [item(A + "raw_unobtainium", 4)], "Unobtainium Ore", deps=["atm_vib_pick", "atm_pad_end"], xp=300,
      section="Unobtainium", subtitle="On the floors of the End highlands", desc=[
        "&eWhat:&r the last legendary metal, found only in the End highlands (the outer islands), on solid floors.",
        "&eHow:&r a vibranium pickaxe or better, by hand. It's rarer than the others: about three tries per chunk.",
        "&eTip:&r a Teleport Pad placed in the End also opens The Beyond, a quiet empty world to build in."]),
    Q("atm_unob_ingot", 0, 0, [item(A + "unobtainium_ingot")], "The Fluoride Route", deps=["atm_unob_raw", "t6_hf", "t4_sodium"], xp=400,
      size=1.5, mirror="4A079D40C0AF6BC3", subtitle="Hydrofluoric acid and molten sodium", desc=[
        "&eWhat:&r unobtainium is refined like tantalum, the metal of capacitors and surgical implants.",
        "&eChemistry:&r HF digests the ore into a fluoride complex (K₂TaF₇ for tantalum), and molten sodium reduces it: K₂TaF₇ + 5Na → Ta + 2KF + 5NaF.",
        "&eHow:&r EBF (kanthal, 128 EU/t, 40 s): raw unobtainium (or dust) + 2 sodium dust + 250 mB hydrofluoric acid + 100 mB argon → 1 ingot.",
        "&eTip:&r HF eats glass and bone. In game it just needs Mekanism tanks; in a real lab it needs calcium gluconate on the bench."]),
    Q("atm_unob_template", 0, 0, [item(A + "unobtainium_upgrade_smithing_template")], "The Library Chest", deps=["atm_other"], xp=250,
      size=1.5, mirror="3F8D515D7B81B0E3", subtitle="Hidden in The Other's dungeon", desc=[
        "&eWhat:&r the template that upgrades vibranium gear to unobtainium.",
        "&eHow:&r find the dungeon in The Other's warped forests and loot the chest in its library room.",
        "&eTip:&r copy it: template + 7 vibranium ingots + end stone makes 2."]),
    Q("atm_unob_gear", 0, 0, [anyof([A + "unobtainium_sword", A + "unobtainium_pickaxe", A + "unobtainium_axe", A + "unobtainium_shovel",
                                       A + "unobtainium_hoe"])], "Unobtainium Tool", deps=["atm_unob_ingot", "atm_unob_template"], xp=400,
      mirror="089B1B9837AF4938", subtitle="The top of the ladder", desc=[
        "&eWhat:&r any unobtainium tool or weapon. The unobtainium pick mines everything here, including ancient stone bricks and the alloy blocks.",
        "&eHow:&r smithing table: unobtainium template + vibranium tool + unobtainium ingot."]),
    Q("atm_unob_armor", 0, 0, [anyof([A + "unobtainium_helmet", A + "unobtainium_chestplate", A + "unobtainium_leggings", A + "unobtainium_boots"])],
      "Unobtainium Armour", deps=["atm_unob_ingot", "atm_unob_template"], xp=400, mirror="4E737C490DCC5D6C", subtitle="Any piece, at the top", desc=[
        "&eWhat:&r the last armour upgrade. The unobtainium chestplate cuts magic damage to a tenth.",
        "&eHow:&r smithing table: unobtainium template + vibranium armour piece + unobtainium ingot. Any one piece completes this quest."]),
    Q("atm_unob_sword", 0, 0, [item(A + "unobtainium_sword")], "Unobtainium Sword", deps=["atm_unob_ingot", "atm_unob_template"], xp=300,
      optional=True, tokens=2, mirror="47F734CDD5793F26", subtitle="Optional: the last legendary blade", desc=[
        "&eWhat:&r the unobtainium sword.",
        "&eHow:&r smithing table: unobtainium template + vibranium sword + unobtainium ingot."]),
    Q("atm_unob_mace", 0, 0, [item(A + "unobtainium_mace")], "Unobtainium Mace", deps=["atm_unob_ingot", "atm_unob_template"], xp=300,
      mirror="0A9D5C5D2F4CDCC3", subtitle="The heaviest thing you can swing", desc=[
        "&eWhat:&r the vibranium mace, upgraded with unobtainium.",
        "&eHow:&r smithing table: unobtainium template + vibranium mace + a block of unobtainium (check JEI)."]),
    Q("atm_alloys", 0, 0, [item(A + "unobtainium_vibranium_alloy_ingot")],
      "Forged in Annihilation", deps=["atm_unob_ingot", "atm_va_alloy", "t7_antimatter"], xp=600, size=2.0,
      mirror="2CF6EA138B53CE1B", subtitle="Antimatter is the only heat left", desc=[
        "&6Matter meets its mirror and both are gone, and the metals finally yield. You remember this fire. It was yours.&r",
        "&eWhat:&r the unobtainium-vibranium alloy, one of the two rarest materials in the pack.",
        "&eChemistry:&r antimatter turns its whole mass into energy (E = mc²): one gram meeting one gram of matter releases about 1.8 × 10¹⁴ J, some 43 kilotons of TNT.",
        "&eHow:&r Mixer: unobtainium dust + vibranium dust + Piglich Heart → 2 alloy dust. EBF (128 EU/t): 8 alloy dust + 1 antimatter pellet + 1000 mB argon → 8 ingots.",
        "&eTip:&r one pellet fuses a whole batch of eight. Make the dust first, then spend the antimatter."]),
    Q("atm_ua_alloy", 0, 0, [item(A + "unobtainium_allthemodium_alloy_ingot")], "Unobtainium-Allthemodium Alloy",
      deps=["atm_unob_ingot", "atm_va_alloy", "t7_antimatter"], xp=500, mirror="1A05C605A52A4218", subtitle="The other annihilation alloy", desc=[
        "&eWhat:&r the unobtainium-allthemodium alloy, the twin of the vibranium one.",
        "&eHow:&r Mixer: unobtainium dust + allthemodium dust + Piglich Heart → 2 alloy dust. EBF (128 EU/t): 8 alloy dust + 1 antimatter pellet + 1000 mB argon → 8 ingots.",
        "&eTip:&r run both alloys in the same antimatter session: each pellet fuses a batch of eight."]),

    # --- The Beyond ----------------------------------------------------------------------------------
    Q("atm_beyond", 0, 0, [dim(A + "the_beyond")], "The Beyond", deps=["atm_pad_end"], xp=150,
      mirror="11E957CDEFA0CAAB", subtitle="An empty world past the End", desc=[
        "&eWhat:&r a blank world with no features at all: a clean canvas for a demigod's building project.",
        "&eHow:&r place a Teleport Pad in the End and use it.",
        "&eTip:&r nothing spawns there to bother your builds, and nothing there needs mining. Bring your own blocks."]),
], links=[("t4_separator", -2, 0), ("hv_netherite_pick", -2, 0), ("t3_ebf", -2, 0), ("t6_kanthal_coil", -2, 0),
          ("t6_hf", -2, 0), ("t7_antimatter", -2, 0)], mirror="allthemodium")
