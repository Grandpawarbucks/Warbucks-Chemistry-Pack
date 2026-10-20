import sys; sys.path.insert(0, 'scratchpad/c6b')
from qedit import F
f = F('tools/quests/allthemodium.py')
S, H = f.sub, f.header

# ---- start: netherite, the guide, the Ancient City ----
H("atm_raw", '''Q("atm_raw", 0, 0, [item(A + "raw_allthemodium", 4)], "Allthemodium Ore", deps=["t4_separator", "atm_city"], xp=150,
      subtitle="Yellow seams on the ceiling of the Deep Dark", desc=[''')
S("atm_raw", '''        "&6There were metals you once named yourself. One of them is waiting under the sculk.&r",
''', "")
f.t = f.t.replace('''    # --- allthemodium (design T3) -----------------------------------------------------------------
''', '''    # ============================ the way in (ATM10: netherite, the guide, the Ancient City) ============================
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
''')
H("atm_ingot", '''Q("atm_ingot", 0, 0, [item(A + "allthemodium_ingot")], "Reduce It", deps=["atm_raw", "t3_ebf"], xp=200, size=1.5,
      mirror="201EE3566D4D3123", subtitle="Coke and a cupronickel EBF", desc=[''')
H("atm_pad", '''Q("atm_pad", 0, 0, [item(A + "teleport_pad")], "The Teleport Pad", deps=["atm_ingot", "t3_analog"], xp=250, size=1.5,
      mirror="07FDA46D83F8360D", section="The Teleport Pad", subtitle="Steel, a pearl and a circuit", desc=[''')
f.after("atm_pad", '''    Q("atm_pad_overworld", 0, 0, [dim("minecraft:overworld")], "A Pad at Home", deps=["atm_pad"], xp=50, mirror="2C4299D33D419AA0",
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
        "&eTip:&r the End's outer islands are also where unobtainium grows."]),''')
H("atm_mining", '''Q("atm_mining", 0, 0, [dim(A + "mining")], "The Mining Dimension", deps=["atm_pad_overworld"], xp=300,
      mirror="6D738730B371B152", subtitle="A flat world made of ore", desc=[''')
H("atm_debris", '''Q("atm_debris", 0, 0, [item("minecraft:ancient_debris", 16)], "Rich Seams", deps=["atm_mining"], xp=150,
      optional=True, tokens=1, mirror="18FAD56CDE05646A", subtitle="Optional: debris in the netherrack layer", desc=[''')
H("atm_template", '''Q("atm_template", 0, 0, [item(A + "allthemodium_upgrade_smithing_template")], "Brush the City", deps=["atm_city"], xp=200, size=1.5,
      mirror="71E4FD61787DE299", subtitle="Archaeology in the Ancient City", desc=[''')
H("atm_pick", '''Q("atm_pick", 0, 0, [item(A + "allthemodium_pickaxe")], "Allthemodium Pickaxe", deps=["atm_template", "atm_ingot"], xp=200,
      mirror="6E0624750DF8CD18", section="Allthemodium Gear", subtitle="The pick that breaks vibranium", desc=[''')
f.after("atm_pick", '''    Q("atm_sword", 0, 0, [item(A + "allthemodium_sword")], "Allthemodium Sword", deps=["atm_template", "atm_ingot"], xp=150,
      optional=True, tokens=1, mirror="1F6C8117F3CED939", subtitle="Optional: a netherite sword, raised a rung", desc=[
        "&eWhat:&r the allthemodium sword, the first legendary blade.",
        "&eHow:&r smithing table: allthemodium template + netherite sword + allthemodium ingot. Enchantments carry over."]),
    Q("atm_mace", 0, 0, [item(A + "allthemodium_mace")], "Allthemodium Mace", deps=["atm_template", "atm_ingot"], xp=150,
      mirror="44D5EDB8711EC7A0", subtitle="A mace that falls even harder", desc=[
        "&eWhat:&r the vanilla mace, upgraded with allthemodium.",
        "&eChemistry:&r a falling mace turns height into energy: E = mgh, so doubling the drop doubles what it delivers on impact.",
        "&eHow:&r smithing table: allthemodium template + mace + allthemodium ingot (check JEI). A mace needs a heavy core from a Trial Chamber vault and a breeze rod.",
        "&eTip:&r pair it with a jump or a fall from a height; that's where a mace earns its keep."]),''')
H("atm_armor", '''Q("atm_armor", 0, 0, [anyof([A + "allthemodium_helmet", A + "allthemodium_chestplate", A + "allthemodium_leggings", A + "allthemodium_boots"])],
      "Allthemodium Armour", deps=["atm_template", "atm_ingot"], xp=250, mirror="6ECDD26CCCBC07C3", subtitle="Any piece, upgraded from netherite", desc=[''')
S("atm_armor", "&eHow:&r smithing table, one template and one allthemodium ingot per netherite piece.",
  "&eHow:&r smithing table, one template and one allthemodium ingot per netherite piece. Any one piece completes this quest.")

# ---- The Other / Beyond ----
H("atm_other", '''Q("atm_other", 0, 0, [dim(A + "the_other")], "The Other", deps=["atm_pad_nether"], xp=250,
      mirror="15FEA03A2CDBA33B", section="The Other", subtitle="A pad in the Nether leads somewhere older", desc=[''')
H("atm_pyramid", '''Q("atm_pyramid", 0, 0, [structure(A + "ancient_pyramid")], "The Ancient Pyramid", deps=["atm_other"], xp=200,
      mirror="24934231538B6492", subtitle="In the soul sand valleys", desc=[''')
H("atm_piglich", '''Q("atm_piglich", 0, 0, [item(A + "piglich_heart")], "Piglich Heart", deps=["atm_pyramid"], xp=250,
      mirror="5BA986D7928BF09F", subtitle="The pyramid's undead lord", desc=[''')
H("atm_dungeon", '''Q("atm_dungeon", 0, 0, [structure(A + "dungeon")], "The Dungeon", deps=["atm_other"], xp=200,
      optional=True, tokens=1, subtitle="Optional: in the warped forests", desc=[''')
H("atm_beyond", '''Q("atm_beyond", 0, 0, [dim(A + "the_beyond")], "The Beyond", deps=["atm_pad_end"], xp=150,
      mirror="11E957CDEFA0CAAB", subtitle="An empty world past the End", desc=[''')

# ---- vibranium ----
H("atm_vib_raw", '''Q("atm_vib_raw", 0, 0, [item(A + "raw_vibranium", 4)], "Vibranium Ore", deps=["atm_pick", "atm_pad_nether"], xp=200,
      section="Vibranium", subtitle="Hanging from the Nether's ceilings", desc=[''')
H("atm_vib_ingot", '''Q("atm_vib_ingot", 0, 0, [item(A + "vibranium_ingot")], "The Kroll Route", deps=["atm_vib_raw", "t6_kanthal_coil", "t6_argon"], xp=300,
      size=1.5, mirror="144BB025516E0994", subtitle="Chlorine, magnesium, argon, kanthal", desc=[''')
H("atm_vib_template", '''Q("atm_vib_template", 0, 0, [item(A + "vibranium_upgrade_smithing_template")], "Brush the Bastion", deps=["atm_pad_nether"], xp=200,
      size=1.5, mirror="226B8B60AF864FEF", subtitle="Archaeology in a treasure room", desc=[''')
H("atm_vib_pick", '''Q("atm_vib_pick", 0, 0, [item(A + "vibranium_pickaxe")], "Vibranium Pickaxe", deps=["atm_vib_ingot", "atm_vib_template"], xp=250,
      mirror="5AAF6CA41209B365", subtitle="The pick that breaks unobtainium", desc=[''')
f.after("atm_vib_pick", '''    Q("atm_vib_sword", 0, 0, [item(A + "vibranium_sword")], "Vibranium Sword", deps=["atm_vib_ingot", "atm_vib_template"], xp=200,
      optional=True, tokens=1, mirror="151D836C7B0E6FAF", subtitle="Optional: the second legendary blade", desc=[
        "&eWhat:&r the vibranium sword.",
        "&eHow:&r smithing table: vibranium template + allthemodium sword + vibranium ingot."]),
    Q("atm_vib_mace", 0, 0, [item(A + "vibranium_mace")], "Vibranium Mace", deps=["atm_vib_ingot", "atm_vib_template"], xp=200,
      mirror="68E6AE1B9EBCEFFF", subtitle="The mace, another rung up", desc=[
        "&eWhat:&r the allthemodium mace, upgraded with vibranium.",
        "&eHow:&r smithing table: vibranium template + allthemodium mace + vibranium ingot (check JEI)."]),''')
H("atm_vib_armor", '''Q("atm_vib_armor", 0, 0, [anyof([A + "vibranium_helmet", A + "vibranium_chestplate", A + "vibranium_leggings", A + "vibranium_boots"])],
      "Vibranium Armour", deps=["atm_vib_ingot", "atm_vib_template"], xp=300, mirror="7DE2154159D273C3", subtitle="Any piece, upgraded again", desc=[''')
S("atm_vib_armor", "&eHow:&r one vibranium template and ingot per allthemodium piece.",
  "&eHow:&r one vibranium template and ingot per allthemodium piece. Any one piece completes this quest.")
H("atm_va_alloy", '''Q("atm_va_alloy", 0, 0, [item(A + "vibranium_allthemodium_alloy_ingot")], "Vibranium-Allthemodium Alloy", deps=["atm_vib_ingot", "atm_piglich"], xp=300,
      mirror="66039B738CF0718A", section="The Legendary Alloys", subtitle="Powder metallurgy, with a heart in it", desc=[''')

# ---- unobtainium ----
H("atm_unob_raw", '''Q("atm_unob_raw", 0, 0, [item(A + "raw_unobtainium", 4)], "Unobtainium Ore", deps=["atm_vib_pick", "atm_pad_end"], xp=300,
      section="Unobtainium", subtitle="On the floors of the End highlands", desc=[''')
H("atm_unob_ingot", '''Q("atm_unob_ingot", 0, 0, [item(A + "unobtainium_ingot")], "The Fluoride Route", deps=["atm_unob_raw", "t6_hf", "t4_sodium"], xp=400,
      size=1.5, mirror="4A079D40C0AF6BC3", subtitle="Hydrofluoric acid and molten sodium", desc=[''')
H("atm_unob_template", '''Q("atm_unob_template", 0, 0, [item(A + "unobtainium_upgrade_smithing_template")], "The Library Chest", deps=["atm_other"], xp=250,
      size=1.5, mirror="3F8D515D7B81B0E3", subtitle="Hidden in The Other's dungeon", desc=[''')
S("atm_unob_template", "&eHow:&r loot the chest in the dungeon's library room.",
  "&eHow:&r find the dungeon in The Other's warped forests and loot the chest in its library room.")
H("atm_unob_gear", '''Q("atm_unob_gear", 0, 0, [anyof([A + "unobtainium_sword", A + "unobtainium_pickaxe", A + "unobtainium_axe", A + "unobtainium_shovel",
                                       A + "unobtainium_hoe"])], "Unobtainium Tool", deps=["atm_unob_ingot", "atm_unob_template"], xp=400,
      mirror="089B1B9837AF4938", subtitle="The top of the ladder", desc=[''')
S("atm_unob_gear", "&eWhat:&r the unobtainium pick mines everything here, including ancient stone bricks and the alloy blocks. The chestplate cuts magic damage to a tenth.",
  "&eWhat:&r any unobtainium tool or weapon. The unobtainium pick mines everything here, including ancient stone bricks and the alloy blocks.")
S("atm_unob_gear", "&eHow:&r smithing table: unobtainium template + vibranium piece + unobtainium ingot.",
  "&eHow:&r smithing table: unobtainium template + vibranium tool + unobtainium ingot.")
f.after("atm_unob_gear", '''    Q("atm_unob_armor", 0, 0, [anyof([A + "unobtainium_helmet", A + "unobtainium_chestplate", A + "unobtainium_leggings", A + "unobtainium_boots"])],
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
        "&eHow:&r smithing table: unobtainium template + vibranium mace + unobtainium ingot (check JEI)."]),''')
H("atm_alloys", '''Q("atm_alloys", 0, 0, [item(A + "unobtainium_vibranium_alloy_ingot")],
      "Forged in Annihilation", deps=["atm_unob_ingot", "atm_va_alloy", "t7_antimatter"], xp=600, size=2.0,
      mirror="2CF6EA138B53CE1B", subtitle="Antimatter is the only heat left", desc=[''')
S("atm_alloys", "&eWhat:&r the two unobtainium alloys, the rarest materials in the pack.",
  "&eWhat:&r the unobtainium-vibranium alloy, one of the two rarest materials in the pack.")
S("atm_alloys", "&eHow:&r Mixer: unobtainium dust + vibranium or allthemodium dust + Piglich Heart → 2 alloy dust.",
  "&eHow:&r Mixer: unobtainium dust + vibranium dust + Piglich Heart → 2 alloy dust.")
f.after("atm_alloys", '''    Q("atm_ua_alloy", 0, 0, [item(A + "unobtainium_allthemodium_alloy_ingot")], "Unobtainium-Allthemodium Alloy",
      deps=["atm_unob_ingot", "atm_va_alloy", "t7_antimatter"], xp=500, mirror="1A05C605A52A4218", subtitle="The other annihilation alloy", desc=[
        "&eWhat:&r the unobtainium-allthemodium alloy, the twin of the vibranium one.",
        "&eHow:&r Mixer: unobtainium dust + allthemodium dust + Piglich Heart → 2 alloy dust. EBF (128 EU/t): 8 alloy dust + 1 antimatter pellet + 1000 mB argon → 8 ingots.",
        "&eTip:&r run both alloys in the same antimatter session: each pellet fuses a batch of eight."]),''')
f.t = f.t.replace('], links=[("t4_separator", -2, 0), ("hv_netherite_pick", -2, 0), ("t3_ebf", -2, 0), ("t6_kanthal_coil", -2, 0),\n          ("t6_hf", -2, 0), ("t7_antimatter", -2, 0)])',
                  '], links=[("t4_separator", -2, 0), ("hv_netherite_pick", -2, 0), ("t3_ebf", -2, 0), ("t6_kanthal_coil", -2, 0),\n          ("t6_hf", -2, 0), ("t7_antimatter", -2, 0)], mirror="allthemodium")')
f.save()
